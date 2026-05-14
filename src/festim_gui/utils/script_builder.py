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


def build_script(pages, include_header: bool = False) -> str:
    lines = list(HEADER_LINES) if include_header else []
    for page in pages:
        lines.extend(page.script_lines())
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines) + "\n"
