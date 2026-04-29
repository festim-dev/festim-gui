from trame.widgets import html
from trame.widgets import vuetify3 as v3


def build_navigation(total_pages: int, on_prev, on_next) -> None:
    with v3.VCard(variant="outlined", classes="mt-4"):
        with v3.VCardText(classes="d-flex align-center ga-2 flex-wrap"):
            v3.VBtn(
                "Previous",
                variant="outlined",
                click=on_prev,
                disabled=("page_index <= 0",),
            )
            v3.VBtn(
                "Next",
                color="primary",
                variant="flat",
                click=on_next,
                disabled=(f"page_index >= {total_pages - 1}",),
            )
            v3.VSpacer()
            html.Div("{{ page_index + 1 }} / {{ total_pages }}", classes="text-caption")
