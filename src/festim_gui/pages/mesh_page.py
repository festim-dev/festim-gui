from festim_gui.festim_ui.mesh import MeshComponent
from festim_gui.festim_ui.problem import ProblemComponent
from festim_gui.pages.page import Page


class MeshPage(Page):
    id = "mesh"
    title = "2. Mesh"
    description = "Configure mesh geometry and metadata."
    state_keys = MeshComponent.state_keys

    def init_state(self, state) -> None:
        MeshComponent.init_state(state)

    def build_ui(self) -> None:
        MeshComponent()

    def script_lines(self, state) -> list[str]:
        problem_var = ProblemComponent.from_state(state).var_name
        return ["# 2. Create mesh", *MeshComponent.to_script_lines(state, problem_var)]
