from dataclasses import dataclass

from trame.widgets import vuetify3 as v3

from festim_gui.festim_ui.component import FestimComponent
from festim_gui.utils.utils import set_missing_state_defaults

DEFAULTS = {
    "problem_var": "problem",
    "problem_class": "HydrogenTransportProblemDiscontinuous",
}
PROBLEM_TYPES = [
    "HydrogenTransportProblem",
    "HydrogenTransportProblemDiscontinuous",
]
STATE_KEYS = list(DEFAULTS.keys())


@dataclass
class ProblemModel:
    var_name: str
    klass: str


class ProblemComponent(FestimComponent):
    card_title = "1. Problem"
    defaults = DEFAULTS
    problem_types = PROBLEM_TYPES
    state_keys = STATE_KEYS

    @staticmethod
    def init_state(state) -> None:
        set_missing_state_defaults(state, ProblemComponent.defaults)

    @staticmethod
    def from_state(state) -> ProblemModel:
        return ProblemModel(
            var_name=state.problem_var,
            klass=state.problem_class,
        )

    def build_content(self) -> None:
        v3.VTextField(
            v_model=("problem_var", self.defaults["problem_var"]),
            label="Python variable",
            density="comfortable",
            variant="outlined",
        )
        v3.VSelect(
            v_model=("problem_class", self.defaults["problem_class"]),
            items=(self.problem_types,),
            label="FESTIM problem class",
            density="comfortable",
            variant="outlined",
        )

    @staticmethod
    def to_script_lines(model: ProblemModel) -> list[str]:
        return [f"{model.var_name} = F.{model.klass}()"]
