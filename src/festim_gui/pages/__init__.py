from .boundary_conditions_page import BoundaryConditionsPage
from .domains_page import DomainsPage
from .exports_page import ExportsPage
from .initial_conditions_page import InitialConditionsPage
from .materials_page import MaterialsPage
from .mesh_page import MeshPage
from .page import Page
from .particle_source_page import ParticleSourcePage
from .problem_page import ProblemPage
from .reactions_page import ReactionsPage
from .run_page import RunPage
from .settings_page import SettingsPage
from .species_page import SpeciesPage
from .temperature_page import TemperaturePage


def create_pages(server):
    pages = [
        ProblemPage(server).activate(),
        MeshPage(server),
        MaterialsPage(server),
        DomainsPage(server),
        SpeciesPage(server),
        InitialConditionsPage(server),
        ReactionsPage(server),
        BoundaryConditionsPage(server),
        ParticleSourcePage(server),
        TemperaturePage(server),
        SettingsPage(server),
        ExportsPage(server),
    ]
    pages.append(RunPage(server, pages))
    return pages


__all__ = ["Page", "create_pages"]
