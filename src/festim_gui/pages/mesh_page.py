from festim_gui.festim_ui import mesh, problem

PAGE_ID = "mesh"
TITLE = "2. Mesh"
DESCRIPTION = "Configure mesh geometry and metadata."
STATE_KEYS = mesh.STATE_KEYS


def init_state(state):
    mesh.init_state(state)


def build_ui():
    mesh.build_form()


def script_lines(state):
    problem_var = problem.from_state(state).var_name
    return ["# 2. Create mesh", *mesh.to_script_lines(state, problem_var)]
