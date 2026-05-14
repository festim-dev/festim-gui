from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import as_float, build_initial_rows, resolve_template_row

INITIAL_CONCENTRATION_DEFAULTS = {
    "var": "ic_{i}",
    "species_var": "empty_trap",
    "value": 1.0,
    "volume_var": "volume_1",
}
INITIAL_CONCENTRATIONS = [
    {
        "var": "ic_1",
        "species_var": "empty_trap",
        "value": 1.0,
        "volume_var": "volume_1",
    }
]


class InitialConditionsPageState(StateDataModel):
    initial_condition_rows = Sync(
        list,
        lambda: build_initial_rows(
            INITIAL_CONCENTRATION_DEFAULTS, INITIAL_CONCENTRATIONS
        ),
        client_deep_reactive=True,
    )


class InitialConditionsPage(Page):
    id = "initial_conditions"
    title = "5b. Initial Conditions"
    description = "Create one or more F.InitialConcentration objects."

    def __init__(self, server, problem_page):
        super().__init__(server)
        self._problem_page = problem_page
        self.config = InitialConditionsPageState(server)
        self.config.watch(
            ["initial_condition_rows"], self.notify_script_change, sync=True
        )

    def add_initial_condition(self, *_args, **_kwargs):
        rows = list(self.config.initial_condition_rows)
        rows.append(resolve_template_row(INITIAL_CONCENTRATION_DEFAULTS, len(rows)))
        self.config.initial_condition_rows = rows

    def remove_initial_condition(self, *_args, **_kwargs):
        rows = list(self.config.initial_condition_rows)
        if len(rows) <= 1:
            return
        rows.pop()
        self.config.initial_condition_rows = rows

    def build_ui(self) -> None:
        with self.config.provide_as("initial_conditions_config"):
            with v3.VCard(variant="outlined"):
                with v3.VCardText(classes="d-flex flex-column ga-3"):
                    RepeatedItemControls(
                        on_add=self.add_initial_condition,
                        on_remove=self.remove_initial_condition,
                    )
                    with v3.VCard(
                        variant="tonal",
                        v_for="(ic_row, idx) in initial_conditions_config.initial_condition_rows",
                        key=("idx",),
                    ):
                        with v3.VCardText(classes="d-flex flex-column ga-2"):
                            v3.VLabel(
                                "Initial concentration {{ idx + 1 }}",
                                classes="text-caption",
                            )
                            with v3.VRow(classes="ga-0"):
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="ic_row.var",
                                        label="Variable",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="ic_row.species_var",
                                        label="species variable",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                            with v3.VRow(classes="ga-0"):
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="ic_row.value",
                                        label="value",
                                        type="number",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="ic_row.volume_var",
                                        label="volume variable",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )

    def script_lines(self) -> list[str]:
        problem_var = self._problem_page.problem_var
        lines = ["# 5b. Create initial conditions"]
        rows = self.config.initial_condition_rows

        condition_var_names = []
        for idx, row in enumerate(rows):
            defaults = resolve_template_row(INITIAL_CONCENTRATION_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            species_var = str(row.get("species_var", defaults["species_var"]))
            value = as_float(
                row.get("value", defaults["value"]),
                INITIAL_CONCENTRATION_DEFAULTS["value"],
            )
            volume_var = str(row.get("volume_var", defaults["volume_var"]))
            condition_var_names.append(var_name)
            lines.append(
                f"{var_name} = F.InitialConcentration("
                f"species={species_var}, value={value}, volume={volume_var})"
            )

        if condition_var_names:
            lines.append(
                f"{problem_var}.initial_conditions = [{', '.join(condition_var_names)}]"
            )

        return lines
