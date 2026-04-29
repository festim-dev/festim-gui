from trame.widgets import vuetify3 as v3

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


def init_state(state) -> None:
    for key, value in DEFAULTS.items():
        if not state.has(key):
            state[key] = value


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
