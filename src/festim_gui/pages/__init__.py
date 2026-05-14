from .boundary_conditions_page import BoundaryConditionsPage
from .domains_page import DomainsPage
from .exports_page import ExportsPage
from .initial_conditions_page import InitialConditionsPage
from .materials_page import MaterialsPage
from .mesh_page import MeshPage
from .page import Page
from .problem_page import ProblemPage
from .reactions_page import ReactionsPage
from .run_page import RunPage
from .settings_page import SettingsPage
from .species_page import SpeciesPage
from .temperature_page import TemperaturePage


def create_pages(server):
    problem = ProblemPage(server)
    mesh = MeshPage(server, problem)
    materials = MaterialsPage(server)
    domains = DomainsPage(server, problem)
    species = SpeciesPage(server, problem)
    initial_conditions = InitialConditionsPage(server, problem)
    reactions = ReactionsPage(server, problem)
    boundary_conditions = BoundaryConditionsPage(server, problem)
    temperature = TemperaturePage(server, problem)
    settings = SettingsPage(server, problem)
    exports = ExportsPage(server, problem)
    run = RunPage(server, problem)
    return [
        problem,
        mesh,
        materials,
        domains,
        species,
        initial_conditions,
        reactions,
        boundary_conditions,
        temperature,
        settings,
        exports,
        run,
    ]


__all__ = ["Page", "create_pages"]
