from django.core.cache import cache
from ipware import get_client_ip

from .app_settings import VISIT_COUNT_DEFAULT_SESSION_DURATION


def is_new_visit(request, obj, *, session_duration=VISIT_COUNT_DEFAULT_SESSION_DURATION):
    if request.user.is_authenticated:
        user_key = f"user-{request.user.id}"
    else:
        google_analytics_id = request.COOKIES.get("_gid", request.COOKIES.get("_ga", ""))
        user_key = f"{get_client_ip(request)[0]}-{google_analytics_id[:120]}"

    object_key = f"{obj.__class__.__name__}-{getattr(obj, 'pk', obj)}"

    cache_key = f"__visit__:{object_key}:{user_key}"

    if cache.get(cache_key):
        return False

    cache.set(cache_key, True, timeout=session_duration)
    return True
