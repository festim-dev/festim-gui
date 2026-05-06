from typing import Any


def as_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default

    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False

    return default


def set_missing_state_defaults(state, defaults: dict[str, Any]) -> None:
    for key, value in defaults.items():
        if not state.has(key):
            state[key] = value


def _resolve_default(value: Any, index: int) -> Any:
    if callable(value):
        return value(index)
    if isinstance(value, str):
        return value.format(i=index + 1)
    return value


def repeated_state_keys(
    prefix: str,
    fields: dict[str, Any],
    max_items: int,
) -> list[str]:
    keys = [f"{prefix}_count"]
    for idx in range(max_items):
        keys.extend([f"{prefix}_{idx}_{name}" for name in fields])
    return keys


def init_repeated_state(
    state,
    prefix: str,
    fields: dict[str, Any],
    max_items: int,
    initial_items: list[dict[str, Any]],
) -> None:
    default_count = max(1, min(len(initial_items), max_items))
    if not state.has(f"{prefix}_count"):
        state[f"{prefix}_count"] = default_count

    for idx in range(max_items):
        initial_row = initial_items[idx] if idx < len(initial_items) else {}
        for name, default in fields.items():
            key = f"{prefix}_{idx}_{name}"
            if not state.has(key):
                state[key] = initial_row.get(name, _resolve_default(default, idx))


def collection_count(state, prefix: str, max_items: int) -> int:
    raw = as_int(state[f"{prefix}_count"], 1)
    return max(1, min(raw, max_items))


def collection_rows(
    state,
    prefix: str,
    fields: dict[str, Any],
    max_items: int,
) -> list[dict[str, Any]]:
    count = collection_count(state, prefix, max_items)
    rows: list[dict[str, Any]] = []
    for idx in range(count):
        row = {}
        for name in fields:
            row[name] = state[f"{prefix}_{idx}_{name}"]
        rows.append(row)

    return rows
