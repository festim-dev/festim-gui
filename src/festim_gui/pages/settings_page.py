from trame.app.dataclass import StateDataModel, Sync
from trame.ui.html import DivLayout
from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page
from festim_gui.utils import as_bool, as_float

DEFAULTS = {
    "atol": 1e-10,
    "rtol": 1e-10,
    "transient": True,
    "stepsize": 0.05,
    "final_time": 2.0,
}


class SettingsPageState(StateDataModel):
    atol = Sync(float, DEFAULTS["atol"])
    rtol = Sync(float, DEFAULTS["rtol"])
    transient = Sync(bool, DEFAULTS["transient"])
    stepsize = Sync(float, DEFAULTS["stepsize"])
    final_time = Sync(float, DEFAULTS["final_time"])


class SettingsPage(Page):
    id = "settings"
    title = "8. Settings"
    description = "Set solver/runtime settings via F.Settings."

    def __init__(self, server):
        super().__init__(server, ctx_name="page_settings")
        self.config = SettingsPageState(server)
        self.config.watch(
            ["atol", "rtol", "transient", "stepsize", "final_time"],
            self.notify_script_change,
            sync=True,
        )
        self.build_ui()

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("settings_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="settings_config.atol",
                                    label="atol",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="settings_config.rtol",
                                    label="rtol",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    update_modelValue=self.notify_script_change,
                                )

                        v3.VSwitch(
                            v_model="settings_config.transient",
                            label="transient",
                            color="primary",
                            hide_details=True,
                            update_modelValue=self.notify_script_change,
                        )

                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="settings_config.stepsize",
                                    label="stepsize",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="settings_config.final_time",
                                    label="final_time",
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
        atol = as_float(self.config.atol, DEFAULTS["atol"])
        rtol = as_float(self.config.rtol, DEFAULTS["rtol"])
        transient = as_bool(self.config.transient, DEFAULTS["transient"])
        stepsize = as_float(self.config.stepsize, DEFAULTS["stepsize"])
        final_time = as_float(self.config.final_time, DEFAULTS["final_time"])
        return [
            "# 8. Settings",
            f"{problem_var}.settings = F.Settings(",
            f"    atol={atol}, rtol={rtol}, transient={transient},",
            f"    stepsize={stepsize}, final_time={final_time}",
            ")",
        ]
