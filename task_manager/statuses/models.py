"""Status model for task statuses."""

from django.db import models
from django.utils.translation import gettext, gettext_noop
from django.utils.translation import gettext_lazy as _

# Mark default status names for translation extraction.
# These are stored in the database in English and translated at display time.
gettext_noop('New')
gettext_noop('In progress')
gettext_noop('Testing')
gettext_noop('Done')


class Status(models.Model):
    """Task status model."""

    name = models.CharField(max_length=150, unique=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for Status model."""

        verbose_name = _('Task status')

    def __str__(self):
        """Return the translated status name."""
        return gettext(self.name)
