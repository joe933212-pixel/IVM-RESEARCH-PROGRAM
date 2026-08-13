from typing import Any

def get_path(document: dict[str, Any], path: str) -> Any:
    current: Any = document
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current

def evaluate_rule(event_payload: dict[str, Any], rule) -> bool:
    actual = get_path(event_payload, rule.field)
    expected = rule.value
    op = rule.operator
    if op == "equals": return actual == expected
    if op == "not_equals": return actual != expected
    if op == "in": return actual in expected
    if op == "not_in": return actual not in expected
    if op == "gte": return actual is not None and actual >= expected
    if op == "lte": return actual is not None and actual <= expected
    if op == "gt": return actual is not None and actual > expected
    if op == "lt": return actual is not None and actual < expected
    if op == "exists": return actual is not None
    raise ValueError(f"Unsupported rule operator: {op}")
