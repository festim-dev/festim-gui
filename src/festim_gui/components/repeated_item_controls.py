from trame.widgets import vuetify3 as v3


class RepeatedItemControls(v3.VRow):
    def __init__(self, prefix: str, max_items: int, **kwargs):
        super().__init__(classes="ga-0", **kwargs)

        with self:
            with v3.VCol(cols="12"):
                with v3.VBtnToggle(
                    density="compact", divided=True, variant="outlined"
                ):
                    v3.VBtn(
                        "Add",
                        prepend_icon="mdi-plus",
                        click=(
                            f"{prefix}_count = "
                            f"Math.min({prefix}_count + 1, {max_items})"
                        ),
                    )
                    v3.VBtn(
                        "Remove",
                        prepend_icon="mdi-minus",
                        click=f"{prefix}_count = Math.max({prefix}_count - 1, 1)",
                    )
