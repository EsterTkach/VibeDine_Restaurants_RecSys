import time

_cache: dict[str, tuple[dict, float]] = {}
TTL_SECONDS = 300  # 5 minutes


def get(user_id: str):
    entry = _cache.get(user_id)
    if entry is None:
        return None
    scores, ts = entry
    if time.time() - ts > TTL_SECONDS:
        _cache.pop(user_id, None)
        return None
    return scores


def set(user_id: str, scores: dict):
    _cache[user_id] = (scores, time.time())


def invalidate(user_id: str):
    _cache.pop(user_id, None)
