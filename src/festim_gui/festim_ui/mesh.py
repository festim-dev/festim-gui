from trame.widgets import vuetify3 as v3

from .utils import as_float, as_int, set_missing_state_defaults

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


def init_state(state) -> None:
    set_missing_state_defaults(state, DEFAULTS)


def build_form() -> None:
    with v3.VCard(variant="outlined"):
        v3.VCardTitle("2. Mesh")
        with v3.VCardText(classes="d-flex flex-column ga-3"):
            v3.VTextField(
                v_model=("mesh_var", DEFAULTS["mesh_var"]),
                label="dolfinx mesh variable",
                variant="outlined",
                density="comfortable",
            )
            with v3.VRow(classes="ga-0"):
                with v3.VCol(cols="6"):
                    v3.VTextField(
                        v_model=("mesh_nx", DEFAULTS["mesh_nx"]),
                        label="nx",
                        type="number",
                        variant="outlined",
                        density="comfortable",
                    )
                with v3.VCol(cols="6"):
                    v3.VTextField(
                        v_model=("mesh_ny", DEFAULTS["mesh_ny"]),
                        label="ny",
                        type="number",
                        variant="outlined",
                        density="comfortable",
                    )
            with v3.VRow(classes="ga-0"):
                with v3.VCol(cols="6"):
                    v3.VTextField(
                        v_model=("mesh_xmin", DEFAULTS["mesh_xmin"]),
                        label="xmin",
                        type="number",
                        variant="outlined",
                        density="comfortable",
                    )
                with v3.VCol(cols="6"):
                    v3.VTextField(
                        v_model=("mesh_xmax", DEFAULTS["mesh_xmax"]),
                        label="xmax",
                        type="number",
                        variant="outlined",
                        density="comfortable",
                    )
            with v3.VRow(classes="ga-0"):
                with v3.VCol(cols="6"):
                    v3.VTextField(
                        v_model=("mesh_ymin", DEFAULTS["mesh_ymin"]),
                        label="ymin",
                        type="number",
                        variant="outlined",
                        density="comfortable",
                    )
                with v3.VCol(cols="6"):
                    v3.VTextField(
                        v_model=("mesh_ymax", DEFAULTS["mesh_ymax"]),
                        label="ymax",
                        type="number",
                        variant="outlined",
                        density="comfortable",
                    )
            v3.VSelect(
                v_model=("mesh_coordinate_system", DEFAULTS["mesh_coordinate_system"]),
                items=(COORDINATE_SYSTEMS,),
                label="Coordinate system",
                variant="outlined",
                density="comfortable",
            )
            v3.VSelect(
                v_model=("mesh_cell_type", DEFAULTS["mesh_cell_type"]),
                items=(CELL_TYPES,),
                label="Cell type",
                variant="outlined",
                density="comfortable",
            )


def to_script_lines(state, problem_var: str) -> list[str]:
    nx = as_int(state.mesh_nx, DEFAULTS["mesh_nx"])
    ny = as_int(state.mesh_ny, DEFAULTS["mesh_ny"])
    xmin = as_float(state.mesh_xmin, DEFAULTS["mesh_xmin"])
    ymin = as_float(state.mesh_ymin, DEFAULTS["mesh_ymin"])
    xmax = as_float(state.mesh_xmax, DEFAULTS["mesh_xmax"])
    ymax = as_float(state.mesh_ymax, DEFAULTS["mesh_ymax"])
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
