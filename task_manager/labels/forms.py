"""Label forms."""

from django.forms import ModelForm

from task_manager.labels.models import Label


class LabelForm(ModelForm):
    """Form for creating and updating labels."""

    class Meta:
        """Meta class for LabelForm."""

        model = Label
        fields = ('name',)
