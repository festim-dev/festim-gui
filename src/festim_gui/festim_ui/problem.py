from dataclasses import dataclass

from trame.widgets import vuetify3 as v3

from .utils import set_missing_state_defaults

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


def init_state(state) -> None:
    set_missing_state_defaults(state, DEFAULTS)


def from_state(state) -> ProblemModel:
    return ProblemModel(
        var_name=state.problem_var,
        klass=state.problem_class,
    )


def build_form() -> None:
    with v3.VCard(variant="outlined"):
        v3.VCardTitle("1. Problem")
        with v3.VCardText(classes="d-flex flex-column ga-3"):
            v3.VTextField(
                v_model=("problem_var", DEFAULTS["problem_var"]),
                label="Python variable",
                density="comfortable",
                variant="outlined",
            )
            v3.VSelect(
                v_model=("problem_class", DEFAULTS["problem_class"]),
                items=(PROBLEM_TYPES,),
                label="FESTIM problem class",
                density="comfortable",
                variant="outlined",
            )


def to_script_lines(model: ProblemModel) -> list[str]:
    return [f"{model.var_name} = F.{model.klass}()"]
