import os, requests
BASE = os.getenv("EXTERNAL_EXERCISEDB_BASE", "https://v1.exercisedb.dev/api/v1").rstrip("/")

def _get(path, params=None, timeout=20):
    url = f"{BASE}{path}"
    r = requests.get(url, params=params or {}, timeout=timeout)
    r.raise_for_status()
    payload = r.json()
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"], payload.get("metadata", {})
    return payload, {}

def _params(limit=None, offset=None):
    p = {}
    if limit  is not None:  p["limit"]  = limit
    if offset is not None:  p["offset"] = offset
    return p

def list_all(limit=None, offset=None):
    return _get("/exercises", _params(limit, offset))

def by_body_part(part, limit=None, offset=None):
    return _get(f"/exercises/bodyPart/{part}", _params(limit, offset))

def by_target(target, limit=None, offset=None):
    return _get(f"/exercises/target/{target}", _params(limit, offset))

def by_equipment(eq, limit=None, offset=None):
    return _get(f"/exercises/equipment/{eq}", _params(limit, offset))