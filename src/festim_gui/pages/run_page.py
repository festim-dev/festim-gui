from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page


class RunPage(Page):
    id = "run"
    title = "10. Run"
    description = "Review the full script and run the simulation."

    def __init__(self, server, problem_page):
        super().__init__(server)
        self._problem_page = problem_page

    def build_ui(self) -> None:
        with v3.VCard(variant="outlined"):
            with v3.VCardText(classes="d-flex flex-column ga-2"):
                v3.VLabel("Run", classes="text-subtitle-2")
                v3.VLabel(
                    "This final step shows the full script. "
                    "Use the code panel toggle to switch views if needed.",
                    classes="text-body-2 text-medium-emphasis",
                )

    def script_lines(self) -> list[str]:
        problem_var = self._problem_page.problem_var
        return [
            "# 10. Run",
            "",
            "# initialise and run the problem",
            f"{problem_var}.initialise()",
            f"{problem_var}.run()",
        ]
