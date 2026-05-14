from trame.app import TrameApp
from trame.decorators import change
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import client, html
from trame.widgets import vuetify3 as v3

from festim_gui.components import Navigation, PageNavigationBar, ScriptEditor
from festim_gui.pages import create_pages
from festim_gui.utils.script_builder import build_script


class FestimGUI(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="vue3")

        self.state.trame__title = "FESTIM Script Modeler"
        self.pages = create_pages(self.server)

        for page in self.pages:
            page.register_script_change_callback(self._refresh_script)

        self.state.page_index = 0
        self.state.page_name = self.pages[0].id
        self.state.page_title = self.pages[0].title
        self.state.page_description = self.pages[0].description
        self.state.generated_script = ""

        self._refresh_script()

        if self.server.hot_reload:
            self.server.controller.on_server_reload.add(self._build_ui)

        self._build_ui()

    def _set_page_metadata(self, page_index: int) -> None:
        safe_index = max(0, min(page_index, len(self.pages) - 1))
        page = self.pages[safe_index]
        self.state.page_name = page.id
        self.state.page_title = page.title
        self.state.page_description = page.description

    def _refresh_script(self) -> None:
        page = self.pages[self.state.page_index]
        self.state.generated_script = build_script([page], include_header=False)

    def previous_page(self):
        self.state.page_index = max(0, self.state.page_index - 1)

    def next_page(self):
        self.state.page_index = min(len(self.pages) - 1, self.state.page_index + 1)

    @change("page_index")
    def on_page_change(self, page_index, **_kwargs):
        self._set_page_metadata(page_index)
        self._refresh_script()

    def _build_page_templates(self):
        for page in self.pages:
            page.mount_template()

    def _build_ui(self, *_args, **_kwargs):
        self._build_page_templates()

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
                                PageNavigationBar(self.pages)
                                client.ServerTemplate(
                                    name=("page_name", self.pages[0].id)
                                )

                            with html.Div(classes="pt-3 mt-auto"):
                                Navigation(
                                    total_pages=len(self.pages),
                                    on_prev=self.previous_page,
                                    on_next=self.next_page,
                                )

                        with v3.VCol(
                            cols="12",
                            md="6",
                            classes="d-flex flex-column",
                            style="height: calc(100vh - 128px); min-height: 0;",
                        ):
                            ScriptEditor()


def main():
    app = FestimGUI()
    app.server.start(show_connection_info=True, open_browser=False)


if __name__ == "__main__":
    main()
