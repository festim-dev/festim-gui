from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3

from festim_gui.festim_ui import problem


class FestimGUI(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="vue3")

        self.state.trame__title = "FESTIM Script Modeler"
        problem.init_state(self.state)

        if self.server.hot_reload:
            self.server.controller.on_server_reload.add(self._build_ui)

        self._build_ui()

    def _build_ui(self, *_args, **_kwargs):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("FESTIM Script Builder")
            with self.ui.toolbar:
                v3.VSpacer()

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="pa-4"):
                    with v3.VRow():
                        with v3.VCol(cols="12", md="8", lg="6"):
                            problem.build_form()


def main():
    app = FestimGUI()
    app.server.start(show_connection_info=True, open_browser=False)


if __name__ == "__main__":
    main()
