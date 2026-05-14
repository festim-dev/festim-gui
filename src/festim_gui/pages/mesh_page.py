from trame.app.dataclass import StateDataModel, Sync
from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page
from festim_gui.utils import as_float, as_int

DEFAULTS = {
    "mesh_var": "mesh_dolfinx",
    "mesh_nx": 20,
    "mesh_ny": 20,
    "mesh_coordinate_system": "cartesian",
    "mesh_xmin": 0.0,
    "mesh_ymin": 0.0,
    "mesh_xmax": 1.0,
    "mesh_ymax": 1.0,
    "mesh_cell_type": "triangle",
}
COORDINATE_SYSTEMS = ["cartesian", "cylindrical", "spherical"]
CELL_TYPES = ["triangle", "quadrilateral"]
WATCH_FIELDS = list(DEFAULTS.keys())


class MeshPageState(StateDataModel):
    mesh_var = Sync(str, DEFAULTS["mesh_var"])
    mesh_nx = Sync(int, DEFAULTS["mesh_nx"])
    mesh_ny = Sync(int, DEFAULTS["mesh_ny"])
    mesh_coordinate_system = Sync(str, DEFAULTS["mesh_coordinate_system"])
    mesh_xmin = Sync(float, DEFAULTS["mesh_xmin"])
    mesh_ymin = Sync(float, DEFAULTS["mesh_ymin"])
    mesh_xmax = Sync(float, DEFAULTS["mesh_xmax"])
    mesh_ymax = Sync(float, DEFAULTS["mesh_ymax"])
    mesh_cell_type = Sync(str, DEFAULTS["mesh_cell_type"])


class MeshPage(Page):
    id = "mesh"
    title = "2. Mesh"
    description = "Configure mesh geometry and metadata."
    coordinate_systems = COORDINATE_SYSTEMS
    cell_types = CELL_TYPES

    def __init__(self, server, problem_page):
        super().__init__(server)
        self._problem_page = problem_page
        self.config = MeshPageState(server)
        self.config.watch(WATCH_FIELDS, self._on_state_change, sync=True)

    def _on_state_change(self, *_args):
        self.notify_script_change()

    def _on_field_update(self, *_args, **_kwargs):
        self.notify_script_change()

    def build_ui(self) -> None:
        with v3.VCard(variant="outlined"):
            with v3.VCardText(classes="d-flex flex-column ga-3"):
                with self.config.provide_as("mesh_config"):
                    v3.VTextField(
                        v_model="mesh_config.mesh_var",
                        label="dolfinx mesh variable",
                        variant="outlined",
                        density="comfortable",
                        update_modelValue=self._on_field_update,
                    )
                    with v3.VRow(classes="ga-0"):
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model="mesh_config.mesh_nx",
                                label="nx",
                                type="number",
                                variant="outlined",
                                density="comfortable",
                                update_modelValue=self._on_field_update,
                            )
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model="mesh_config.mesh_ny",
                                label="ny",
                                type="number",
                                variant="outlined",
                                density="comfortable",
                                update_modelValue=self._on_field_update,
                            )
                    with v3.VRow(classes="ga-0"):
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model="mesh_config.mesh_xmin",
                                label="xmin",
                                type="number",
                                variant="outlined",
                                density="comfortable",
                                update_modelValue=self._on_field_update,
                            )
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model="mesh_config.mesh_xmax",
                                label="xmax",
                                type="number",
                                variant="outlined",
                                density="comfortable",
                                update_modelValue=self._on_field_update,
                            )
                    with v3.VRow(classes="ga-0"):
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model="mesh_config.mesh_ymin",
                                label="ymin",
                                type="number",
                                variant="outlined",
                                density="comfortable",
                                update_modelValue=self._on_field_update,
                            )
                        with v3.VCol(cols="6"):
                            v3.VTextField(
                                v_model="mesh_config.mesh_ymax",
                                label="ymax",
                                type="number",
                                variant="outlined",
                                density="comfortable",
                                update_modelValue=self._on_field_update,
                            )
                    v3.VSelect(
                        v_model="mesh_config.mesh_coordinate_system",
                        items=(self.coordinate_systems,),
                        label="Coordinate system",
                        variant="outlined",
                        density="comfortable",
                        update_modelValue=self._on_field_update,
                    )
                    v3.VSelect(
                        v_model="mesh_config.mesh_cell_type",
                        items=(self.cell_types,),
                        label="Cell type",
                        variant="outlined",
                        density="comfortable",
                        update_modelValue=self._on_field_update,
                    )

    def script_lines(self) -> list[str]:
        nx = as_int(self.config.mesh_nx, DEFAULTS["mesh_nx"])
        ny = as_int(self.config.mesh_ny, DEFAULTS["mesh_ny"])
        xmin = as_float(self.config.mesh_xmin, DEFAULTS["mesh_xmin"])
        ymin = as_float(self.config.mesh_ymin, DEFAULTS["mesh_ymin"])
        xmax = as_float(self.config.mesh_xmax, DEFAULTS["mesh_xmax"])
        ymax = as_float(self.config.mesh_ymax, DEFAULTS["mesh_ymax"])

        return [
            "# 2. Create mesh",
            f"nx = {nx}",
            f"ny = {ny}",
            f'coordinate_system = "{self.config.mesh_coordinate_system}"',
            f"lower_left = np.array([{xmin}, {ymin}])",
            f"upper_right = np.array([{xmax}, {ymax}])",
            f"cell_type = dolfinx.mesh.CellType.{self.config.mesh_cell_type}",
            "",
            f"{self.config.mesh_var} = dolfinx.mesh.create_rectangle(",
            "    MPI.COMM_WORLD, [lower_left, upper_right], [nx, ny], cell_type=cell_type",
            ")",
            (
                f"{self._problem_page.problem_var}.mesh = "
                f"F.Mesh({self.config.mesh_var}, coordinate_system=coordinate_system)"
            ),
        ]
