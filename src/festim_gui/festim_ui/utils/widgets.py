from trame.widgets import vuetify3 as v3


def build_repeated_item_controls(prefix: str, max_items: int) -> None:
    with v3.VRow(classes="ga-0"):
        with v3.VCol(cols="12"):
            with v3.VBtnToggle(density="compact", divided=True, variant="outlined"):
                v3.VBtn(
                    "Add",
                    prepend_icon="mdi-plus",
                    click=f"{prefix}_count = Math.min({prefix}_count + 1, {max_items})",
                )
                v3.VBtn(
                    "Remove",
                    prepend_icon="mdi-minus",
                    click=f"{prefix}_count = Math.max({prefix}_count - 1, 1)",
                )
