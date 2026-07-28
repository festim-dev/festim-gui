import asyncio
from pathlib import Path

from paraview import simple
from trame.app import TrameApp, asynchronous
from trame.decorators import change
from trame.ui.html import DivLayout
from trame.widgets import client, html
from trame.widgets import paraview as pvw
from trame.widgets import vuetify3 as v3

RESULTS_AVAILABLE = "page_name === 'run' && vtx_paths.length"
RESULTS_PANEL_VISIBLE = f"{RESULTS_AVAILABLE} && panel_view_mode === 'results'"


class ResultsViewToggle(v3.VBtnToggle):
    """Switch the right hand panel between the generated script and the results."""

    def __init__(self, **kwargs):
        super().__init__(
            v_model=("panel_view_mode", "script"),
            v_if=RESULTS_AVAILABLE,
            mandatory=True,
            density="compact",
            divided=True,
            variant="outlined",
            **kwargs,
        )

        with self:
            v3.VBtn("Script", value="script")
            v3.VBtn("Results", value="results")


class ResultsPanel(v3.VCard):
    """Host the post-processing template in place of the script editor."""

    def __init__(self, **kwargs):
        super().__init__(
            variant="outlined",
            classes="fill-height d-flex flex-column overflow-hidden",
            **kwargs,
        )

        with self:
            client.ServerTemplate(name="post-processing")


class PostProcessing(TrameApp):
    def __init__(self, server=None, template_name="post-processing"):
        super().__init__(server)

        self.server.cli.add_argument(
            "--gpu",
            action="store_true",
            help="Use GPU for rendering.",
        )
        self.use_gpu = self.server.cli.parse_known_args()[0].gpu

        pvw.initialize(self.server)
        v3.initialize(self.server)

        self._setup_pv()
        self._build_ui(template_name)

    def _setup_pv(self):
        self.times = []
        self.state.time_value = ""
        self.state.pv_time_idx_max = -1
        self.state.pv_time_controls_width = self._time_controls_width(0)
        self.state.pv_color_options = []
        self.state.pv_color_by = None
        self.animation_scene = simple.GetAnimationScene()

        self.reader = None
        self.representation = None
        self.view = simple.GetActiveViewOrCreate("RenderView")
        self.view.Set(
            OrientationAxesVisibility=1,
            Background=[0.12, 0.12, 0.12],
        )

    def _time_controls_width(self, time_count):
        return f"min(100%, calc({max(time_count, 1)} * 5px + 24rem))"

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
        self.animation_scene.UpdateAnimationUsingDataTimeSteps()
        self.state.pv_time_idx_max = len(self.times) - 1
        self.state.pv_time_idx = 0
        self.state.pv_time_controls_width = self._time_controls_width(len(self.times))
        # pv_time_idx may already be 0, so apply the time rather than rely on @change
        self._apply_time(0)

        self.state.pv_color_options = options
        if self.state.pv_color_by not in {option["value"] for option in options}:
            self.state.pv_color_by = None

        self.representation.Visibility = 1
        self.representation.SetScalarBarVisibility(self.view, True)

        self.view.ResetCamera()
        if self.ctx.view:
            self.ctx.view.reset_camera()
            self.ctx.view.update()

    def _apply_time(self, time_index):
        if not self.times or time_index >= len(self.times):
            self.state.time_value = ""
            return

        time_value = self.times[time_index]
        self.state.time_value = f"{time_value:.3f}"
        self.animation_scene.AnimationTime = time_value

    def reset_color_range(self):
        self.representation.RescaleTransferFunctionToDataRange(True, False)
        self.ctx.view.update()

    @change("pv_time_idx")
    def _on_time_change(self, pv_time_idx, **_):
        if not self.times:
            return

        self._apply_time(pv_time_idx)
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

    @change("pv_play")
    def _on_play(self, pv_play, **_):
        if pv_play:
            asynchronous.create_task(self._animate())

    def view_action(self, action):
        getattr(self.view, action)()
        if self.use_gpu:
            self.ctx.view.reset_camera()
        else:
            simple.ResetCamera(self.view)
            self.ctx.view.push_camera()

    def reset_camera(self):
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
        with DivLayout(
            self.server,
            template_name=template_name,
            classes="d-flex flex-column pt-1",
            style="height: 100%; min-height: 0;",
        ) as self.ui:
            with v3.VToolbar(density="compact", color="transparent", flat=True):
                v3.VToolbarTitle("Result view")

                v3.VSpacer()
                v3.VSelect(
                    label="Color By",
                    v_model=("pv_color_by", None),
                    items=("pv_color_options", []),
                    density="compact",
                    hide_details=True,
                    variant="outlined",
                    style="max-width: 220px;",
                    classes="mx-2",
                )

                with html.Div(classes="d-flex ga-2 mr-2"):
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
                        click=self.reset_camera,
                        classes="rounded",
                        density="compact",
                    )

                ResultsViewToggle(classes="mr-2")

            with html.Div(
                classes="flex-grow-1",
                style="position: relative; width: 100%; min-height: 0;",
            ):
                if self.use_gpu:
                    pvw.VtkRemoteView(
                        self.view,
                        interactive_ratio=1,
                        ctx_name="view",
                    )
                else:
                    pvw.VtkLocalView(
                        self.view,
                        ctx_name="view",
                    )
                with html.Div(
                    style=(
                        "{"
                        " position: 'absolute',"
                        " left: '1rem',"
                        " right: '1rem',"
                        " bottom: '0.5rem',"
                        " display: 'flex',"
                        " justifyContent: 'center',"
                        " zIndex: 10,"
                        " pointerEvents: 'none'"
                        "}",
                    )
                ):
                    with v3.VCard(
                        elevation=4,
                        style=(
                            "{"
                            " backgroundColor: '#ffffff',"
                            " width: pv_time_controls_width,"
                            " maxWidth: '100%',"
                            " pointerEvents: 'auto'"
                            "}",
                        ),
                    ):
                        with v3.VCardText(classes="px-2 py-1"):
                            with html.Div(classes="d-flex align-center ga-0"):
                                v3.VBtn(
                                    icon="mdi-skip-previous",
                                    variant="plain",
                                    click="pv_time_idx = 0",
                                    density="compact",
                                    disabled=("pv_time_idx <= 0", True),
                                )
                                v3.VBtn(
                                    icon="mdi-chevron-left",
                                    variant="plain",
                                    click="pv_time_idx = Math.max(pv_time_idx - 1, 0)",
                                    density="compact",
                                    disabled=("pv_time_idx <= 0", True),
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
                                    icon="mdi-chevron-right",
                                    variant="plain",
                                    click="pv_time_idx = Math.min(pv_time_idx + 1, pv_time_idx_max)",
                                    density="compact",
                                    disabled=(
                                        "pv_time_idx < 0 || pv_time_idx >= pv_time_idx_max",
                                        True,
                                    ),
                                )
                                v3.VBtn(
                                    icon="mdi-skip-next",
                                    variant="plain",
                                    click="pv_time_idx = pv_time_idx_max",
                                    density="compact",
                                    disabled=(
                                        "pv_time_idx < 0 || pv_time_idx >= pv_time_idx_max",
                                        True,
                                    ),
                                )
                                with html.Div(classes="flex-grow-1"):
                                    v3.VSlider(
                                        v_model=("pv_time_idx", -1),
                                        min=0,
                                        step=1,
                                        max=("pv_time_idx_max", -1),
                                        hide_details=True,
                                        density="comfortable",
                                        disabled=("pv_time_idx_max < 0", True),
                                        classes="px-2",
                                    )
                                html.Div(
                                    "{{ pv_time_idx_max >= 0 ? '(' + (pv_time_idx + 1) + ' / ' + (pv_time_idx_max + 1) + ')' : '(0 / 0)' }}",
                                    classes="text-body-2 text-no-wrap pr-2",
                                )
                                html.Div(
                                    "t = {{ time_value }}",
                                    classes="text-body-2 text-no-wrap",
                                )
