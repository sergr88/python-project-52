"""Tests for status CRUD operations."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusReadTest(TestCase):
    """Tests for status list page (Read)."""

    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        """Set up test data for status list."""
        self.url = reverse('statuses')
        self.user = User.objects.get(username='johndoe')

    def test_status_list_page_loads(self):
        """Test that the status list page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_list_contains_all_statuses(self):
        """Test that the status list page displays all statuses."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertContains(response, 'Pending review')
        self.assertContains(response, 'Archived')

    def test_status_list_context(self):
        """Test that the status list context contains all statuses."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        statuses = response.context['statuses']
        self.assertEqual(statuses.count(), 6)

    def test_status_list_unavailable_for_unauthenticated_users(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))


class StatusCreateTest(TestCase):
    """Tests for status creation (Create)."""

    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        """Set up test data for status creation."""
        self.url = reverse('status_create')
        self.valid_data = {'name': 'Blocked'}

    def test_create_page_loads(self):
        """Test that the create page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_creation(self):
        """Test that valid data creates a status and redirects."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='Blocked').exists())

    def test_creation_with_missing_name(self):
        """Test that empty form submission does not create a status."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 6)

    def test_creation_with_existing_name(self):
        """Test that duplicate name prevents creation."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, {'name': 'Pending review'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Status.objects.filter(name='Pending review').count(),
            1,
        )

    def test_create_by_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(Status.objects.filter(name='Blocked').exists())


class StatusUpdateTest(TestCase):
    """Tests for status update (Update)."""

    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        """Set up test data for status update."""
        self.status = Status.objects.get(name='Pending review')
        self.url = reverse('status_update', kwargs={'pk': self.status.pk})
        self.update_data = {'name': 'Updated'}

    def test_update_page_loads(self):
        """Test that the update page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_update(self):
        """Test that valid data updates the status and redirects."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated')

    def test_update_with_existing_name(self):
        """Test that updating to an existing name fails."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, {'name': 'Archived'})
        self.assertEqual(response.status_code, 200)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Pending review')

    def test_update_by_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('login'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Pending review')


class StatusDeleteTest(TestCase):
    """Tests for status deletion (Delete)."""

    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        """Set up test data for status deletion."""
        self.status = Status.objects.get(name='Pending review')
        self.url = reverse('status_delete', kwargs={'pk': self.status.pk})

    def test_delete_page_loads(self):
        """Test that the delete page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_delete(self):
        """Test that an authenticated user can delete a status."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(name='Pending review').exists())

    def test_delete_by_unauthenticated_user(self):
        """Test that unauthenticated users cannot delete statuses."""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Status.objects.filter(name='Pending review').exists())
