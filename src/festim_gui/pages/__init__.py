from . import materials_page, mesh_page, problem_page
from .page import Page

PAGES = [
    problem_page.ProblemPage(),
    mesh_page.MeshPage(),
    materials_page.MaterialsPage(),
]

FORM_STATE_KEYS = list(dict.fromkeys(key for page in PAGES for key in page.state_keys))

__all__ = ["FORM_STATE_KEYS", "PAGES", "Page"]
