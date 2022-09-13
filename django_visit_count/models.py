from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from .utils import is_new_visit


class VisitCountMixin:
    visit_count = models.PositiveIntegerField(default=0, help_text=_("Visit count"))

    def update_visit_count(self, request):
        if is_new_visit(request, self):
            self.visit_count = F("visit_count") + 1
            self.save(update_fields=["visit_count"])
