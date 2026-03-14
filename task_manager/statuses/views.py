"""Status views for CRUD operations."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusLoginRequiredMixin(LoginRequiredMixin):
    """Mixin that redirects unauthenticated users to login."""

    def handle_no_permission(self):
        """Redirect with an error message on permission failure."""
        messages.error(self.request, _('You are not logged in! Please log in.'))
        return redirect('login')


class StatusListView(StatusLoginRequiredMixin, ListView):
    """View for listing all statuses."""

    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(
    StatusLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    """View for creating a status."""

    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status created successfully')


class StatusUpdateView(
    StatusLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    """View for updating a status."""

    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status updated successfully')


class StatusDeleteView(
    StatusLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    """View for deleting a status."""

    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status deleted successfully')

    def post(self, request, *args, **kwargs):
        """Handle ProtectedError when status is referenced by tasks."""
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _('Cannot delete status because it is in use'),
            )
            return redirect('statuses')
