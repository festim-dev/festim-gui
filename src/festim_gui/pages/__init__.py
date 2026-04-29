from dataclasses import dataclass
from typing import Callable

from . import mesh_page, problem_page


@dataclass(frozen=True)
class Page:
    id: str
    title: str
    description: str
    init_state: Callable
    build_ui: Callable


PAGES = [
    Page(
        id=problem_page.PAGE_ID,
        title=problem_page.TITLE,
        description=problem_page.DESCRIPTION,
        init_state=problem_page.init_state,
        build_ui=problem_page.build_ui,
    ),
    Page(
        id=mesh_page.PAGE_ID,
        title=mesh_page.TITLE,
        description=mesh_page.DESCRIPTION,
        init_state=mesh_page.init_state,
        build_ui=mesh_page.build_ui,
    ),
]

__all__ = ["PAGES", "Page"]
