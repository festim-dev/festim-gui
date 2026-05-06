from festim_gui.pages import PAGES

HEADER_LINES = [
    "import warnings",
    "",
    "import dolfinx",
    "import festim as F",
    "import numpy as np",
    "from mpi4py import MPI",
    "",
    'if F.__version__ != "2.0b2.post2":',
    "    warnings.warn(",
    '        "This script template was calibrated against FESTIM 2.0b2.post2. "',
    '        "Adjust section values if your FESTIM version differs.",',
    "        stacklevel=2,",
    "    )",
    "",
]


def build_script_from_state(state, pages=None) -> str:
    active_pages = pages or PAGES
    lines = list(HEADER_LINES)
    for page in active_pages:
        lines.extend(page.script_lines(state))
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines) + "\n"
