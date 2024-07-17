from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTests(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'name': 'Test User',
            'password': 'testpassword',
            'designation': 'employee',
        }
        User.objects.create_user(**self.user_data)

    def test_registration(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect after registration

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': self.user_data['email'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after login
        self.assertIn('_auth_user_id', self.client.session)  # Check if user is authenticated

    def test_logout(self):
        self.client.login(username=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Check for redirect after logout
        self.assertNotIn('_auth_user_id', self.client.session)  # Check if user is logged out

    def test_access_control(self):
        # Example: Access profile page
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Check if unauthorized user is redirected to login

        self.client.login(username=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Check if authorized user can access profile

    # Add more tests for specific scenarios as needed

