from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3
from trame.ui.html import DivLayout

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import (
    as_float,
    build_initial_rows,
    comma_separated_list_expr,
    resolve_template_row,
)

REACTION_DEFAULTS = {
    "var": "reac_{i}",
    "reactants": "H, empty_trap",
    "products": "H_trapped",
    "k_0": 0.05,
    "E_k": 0.0,
    "p_0": 0.1,
    "E_p": 0.0,
    "volume_var": "volume_1",
}
INITIAL_REACTIONS = [
    {
        "var": "reac_1",
        "reactants": "H, empty_trap",
        "products": "H_trapped",
        "k_0": 0.05,
        "E_k": 0.0,
        "p_0": 0.1,
        "E_p": 0.0,
        "volume_var": "volume_1",
    }
]


class ReactionsPageState(StateDataModel):
    reaction_rows = Sync(
        list,
        lambda: build_initial_rows(REACTION_DEFAULTS, INITIAL_REACTIONS),
        client_deep_reactive=True,
    )


class ReactionsPage(Page):
    id = "reactions"
    title = "5c. Reactions"
    description = "Create one or more F.Reaction objects."

    def __init__(self, server):
        super().__init__(server, ctx_name="page_reactions")
        self.config = ReactionsPageState(server)
        self.config.watch(["reaction_rows"], self.notify_script_change, sync=True)
        self.build_ui()

    def add_reaction(self, *_args, **_kwargs):
        rows = list(self.config.reaction_rows)
        rows.append(resolve_template_row(REACTION_DEFAULTS, len(rows)))
        self.config.reaction_rows = rows

    def remove_reaction(self, *_args, **_kwargs):
        rows = list(self.config.reaction_rows)
        if len(rows) <= 1:
            return
        rows.pop()
        self.config.reaction_rows = rows

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("reactions_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        RepeatedItemControls(
                            on_add=self.add_reaction, on_remove=self.remove_reaction
                        )
                        with v3.VCard(
                            variant="tonal",
                            v_for="(reaction_row, idx) in reactions_config.reaction_rows",
                            key=("idx",),
                        ):
                            with v3.VCardText(classes="d-flex flex-column ga-2"):
                                v3.VLabel("Reaction {{ idx + 1 }}", classes="text-caption")
                                v3.VTextField(
                                    v_model="reaction_row.var",
                                    label="Variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                                v3.VTextField(
                                    v_model="reaction_row.reactants",
                                    label="reactants (comma-separated vars)",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                                v3.VTextField(
                                    v_model="reaction_row.products",
                                    label="products (comma-separated vars)",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="reaction_row.k_0",
                                            label="k_0",
                                            type="number",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="reaction_row.E_k",
                                            label="E_k",
                                            type="number",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="reaction_row.p_0",
                                            label="p_0",
                                            type="number",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="reaction_row.E_p",
                                            label="E_p",
                                            type="number",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                v3.VTextField(
                                    v_model="reaction_row.volume_var",
                                    label="volume variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        problem_var = self.page_problem.problem_var
        lines = ["# 5c. Create reactions"]
        rows = self.config.reaction_rows

        reaction_var_names = []
        for idx, row in enumerate(rows):
            defaults = resolve_template_row(REACTION_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            reactants_expr = str(row.get("reactants", defaults["reactants"]))
            products_expr = str(row.get("products", defaults["products"]))
            k_0 = as_float(row.get("k_0", defaults["k_0"]), REACTION_DEFAULTS["k_0"])
            e_k = as_float(row.get("E_k", defaults["E_k"]), REACTION_DEFAULTS["E_k"])
            p_0 = as_float(row.get("p_0", defaults["p_0"]), REACTION_DEFAULTS["p_0"])
            e_p = as_float(row.get("E_p", defaults["E_p"]), REACTION_DEFAULTS["E_p"])
            volume_var = str(row.get("volume_var", defaults["volume_var"]))
            reaction_var_names.append(var_name)
            lines.extend(
                [
                    f"{var_name} = F.Reaction(",
                    f"    reactant={comma_separated_list_expr(reactants_expr)},",
                    f"    product={comma_separated_list_expr(products_expr)},",
                    f"    k_0={k_0},",
                    f"    E_k={e_k},",
                    f"    p_0={p_0},",
                    f"    E_p={e_p},",
                    f"    volume={volume_var},",
                    ")",
                ]
            )

        if reaction_var_names:
            lines.append(f"{problem_var}.reactions = [{', '.join(reaction_var_names)}]")

        return lines
