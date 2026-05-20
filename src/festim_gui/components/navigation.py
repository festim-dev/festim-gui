from trame.widgets import html
from trame.widgets import vuetify3 as v3


class PageNavigationBar(v3.VCard):
    def __init__(self, pages, on_navigate, **kwargs):
        super().__init__(variant="outlined", classes="mb-4", **kwargs)

        with self:
            with v3.VCardText(classes="d-flex flex-column ga-2"):
                html.Div(
                    "{{ page_title }}",
                    classes="text-h6 font-weight-medium",
                )
                html.Div(
                    "{{ page_description }}",
                    classes="text-body-2 text-medium-emphasis",
                )
                with html.Div(classes="d-flex flex-wrap ga-2"):
                    for index, page in enumerate(pages):
                        v3.VChip(
                            f"{page.title}",
                            variant="outlined",
                            color=(
                                f"page_index === {index} ? 'primary'"
                                f" : (page_errors && page_errors[{index}] && page_visited && page_visited[{index}] ? 'error' : 'default')",
                            ),
                            classes="text-caption",
                            click=(on_navigate, f"[{index}]"),
                        )


class Navigation(v3.VCard):
    def __init__(self, total_pages: int, on_prev, on_next, **kwargs):
        super().__init__(variant="outlined", classes="mt-4", **kwargs)

        with self:
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
                html.Div(
                    f"{{{{ page_index + 1 }}}} / {total_pages}",
                    classes="text-caption",
                )
