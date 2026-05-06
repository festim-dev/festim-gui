from abc import ABC, abstractmethod

from trame.ui.html import DivLayout


class Page(ABC):
    id = ""
    title = ""
    description = ""
    state_keys = ()

    def __init__(self):
        self._layout = None

    @property
    def template_name(self) -> str:
        return self.id

    def mount_template(self, server) -> None:
        with DivLayout(server, template_name=self.template_name) as layout:
            self.build_ui()
        self._layout = layout

    @abstractmethod
    def init_state(self, state) -> None:
        pass

    @abstractmethod
    def build_ui(self) -> None:
        pass

    @abstractmethod
    def script_lines(self, state) -> list[str]:
        pass
