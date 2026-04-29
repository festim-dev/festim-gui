from typing import Any


def set_missing_state_defaults(state, defaults: dict[str, Any]) -> None:
    for key, value in defaults.items():
        if not state.has(key):
            state[key] = value
