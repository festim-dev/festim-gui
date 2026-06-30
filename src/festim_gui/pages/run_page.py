import asyncio

from trame.app.dataclass import StateDataModel, Sync, watch
from trame.ui.html import DivLayout
from trame.widgets import html
from trame.widgets import vuetify3 as v3

from festim_gui.execution import ScriptExecutionManager
from festim_gui.pages.page import Page
from festim_gui.utils.script_builder import build_script

RUN_LOG_TAIL_MAX_CHARS = 200_000

RUN_STATUS_METADATA = {
    "idle": ("Idle", "default"),
    "starting": ("Starting", "warning"),
    "running": ("Running", "warning"),
    "succeeded": ("Succeeded", "success"),
    "failed": ("Failed", "error"),
}


def _append_log_tail(current: str, text: str) -> str:
    combined = f"{current}{text}"
    if len(combined) <= RUN_LOG_TAIL_MAX_CHARS:
        return combined
    return combined[-RUN_LOG_TAIL_MAX_CHARS:]


class RunPageState(StateDataModel):
    is_active = Sync(bool, False)
    log_tail = Sync(str, "")
    output_dir = Sync(str, "")
    log_path = Sync(str, "")
    return_code = Sync(str, "")
    started_at = Sync(str, "")
    finished_at = Sync(str, "")
    status = Sync(str, "idle")
    status_label = Sync(str, RUN_STATUS_METADATA["idle"][0])
    status_color = Sync(str, RUN_STATUS_METADATA["idle"][1])
    status_message = Sync(str, "Ready to execute the generated script.")

    @watch("status", sync=True)
    def _sync_status_display(self, status: str) -> None:
        label, color = RUN_STATUS_METADATA[status]
        self.status_label = label
        self.status_color = color


class RunPage(Page):
    id = "run"
    title = "10. Run"
    description = "Review the full script and run the simulation."

    def __init__(self, server, pages: list):
        super().__init__(server, ctx_name="page_run")
        self.config = RunPageState(server)
        self._pages = pages
        self._execution = ScriptExecutionManager()

        server.controller.on_server_ready.add_task(self._monitor_execution_events)

        self.build_ui()

    def _set_run_status(self, status: str, message: str) -> None:
        self.config.update(status=status, status_message=message)

    def _reset_run_state(self) -> None:
        self.config.update(
            is_active=False,
            log_tail="",
            output_dir="",
            log_path="",
            return_code="",
            started_at="",
            finished_at="",
        )

    def _run_simulation(self) -> None:
        if self._execution.is_running:
            self._set_run_status("running", "A simulation is already running.")
            return

        self._reset_run_state()
        self._set_run_status("starting", "Launching simulation...")

        try:
            self._execution.start(build_script(self._pages, include_header=True))
        except Exception as exc:
            self.config.log_tail = f"[festim-gui] {exc}\n"
            self._set_run_status("failed", str(exc))

    async def _monitor_execution_events(self, **_kwargs) -> None:
        while True:
            events = self._execution.drain_events()
            for event in events:
                if event.kind == "started":
                    self.config.is_active = True
                    self.config.output_dir = event.output_dir
                    self.config.log_path = event.log_path
                    self.config.started_at = event.timestamp
                    self._set_run_status(
                        "running",
                        "Simulation is running. Log view shows the live tail.",
                    )

                elif event.kind in ("log", "error"):
                    self.config.log_tail = _append_log_tail(
                        self.config.log_tail,
                        event.text,
                    )

                elif event.kind == "finished":
                    self.config.is_active = False
                    self.config.finished_at = event.timestamp
                    self.config.return_code = str(event.return_code) if event.return_code is not None else ""
                    if event.return_code == 0:
                        self._set_run_status(
                            "succeeded",
                            "Simulation completed successfully.",
                        )
                    else:
                        msg = (
                            f"Simulation failed with exit code {event.return_code}."
                            if event.return_code is not None
                            else "Simulation was interrupted."
                        )
                        self._set_run_status("failed", msg)

            await asyncio.sleep(0.1)

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("run_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        v3.VLabel("Run", classes="text-subtitle-2")
                        v3.VLabel(
                            "Run the full generated script in the current Python environment. "
                            "The log panel shows a live tail while the full log is written to disk.",
                            classes="text-body-2 text-medium-emphasis",
                        )
                        with v3.VRow(classes="ga-2 align-center"):
                            with v3.VCol(cols="12", sm="auto"):
                                v3.VBtn(
                                    "Run simulation",
                                    color="primary",
                                    prepend_icon="mdi-play",
                                    variant="flat",
                                    click=self._run_simulation,
                                    loading=("run_config.is_active", False),
                                    disabled=("run_config.is_active", False),
                                )
                            with v3.VCol(cols="12", sm="auto"):
                                v3.VChip(
                                    "{{ run_config.status_label }}",
                                    color=("run_config.status_color", "default"),
                                    variant="tonal",
                                )
                        html.Div(
                            "{{ run_config.status_message }}",
                            classes="text-body-2",
                        )
                        html.Div(
                            "Output directory: {{ run_config.output_dir }}",
                            classes="text-caption",
                            v_if=("run_config.output_dir",),
                        )
                        html.Div(
                            "Log file: {{ run_config.log_path }}",
                            classes="text-caption text-medium-emphasis",
                            v_if=("run_config.log_path",),
                        )
                        html.Div(
                            "Exit code: {{ run_config.return_code }}",
                            classes="text-caption text-medium-emphasis",
                            v_if=("run_config.return_code !== ''",),
                        )
                        with v3.VSheet(
                            border=True,
                            rounded="lg",
                            classes="pa-3 overflow-y-auto",
                            style="background-color: #111111; min-height: 280px; max-height: 420px;",
                        ):
                            html.Pre(
                                "{{ run_config.log_tail || 'No log output yet.' }}",
                                style=(
                                    "margin: 0; white-space: pre-wrap; word-break: break-word; "
                                    "font-family: monospace; font-size: 0.875rem; color: #d4d4d4;"
                                ),
                            )

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        problem_var = self.page_problem.problem_var
        return [
            "# 10. Run",
            "",
            "# initialise and run the problem",
            f"{problem_var}.initialise()",
            f"{problem_var}.run()",
        ]
