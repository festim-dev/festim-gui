from trame.widgets import vuetify3 as v3


def build_script_editor() -> None:
    with v3.VCard(variant="outlined", classes="fill-height"):
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
