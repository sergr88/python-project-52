"""Tests for task CRUD operations."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import Task


class TaskReadTest(TestCase):
    """Tests for task list page (Read)."""

    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        """Set up test data for task list."""
        self.url = reverse('tasks')
        self.user = User.objects.get(username='johndoe')

    def test_task_list_page_loads(self):
        """Test that the task list page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_list_contains_all_tasks(self):
        """Test that the task list page displays all tasks."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertContains(response, 'Test task')

    def test_task_list_context(self):
        """Test that the task list context contains all tasks."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 1)

    def test_task_list_unavailable_for_unauthenticated_users(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))


class TaskCreateTest(TestCase):
    """Tests for task creation (Create)."""

    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        """Set up test data for task creation."""
        self.url = reverse('task_create')
        self.valid_data = {
            'name': 'New task',
            'description': 'New task description',
            'status': 100,
            'executor': 101,
        }

    def test_create_page_loads(self):
        """Test that the create page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_creation(self):
        """Test that valid data creates a task and redirects."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('tasks'))
        task = Task.objects.get(name='New task')
        self.assertEqual(task.author.username, 'johndoe')

    def test_creation_with_missing_name(self):
        """Test that empty form submission does not create a task."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_creation_with_existing_name(self):
        """Test that duplicate name prevents creation."""
        self.client.login(username='johndoe', password='testpass123')
        self.client.post(self.url, self.valid_data)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Task.objects.filter(name='New task').count(),
            1,
        )

    def test_create_by_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(Task.objects.filter(name='New task').exists())


class TaskUpdateTest(TestCase):
    """Tests for task update (Update)."""

    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        """Set up test data for task update."""
        self.task = Task.objects.get(name='Test task')
        self.url = reverse('task_update', kwargs={'pk': self.task.pk})
        self.update_data = {
            'name': 'Updated task',
            'description': 'Updated description',
            'status': 100,
            'executor': 101,
        }

    def test_update_page_loads(self):
        """Test that the update page returns 200 for authenticated user."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_update(self):
        """Test that valid data updates the task and redirects."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated task')

    def test_update_by_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('login'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Test task')


class TaskDeleteTest(TestCase):
    """Tests for task deletion (Delete)."""

    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        """Set up test data for task deletion."""
        self.task = Task.objects.get(name='Test task')
        self.url = reverse('task_delete', kwargs={'pk': self.task.pk})

    def test_delete_page_loads(self):
        """Test that the delete page returns 200 for the author."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_delete(self):
        """Test that the author can delete a task."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(name='Test task').exists())

    def test_delete_by_non_author(self):
        """Test that a non-author cannot delete a task."""
        self.client.login(username='janedoe', password='testpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(name='Test task').exists())

    def test_delete_by_unauthenticated_user(self):
        """Test that unauthenticated users cannot delete tasks."""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Task.objects.filter(name='Test task').exists())
