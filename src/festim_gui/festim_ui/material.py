from dataclasses import dataclass

from trame.widgets import vuetify3 as v3

from .utils import (
    as_float,
    build_repeated_item_controls,
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


def init_state(state) -> None:
    init_repeated_state(state, PREFIX, FIELDS, MAX_ITEMS, INITIAL_ITEMS)


def from_state(state) -> list[MaterialModel]:
    rows = collection_rows(state, PREFIX, FIELDS, MAX_ITEMS)
    return [
        MaterialModel(
            var_name=row["var"],
            name=row["name"],
            d_0=as_float(row["D_0"], FIELDS["D_0"]),
            e_d=as_float(row["E_D"], FIELDS["E_D"]),
            k_s_0=as_float(row["K_S_0"], FIELDS["K_S_0"]),
            e_k_s=as_float(row["E_K_S"], FIELDS["E_K_S"]),
        )
        for row in rows
    ]


def build_form() -> None:
    with v3.VCard(variant="outlined"):
        v3.VCardTitle("3. Materials")
        with v3.VCardText(classes="d-flex flex-column ga-3"):
            build_repeated_item_controls(PREFIX, MAX_ITEMS)
            for idx in range(MAX_ITEMS):
                with v3.VCard(variant="tonal", v_show=f"{PREFIX}_count > {idx}"):
                    with v3.VCardText(classes="d-flex flex-column ga-2"):
                        v3.VLabel(f"Material {idx + 1}", classes="text-caption")
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(f"{PREFIX}_{idx}_var",),
                                    label="Variable",
                                    variant="outlined",
                                    density="compact",
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(f"{PREFIX}_{idx}_name",),
                                    label="name",
                                    variant="outlined",
                                    density="compact",
                                )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(f"{PREFIX}_{idx}_D_0",),
                                    label="D_0",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(f"{PREFIX}_{idx}_E_D",),
                                    label="E_D",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(f"{PREFIX}_{idx}_K_S_0",),
                                    label="K_S_0",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(f"{PREFIX}_{idx}_E_K_S",),
                                    label="E_K_S",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                )


def to_script_lines(items: list[MaterialModel]) -> list[str]:
    lines = []
    for item in items:
        lines.append(
            f'{item.var_name} = F.Material(name="{item.name}", D_0={item.d_0}, '
            f"E_D={item.e_d}, K_S_0={item.k_s_0}, E_K_S={item.e_k_s})"
        )
    return lines
