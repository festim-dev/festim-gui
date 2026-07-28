from trame.widgets import html
from trame.widgets import vuetify3 as v3


class Navigation(v3.VToolbar):
    def __init__(self, pages, on_prev, on_next, **kwargs):
        super().__init__(
            border=True,
            rounded="lg",
            classes="mb-4 flex-shrink-0",
            height="auto",
            style="position: sticky; top: 0; z-index: 10;",
            **kwargs,
        )

        split_index = (len(pages) + 1) // 2

        with self:
            with html.Div(
                classes="d-flex flex-column ga-2 pa-3 w-100",
                style="min-width: 0;",
            ):
                with html.Div(classes="d-flex ga-4"):
                    html.Div(
                        "{{ page_title }}",
                        classes="text-h6 font-weight-medium flex-shrink-0",
                        style="width: 26rem;",
                    )

                    with html.Div(
                        classes="d-none d-lg-flex flex-grow-1 ga-2 overflow-x-auto",
                        style="min-width: 0;",
                    ):
                        for index, page in enumerate(pages[:split_index]):
                            v3.VChip(
                                page.title,
                                variant="outlined",
                                color=(
                                    f"page_index === {index} ? 'primary' : 'default'",
                                ),
                                classes="text-caption",
                                click=f"page_index = {index}",
                            )

                    with v3.VBtnGroup(
                        density="compact",
                        variant="outlined",
                        divided=True,
                        classes="ml-auto",
                    ):
                        with v3.VBtn(
                            icon=True,
                            title="Previous page",
                            click=on_prev,
                            disabled=("page_index <= 0",),
                        ):
                            v3.VIcon("mdi-chevron-left")
                        with v3.VBtn(
                            icon=True,
                            title="Next page",
                            click=on_next,
                            disabled=(f"page_index >= {len(pages) - 1}",),
                        ):
                            v3.VIcon("mdi-chevron-right")

                with html.Div(classes="d-flex align-center ga-4"):
                    html.Div(
                        "{{ page_description }}",
                        classes="text-body-2 text-medium-emphasis flex-shrink-0",
                        style="width: 26rem;",
                    )

                    with html.Div(
                        classes="d-none d-lg-flex flex-grow-1 ga-2 overflow-x-auto",
                        style="min-width: 0;",
                    ):
                        for index, page in enumerate(
                            pages[split_index:], start=split_index
                        ):
                            v3.VChip(
                                page.title,
                                variant="outlined",
                                color=(
                                    f"page_index === {index} ? 'primary' : 'default'",
                                ),
                                classes="text-caption",
                                click=f"page_index = {index}",
                            )
