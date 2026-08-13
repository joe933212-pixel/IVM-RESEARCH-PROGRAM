from .canonical import deep_copy

def set_path(document, path, value):
    parts = path.split(".")
    if not parts or any(not p for p in parts):
        raise ValueError("Invalid state path")
    current = document
    for part in parts[:-1]:
        if part not in current: current[part] = {}
        if not isinstance(current[part], dict):
            raise ValueError(f"Cannot descend through non-object field: {part}")
        current = current[part]
    current[parts[-1]] = deep_copy(value)

def apply_transition(state, operations):
    candidate = deep_copy(state)
    for operation in operations:
        if operation.get("op") != "set":
            raise ValueError(f"Unsupported transition operation: {operation.get('op')}")
        set_path(candidate, operation["path"], operation.get("value"))
    return candidate
