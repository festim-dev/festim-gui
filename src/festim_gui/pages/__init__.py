from . import materials_page, mesh_page, problem_page
from .page import Page


def create_pages(server):
    problem = problem_page.ProblemPage(server)
    mesh = mesh_page.MeshPage(server, problem)
    materials = materials_page.MaterialsPage(server)
    return [problem, mesh, materials]


__all__ = ["Page", "create_pages"]
