from abc import ABC, abstractmethod

from trame.app import TrameComponent


class Page(TrameComponent, ABC):
    id = ""
    title = ""
    description = ""

    def __init__(self, server, **kwargs):
        super().__init__(server, **kwargs)
        self._script_change_callback = None

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

    def is_valid(self) -> bool:
        return True

    def validate(self) -> bool:
        return self.is_valid()

    def activate(self):
        self.state.page_name = self.id
        self.state.page_title = self.title
        self.state.page_description = self.description
        return self
