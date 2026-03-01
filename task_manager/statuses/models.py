"""Status model for task statuses."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Task status model."""

    name = models.CharField(max_length=150, unique=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the status name."""
        return self.name
