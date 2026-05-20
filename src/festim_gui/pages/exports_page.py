from trame.app.dataclass import StateDataModel, Sync
from trame.ui.html import DivLayout
from trame.widgets import vuetify3 as v3

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import build_initial_rows, resolve_template_row

DEFAULTS = {
    "field_exports_var": "concentration_field_exports",
    "derived_exports_var": "derived_quantities",
    "vtx_filename_template": "out/vol_{subdomain.id}.bp",
}

VTX_EXPORT_DEFAULTS = {
    "var": "vtx_export_{i}",
    "field_expr": "problem.species",
    "subdomain_var": "volume_1",
}
VTX_EXPORTS = [
    {
        "var": "vtx_export_1",
        "field_expr": "problem.species",
        "subdomain_var": "volume_1",
    }
]

SURFACE_QUANTITY_TYPES = [
    "SurfaceFlux",
    "TotalSurface",
    "AverageSurface",
    "MinimumSurface",
    "MaximumSurface",
]
SURFACE_QUANTITY_DEFAULTS = {
    "var": "surface_quantity_{i}",
    "quantity_class": "SurfaceFlux",
    "field_expr": "H",
    "surface_var": "surface_1",
}
SURFACE_QUANTITIES = [
    {
        "var": "surface_quantity_1",
        "quantity_class": "SurfaceFlux",
        "field_expr": "H",
        "surface_var": "surface_1",
    }
]

VOLUME_QUANTITY_TYPES = [
    "TotalVolume",
    "AverageVolume",
    "MinimumVolume",
    "MaximumVolume",
]
VOLUME_QUANTITY_DEFAULTS = {
    "var": "volume_quantity_{i}",
    "quantity_class": "TotalVolume",
    "field_expr": "H",
    "volume_var": "volume_1",
}
VOLUME_QUANTITIES = [
    {
        "var": "volume_quantity_1",
        "quantity_class": "TotalVolume",
        "field_expr": "H",
        "volume_var": "volume_1",
    }
]


class ExportsPageState(StateDataModel):
    field_exports_var = Sync(str, DEFAULTS["field_exports_var"])
    derived_exports_var = Sync(str, DEFAULTS["derived_exports_var"])
    vtx_filename_template = Sync(str, DEFAULTS["vtx_filename_template"])
    vtx_export_rows = Sync(
        list,
        lambda: build_initial_rows(VTX_EXPORT_DEFAULTS, VTX_EXPORTS),
        client_deep_reactive=True,
    )
    surface_quantity_rows = Sync(
        list,
        lambda: build_initial_rows(SURFACE_QUANTITY_DEFAULTS, SURFACE_QUANTITIES),
        client_deep_reactive=True,
    )
    volume_quantity_rows = Sync(
        list,
        lambda: build_initial_rows(VOLUME_QUANTITY_DEFAULTS, VOLUME_QUANTITIES),
        client_deep_reactive=True,
    )


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
                "vtx_filename_template",
                "vtx_export_rows",
                "surface_quantity_rows",
                "volume_quantity_rows",
            ],
            self.notify_script_change,
            sync=True,
        )
        self.build_ui()

    def add_vtx_export(self, *_args, **_kwargs):
        rows = list(self.config.vtx_export_rows)
        rows.append(resolve_template_row(VTX_EXPORT_DEFAULTS, len(rows)))
        self.config.vtx_export_rows = rows

    def remove_vtx_export(self, *_args, **_kwargs):
        rows = list(self.config.vtx_export_rows)
        if not rows:
            return
        rows.pop()
        self.config.vtx_export_rows = rows

    def add_surface_quantity(self, *_args, **_kwargs):
        rows = list(self.config.surface_quantity_rows)
        rows.append(resolve_template_row(SURFACE_QUANTITY_DEFAULTS, len(rows)))
        self.config.surface_quantity_rows = rows

    def remove_surface_quantity(self, *_args, **_kwargs):
        rows = list(self.config.surface_quantity_rows)
        if not rows:
            return
        rows.pop()
        self.config.surface_quantity_rows = rows

    def add_volume_quantity(self, *_args, **_kwargs):
        rows = list(self.config.volume_quantity_rows)
        rows.append(resolve_template_row(VOLUME_QUANTITY_DEFAULTS, len(rows)))
        self.config.volume_quantity_rows = rows

    def remove_volume_quantity(self, *_args, **_kwargs):
        rows = list(self.config.volume_quantity_rows)
        if not rows:
            return
        rows.pop()
        self.config.volume_quantity_rows = rows

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("exports_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        v3.VTextField(
                            v_model="exports_config.field_exports_var",
                            label="Field export list variable",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )
                        v3.VTextField(
                            v_model="exports_config.derived_exports_var",
                            label="Derived export list variable",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )
                        v3.VTextField(
                            v_model="exports_config.vtx_filename_template",
                            label="VTX filename template",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )

                        v3.VDivider(classes="my-1")

                        v3.VLabel("VTX Species Exports", classes="text-caption")
                        RepeatedItemControls(
                            on_add=self.add_vtx_export,
                            on_remove=self.remove_vtx_export,
                        )
                        with v3.VCard(
                            variant="tonal",
                            v_for="(vtx_row, idx) in exports_config.vtx_export_rows",
                            key=("idx",),
                        ):
                            with v3.VCardText(classes="d-flex flex-column ga-2"):
                                v3.VLabel(
                                    "VTX export {{ idx + 1 }}", classes="text-caption"
                                )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="vtx_row.var",
                                            label="Variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="vtx_row.subdomain_var",
                                            label="Volume subdomain variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                v3.VTextField(
                                    v_model="vtx_row.field_expr",
                                    label="Field expression",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )

                        v3.VDivider(classes="my-1")

                        v3.VLabel(
                            "Derived Quantities - Surface", classes="text-caption"
                        )
                        RepeatedItemControls(
                            on_add=self.add_surface_quantity,
                            on_remove=self.remove_surface_quantity,
                        )
                        with v3.VCard(
                            variant="tonal",
                            v_for="(surface_row, idx) in exports_config.surface_quantity_rows",
                            key=("idx",),
                        ):
                            with v3.VCardText(classes="d-flex flex-column ga-2"):
                                v3.VLabel(
                                    "Surface quantity {{ idx + 1 }}",
                                    classes="text-caption",
                                )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="surface_row.var",
                                            label="Variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VSelect(
                                            v_model="surface_row.quantity_class",
                                            items=(SURFACE_QUANTITY_TYPES,),
                                            label="Quantity type",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="surface_row.field_expr",
                                            label="Field expression",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="surface_row.surface_var",
                                            label="Surface variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )

                        v3.VDivider(classes="my-1")

                        v3.VLabel("Derived Quantities - Volume", classes="text-caption")
                        RepeatedItemControls(
                            on_add=self.add_volume_quantity,
                            on_remove=self.remove_volume_quantity,
                        )
                        with v3.VCard(
                            variant="tonal",
                            v_for="(volume_row, idx) in exports_config.volume_quantity_rows",
                            key=("idx",),
                        ):
                            with v3.VCardText(classes="d-flex flex-column ga-2"):
                                v3.VLabel(
                                    "Volume quantity {{ idx + 1 }}",
                                    classes="text-caption",
                                )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="volume_row.var",
                                            label="Variable",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VSelect(
                                            v_model="volume_row.quantity_class",
                                            items=(VOLUME_QUANTITY_TYPES,),
                                            label="Quantity type",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                with v3.VRow(classes="ga-0"):
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="volume_row.field_expr",
                                            label="Field expression",
                                            variant="outlined",
                                            density="compact",
                                            update_modelValue=self.notify_script_change,
                                        )
                                    with v3.VCol(cols="6"):
                                        v3.VTextField(
                                            v_model="volume_row.volume_var",
                                            label="Volume variable",
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

        lines = ["# 9. Exports"]
        vtx_var_names = []
        for idx, row in enumerate(self.config.vtx_export_rows):
            defaults = resolve_template_row(VTX_EXPORT_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            field_expr = str(row.get("field_expr", defaults["field_expr"]))
            subdomain_var = str(row.get("subdomain_var", defaults["subdomain_var"]))
            vtx_var_names.append(var_name)
            lines.extend(
                [
                    f"{var_name} = F.VTXSpeciesExport(",
                    f'    filename=f"{vtx_filename_template}",',
                    f"    field={field_expr},",
                    f"    subdomain={subdomain_var},",
                    ")",
                ]
            )

        if vtx_var_names:
            lines.append(f"{field_exports_var} = [{', '.join(vtx_var_names)}]")
        else:
            lines.append(f"{field_exports_var} = []")

        lines.append("")

        derived_var_names = []
        for idx, row in enumerate(self.config.surface_quantity_rows):
            defaults = resolve_template_row(SURFACE_QUANTITY_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            quantity_class = str(row.get("quantity_class", defaults["quantity_class"]))
            field_expr = str(row.get("field_expr", defaults["field_expr"]))
            surface_var = str(row.get("surface_var", defaults["surface_var"]))
            derived_var_names.append(var_name)
            lines.extend(
                [
                    f"{var_name} = F.{quantity_class}(",
                    f"    field={field_expr},",
                    f"    surface={surface_var},",
                    ")",
                ]
            )

        for idx, row in enumerate(self.config.volume_quantity_rows):
            defaults = resolve_template_row(VOLUME_QUANTITY_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            quantity_class = str(row.get("quantity_class", defaults["quantity_class"]))
            field_expr = str(row.get("field_expr", defaults["field_expr"]))
            volume_var = str(row.get("volume_var", defaults["volume_var"]))
            derived_var_names.append(var_name)
            lines.extend(
                [
                    f"{var_name} = F.{quantity_class}(",
                    f"    field={field_expr},",
                    f"    volume={volume_var},",
                    ")",
                ]
            )

        if derived_var_names:
            lines.append(f"{derived_exports_var} = [{', '.join(derived_var_names)}]")
        else:
            lines.append(f"{derived_exports_var} = []")

        lines.append("")
        lines.append(
            f"{problem_var}.exports = {field_exports_var} + {derived_exports_var}"
        )

        return lines
