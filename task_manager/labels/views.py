"""Label views for CRUD operations."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelLoginRequiredMixin(LoginRequiredMixin):
    """Mixin that redirects unauthenticated users to login."""

    def handle_no_permission(self):
        """Redirect with an error message on permission failure."""
        messages.error(self.request, _('You are not logged in! Please log in.'))
        return redirect('login')


class LabelListView(LabelLoginRequiredMixin, ListView):
    """View for listing all labels."""

    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(LabelLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """View for creating a label."""

    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label created successfully')


class LabelUpdateView(LabelLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View for updating a label."""

    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label updated successfully')


class LabelDeleteView(LabelLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """View for deleting a label."""

    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label deleted successfully')

    def post(self, request, *args, **kwargs):
        """Prevent deletion when label is referenced by tasks."""
        label = self.get_object()
        if label.task_set.exists():
            messages.error(
                request,
                _('Cannot delete label because it is in use'),
            )
            return redirect('labels')
        return super().post(request, *args, **kwargs)
