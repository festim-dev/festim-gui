from trame.app.dataclass import StateDataModel, Sync
from trame.ui.html import DivLayout
from trame.widgets import vuetify3 as v3

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import build_initial_rows, resolve_template_row

PARTICLE_SOURCE_DEFAULTS = {
    "var": "source_{i}",
    "species_var": "H",
    "volume_var": "volume_1",
    "value": "lambda t: 3 if t < 0.5 else 0.0",
}
PARTICLE_SOURCES = [
    {
        "var": "source_1",
        "species_var": "H",
        "volume_var": "volume_1",
        "value": "lambda t: 3 if t < 0.5 else 0.0",
    }
]


class ParticleSourcePageState(StateDataModel):
    particle_source_rows = Sync(
        list,
        lambda: build_initial_rows(PARTICLE_SOURCE_DEFAULTS, PARTICLE_SOURCES),
        client_deep_reactive=True,
    )


class ParticleSourcePage(Page):
    id = "particle_source"
    title = "5c. Particle Sources"
    description = "Create one or more F.ParticleSource objects."

    def __init__(self, server):
        super().__init__(server, ctx_name="page_particle_source")
        self.config = ParticleSourcePageState(server)
        self.config.watch(
            ["particle_source_rows"], self.notify_script_change, sync=True
        )
        self.build_ui()

    def add_particle_source(self, *_args, **_kwargs):
        rows = list(self.config.particle_source_rows)
        rows.append(resolve_template_row(PARTICLE_SOURCE_DEFAULTS, len(rows)))
        self.config.particle_source_rows = rows

    def remove_particle_source(self, *_args, **_kwargs):
        rows = list(self.config.particle_source_rows)
        if len(rows) <= 1:
            return
        rows.pop()
        self.config.particle_source_rows = rows

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("particle_source_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        RepeatedItemControls(
                            on_add=self.add_particle_source,
                            on_remove=self.remove_particle_source,
                        )
                        with v3.VCard(
                            variant="tonal",
                            v_for="(source_row, idx) in particle_source_config.particle_source_rows",
                            key=("idx",),
                        ):
                            with v3.VCardText(classes="d-flex flex-column ga-2"):
                                v3.VLabel(
                                    "Particle source {{ idx + 1 }}",
                                    classes="text-caption",
                                )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="source_row.var",
                                            label="Variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="source_row.species_var",
                                            label="Species variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="source_row.volume_var",
                                            label="Volume variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="source_row.value",
                                            label="Value expression",
                                            hint="e.g. lambda t: 3 if t < 0.5 else 0.0",
                                            persistent_hint=True,
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        problem_var = self.page_problem.problem_var
        lines = ["# 5c. Create particle sources"]
        rows = self.config.particle_source_rows

        source_var_names = []
        for idx, row in enumerate(rows):
            defaults = resolve_template_row(PARTICLE_SOURCE_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            species_var = str(row.get("species_var", defaults["species_var"]))
            volume_var = str(row.get("volume_var", defaults["volume_var"]))
            value = str(row.get("value", defaults["value"]))
            source_var_names.append(var_name)
            lines.append(
                f"{var_name} = F.ParticleSource("
                f"species={species_var}, volume={volume_var}, value={value})"
            )

        if source_var_names:
            lines.append(f"{problem_var}.sources = [{', '.join(source_var_names)}]")

        return lines
