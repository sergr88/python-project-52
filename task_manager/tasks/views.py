"""Task views for CRUD operations."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskLoginRequiredMixin(LoginRequiredMixin):
    """Mixin that redirects unauthenticated users to login."""

    def handle_no_permission(self):
        """Redirect with an error message on permission failure."""
        messages.error(self.request, _('You are not logged in! Please log in.'))
        return redirect('login')


class TaskListView(TaskLoginRequiredMixin, FilterView):
    """View for listing all tasks with filtering."""

    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(TaskLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """View for creating a task."""

    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task created successfully')

    def form_valid(self, form):
        """Set the author to the current user."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View for updating a task."""

    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task updated successfully')


class TaskDetailView(TaskLoginRequiredMixin, DetailView):
    """View for viewing task details."""

    model = Task
    template_name = 'tasks/detail.html'


class TaskDeleteView(TaskLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """View for deleting a task."""

    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task deleted successfully')

    def dispatch(self, request, *args, **kwargs):
        """Only allow the author to delete the task."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        task = self.get_object()
        if task.author != request.user:
            messages.error(
                request, _('A task can only be deleted by its author.')
            )
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)
