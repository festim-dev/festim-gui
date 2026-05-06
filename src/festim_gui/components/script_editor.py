from trame.widgets import vuetify3 as v3


class ScriptEditor(v3.VCard):
    def __init__(self, **kwargs):
        super().__init__(variant="outlined", classes="fill-height", **kwargs)

        with self:
            v3.VCardTitle("Generated FESTIM Script")
            with v3.VCardText(classes="fill-height"):
                v3.VTextarea(
                    v_model=("generated_script", ""),
                    rows=32,
                    auto_grow=False,
                    variant="outlined",
                    readonly=True,
                    classes="font-monospace",
                )
