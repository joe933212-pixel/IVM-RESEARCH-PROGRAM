import hashlib, json

def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def deep_copy(value):
    return json.loads(json.dumps(value, ensure_ascii=False))
