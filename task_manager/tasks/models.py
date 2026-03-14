"""Task model."""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    """Task model."""

    name = models.CharField(max_length=150, unique=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status')
    )
    executor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='tasks_assigned',
        verbose_name=_('Executor'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_authored',
        verbose_name=_('Author'),
    )
    labels = models.ManyToManyField(Label, blank=True, verbose_name=_('Labels'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the task name."""
        return self.name
