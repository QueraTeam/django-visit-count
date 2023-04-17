from django.db import models
from django.utils.translation import gettext_lazy as _

from .app_settings import VISIT_COUNT_DEFAULT_SESSION_DURATION
from .utils import is_new_visit


class VisitCountMixin(models.Model):
    visit_count = models.PositiveIntegerField(default=0, help_text=_("Visit count"))

    class Meta:
        abstract = True

    def count_visit(self, request, session_duration=VISIT_COUNT_DEFAULT_SESSION_DURATION):
        if is_new_visit(request, self, session_duration=session_duration):
            self.visit_count = models.F("visit_count") + 1
            self.save(update_fields=["visit_count"])

    def reset_visits(self, save=True):
        self.visit_count = 0
        if save:
            self.save(update_fields=["visit_count"])
