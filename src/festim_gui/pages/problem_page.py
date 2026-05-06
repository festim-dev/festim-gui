from festim_gui.festim_ui.problem import ProblemComponent
from festim_gui.pages.page import Page


class ProblemPage(Page):
    id = "problem"
    title = "1. Problem"
    description = "Create the root FESTIM problem object."
    state_keys = ProblemComponent.state_keys

    def init_state(self, state) -> None:
        ProblemComponent.init_state(state)

    def build_ui(self) -> None:
        ProblemComponent()

    def script_lines(self, state) -> list[str]:
        model = ProblemComponent.from_state(state)
        return ["# 1. Create empty problem", *ProblemComponent.to_script_lines(model)]
