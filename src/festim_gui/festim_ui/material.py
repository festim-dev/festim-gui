from dataclasses import dataclass

from trame.widgets import vuetify3 as v3

from festim_gui.components.repeated_item_controls import RepeatedItemControls
from festim_gui.festim_ui.component import FestimComponent
from festim_gui.utils.utils import (
    as_float,
    collection_rows,
    init_repeated_state,
    repeated_state_keys,
)

PREFIX = "material"
MAX_ITEMS = 8
FIELDS = {
    "var": "mat_{i}",
    "name": "mat_{i}",
    "D_0": 1.0,
    "E_D": 0.0,
    "K_S_0": 0.1,
    "E_K_S": 0.0,
}
INITIAL_ITEMS = [
    {"var": "mat_1", "name": "mat_1", "D_0": 1.0, "K_S_0": 0.1},
    {"var": "mat_2", "name": "mat_2", "D_0": 0.1, "K_S_0": 0.5},
]
STATE_KEYS = repeated_state_keys(PREFIX, FIELDS, MAX_ITEMS)


@dataclass
class MaterialModel:
    var_name: str
    name: str
    d_0: float
    e_d: float
    k_s_0: float
    e_k_s: float


class MaterialComponent(FestimComponent):
    card_title = "3. Materials"
    prefix = PREFIX
    max_items = MAX_ITEMS
    fields = FIELDS
    initial_items = INITIAL_ITEMS
    state_keys = STATE_KEYS

    @staticmethod
    def init_state(state) -> None:
        init_repeated_state(
            state,
            MaterialComponent.prefix,
            MaterialComponent.fields,
            MaterialComponent.max_items,
            MaterialComponent.initial_items,
        )

    @staticmethod
    def from_state(state) -> list[MaterialModel]:
        rows = collection_rows(
            state,
            MaterialComponent.prefix,
            MaterialComponent.fields,
            MaterialComponent.max_items,
        )
        return [
            MaterialModel(
                var_name=row["var"],
                name=row["name"],
                d_0=as_float(row["D_0"], MaterialComponent.fields["D_0"]),
                e_d=as_float(row["E_D"], MaterialComponent.fields["E_D"]),
                k_s_0=as_float(row["K_S_0"], MaterialComponent.fields["K_S_0"]),
                e_k_s=as_float(row["E_K_S"], MaterialComponent.fields["E_K_S"]),
            )
            for row in rows
        ]

    def build_content(self) -> None:
        RepeatedItemControls(prefix=self.prefix, max_items=self.max_items)
        for idx in range(self.max_items):
            with v3.VCard(variant="tonal", v_show=f"{self.prefix}_count > {idx}"):
                with v3.VCardText(classes="d-flex flex-column ga-2"):
                    v3.VLabel(f"Material {idx + 1}", classes="text-caption")
                    with v3.VRow(classes="ga-0"):
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model=(f"{self.prefix}_{idx}_var",),
                                label="Variable",
                                variant="outlined",
                                density="compact",
                            )
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model=(f"{self.prefix}_{idx}_name",),
                                label="name",
                                variant="outlined",
                                density="compact",
                            )
                    with v3.VRow(classes="ga-0"):
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model=(f"{self.prefix}_{idx}_D_0",),
                                label="D_0",
                                type="number",
                                variant="outlined",
                                density="compact",
                            )
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model=(f"{self.prefix}_{idx}_E_D",),
                                label="E_D",
                                type="number",
                                variant="outlined",
                                density="compact",
                            )
                    with v3.VRow(classes="ga-0"):
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model=(f"{self.prefix}_{idx}_K_S_0",),
                                label="K_S_0",
                                type="number",
                                variant="outlined",
                                density="compact",
                            )
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model=(f"{self.prefix}_{idx}_E_K_S",),
                                label="E_K_S",
                                type="number",
                                variant="outlined",
                                density="compact",
                            )

    @staticmethod
    def to_script_lines(items: list[MaterialModel]) -> list[str]:
        lines = []
        for item in items:
            lines.append(
                f'{item.var_name} = F.Material(name="{item.name}", D_0={item.d_0}, '
                f"E_D={item.e_d}, K_S_0={item.k_s_0}, E_K_S={item.e_k_s})"
            )
        return lines
