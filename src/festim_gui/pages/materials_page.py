from festim_gui.festim_ui import material

PAGE_ID = "materials"
TITLE = "3. Materials"
DESCRIPTION = "Create one or more F.Material objects."
STATE_KEYS = material.STATE_KEYS


def init_state(state):
    material.init_state(state)


def build_ui():
    material.build_form()


def script_lines(state):
    items = material.from_state(state)
    return ["# 3. Create materials", *material.to_script_lines(items)]
