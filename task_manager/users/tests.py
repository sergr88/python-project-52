"""Tests for user CRUD operations."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCreateTest(TestCase):
    """Tests for user registration (Create)."""

    fixtures = ['users.json']

    def setUp(self):
        """Set up test data for user creation."""
        self.url = reverse('user_create')
        self.valid_data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

    def test_registration_page_loads(self):
        """Test that the registration page returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        """Test that valid data creates a user and redirects to login."""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')

    def test_registration_with_missing_fields(self):
        """Test that empty form submission does not create a user."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)

    def test_registration_with_password_mismatch(self):
        """Test that mismatched passwords prevent registration."""
        data = self.valid_data.copy()
        data['password2'] = 'wrongpass'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_registration_with_existing_username(self):
        """Test that duplicate username prevents registration."""
        data = self.valid_data.copy()
        data['username'] = 'johndoe'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='johndoe').count(), 1)


class UserUpdateTest(TestCase):
    """Tests for user update (Update)."""

    fixtures = ['users.json']

    def setUp(self):
        """Set up test data for user update."""
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('user_update', kwargs={'pk': self.user.pk})
        self.update_data = {
            'first_name': 'Johnny',
            'last_name': 'Updated',
            'username': 'johndoe',
            'password1': 'newpass123',
            'password2': 'newpass123',
        }

    def test_update_page_loads_for_owner(self):
        """Test that the update page returns 200 for the profile owner."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_update(self):
        """Test that valid data updates the user and redirects."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Johnny')
        self.assertEqual(self.user.last_name, 'Updated')

    def test_update_username(self):
        """Test that the username can be changed successfully."""
        self.client.login(username='johndoe', password='testpass123')
        data = self.update_data.copy()
        data['username'] = 'john_updated'
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'john_updated')

    def test_update_by_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))

    def test_update_other_user_forbidden(self):
        """Test that GET to another user's update page is forbidden."""
        self.client.login(username='janedoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('users'))

    def test_update_other_user_post_forbidden(self):
        """Test that POST to another user's update page is forbidden."""
        self.client.login(username='janedoe', password='testpass123')
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, reverse('users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')


class UserDeleteTest(TestCase):
    """Tests for user deletion (Delete)."""

    fixtures = ['users.json']

    def setUp(self):
        """Set up test data for user deletion."""
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('user_delete', kwargs={'pk': self.user.pk})

    def test_delete_page_loads_for_owner(self):
        """Test that the delete page returns 200 for the profile owner."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_delete(self):
        """Test that the owner can delete their account."""
        self.client.login(username='johndoe', password='testpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('users'))
        self.assertFalse(User.objects.filter(username='johndoe').exists())

    def test_delete_by_unauthenticated_user(self):
        """Test that unauthenticated users cannot delete accounts."""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='johndoe').exists())

    def test_delete_other_user_forbidden(self):
        """Test that users cannot delete other users' accounts."""
        self.client.login(username='janedoe', password='testpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('users'))
        self.assertTrue(User.objects.filter(username='johndoe').exists())
