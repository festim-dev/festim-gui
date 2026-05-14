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


def comma_separated_list_expr(value: str) -> str:
    items = [item.strip() for item in str(value).split(",") if item.strip()]
    return f"[{', '.join(items)}]"


def resolve_template_row(defaults: dict[str, Any], index: int) -> dict[str, Any]:
    row = {}
    for key, value in defaults.items():
        if callable(value):
            row[key] = value(index)
        elif isinstance(value, str):
            row[key] = value.format(i=index + 1)
        else:
            row[key] = value
    return row


def build_initial_rows(
    defaults: dict[str, Any], initial_items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    return [
        {**resolve_template_row(defaults, idx), **row}
        for idx, row in enumerate(initial_items)
    ]
