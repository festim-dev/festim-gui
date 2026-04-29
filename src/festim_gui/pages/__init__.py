from dataclasses import dataclass
from typing import Callable

from . import mesh_page, problem_page


@dataclass(frozen=True)
class Page:
    id: str
    title: str
    description: str
    state_keys: list[str]
    init_state: Callable
    build_ui: Callable
    script_lines: Callable


PAGES = [
    Page(
        id=problem_page.PAGE_ID,
        title=problem_page.TITLE,
        description=problem_page.DESCRIPTION,
        state_keys=problem_page.STATE_KEYS,
        init_state=problem_page.init_state,
        build_ui=problem_page.build_ui,
        script_lines=problem_page.script_lines,
    ),
    Page(
        id=mesh_page.PAGE_ID,
        title=mesh_page.TITLE,
        description=mesh_page.DESCRIPTION,
        state_keys=mesh_page.STATE_KEYS,
        init_state=mesh_page.init_state,
        build_ui=mesh_page.build_ui,
        script_lines=mesh_page.script_lines,
    ),
]

FORM_STATE_KEYS = list(dict.fromkeys(key for page in PAGES for key in page.state_keys))

__all__ = ["FORM_STATE_KEYS", "PAGES", "Page"]
