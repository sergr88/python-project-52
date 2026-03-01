"""Status forms."""

from django.forms import ModelForm

from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    """Form for creating and updating statuses."""

    class Meta:
        """Meta class for StatusForm."""

        model = Status
        fields = ('name',)
