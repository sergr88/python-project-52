"""Tests for label CRUD operations."""

from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class LabelReadTest(TestCase):
    """Tests for label list page (Read)."""

    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        """Set up test data for label list."""
        self.url = reverse('labels')

    def test_label_list_page_loads(self):
        """Test that the label list page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_label_list_contains_all_labels(self):
        """Test that the label list page displays all labels."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertContains(response, 'Bug')
        self.assertContains(response, 'Feature')

    def test_label_list_context(self):
        """Test that the label list context contains all labels."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        labels = response.context['labels']
        self.assertEqual(labels.count(), 2)

    def test_label_list_unavailable_for_unauthenticated_users(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))


class LabelCreateTest(TestCase):
    """Tests for label creation (Create)."""

    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        """Set up test data for label creation."""
        self.url = reverse('label_create')
        self.valid_data = {'name': 'Urgent'}

    def test_create_page_loads(self):
        """Test that the create page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_creation(self):
        """Test that valid data creates a label and redirects."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='Urgent').exists())

    def test_creation_with_missing_name(self):
        """Test that empty form submission does not create a label."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 2)

    def test_creation_with_existing_name(self):
        """Test that duplicate name prevents creation."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, {'name': 'Bug'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.filter(name='Bug').count(), 1)

    def test_create_by_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(Label.objects.filter(name='Urgent').exists())


class LabelUpdateTest(TestCase):
    """Tests for label update (Update)."""

    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        """Set up test data for label update."""
        self.label = Label.objects.get(name='Bug')
        self.url = reverse('label_update', kwargs={'pk': self.label.pk})
        self.update_data = {'name': 'Critical'}

    def test_update_page_loads(self):
        """Test that the update page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_update(self):
        """Test that valid data updates the label and redirects."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Critical')

    def test_update_with_existing_name(self):
        """Test that updating to an existing name fails."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, {'name': 'Feature'})
        self.assertEqual(response.status_code, 200)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Bug')

    def test_update_by_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('login'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Bug')


class LabelDeleteTest(TestCase):
    """Tests for label deletion (Delete)."""

    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        """Set up test data for label deletion."""
        self.label = Label.objects.get(name='Bug')
        self.url = reverse('label_delete', kwargs={'pk': self.label.pk})

    def test_delete_page_loads(self):
        """Test that the delete page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_delete(self):
        """Test that an authenticated user can delete an unlinked label."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(name='Bug').exists())

    def test_cannot_delete_label_linked_to_task(self):
        """Test that a label linked to a task cannot be deleted."""
        self.client.login(username='johndoe', password='testpass123')
        task = Task.objects.get(pk=100)
        task.labels.add(self.label)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='Bug').exists())

    def test_delete_by_unauthenticated_user(self):
        """Test that unauthenticated users cannot delete labels."""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Label.objects.filter(name='Bug').exists())
