from trame.widgets import code
from trame.widgets import vuetify3 as v3


class ScriptEditor(v3.VCard):
    def __init__(self, **kwargs):
        super().__init__(
            variant="outlined", classes="fill-height d-flex flex-column", **kwargs
        )

        with self:
            with v3.VCardTitle(classes="d-flex align-center ga-2"):
                v3.VLabel("Generated FESTIM Script")
                v3.VSpacer()
                with v3.VBtnToggle(
                    v_model=("script_view_mode", "snippet"),
                    mandatory=True,
                    density="compact",
                    divided=True,
                    variant="outlined",
                ):
                    v3.VBtn("Snippet", value="snippet")
                    v3.VBtn("Full", value="full")
            with v3.VCardText(classes="flex-grow-1 px-3 pb-3"):
                with v3.VSheet(
                    border=True, rounded="lg", classes="h-100 overflow-hidden"
                ):
                    code.Editor(
                        model_value=("generated_script", ""),
                        language="python",
                        options=(
                            {
                                "readOnly": True,
                                "automaticLayout": True,
                                "minimap": {"enabled": False},
                                "scrollBeyondLastLine": False,
                                "wordWrap": "on",
                            },
                        ),
                        style="height: 100%; width: 100%;",
                    )
