from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page
from festim_gui.utils import as_float

DEFAULTS = {
    "temperature_value": 600.0,
}


class TemperaturePageState(StateDataModel):
    temperature_value = Sync(float, DEFAULTS["temperature_value"])


class TemperaturePage(Page):
    id = "temperature"
    title = "7. Temperature"
    description = "Set problem.temperature."

    def __init__(self, server, problem_page):
        super().__init__(server)
        self._problem_page = problem_page
        self.config = TemperaturePageState(server)
        self.config.watch(["temperature_value"], self.notify_script_change, sync=True)

    def build_ui(self) -> None:
        with self.config.provide_as("temperature_config"):
            with v3.VCard(variant="outlined"):
                with v3.VCardText(classes="d-flex flex-column ga-3"):
                    v3.VTextField(
                        v_model="temperature_config.temperature_value",
                        label="Temperature (K)",
                        type="number",
                        variant="outlined",
                        density="comfortable",
                        update_modelValue=self.notify_script_change,
                    )

    def script_lines(self) -> list[str]:
        problem_var = self._problem_page.problem_var
        temperature_value = as_float(
            self.config.temperature_value, DEFAULTS["temperature_value"]
        )
        return [
            "# 7. Temperature",
            f"{problem_var}.temperature = {temperature_value}  # K",
        ]
