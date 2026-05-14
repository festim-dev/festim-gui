from .domains_page import DomainsPage
from .initial_conditions_page import InitialConditionsPage
from .materials_page import MaterialsPage
from .mesh_page import MeshPage
from .page import Page
from .problem_page import ProblemPage
from .reactions_page import ReactionsPage
from .species_page import SpeciesPage


def create_pages(server):
    problem = ProblemPage(server)
    mesh = MeshPage(server, problem)
    materials = MaterialsPage(server)
    domains = DomainsPage(server, problem)
    species = SpeciesPage(server, problem)
    initial_conditions = InitialConditionsPage(server, problem)
    reactions = ReactionsPage(server, problem)
    return [
        problem,
        mesh,
        materials,
        domains,
        species,
        initial_conditions,
        reactions,
    ]


__all__ = ["Page", "create_pages"]
