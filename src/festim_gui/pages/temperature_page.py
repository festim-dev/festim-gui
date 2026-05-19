from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3
from trame.ui.html import DivLayout

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

    def __init__(self, server):
        super().__init__(server, ctx_name="page_temperature")
        self.config = TemperaturePageState(server)
        self.config.watch(["temperature_value"], self.notify_script_change, sync=True)
        self.build_ui()

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
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

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        problem_var = self.page_problem.problem_var
        temperature_value = as_float(
            self.config.temperature_value, DEFAULTS["temperature_value"]
        )
        return [
            "# 7. Temperature",
            f"{problem_var}.temperature = {temperature_value}  # K",
        ]
