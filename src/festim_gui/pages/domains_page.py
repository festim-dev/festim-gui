from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3
from trame.ui.html import DivLayout

from festim_gui.components import RepeatedItemControls
from festim_gui.pages.page import Page
from festim_gui.utils import (
    as_float,
    as_int,
    build_initial_rows,
    comma_separated_list_expr,
    resolve_template_row,
)

DOMAIN_DEFAULTS = {
    "domains_eps": 1e-3,
}

VOLUME_DEFAULTS = {
    "var": "volume_{i}",
    "id": lambda i: i + 1,
    "material_var": "mat_{i}",
    "locator": "lambda x: x[0] < 0.5 + eps",
}
INITIAL_VOLUMES = [
    {
        "var": "volume_1",
        "id": 1,
        "material_var": "mat_1",
        "locator": "lambda x: x[0] < 0.5 + eps",
    },
    {
        "var": "volume_2",
        "id": 2,
        "material_var": "mat_2",
        "locator": "lambda x: x[0] >= 0.5 - eps",
    },
]

SURFACE_DEFAULTS = {
    "var": "surface_{i}",
    "id": lambda i: i + 3,
    "locator": "lambda x: np.isclose(x[0], 0.0)",
    "linked_volume_var": "volume_1",
}
INITIAL_SURFACES = [
    {
        "var": "surface_1",
        "id": 3,
        "locator": "lambda x: np.isclose(x[0], 0.0)",
        "linked_volume_var": "volume_1",
    },
    {
        "var": "surface_2",
        "id": 4,
        "locator": "lambda x: np.isclose(x[0], 1.0)",
        "linked_volume_var": "volume_2",
    },
]

INTERFACE_DEFAULTS = {
    "var": "interface_{i}",
    "id": lambda i: i + 5,
    "subdomains": "volume_1, volume_2",
    "penalty_term": 100.0,
}
INITIAL_INTERFACES = [
    {
        "var": "interface_1",
        "id": 5,
        "subdomains": "volume_1, volume_2",
        "penalty_term": 100.0,
    }
]


class DomainsPageState(StateDataModel):
    domains_eps = Sync(float, DOMAIN_DEFAULTS["domains_eps"])
    volume_rows = Sync(
        list,
        lambda: build_initial_rows(VOLUME_DEFAULTS, INITIAL_VOLUMES),
        client_deep_reactive=True,
    )
    surface_rows = Sync(
        list,
        lambda: build_initial_rows(SURFACE_DEFAULTS, INITIAL_SURFACES),
        client_deep_reactive=True,
    )
    interface_rows = Sync(
        list,
        lambda: build_initial_rows(INTERFACE_DEFAULTS, INITIAL_INTERFACES),
        client_deep_reactive=True,
    )


class DomainsPage(Page):
    id = "domains"
    title = "4. Domains"
    description = "Create volume/surface subdomains and interfaces."

    def __init__(self, server):
        super().__init__(server, ctx_name="page_domains")
        self.config = DomainsPageState(server)
        self.config.watch(
            ["domains_eps", "volume_rows", "surface_rows", "interface_rows"],
            self.notify_script_change,
            sync=True,
        )
        self.build_ui()

    def _add_row(self, key: str, defaults: dict[str, object]) -> None:
        rows = list(getattr(self.config, key))
        rows.append(resolve_template_row(defaults, len(rows)))
        setattr(self.config, key, rows)

    def _remove_row(self, key: str) -> None:
        rows = list(getattr(self.config, key))
        if len(rows) <= 1:
            return
        rows.pop()
        setattr(self.config, key, rows)

    def add_volume(self, *_args, **_kwargs):
        self._add_row("volume_rows", VOLUME_DEFAULTS)

    def remove_volume(self, *_args, **_kwargs):
        self._remove_row("volume_rows")

    def add_surface(self, *_args, **_kwargs):
        self._add_row("surface_rows", SURFACE_DEFAULTS)

    def remove_surface(self, *_args, **_kwargs):
        self._remove_row("surface_rows")

    def add_interface(self, *_args, **_kwargs):
        self._add_row("interface_rows", INTERFACE_DEFAULTS)

    def remove_interface(self, *_args, **_kwargs):
        self._remove_row("interface_rows")

    def _volume_ui(self) -> None:
        with v3.VCard(variant="outlined"):
            with v3.VCardText(classes="d-flex flex-column ga-3"):
                v3.VLabel("Volume Subdomains", classes="text-subtitle-2")
                RepeatedItemControls(
                    on_add=self.add_volume, on_remove=self.remove_volume
                )
                with v3.VCard(
                    variant="tonal",
                    v_for="(volume_row, idx) in domains_config.volume_rows",
                    key=("idx",),
                ):
                    with v3.VCardText(classes="d-flex flex-column ga-2"):
                        v3.VLabel("Volume {{ idx + 1 }}", classes="text-caption")
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="8"):
                                v3.VTextField(
                                    v_model="volume_row.var",
                                    label="Variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="4"):
                                v3.VTextField(
                                    v_model="volume_row.id",
                                    label="id",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                        v3.VTextField(
                            v_model="volume_row.material_var",
                            label="material variable",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )
                        v3.VTextField(
                            v_model="volume_row.locator",
                            label="locator expression",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )

    def _surface_ui(self) -> None:
        with v3.VCard(variant="outlined"):
            with v3.VCardText(classes="d-flex flex-column ga-3"):
                v3.VLabel("Surface Subdomains", classes="text-subtitle-2")
                RepeatedItemControls(
                    on_add=self.add_surface, on_remove=self.remove_surface
                )
                with v3.VCard(
                    variant="tonal",
                    v_for="(surface_row, idx) in domains_config.surface_rows",
                    key=("idx",),
                ):
                    with v3.VCardText(classes="d-flex flex-column ga-2"):
                        v3.VLabel("Surface {{ idx + 1 }}", classes="text-caption")
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="8"):
                                v3.VTextField(
                                    v_model="surface_row.var",
                                    label="Variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="4"):
                                v3.VTextField(
                                    v_model="surface_row.id",
                                    label="id",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                        v3.VTextField(
                            v_model="surface_row.locator",
                            label="locator expression",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )
                        v3.VTextField(
                            v_model="surface_row.linked_volume_var",
                            label="linked volume variable",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )

    def _interface_ui(self) -> None:
        with v3.VCard(variant="outlined"):
            with v3.VCardText(classes="d-flex flex-column ga-3"):
                v3.VLabel("Interfaces", classes="text-subtitle-2")
                RepeatedItemControls(
                    on_add=self.add_interface, on_remove=self.remove_interface
                )
                with v3.VCard(
                    variant="tonal",
                    v_for="(interface_row, idx) in domains_config.interface_rows",
                    key=("idx",),
                ):
                    with v3.VCardText(classes="d-flex flex-column ga-2"):
                        v3.VLabel("Interface {{ idx + 1 }}", classes="text-caption")
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="8"):
                                v3.VTextField(
                                    v_model="interface_row.var",
                                    label="Variable",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="4"):
                                v3.VTextField(
                                    v_model="interface_row.id",
                                    label="id",
                                    type="number",
                                    variant="outlined",
                                    density="compact",
                                    update_modelValue=self.notify_script_change,
                                )
                        v3.VTextField(
                            v_model="interface_row.subdomains",
                            label="subdomains (comma-separated vars)",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )
                        v3.VTextField(
                            v_model="interface_row.penalty_term",
                            label="penalty_term",
                            type="number",
                            variant="outlined",
                            density="compact",
                            update_modelValue=self.notify_script_change,
                        )

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with self.config.provide_as("domains_config"):
                with v3.VCard(variant="outlined"):
                    with v3.VCardText(classes="d-flex flex-column ga-3"):
                        v3.VTextField(
                            v_model="domains_config.domains_eps",
                            label="epsilon helper variable",
                            type="number",
                            variant="outlined",
                            density="comfortable",
                            update_modelValue=self.notify_script_change,
                        )
                self._volume_ui()
                self._surface_ui()
                self._interface_ui()

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        problem_var = self.page_problem.problem_var
        eps = as_float(self.config.domains_eps, DOMAIN_DEFAULTS["domains_eps"])

        volume_rows = self.config.volume_rows
        surface_rows = self.config.surface_rows
        interface_rows = self.config.interface_rows

        lines = ["# 4. Create domains", f"eps = {eps}"]

        volume_vars = []
        for idx, row in enumerate(volume_rows):
            defaults = resolve_template_row(VOLUME_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            subdomain_id = as_int(row.get("id", defaults["id"]), idx + 1)
            material_var = str(row.get("material_var", defaults["material_var"]))
            locator_expr = str(row.get("locator", defaults["locator"]))
            volume_vars.append(var_name)
            lines.append(
                f"{var_name} = F.VolumeSubdomain(id={subdomain_id}, "
                f"material={material_var}, locator={locator_expr})"
            )

        lines.append("")

        surface_vars = []
        surface_to_volume = []
        for idx, row in enumerate(surface_rows):
            defaults = resolve_template_row(SURFACE_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            subdomain_id = as_int(row.get("id", defaults["id"]), idx + 1)
            locator_expr = str(row.get("locator", defaults["locator"]))
            linked_volume_var = str(
                row.get("linked_volume_var", defaults["linked_volume_var"])
            )
            surface_vars.append(var_name)
            lines.append(
                f"{var_name} = F.SurfaceSubdomain(id={subdomain_id}, locator={locator_expr})"
            )
            if linked_volume_var and var_name:
                surface_to_volume.append((var_name, linked_volume_var))

        lines.append("")
        lines.append(
            f"{problem_var}.subdomains = [{', '.join(volume_vars + surface_vars)}]"
        )

        if surface_to_volume:
            lines.append("")
            lines.append(f"{problem_var}.surface_to_volume = {{")
            for surface_var, volume_var in surface_to_volume:
                lines.append(f"    {surface_var}: {volume_var},")
            lines.append("}")

        interface_var_names = []
        if interface_rows:
            lines.append("")
        for idx, row in enumerate(interface_rows):
            defaults = resolve_template_row(INTERFACE_DEFAULTS, idx)
            var_name = str(row.get("var", defaults["var"]))
            interface_id = as_int(row.get("id", defaults["id"]), idx + 1)
            subdomains_expr = str(row.get("subdomains", defaults["subdomains"]))
            penalty_term = as_float(
                row.get("penalty_term", defaults["penalty_term"]),
                INTERFACE_DEFAULTS["penalty_term"],
            )
            interface_var_names.append(var_name)
            lines.append(
                f"{var_name} = F.Interface(id={interface_id}, "
                f"subdomains={comma_separated_list_expr(subdomains_expr)}, "
                f"penalty_term={penalty_term})"
            )

        if interface_var_names:
            lines.append(
                f"{problem_var}.interfaces = [{', '.join(interface_var_names)}]"
            )

        return lines
