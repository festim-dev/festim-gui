from trame.widgets import vuetify3 as v3


class RepeatedItemControls(v3.VRow):
    def __init__(self, on_add, on_remove, **kwargs):
        super().__init__(classes="ga-0", **kwargs)

        with self:
            with v3.VCol(cols="12"):
                with v3.VBtnToggle(density="compact", divided=True, variant="outlined"):
                    v3.VBtn(
                        "Add",
                        prepend_icon="mdi-plus",
                        click=on_add,
                    )
                    v3.VBtn(
                        "Remove",
                        prepend_icon="mdi-minus",
                        click=on_remove,
                    )
