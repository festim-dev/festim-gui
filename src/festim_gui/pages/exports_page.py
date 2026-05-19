from trame.app.dataclass import StateDataModel, Sync
from trame.ui.html import DivLayout
from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page
from festim_gui.utils import as_bool

DEFAULTS = {
    "field_exports_var": "concentration_field_exports",
    "derived_exports_var": "derived_quantities",
    "enable_vtx_species_exports": True,
    "vtx_filename_template": "out/vol_{subdomain.id}.bp",
    "vtx_field_expr": "problem.species",
    "enable_surface_flux_exports": True,
    "surface_flux_field_var": "H",
}


class ExportsPageState(StateDataModel):
    field_exports_var = Sync(str, DEFAULTS["field_exports_var"])
    derived_exports_var = Sync(str, DEFAULTS["derived_exports_var"])
    enable_vtx_species_exports = Sync(bool, DEFAULTS["enable_vtx_species_exports"])
    vtx_filename_template = Sync(str, DEFAULTS["vtx_filename_template"])
    vtx_field_expr = Sync(str, DEFAULTS["vtx_field_expr"])
    enable_surface_flux_exports = Sync(bool, DEFAULTS["enable_surface_flux_exports"])
    surface_flux_field_var = Sync(str, DEFAULTS["surface_flux_field_var"])


class ExportsPage(Page):
    id = "exports"
    title = "9. Exports"
    description = "Configure VTX species exports and derived quantity exports."

    def __init__(self, server):
        super().__init__(server, ctx_name="page_exports")
        self.config = ExportsPageState(server)
        self.config.watch(
            [
                "field_exports_var",
                "derived_exports_var",
                "enable_vtx_species_exports",
                "vtx_filename_template",
                "vtx_field_expr",
                "enable_surface_flux_exports",
                "surface_flux_field_var",
            ],
            self.notify_script_change,
            sync=True,
        )
        self.build_ui()

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("exports_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        v3.VSwitch(
                            v_model="exports_config.enable_vtx_species_exports",
                            label="Enable VTX species exports",
                            color="primary",
                            hide_details=True,
                            update_modelValue=self.notify_script_change,
                        )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="exports_config.field_exports_var",
                                    label="Field export list variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="exports_config.vtx_field_expr",
                                    label="field expression",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                        v3.VTextField(
                            v_model="exports_config.vtx_filename_template",
                            label="VTX filename template (f-string body)",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )

                        v3.VDivider(classes="my-1")

                        v3.VSwitch(
                            v_model="exports_config.enable_surface_flux_exports",
                            label="Enable surface flux exports",
                            color="primary",
                            hide_details=True,
                            update_modelValue=self.notify_script_change,
                        )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="exports_config.derived_exports_var",
                                    label="Derived export list variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="exports_config.surface_flux_field_var",
                                    label="Surface flux field variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        problem_var = self.page_problem.problem_var
        field_exports_var = (
            self.config.field_exports_var.strip() or DEFAULTS["field_exports_var"]
        )
        derived_exports_var = (
            self.config.derived_exports_var.strip() or DEFAULTS["derived_exports_var"]
        )
        vtx_filename_template = (
            self.config.vtx_filename_template.strip()
            or DEFAULTS["vtx_filename_template"]
        )
        vtx_field_expr = (
            self.config.vtx_field_expr.strip() or DEFAULTS["vtx_field_expr"]
        )
        surface_flux_field_var = (
            self.config.surface_flux_field_var.strip()
            or DEFAULTS["surface_flux_field_var"]
        )

        include_vtx = as_bool(
            self.config.enable_vtx_species_exports,
            DEFAULTS["enable_vtx_species_exports"],
        )
        include_surface_flux = as_bool(
            self.config.enable_surface_flux_exports,
            DEFAULTS["enable_surface_flux_exports"],
        )

        lines = ["# 9. Exports"]
        if include_vtx:
            lines.extend(
                [
                    f"{field_exports_var} = [",
                    "    F.VTXSpeciesExport(",
                    f'        filename=f"{vtx_filename_template}",',
                    f"        field={vtx_field_expr},",
                    "        subdomain=subdomain,",
                    "    )",
                    f"    for subdomain in {problem_var}.volume_subdomains",
                    "]",
                    "",
                ]
            )

        if include_surface_flux:
            lines.extend(
                [
                    f"{derived_exports_var} = [",
                    f"    F.SurfaceFlux(field={surface_flux_field_var}, surface=surf)",
                    f"    for surf in {problem_var}.surface_subdomains",
                    "]",
                    "",
                ]
            )

        if include_vtx and include_surface_flux:
            lines.append(
                f"{problem_var}.exports = {field_exports_var} + {derived_exports_var}"
            )
        elif include_vtx:
            lines.append(f"{problem_var}.exports = {field_exports_var}")
        elif include_surface_flux:
            lines.append(f"{problem_var}.exports = {derived_exports_var}")
        else:
            lines.append(f"{problem_var}.exports = []")

        return lines
