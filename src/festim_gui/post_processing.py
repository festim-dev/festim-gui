import asyncio
from datetime import datetime
from pathlib import Path

from paraview import simple
from trame.app import TrameApp, asynchronous
from trame.decorators import change
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html
from trame.widgets import paraview as pvw
from trame.widgets import vuetify3 as v3

from festim_gui.execution import find_vtx_dirs, read_latest_run_record


class PostProcessing(TrameApp):
    def __init__(self, server=None, template_name="post-processing"):
        super().__init__(server)

        pvw.initialize(self.server)
        v3.initialize(self.server)

        self.state.pv_file_items = []
        self.state.pv_selected_file = None

        available_files = self._resolve_available_files()
        self.state.pv_file_items = [
            self._build_file_item(path) for path in available_files
        ]
        initial_file = available_files[0] if available_files else None

        self._setup_pv(initial_file)
        self._build_ui(template_name)
        self.state.pv_selected_file = initial_file
        if initial_file and self.ctx.view:
            self.ctx.view.reset_camera()
            self.ctx.view.update()

    def _resolve_available_files(self):
        latest_run = read_latest_run_record()
        if latest_run is None:
            return []

        vtx_paths = latest_run.get("vtx_paths") or []
        if not vtx_paths and latest_run.get("output_dir"):
            vtx_paths = find_vtx_dirs(Path(latest_run["output_dir"]))

        return [str(Path(path).resolve()) for path in vtx_paths]

    def _build_file_item(self, file_path):
        path = Path(file_path)
        try:
            created = datetime.fromtimestamp(path.stat().st_ctime).strftime(
                "%Y-%m-%d %H:%M"
            )
        except OSError:
            created = "unknown"

        run_name = path.parent.parent.name or path.parent.name
        return {
            "title": path.name,
            "subtitle": f"{run_name}  ·  {created}",
            "value": str(path),
        }

    def _setup_pv(self, file_to_load):
        self.times = []
        self.animation_scene = simple.GetAnimationScene()

        self.reader = None
        self.representation = None
        self.view = simple.GetActiveViewOrCreate("RenderView")
        self.view.Set(
            OrientationAxesVisibility=1,
            Background=[0.12, 0.12, 0.12],
        )

        if file_to_load:
            self.load_file(file_to_load)

    def load_file(self, file_path):
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            if self.representation is not None:
                self.representation.Visibility = 0
            return

        if self.reader is None:
            self.reader = simple.ADIOS2VTXReader(FileName=str(file_path))
            self.representation = simple.Show(self.reader, self.view)
        else:
            self.reader.FileName = str(file_path)
            simple.ReloadFiles(self.reader)

        self.reader.UpdatePipeline()
        data_info = self.reader.GetDataInformation()
        options = []
        for data_set, location in (
            (data_info.GetPointDataInformation(), "POINTS"),
            (data_info.GetCellDataInformation(), "CELLS"),
        ):
            for index in range(data_set.GetNumberOfArrays()):
                array = data_set.GetArrayInformation(index)
                if array is None or not array.GetName():
                    continue
                name = array.GetName()
                options.append({"title": name, "value": f"{location}:::{name}"})

        self.times = self.reader.TimestepValues
        self.state.pv_time_idx_max = len(self.times) - 1
        self.state.pv_time_idx = 0

        self.state.pv_color_options = options
        self.representation.Visibility = 1
        self.representation.SetScalarBarVisibility(self.view, True)

        self.view.ResetCamera()
        if self.ctx.view:
            self.ctx.view.reset_camera()

    def reset_color_range(self):
        self.representation.RescaleTransferFunctionToDataRange(True, False)
        self.ctx.view.update()

    @change("pv_time_idx")
    def _on_time_change(self, pv_time_idx, **_):
        if not self.times:
            return

        if pv_time_idx < len(self.times):
            self.state.time_value = self.times[pv_time_idx]
            self.animation_scene.AnimationTime = self.state.time_value

        self.ctx.view.update()

    @change("pv_color_by")
    def _on_color_by(self, pv_color_by, **_):
        if self.representation is None:
            return

        if pv_color_by is None:
            self.representation.ColorBy(("POINTS", None))
        else:
            self.representation.ColorBy(pv_color_by.split(":::"))

        if self.ctx.view:
            self.ctx.view.update()

    @change("pv_selected_file")
    def _on_file_selected(self, pv_selected_file, **_):
        if not pv_selected_file or self.view is None:
            return

        self.load_file(pv_selected_file)
        if self.ctx.view:
            self.ctx.view.update()

    @change("pv_play")
    def _on_play(self, pv_play, **_):
        if pv_play:
            asynchronous.create_task(self._animate())

    def view_action(self, action):
        getattr(self.view, action)()
        self.ctx.view.reset_camera()

    async def _animate(self):
        while self.state.pv_play:
            with self.state:
                if self.state.pv_time_idx < self.state.pv_time_idx_max:
                    self.state.pv_time_idx += 1
                else:
                    self.state.pv_time_idx = 0
            await asyncio.sleep(0.1)

    def _build_ui(self, template_name):
        self.state.time_value = ""
        with SinglePageLayout(
            self.server, template_name=template_name, full_height=True
        ) as self.ui:
            with self.ui.content:
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 h-100",
                ):
                    pvw.VtkRemoteView(self.view, interactive_ratio=1, ctx_name="view")

            with self.ui.footer.clear() as footer:
                footer.classes = "pa-0"
                with v3.VCard(tile=True, flat=True, classes="w-100"):
                    with v3.VCardItem(classes="py-0 px-2"):
                        with v3.VRow(classes="d-flex align-center pa-0 ma-0"):
                            v3.VLabel("t=", classes="text-h6")
                            v3.VLabel("{{ time_value }}", classes="text-body-1")
                            v3.VSpacer()
                            v3.VBtn(
                                icon="mdi-skip-previous",
                                variant="plain",
                                click="pv_time_idx = 0",
                                density="compact",
                            )
                            v3.VBtn(
                                icon="mdi-stop",
                                variant="plain",
                                click="pv_play=false",
                                v_if=("pv_play", False),
                                density="compact",
                            )
                            v3.VBtn(
                                icon="mdi-play",
                                variant="plain",
                                click="pv_play=true",
                                v_else=True,
                                density="compact",
                            )
                            v3.VBtn(
                                icon="mdi-skip-next",
                                variant="plain",
                                click="pv_time_idx = pv_time_idx_max",
                                density="compact",
                            )
                    with v3.VCardItem(classes="pa-0"):
                        v3.VSlider(
                            v_model=("pv_time_idx", -1),
                            min=0,
                            step=1,
                            max=("pv_time_idx_max", -1),
                            hide_details=True,
                            density="comfortable",
                            classes="px-3 py-1",
                        )

            with self.ui.toolbar.clear() as toolbar:
                toolbar.density = "comfortable"
                v3.VToolbarTitle("Festim PostProcessor")
                v3.VSpacer()
                with v3.VSelect(
                    label="File",
                    v_model=("pv_selected_file", None),
                    items=("pv_file_items", []),
                    item_title="title",
                    item_value="value",
                    density="compact",
                    hide_details=True,
                    variant="outlined",
                    style="max-width: 320px;",
                    classes="mx-2",
                ):
                    with v3.Template(raw_attrs=['v-slot:item="{ props, item }"']):
                        v3.VListItem(
                            v_bind="props",
                            subtitle=("item.raw.subtitle",),
                        )
                v3.VSelect(
                    label="Color By",
                    v_model=("pv_color_by", None),
                    items=("pv_color_options", []),
                    density="compact",
                    hide_details=True,
                    variant="outlined",
                    style="max-width: 250px;",
                    classes="mx-2",
                )

                with html.Div(classes="d-flex ga-2 mx-2"):
                    v3.VBtn(
                        icon="mdi-arrow-expand-horizontal",
                        click=self.reset_color_range,
                        classes="rounded",
                        density="compact",
                    )
                    v3.VBtn(
                        icon="mdi-axis-x-arrow",
                        click=(self.view_action, "['ResetActiveCameraToPositiveX']"),
                        classes="rounded",
                        density="compact",
                    )
                    v3.VBtn(
                        icon="mdi-axis-y-arrow",
                        click=(self.view_action, "['ResetActiveCameraToPositiveY']"),
                        classes="rounded",
                        density="compact",
                    )
                    v3.VBtn(
                        icon="mdi-axis-z-arrow",
                        click=(self.view_action, "['ResetActiveCameraToPositiveZ']"),
                        classes="rounded",
                        density="compact",
                    )
                    v3.VBtn(
                        icon="mdi-crop-free",
                        click=self.ctx.view.reset_camera,
                        classes="rounded",
                        density="compact",
                    )


if __name__ == "__main__":
    app = PostProcessing()
    app.server.start()
