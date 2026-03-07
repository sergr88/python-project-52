"""Task filters for filtering tasks list."""

import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    """FilterSet for filtering tasks."""

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Label'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('Only own tasks'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        """Meta class for TaskFilter."""

        model = Task
        fields = ('status', 'executor', 'label')

    def filter_self_tasks(self, queryset, name, value):
        """Filter tasks by current user as author."""
        if value and self.request:
            return queryset.filter(author=self.request.user)
        return queryset
