from datetime import datetime
from itertools import pairwise
from pathlib import Path

from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html
from trame.widgets import paraview as pv_widgets
from trame.widgets import vuetify3 as v3

from festim_gui.execution import find_vtx_dirs, resolve_run_root

try:
    from paraview import simple
except ModuleNotFoundError:
    simple = None


class PostProcessing:
    def __init__(self, server):
        self.server = server
        self.state = server.state
        self.view = None
        self.source = None
        self.display = None
        self.html_view = None
        self.scene = None
        self.current_vtx_path = ""

        self._reset_controls()
        self.state.post_processing_status_message = (
            "Open this page after a successful run to inspect the latest VTX output."
        )

        if simple is not None:
            self.view = simple.GetActiveViewOrCreate("RenderView")
            self.scene = simple.GetAnimationScene()
            self.view.OrientationAxesVisibility = 0
            self.view.Background = [0.12, 0.12, 0.12]
            self.view.UseColorPaletteForBackground = 0

        self._build_ui()
        self.state.change("post_processing_selected_vtx")(self._on_vtx_file_selected)
        self.state.change("post_processing_selected_array")(self._on_array_selected)
        self.state.change("post_processing_time")(self._on_time_changed)
        self.server.controller.on_server_ready.add(self.reload)

    def _clear_pipeline(self):
        if self.display is not None:
            simple.Hide(self.source, self.view)
            self.display = None

        if self.source is not None:
            simple.Delete(self.source)
            self.source = None

        self.current_vtx_path = ""

    def _read_arrays(self):
        arrays = {}
        data_info = self.source.GetDataInformation()
        for data_set, location in (
            (data_info.GetPointDataInformation(), "POINTS"),
            (data_info.GetCellDataInformation(), "CELLS"),
        ):
            for index in range(data_set.GetNumberOfArrays()):
                array = data_set.GetArrayInformation(index)
                if array is None or not array.GetName():
                    continue
                label = f"{location}: {array.GetName()}"
                arrays[label] = (location, array.GetName())
        return arrays

    def _render(self):
        if self.view is None:
            return

        self.view.Update()
        if self.html_view is not None and self.server.protocol:
            self.html_view.update()

    def _color_by_array(self, label):
        array_info = self.arrays.get(label)
        if array_info is None or self.display is None:
            return

        simple.ColorBy(self.display, array_info)
        self.display.RescaleTransferFunctionToDataRange(True, False)
        self.display.SetScalarBarVisibility(self.view, True)

    def _reset_controls(self):
        self.arrays = {}
        self.state.post_processing_vtx_items = []
        self.state.post_processing_selected_vtx = ""
        self.state.post_processing_array_items = []
        self.state.post_processing_selected_array = ""
        self.time_values = []
        self.state.post_processing_time = 0.0
        self.state.post_processing_time_min = 0.0
        self.state.post_processing_time_max = 0.0
        self.state.post_processing_time_step = 1.0

    def _go_to_time(self, time_val: float):
        if not self.time_values or self.scene is None:
            return
        nearest = min(self.time_values, key=lambda t: abs(t - time_val))
        self.scene.TimeKeeper.Time = nearest
        self.state.post_processing_time = nearest

    def _on_vtx_file_selected(self, post_processing_selected_vtx, **_kwargs):
        if post_processing_selected_vtx and self.view is not None:
            self._load_vtx(post_processing_selected_vtx)

    def _on_array_selected(self, post_processing_selected_array, **_kwargs):
        self._color_by_array(post_processing_selected_array)
        self._render()

    def _on_time_changed(self, post_processing_time, **_kwargs):
        self._go_to_time(float(post_processing_time))
        self._render()

    def _update_display(self, vtx_dir):
        self.source.UpdatePipeline()
        if self.scene is not None:
            self.scene.UpdateAnimationUsingDataTimeSteps()
            self.time_values = list(self.scene.TimeKeeper.TimestepValues)
            if self.time_values:
                self.state.post_processing_time_min = self.time_values[0]
                self.state.post_processing_time_max = self.time_values[-1]
                if len(self.time_values) > 1:
                    self.state.post_processing_time_step = min(
                        b - a for a, b in pairwise(self.time_values)
                    )

        self.arrays = self._read_arrays()
        array_items = list(self.arrays)
        self.state.post_processing_array_items = array_items

        active_array = self.state.post_processing_selected_array
        if active_array not in self.arrays:
            active_array = array_items[0] if array_items else ""
            self.state.post_processing_selected_array = active_array

        self._go_to_time(self.time_values[0] if self.time_values else 0.0)
        self._color_by_array(active_array)
        self._render()
        self.state.post_processing_status_message = f"Displaying {vtx_dir.name}."

    def _load_vtx(self, vtx_path):
        vtx_dir = Path(vtx_path)
        if not vtx_dir.is_dir():
            self._reset_controls()
            self.state.post_processing_status_message = (
                "The recorded VTX output path no longer exists on disk."
            )
            return

        if (
            self.source is None
            or self.display is None
            or self.current_vtx_path != vtx_path
        ):
            self._clear_pipeline()
            self.source = simple.ADIOS2VTXReader(
                registrationName=vtx_dir.name,
                FileName=str(vtx_dir),
            )
            self.display = simple.Show(
                self.source,
                self.view,
                "UnstructuredGridRepresentation",
            )
            self.display.Representation = "Surface"
            self.current_vtx_path = vtx_path
            self.view.ResetCamera(False, 0.9)

        self._update_display(vtx_dir)

    def reload(self, **_kwargs):
        vtx_dirs = find_vtx_dirs(resolve_run_root())

        if not vtx_dirs:
            self._reset_controls()
            self.state.post_processing_status_message = (
                "No completed run with VTX output is available yet."
            )
            return

        if self.view is None:
            self._reset_controls()
            self.state.post_processing_status_message = (
                "Visualization is unavailable because ParaView is not installed."
            )
            return

        vtx_items = []
        for p in vtx_dirs:
            path = Path(p)
            try:
                ctime = datetime.fromtimestamp(path.stat().st_ctime).strftime("%Y-%m-%d %H:%M")
            except OSError:
                ctime = "unknown"
            vtx_items.append({
                "title": path.name,
                "subtitle": f"{path.parent.parent.name}  ·  {ctime}",
                "value": p,
            })
        self.state.post_processing_vtx_items = vtx_items
        if self.state.post_processing_selected_vtx not in vtx_dirs:
            self.state.post_processing_selected_vtx = vtx_dirs[0]

        self._load_vtx(self.state.post_processing_selected_vtx)

    def _build_ui(self):
        with SinglePageLayout(
            self.server,
            template_name="post-processing",
            full_height=True,
        ) as layout:
            layout.icon.hide()
            layout.title.set_text("Post Processing")
            layout.footer.hide()

            with layout.toolbar:
                v3.VSpacer()
                with v3.VSelect(
                    v_model=("post_processing_selected_vtx", ""),
                    items=("post_processing_vtx_items", []),
                    label="File",
                    item_title="title",
                    item_value="value",
                    hide_details=True,
                    density="compact",
                    variant="outlined",
                    style="max-width: 280px;",
                    classes="mr-3",
                ):
                    with v3.Template(raw_attrs=['v-slot:item="{ props, item }"']):
                        v3.VListItem(
                            v_bind="props",
                            subtitle=("item.raw.subtitle",),
                        )
                v3.VSelect(
                    v_model=("post_processing_selected_array", ""),
                    items=("post_processing_array_items", []),
                    label="Variable",
                    hide_details=True,
                    density="compact",
                    variant="outlined",
                    style="max-width: 280px;",
                    classes="mr-3",
                )
                html.Div(
                    "t = {{ post_processing_time }}",
                    classes="text-caption text-medium-emphasis mr-3",
                )
                v3.VSlider(
                    v_model=("post_processing_time", 0),
                    min=("post_processing_time_min", 0),
                    max=("post_processing_time_max", 0),
                    step=("post_processing_time_step", 1),
                    hide_details=True,
                    density="compact",
                    style="max-width: 240px;",
                    classes="mr-3",
                )
                v3.VBtn(
                    "Refresh",
                    prepend_icon="mdi-refresh",
                    variant="outlined",
                    click=self.reload,
                )

            with layout.content:
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                    style="background-color: #111111;",
                ):
                    if self.view is None:
                        with html.Div(
                            classes="d-flex align-center justify-center fill-height",
                            style="color: #d4d4d4;",
                        ):
                            html.Div(
                                "{{ post_processing_status_message }}",
                                classes="text-body-1",
                                style="white-space: pre-wrap; max-width: 600px;",
                            )
                    else:
                        self.html_view = pv_widgets.VtkLocalView(self.view)
