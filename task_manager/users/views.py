"""User views for registration and authentication."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import (
    CustomUserCreationForm,
    CustomUserUpdateForm,
)


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin ensuring only the user themselves can modify their profile."""

    def test_func(self):
        """Check that the user is modifying their own profile."""
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        """Redirect with an error message on permission failure."""
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, _('You are not logged in! Please log in.')
            )
            return redirect('login')
        messages.error(
            self.request,
            _("You don't have permission to modify another user."),
        )
        return redirect('users')


class UserListView(ListView):
    """View for listing all users."""

    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    """View for user registration."""

    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User registered successfully')


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    """View for updating a user."""

    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User updated successfully')


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    """View for deleting a user."""

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('User deleted successfully')

    def post(self, request, *args, **kwargs):
        """Handle ProtectedError when user is referenced by tasks."""
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _('Cannot delete user because it is in use'),
            )
            return redirect('users')


class UserLoginView(SuccessMessageMixin, LoginView):
    """View for user login."""

    template_name = 'users/login.html'
    success_message = _('You are logged in')


class UserLogoutView(LogoutView):
    """View for user logout."""

    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        """Log out the user and show an info message."""
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, _('You are logged out'))
        return response
