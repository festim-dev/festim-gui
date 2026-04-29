from festim_gui.festim_ui import problem

PAGE_ID = "problem"
TITLE = "1. Problem"
DESCRIPTION = "Create the root FESTIM problem object."
STATE_KEYS = problem.STATE_KEYS


def init_state(state):
    problem.init_state(state)


def build_ui():
    problem.build_form()


def script_lines(state):
    model = problem.from_state(state)
    return ["# 1. Create empty problem", *problem.to_script_lines(model)]
