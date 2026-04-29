from dataclasses import dataclass

from trame.widgets import vuetify3 as v3

PREFIX = "material"
MAX_ITEMS = 8
FIELDS = ("var", "name", "D_0", "E_D", "K_S_0", "E_K_S")


def _state_key(index: int, field: str) -> str:
    return f"{PREFIX}_{index}_{field}"


def _default_row(index: int) -> dict[str, object]:
    i = index + 1
    defaults = {
        "var": f"mat_{i}",
        "name": f"mat_{i}",
        "D_0": 1.0,
        "E_D": 0.0,
        "K_S_0": 0.1,
        "E_K_S": 0.0,
    }
    if index == 1:
        defaults["D_0"] = 0.1
        defaults["K_S_0"] = 0.5
    return defaults


STATE_KEYS = [f"{PREFIX}_count"]
for _idx in range(MAX_ITEMS):
    for _field in FIELDS:
        STATE_KEYS.append(_state_key(_idx, _field))


@dataclass
class MaterialModel:
    var_name: str
    name: str
    d_0: float
    e_d: float
    k_s_0: float
    e_k_s: float


def init_state(state) -> None:
    if not state.has(f"{PREFIX}_count"):
        state[f"{PREFIX}_count"] = 2

    for idx in range(MAX_ITEMS):
        defaults = _default_row(idx)
        for field in FIELDS:
            key = _state_key(idx, field)
            if not state.has(key):
                state[key] = defaults[field]


def _as_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _row_count(state) -> int:
    try:
        raw = int(state[f"{PREFIX}_count"])
    except (TypeError, ValueError):
        raw = 1
    return max(1, min(raw, MAX_ITEMS))


def from_state(state) -> list[MaterialModel]:
    items = []
    for idx in range(_row_count(state)):
        defaults = _default_row(idx)
        items.append(
            MaterialModel(
                var_name=state[_state_key(idx, "var")],
                name=state[_state_key(idx, "name")],
                d_0=_as_float(state[_state_key(idx, "D_0")], defaults["D_0"]),
                e_d=_as_float(state[_state_key(idx, "E_D")], defaults["E_D"]),
                k_s_0=_as_float(state[_state_key(idx, "K_S_0")], defaults["K_S_0"]),
                e_k_s=_as_float(state[_state_key(idx, "E_K_S")], defaults["E_K_S"]),
            )
        )
    return items


def build_form() -> None:
    with v3.VCard(variant="outlined"):
        v3.VCardTitle("3. Materials")
        with v3.VCardText(classes="d-flex flex-column ga-3"):
            with v3.VRow(classes="ga-0"):
                with v3.VCol(cols="12"):
                    with v3.VBtnToggle(
                        density="compact", divided=True, variant="outlined"
                    ):
                        v3.VBtn(
                            "Add",
                            prepend_icon="mdi-plus",
                            click=f"{PREFIX}_count = Math.min({PREFIX}_count + 1, {MAX_ITEMS})",
                        )
                        v3.VBtn(
                            "Remove",
                            prepend_icon="mdi-minus",
                            click=f"{PREFIX}_count = Math.max({PREFIX}_count - 1, 1)",
                        )

            for idx in range(MAX_ITEMS):
                with v3.VCard(variant="tonal", v_show=f"{PREFIX}_count > {idx}"):
                    with v3.VCardText(classes="d-flex flex-column ga-2"):
                        v3.VLabel(f"Material {idx + 1}", classes="text-caption")
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(_state_key(idx, "var"),),
                                    label="Variable",
                                    variant="outlined",
                                    density="compact",
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(_state_key(idx, "name"),),
                                    label="name",
                                    variant="outlined",
                                    density="compact",
                                )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(_state_key(idx, "D_0"),),
                                    label="D_0",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(_state_key(idx, "E_D"),),
                                    label="E_D",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(_state_key(idx, "K_S_0"),),
                                    label="K_S_0",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model=(_state_key(idx, "E_K_S"),),
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
