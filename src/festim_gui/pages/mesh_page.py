from festim_gui.festim_ui import mesh

PAGE_ID = "mesh"
TITLE = "2. Mesh"
DESCRIPTION = "Configure mesh geometry and metadata."


def init_state(state):
    mesh.init_state(state)


def build_ui():
    mesh.build_form()
