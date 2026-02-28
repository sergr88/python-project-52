"""Custom user forms."""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """User creation form with first_name and last_name fields."""

    class Meta(UserCreationForm.Meta):
        """Meta class for CustomUserCreationForm."""

        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class CustomUserUpdateForm(CustomUserCreationForm):
    """User update form reusing creation form fields."""

    class Meta(CustomUserCreationForm.Meta):
        """Meta class for CustomUserUpdateForm."""

    def clean_username(self):
        """Allow the current user to keep their username."""
        return self.cleaned_data['username']
