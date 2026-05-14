from abc import ABC, abstractmethod

from trame.app import TrameComponent
from trame.ui.html import DivLayout


class Page(TrameComponent, ABC):
    id = ""
    title = ""
    description = ""

    def __init__(self, server):
        super().__init__(server)
        self._script_change_callback = None

    def mount_template(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            self.build_ui()

    def register_script_change_callback(self, callback) -> None:
        self._script_change_callback = callback

    def notify_script_change(self, *_args, **_kwargs) -> None:
        if self._script_change_callback is not None:
            self._script_change_callback()

    @abstractmethod
    def build_ui(self) -> None:
        pass

    @abstractmethod
    def script_lines(self) -> list[str]:
        pass
