REQUIRED_KEYS = {
    "event_id", "transition_id", "pre_state", "post_state", "authority_id",
    "rule_set", "rule_version", "commitment_status", "history_id",
    "replay", "recovery", "duplicate_event",
}

def canonicalize(result):
    missing = REQUIRED_KEYS - set(result)
    if missing:
        raise AssertionError(f"missing semantic fields: {sorted(missing)}")
    return {key: result[key] for key in sorted(REQUIRED_KEYS)}

def compare(actual, expected):
    actual = canonicalize(actual)
    expected = canonicalize(expected)
    diff = {
        key: {"actual": actual[key], "expected": expected[key]}
        for key in expected if actual[key] != expected[key]
    }
    return not diff, diff
