from pathlib import Path

from trame.widgets import html
from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page

try:
    from paraview import simple
    from trame.widgets import paraview

    PARAVIEW_AVAILABLE = True
except ImportError:
    PARAVIEW_AVAILABLE = False


class ResultsPage(Page):
    id = "results"
    title = "Results Visualisation"
    description = "Visualise the results of your simulation"

    def __init__(self, server, **kwargs):
        super().__init__(server, **kwargs)
        self.view = None
        self.html_view = None

        if PARAVIEW_AVAILABLE:
            filepath = "out/vol_1.bp"
            if Path(filepath).exists():
                try:
                    self.reader = simple.OpenDataFile(filepath)
                    self.view = simple.GetActiveViewOrCreate("RenderView")
                    simple.Show(self.reader, self.view)
                    simple.Render()
                    simple.ResetCamera()
                except Exception as e:
                    self.error_msg = f"Failed to open file: {e}"
            else:
                self.error_msg = f"Results file '{filepath}' not found."

    def build_ui(self):
        with v3.VContainer(
            v_show=(f"page_name == '{self.id}'",),
            fluid=True,
            classes="fill-height d-flex flex-column pa-0",
        ):
            if not PARAVIEW_AVAILABLE:
                with v3.VAlert(type="warning", prominent=True):
                    html.Div(
                        "ParaView python module is not installed or available in this environment. "
                    )
                    html.Div(
                        "Please install ParaView or run the application using pvpython."
                    )
                return

            filepath = "out/vol_1.bp"
            if not Path(filepath).exists():
                with v3.VAlert(type="info"):
                    html.Div(f"Simulation results ({filepath}) not found.")
                    html.Div("Please run the simulation first.")
                return

            if hasattr(self, "error_msg") and self.error_msg:
                with v3.VAlert(type="error"):
                    html.Div(self.error_msg)
                return

            with v3.VToolbar(dense=True, flat=True, classes="flex-grow-0"):
                v3.VToolbarTitle("ParaView View")
                v3.VSpacer()
                v3.VBtn(
                    "Reset Camera",
                    click=self.html_view.reset_camera if self.html_view else "",
                )

            with html.Div(
                classes="flex-grow-1 w-100",
                style="min-height: 400px; position: relative",
            ):
                self.html_view = paraview.VtkRemoteView(
                    self.view,
                    interactive_ratio=1,
                )

    def script_lines(self) -> list[str]:
        return []
