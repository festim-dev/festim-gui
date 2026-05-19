from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3
from trame.ui.html import DivLayout

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import (
    as_bool,
    build_initial_rows,
    comma_separated_list_expr,
    resolve_template_row,
)

SPECIES_DEFAULTS = {
    "var": "species_{i}",
    "name": "species_{i}",
    "mobile": False,
    "subdomains": "volume_1, volume_2",
}
INITIAL_SPECIES = [
    {"var": "H", "name": "H", "mobile": True, "subdomains": "volume_1, volume_2"},
    {
        "var": "H_trapped",
        "name": "H_trapped",
        "mobile": False,
        "subdomains": "volume_1, volume_2",
    },
    {
        "var": "empty_trap",
        "name": "empty_trap",
        "mobile": False,
        "subdomains": "volume_1, volume_2",
    },
]


class SpeciesPageState(StateDataModel):
    species_rows = Sync(
        list,
        lambda: build_initial_rows(SPECIES_DEFAULTS, INITIAL_SPECIES),
        client_deep_reactive=True,
    )


class SpeciesPage(Page):
    id = "species"
    title = "5a. Species"
    description = "Create one or more F.Species objects."

    def __init__(self, server):
        super().__init__(server, ctx_name="page_species")
        self.config = SpeciesPageState(server)
        self.config.watch(["species_rows"], self.notify_script_change, sync=True)
        self.build_ui()

    def add_species(self, *_args, **_kwargs):
        rows = list(self.config.species_rows)
        rows.append(resolve_template_row(SPECIES_DEFAULTS, len(rows)))
        self.config.species_rows = rows

    def remove_species(self, *_args, **_kwargs):
        rows = list(self.config.species_rows)
        if len(rows) <= 1:
            return
        rows.pop()
        self.config.species_rows = rows

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("species_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        RepeatedItemControls(
                            on_add=self.add_species, on_remove=self.remove_species
                        )
                        with v3.VCard(
                            variant="tonal",
                            v_for="(species_row, idx) in species_config.species_rows",
                            key=("idx",),
                        ):
                            with v3.VCardText(classes="d-flex flex-column ga-2"):
                                v3.VLabel("Species {{ idx + 1 }}", classes="text-caption")
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="species_row.var",
                                            label="Variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="species_row.name",
                                            label="name",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                v3.VSwitch(
                                    v_model="species_row.mobile",
                                    label="mobile",
                                    color="primary",
                                    hide_details=True,
                                    update_modelValue=self.notify_script_change,
                                )
                                v3.VTextField(
                                    v_model="species_row.subdomains",
                                    label="subdomains (comma-separated vars)",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        problem_var = self.page_problem.problem_var
        lines = ["# 5a. Create species"]
        rows = self.config.species_rows

        species_var_names = []
        for idx, row in enumerate(rows):
            defaults = resolve_template_row(SPECIES_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            name = str(row.get("name", defaults["name"]))
            mobile = as_bool(row.get("mobile", defaults["mobile"]), False)
            subdomains_expr = str(row.get("subdomains", defaults["subdomains"]))
            species_var_names.append(var_name)
            lines.append(f'{var_name} = F.Species(name="{name}", mobile={mobile})')
            lines.append(
                f"{var_name}.subdomains = {comma_separated_list_expr(subdomains_expr)}"
            )

        if species_var_names:
            lines.append(f"{problem_var}.species = [{', '.join(species_var_names)}]")

        return lines
