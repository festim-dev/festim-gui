from festim_gui.festim_ui.material import MaterialComponent
from festim_gui.pages.page import Page


class MaterialsPage(Page):
    id = "materials"
    title = "3. Materials"
    description = "Create one or more F.Material objects."
    state_keys = MaterialComponent.state_keys

    def init_state(self, state) -> None:
        MaterialComponent.init_state(state)

    def build_ui(self) -> None:
        MaterialComponent()

    def script_lines(self, state) -> list[str]:
        items = MaterialComponent.from_state(state)
        return ["# 3. Create materials", *MaterialComponent.to_script_lines(items)]
