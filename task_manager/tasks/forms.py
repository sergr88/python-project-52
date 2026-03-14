"""Task forms."""

from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    """Form for creating and updating tasks."""

    class Meta:
        """Meta class for TaskForm."""

        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')

    def __init__(self, *args, **kwargs):
        """Set executor field to display full names."""
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda user: (
            user.get_full_name() or user.username
        )
