from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import as_float, build_initial_rows, resolve_template_row

MATERIAL_DEFAULTS = {
    "var": "mat_{i}",
    "name": "mat_{i}",
    "D_0": 1.0,
    "E_D": 0.0,
    "K_S_0": 0.1,
    "E_K_S": 0.0,
}
INITIAL_MATERIALS = [
    {"var": "mat_1", "name": "mat_1", "D_0": 1.0, "K_S_0": 0.1},
    {"var": "mat_2", "name": "mat_2", "D_0": 0.1, "K_S_0": 0.5},
]


class MaterialsPageState(StateDataModel):
    material_rows = Sync(
        list,
        lambda: build_initial_rows(MATERIAL_DEFAULTS, INITIAL_MATERIALS),
        client_deep_reactive=True,
    )


class MaterialsPage(Page):
    id = "materials"
    title = "3. Materials"
    description = "Create one or more F.Material objects."

    def __init__(self, server):
        super().__init__(server)
        self.config = MaterialsPageState(server)
        self.config.watch(["material_rows"], self.notify_script_change, sync=True)

    def add_material(self, *_args, **_kwargs):
        rows = list(self.config.material_rows)
        rows.append(resolve_template_row(MATERIAL_DEFAULTS, len(rows)))
        self.config.material_rows = rows

    def remove_material(self, *_args, **_kwargs):
        rows = list(self.config.material_rows)
        if len(rows) <= 1:
            return
        rows.pop()
        self.config.material_rows = rows

    def build_ui(self) -> None:
        with v3.VCard(variant="outlined"):
            with v3.VCardText(classes="d-flex flex-column ga-3"):
                with self.config.provide_as("materials_config"):
                    RepeatedItemControls(
                        on_add=self.add_material, on_remove=self.remove_material
                    )
                    with v3.VCard(
                        variant="tonal",
                        v_for="(material_row, idx) in materials_config.material_rows",
                        key=("idx",),
                    ):
                        with v3.VCardText(classes="d-flex flex-column ga-2"):
                            v3.VLabel("Material {{ idx + 1 }}", classes="text-caption")
                            with v3.VRow(classes="ga-0"):
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="material_row.var",
                                        label="Variable",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="material_row.name",
                                        label="name",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                            with v3.VRow(classes="ga-0"):
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="material_row.D_0",
                                        label="D_0",
                                        type="number",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="material_row.E_D",
                                        label="E_D",
                                        type="number",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                            with v3.VRow(classes="ga-0"):
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="material_row.K_S_0",
                                        label="K_S_0",
                                        type="number",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )
                                with v3.VCol(cols="6"):
                                    v3.VTextField(
                                        v_model="material_row.E_K_S",
                                        label="E_K_S",
                                        type="number",
                                        variant="outlined",
                                        density="compact",
                                        update_modelValue=self.notify_script_change,
                                    )

    def script_lines(self) -> list[str]:
        lines = ["# 3. Create materials"]
        rows = self.config.material_rows
        if not rows:
            rows = [resolve_template_row(MATERIAL_DEFAULTS, 0)]

        for idx, row in enumerate(rows):
            row_dict = row if isinstance(row, dict) else {}
            defaults = resolve_template_row(MATERIAL_DEFAULTS, idx)
            var_name = str(row_dict.get("var", defaults["var"]))
            name = str(row_dict.get("name", defaults["name"]))
            d_0 = as_float(
                row_dict.get("D_0", defaults["D_0"]), MATERIAL_DEFAULTS["D_0"]
            )
            e_d = as_float(
                row_dict.get("E_D", defaults["E_D"]), MATERIAL_DEFAULTS["E_D"]
            )
            k_s_0 = as_float(
                row_dict.get("K_S_0", defaults["K_S_0"]), MATERIAL_DEFAULTS["K_S_0"]
            )
            e_k_s = as_float(
                row_dict.get("E_K_S", defaults["E_K_S"]), MATERIAL_DEFAULTS["E_K_S"]
            )
            lines.append(
                f'{var_name} = F.Material(name="{name}", D_0={d_0}, '
                f"E_D={e_d}, K_S_0={k_s_0}, E_K_S={e_k_s})"
            )

        return lines
