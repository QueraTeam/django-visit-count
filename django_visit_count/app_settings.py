import os

from django.conf import settings

VISIT_COUNT_DEFAULT_SESSION_DURATION = getattr(settings, "VISIT_COUNT_DEFAULT_SESSION_DURATION", 5 * 60)
