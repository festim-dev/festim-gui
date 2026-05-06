from abc import ABC, abstractmethod

from trame.widgets import vuetify3 as v3


class FestimComponent(v3.VCard, ABC):
    card_title = ""
    card_text_classes = "d-flex flex-column ga-3"
    state_keys = ()

    def __init__(self, **kwargs):
        super().__init__(variant="outlined", **kwargs)
        with self:
            with v3.VCardText(classes=self.card_text_classes):
                self.build_content()

    @abstractmethod
    def build_content(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def init_state(state) -> None:
        pass

    @staticmethod
    @abstractmethod
    def to_script_lines(*args, **kwargs) -> list[str]:
        pass
