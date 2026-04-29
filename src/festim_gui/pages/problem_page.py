from festim_gui.festim_ui import problem

PAGE_ID = "problem"
TITLE = "1. Problem"
DESCRIPTION = "Create the root FESTIM problem object."


def init_state(state):
    problem.init_state(state)


def build_ui():
    problem.build_form()
