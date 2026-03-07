"""Label model for task labels."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Task label model."""

    name = models.CharField(max_length=150, unique=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the label name."""
        return self.name
