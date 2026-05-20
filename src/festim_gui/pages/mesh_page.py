from trame.app.dataclass import StateDataModel, Sync
from trame.ui.html import DivLayout
from trame.widgets import vuetify3 as v3

from festim_gui.pages.page import Page
from festim_gui.utils import as_float, as_int

DEFAULTS = {
    "mesh_var": "mesh_dolfinx",
    "mesh_nx": None,
    "mesh_ny": None,
    "mesh_coordinate_system": "cartesian",
    "mesh_xmin": None,
    "mesh_ymin": None,
    "mesh_xmax": None,
    "mesh_ymax": None,
    "mesh_cell_type": "triangle",
}
COORDINATE_SYSTEMS = ["cartesian", "cylindrical", "spherical"]
CELL_TYPES = ["triangle", "quadrilateral"]
WATCH_FIELDS = [
    *DEFAULTS.keys(),
    "mesh_nx_error",
    "mesh_ny_error",
    "mesh_xmin_error",
    "mesh_ymin_error",
    "mesh_xmax_error",
    "mesh_ymax_error",
]


class MeshPageState(StateDataModel):
    mesh_var = Sync(str, DEFAULTS["mesh_var"])
    mesh_nx = Sync(str, "")
    mesh_ny = Sync(str, "")
    mesh_nx_error = Sync(bool, False)
    mesh_ny_error = Sync(bool, False)
    mesh_coordinate_system = Sync(str, DEFAULTS["mesh_coordinate_system"])
    mesh_xmin = Sync(str, "")
    mesh_ymin = Sync(str, "")
    mesh_xmax = Sync(str, "")
    mesh_ymax = Sync(str, "")
    mesh_xmin_error = Sync(bool, False)
    mesh_ymin_error = Sync(bool, False)
    mesh_xmax_error = Sync(bool, False)
    mesh_ymax_error = Sync(bool, False)
    mesh_cell_type = Sync(str, DEFAULTS["mesh_cell_type"])


class MeshPage(Page):
    id = "mesh"
    title = "2. Mesh"
    description = "Configure mesh geometry and metadata."
    coordinate_systems = COORDINATE_SYSTEMS
    cell_types = CELL_TYPES

    _REQUIRED_FIELDS = (
        ("mesh_nx", "mesh_nx_error"),
        ("mesh_ny", "mesh_ny_error"),
        ("mesh_xmin", "mesh_xmin_error"),
        ("mesh_xmax", "mesh_xmax_error"),
        ("mesh_ymin", "mesh_ymin_error"),
        ("mesh_ymax", "mesh_ymax_error"),
    )

    def __init__(self, server):
        super().__init__(server, ctx_name="page_mesh")
        self.config = MeshPageState(server)
        self.config.watch(WATCH_FIELDS, self.notify_script_change, sync=True)
        self.config.watch(
            [f for f, _ in self._REQUIRED_FIELDS], self._clear_errors, sync=True
        )
        self.build_ui()

    def _clear_errors(self):
        for field, error_field in self._REQUIRED_FIELDS:
            if str(getattr(self.config, field)).strip():
                setattr(self.config, error_field, False)

    def build_ui(self) -> None:
        with DivLayout(self.server, template_name=self.id):
            with v3.VCard(variant="outlined"):
                with v3.VCardText(classes="d-flex flex-column ga-3"):
                    with self.config.provide_as("mesh_config"):
                        v3.VTextField(
                            v_model="mesh_config.mesh_var",
                            label="dolfinx mesh variable",
                            variant="outlined",
                            density="comfortable",
                            update_modelValue=self.notify_script_change,
                        )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="mesh_config.mesh_nx",
                                    label="nx",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    error=("mesh_config.mesh_nx_error",),
                                    error_messages=(
                                        "mesh_config.mesh_nx_error ? 'Required' : ''",
                                    ),
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="mesh_config.mesh_ny",
                                    label="ny",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    error=("mesh_config.mesh_ny_error",),
                                    error_messages=(
                                        "mesh_config.mesh_ny_error ? 'Required' : ''",
                                    ),
                                    update_modelValue=self.notify_script_change,
                                )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="mesh_config.mesh_xmin",
                                    label="xmin",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    error=("mesh_config.mesh_xmin_error",),
                                    error_messages=(
                                        "mesh_config.mesh_xmin_error ? 'Required' : ''",
                                    ),
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="mesh_config.mesh_xmax",
                                    label="xmax",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    error=("mesh_config.mesh_xmax_error",),
                                    error_messages=(
                                        "mesh_config.mesh_xmax_error ? 'Required' : ''",
                                    ),
                                    update_modelValue=self.notify_script_change,
                                )
                        with v3.VRow(classes="ga-0"):
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="mesh_config.mesh_ymin",
                                    label="ymin",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    error=("mesh_config.mesh_ymin_error",),
                                    error_messages=(
                                        "mesh_config.mesh_ymin_error ? 'Required' : ''",
                                    ),
                                    update_modelValue=self.notify_script_change,
                                )
                            with v3.VCol(cols="6"):
                                v3.VTextField(
                                    v_model="mesh_config.mesh_ymax",
                                    label="ymax",
                                    type="number",
                                    variant="outlined",
                                    density="comfortable",
                                    error=("mesh_config.mesh_ymax_error",),
                                    error_messages=(
                                        "mesh_config.mesh_ymax_error ? 'Required' : ''",
                                    ),
                                    update_modelValue=self.notify_script_change,
                                )
                        v3.VSelect(
                            v_model="mesh_config.mesh_coordinate_system",
                            items=(self.coordinate_systems,),
                            label="Coordinate system",
                            variant="outlined",
                            density="comfortable",
                            update_modelValue=self.notify_script_change,
                        )
                        v3.VSelect(
                            v_model="mesh_config.mesh_cell_type",
                            items=(self.cell_types,),
                            label="Cell type",
                            variant="outlined",
                            density="comfortable",
                            update_modelValue=self.notify_script_change,
                        )

    def is_valid(self) -> bool:
        return all(
            str(getattr(self.config, field)).strip()
            for field, _ in self._REQUIRED_FIELDS
        )

    def validate(self) -> bool:
        valid = True
        for field, error_field in self._REQUIRED_FIELDS:
            empty = not str(getattr(self.config, field)).strip()
            setattr(self.config, error_field, empty)
            if empty:
                valid = False
        return valid

    @property
    def page_problem(self):
        return self.ctx.page_problem

    def script_lines(self) -> list[str]:
        nx = as_int(self.config.mesh_nx, 0)
        ny = as_int(self.config.mesh_ny, 0)
        xmin = as_float(self.config.mesh_xmin, 0.0)
        ymin = as_float(self.config.mesh_ymin, 0.0)
        xmax = as_float(self.config.mesh_xmax, 0.0)
        ymax = as_float(self.config.mesh_ymax, 0.0)

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
                f"{self.page_problem.problem_var}.mesh = "
                f"F.Mesh({self.config.mesh_var}, coordinate_system=coordinate_system)"
            ),
        ]
