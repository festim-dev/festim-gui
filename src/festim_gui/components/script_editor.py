from trame.widgets import code, html
from trame.widgets import vuetify3 as v3


class ScriptEditor(v3.VCard):
    def __init__(self, **kwargs):
        super().__init__(
            variant="outlined", classes="fill-height d-flex flex-column", **kwargs
        )
        editor_options = {
            "readOnly": True,
            "automaticLayout": True,
            "minimap": {"enabled": False},
            "scrollBeyondLastLine": False,
            "wordWrap": "on",
        }

        with self:
            with v3.VCardTitle(classes="d-flex align-center ga-2"):
                v3.VLabel("Generated FESTIM Script")
                v3.VSpacer()
                with html.A(
                    href=("download_script_href", ""),
                    download=("download_script_filename", "script.py"),
                    style="text-decoration: none;",
                    v_if="page_name === 'run'",
                ):
                    v3.VBtn(
                        "Download",
                        prepend_icon="mdi-download",
                        variant="text",
                    )
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
                    border=True,
                    rounded="lg",
                    classes="h-100 overflow-hidden pt-2",
                    style="background-color: #1e1e1e;",
                ):
                    code.Editor(
                        model_value=("generated_script", ""),
                        language="python",
                        options=("script_editor_options", editor_options),
                        style="height: 100%; width: 100%;",
                    )
