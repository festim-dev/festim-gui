from trame.app import TrameApp
from trame.decorators import change
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html
from trame.widgets import vuetify3 as v3

from festim_gui.components import (
    build_navigation,
    build_script_editor,
    build_script_from_state,
)
from festim_gui.pages import FORM_STATE_KEYS, PAGES


class FestimGUI(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="vue3")

        self.state.trame__title = "FESTIM Script Modeler"
        self.state.total_pages = len(PAGES)
        self.state.page_index = 0
        self.state.page_title = PAGES[0].title
        self.state.page_description = PAGES[0].description
        self.state.generated_script = ""

        for page in PAGES:
            page.init_state(self.state)

        self._refresh_script()

        if self.server.hot_reload:
            self.server.controller.on_server_reload.add(self._build_ui)

        self._build_ui()

    def _set_page_metadata(self, page_index: int) -> None:
        safe_index = max(0, min(page_index, len(PAGES) - 1))
        page = PAGES[safe_index]
        self.state.page_title = page.title
        self.state.page_description = page.description

    def _refresh_script(self) -> None:
        self.state.generated_script = build_script_from_state(self.state)

    def previous_page(self):
        self.state.page_index = max(0, self.state.page_index - 1)

    def next_page(self):
        self.state.page_index = min(len(PAGES) - 1, self.state.page_index + 1)

    @change("page_index")
    def on_page_change(self, page_index, **_kwargs):
        self._set_page_metadata(page_index)
        self._refresh_script()

    @change(*FORM_STATE_KEYS)
    def on_form_change(self, **_kwargs):
        self._refresh_script()

    def _build_page_chips(self):
        with html.Div(classes="d-flex flex-wrap ga-2"):
            for index, page in enumerate(PAGES):
                v3.VChip(
                    f"{page.title}",
                    variant="outlined",
                    color=(f"page_index === {index} ? 'primary' : 'default'",),
                    classes="text-caption",
                )

    def _build_ui(self, *_args, **_kwargs):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("FESTIM Script Builder")
            with self.ui.toolbar:
                v3.VSpacer()
                html.Div("{{ page_title }}", classes="text-caption pr-4")

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="pa-4 fill-height"):
                    with v3.VRow(classes="fill-height"):
                        with v3.VCol(
                            cols="12",
                            md="6",
                            classes="d-flex flex-column",
                            style="height: calc(100vh - 128px); min-height: 0;",
                        ):
                            with html.Div(classes="flex-grow-1 overflow-y-auto pr-1"):
                                with v3.VCard(variant="outlined", classes="mb-4"):
                                    with v3.VCardText(
                                        classes="d-flex flex-column ga-2"
                                    ):
                                        html.Div(
                                            "{{ page_title }}",
                                            classes="text-h6 font-weight-medium",
                                        )
                                        html.Div(
                                            "{{ page_description }}",
                                            classes="text-body-2 text-medium-emphasis",
                                        )
                                        self._build_page_chips()

                                for index, page in enumerate(PAGES):
                                    with html.Div(v_if=f"page_index === {index}"):
                                        page.build_ui()

                            with html.Div(classes="pt-3 mt-auto"):
                                build_navigation(
                                    total_pages=len(PAGES),
                                    on_prev=self.previous_page,
                                    on_next=self.next_page,
                                )

                        with v3.VCol(
                            cols="12",
                            md="6",
                            classes="d-flex flex-column",
                            style="height: calc(100vh - 128px); min-height: 0;",
                        ):
                            build_script_editor()


def main():
    app = FestimGUI()
    app.server.start(show_connection_info=True, open_browser=False)


if __name__ == "__main__":
    main()
