from trame.widgets import vuetify3 as v3

from festim_gui.festim_ui.component import FestimComponent
from festim_gui.utils.utils import as_float, as_int, set_missing_state_defaults

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
STATE_KEYS = list(DEFAULTS.keys())


class MeshComponent(FestimComponent):
    card_title = "2. Mesh"
    defaults = DEFAULTS
    coordinate_systems = COORDINATE_SYSTEMS
    cell_types = CELL_TYPES
    state_keys = STATE_KEYS

    @staticmethod
    def init_state(state) -> None:
        set_missing_state_defaults(state, MeshComponent.defaults)

    def build_content(self) -> None:
        v3.VTextField(
            v_model=("mesh_var", self.defaults["mesh_var"]),
            label="dolfinx mesh variable",
            variant="outlined",
            density="comfortable",
        )
        with v3.VRow(classes="ga-0"):
            with v3.VCol(cols="6"):
                v3.VTextField(
                    v_model=("mesh_nx", self.defaults["mesh_nx"]),
                    label="nx",
                    type="number",
                    variant="outlined",
                    density="comfortable",
                )
            with v3.VCol(cols="6"):
                v3.VTextField(
                    v_model=("mesh_ny", self.defaults["mesh_ny"]),
                    label="ny",
                    type="number",
                    variant="outlined",
                    density="comfortable",
                )
        with v3.VRow(classes="ga-0"):
            with v3.VCol(cols="6"):
                v3.VTextField(
                    v_model=("mesh_xmin", self.defaults["mesh_xmin"]),
                    label="xmin",
                    type="number",
                    variant="outlined",
                    density="comfortable",
                )
            with v3.VCol(cols="6"):
                v3.VTextField(
                    v_model=("mesh_xmax", self.defaults["mesh_xmax"]),
                    label="xmax",
                    type="number",
                    variant="outlined",
                    density="comfortable",
                )
        with v3.VRow(classes="ga-0"):
            with v3.VCol(cols="6"):
                v3.VTextField(
                    v_model=("mesh_ymin", self.defaults["mesh_ymin"]),
                    label="ymin",
                    type="number",
                    variant="outlined",
                    density="comfortable",
                )
            with v3.VCol(cols="6"):
                v3.VTextField(
                    v_model=("mesh_ymax", self.defaults["mesh_ymax"]),
                    label="ymax",
                    type="number",
                    variant="outlined",
                    density="comfortable",
                )
        v3.VSelect(
            v_model=("mesh_coordinate_system", self.defaults["mesh_coordinate_system"]),
            items=(self.coordinate_systems,),
            label="Coordinate system",
            variant="outlined",
            density="comfortable",
        )
        v3.VSelect(
            v_model=("mesh_cell_type", self.defaults["mesh_cell_type"]),
            items=(self.cell_types,),
            label="Cell type",
            variant="outlined",
            density="comfortable",
        )

    @staticmethod
    def to_script_lines(state, problem_var: str) -> list[str]:
        nx = as_int(state.mesh_nx, MeshComponent.defaults["mesh_nx"])
        ny = as_int(state.mesh_ny, MeshComponent.defaults["mesh_ny"])
        xmin = as_float(state.mesh_xmin, MeshComponent.defaults["mesh_xmin"])
        ymin = as_float(state.mesh_ymin, MeshComponent.defaults["mesh_ymin"])
        xmax = as_float(state.mesh_xmax, MeshComponent.defaults["mesh_xmax"])
        ymax = as_float(state.mesh_ymax, MeshComponent.defaults["mesh_ymax"])
        coordinate_system = state.mesh_coordinate_system
        cell_type = state.mesh_cell_type

        return [
            f"nx = {nx}",
            f"ny = {ny}",
            f'coordinate_system = "{coordinate_system}"',
            f"lower_left = np.array([{xmin}, {ymin}])",
            f"upper_right = np.array([{xmax}, {ymax}])",
            f"cell_type = dolfinx.mesh.CellType.{cell_type}",
            "",
            f"{state.mesh_var} = dolfinx.mesh.create_rectangle(",
            "    MPI.COMM_WORLD, [lower_left, upper_right], [nx, ny], cell_type=cell_type",
            ")",
            f"{problem_var}.mesh = F.Mesh({state.mesh_var}, coordinate_system=coordinate_system)",
        ]
