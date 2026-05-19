from trame.widgets import vuetify3 as v3
from trame.ui.html import DivLayout

from festim_gui.pages.page import Page


class RunPage(Page):
    id = "run"
    title = "10. Run"
    description = "Review the full script and run the simulation."

    def __init__(self, server):
        super().__init__(server, ctx_name="page_run")
        self.build_ui()

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with v3.VCard(variant="outlined"):
                with v3.VCardText(classes="d-flex flex-column ga-2"):
                    v3.VLabel("Run", classes="text-subtitle-2")
                    v3.VLabel(
                        "This final step shows the full script. "
                        "Use the code panel toggle to switch views if needed.",
                        classes="text-body-2 text-medium-emphasis",
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
