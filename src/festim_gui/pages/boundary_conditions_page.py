from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import as_float, build_initial_rows, resolve_template_row

BOUNDARY_CONDITION_DEFAULTS = {
    "var": "bc_{i}",
    "subdomain_var": "surface_{i}",
    "species_var": "H",
    "value": 1.0,
}
INITIAL_BOUNDARY_CONDITIONS = [
    {"var": "bc_1", "subdomain_var": "surface_1", "species_var": "H", "value": 1.0},
    {"var": "bc_2", "subdomain_var": "surface_2", "species_var": "H", "value": 0.0},
]


class BoundaryConditionsPageState(StateDataModel):
    boundary_condition_rows = Sync(
        list,
        lambda: build_initial_rows(
            BOUNDARY_CONDITION_DEFAULTS, INITIAL_BOUNDARY_CONDITIONS
        ),
        client_deep_reactive=True,
    )


class BoundaryConditionsPage(Page):
    id = "boundary_conditions"
    title = "6. Boundary Conditions"
    description = "Create one or more F.FixedConcentrationBC objects."

    def __init__(self, server, problem_page):
        super().__init__(server)
        self._problem_page = problem_page
        self.config = BoundaryConditionsPageState(server)
        self.config.watch(
            ["boundary_condition_rows"], self.notify_script_change, sync=True
        )

    def add_boundary_condition(self, *_args, **_kwargs):
        rows = list(self.config.boundary_condition_rows)
        rows.append(resolve_template_row(BOUNDARY_CONDITION_DEFAULTS, len(rows)))
        self.config.boundary_condition_rows = rows

    def remove_boundary_condition(self, *_args, **_kwargs):
        rows = list(self.config.boundary_condition_rows)
        if len(rows) <= 1:
            return
        rows.pop()
        self.config.boundary_condition_rows = rows

    def build_ui(self) -> None:
        with self.config.provide_as("boundary_conditions_config"):
            with v3.VCard(variant="outlined"):
                with v3.VCardText(classes="d-flex flex-column ga-3"):
                    RepeatedItemControls(
                        on_add=self.add_boundary_condition,
                        on_remove=self.remove_boundary_condition,
                    )
                    with v3.VCard(
                        variant="tonal",
                        v_for="(bc_row, idx) in boundary_conditions_config.boundary_condition_rows",
                        key=("idx",),
                    ):
                        with v3.VCardText(classes="d-flex flex-column ga-2"):
                            v3.VLabel("BC {{ idx + 1 }}", classes="text-caption")
                            with v3.VRow(classes="ga-0"):
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="bc_row.var",
                                        label="Variable",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="bc_row.value",
                                        label="value",
                                        type="number",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                            with v3.VRow(classes="ga-0"):
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="bc_row.subdomain_var",
                                        label="surface subdomain variable",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="bc_row.species_var",
                                        label="species variable",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )

    def script_lines(self) -> list[str]:
        problem_var = self._problem_page.problem_var
        lines = ["# 6. Create boundary conditions"]
        rows = self.config.boundary_condition_rows
        if not rows:
            rows = [resolve_template_row(BOUNDARY_CONDITION_DEFAULTS, 0)]

        bc_var_names = []
        for idx, row in enumerate(rows):
            defaults = resolve_template_row(BOUNDARY_CONDITION_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            subdomain_var = str(row.get("subdomain_var", defaults["subdomain_var"]))
            species_var = str(row.get("species_var", defaults["species_var"]))
            value = as_float(
                row.get("value", defaults["value"]),
                BOUNDARY_CONDITION_DEFAULTS["value"],
            )
            bc_var_names.append(var_name)
            lines.append(
                f"{var_name} = F.FixedConcentrationBC("
                f"subdomain={subdomain_var}, value={value}, species={species_var})"
            )

        lines.append(f"{problem_var}.boundary_conditions = [{', '.join(bc_var_names)}]")
        return lines
