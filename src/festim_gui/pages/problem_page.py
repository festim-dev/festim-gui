from trame.app.dataclass import StateDataModel, Sync
from trame.ui.html import DivLayout
from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page

DEFAULTS = {
    "problem_var": "problem",
    "problem_class": "HydrogenTransportProblemDiscontinuous",
}
PROBLEM_TYPES = [
    "HydrogenTransportProblem",
    "HydrogenTransportProblemDiscontinuous",
]


class ProblemPageState(StateDataModel):
    problem_var = Sync(str, DEFAULTS["problem_var"])
    problem_class = Sync(str, DEFAULTS["problem_class"])


class ProblemPage(Page):
    id = "problem"
    title = "1. Problem"
    description = "Create the root FESTIM problem object."
    problem_types = PROBLEM_TYPES

    def __init__(self, server):
        super().__init__(server, ctx_name="page_problem")
        self.config = ProblemPageState(server)
        self.config.watch(
            ["problem_var", "problem_class"], self.notify_script_change, sync=True
        )
        self.build_ui()

    @property
    def problem_var(self) -> str:
        return self.config.problem_var

    def build_ui(self):
        with DivLayout(self.server, template_name=self.id):
            with v3.VCard(variant="outlined"):
                with v3.VCardText(classes="d-flex flex-column ga-3"):
                    with self.config.provide_as("problem_config"):
                        v3.VTextField(
                            v_model="problem_config.problem_var",
                            label="Python variable",
                            density="comfortable",
                            variant="outlined",
                            update_modelValue=self.notify_script_change,
                        )
                        v3.VSelect(
                            v_model="problem_config.problem_class",
                            items=(self.problem_types,),
                            label="FESTIM problem class",
                            density="comfortable",
                            variant="outlined",
                            update_modelValue=self.notify_script_change,
                        )

    def script_lines(self) -> list[str]:
        return [
            "# 1. Create empty problem",
            f"{self.config.problem_var} = F.{self.config.problem_class}()",
        ]
