from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from rest_framework.test import APITestCase


class TestLogoutAPIView(APITestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'email': 'marion@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_logout_success(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(self.client.cookies['sessionid'].value), 0)
        csrf_token = self.client.cookies['csrftoken'].value
        response = self.client.post(self.logout_url, headers={'X-CSRFToken': csrf_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('', self.client.cookies['sessionid'].value)

    def test_logout_failure_not_logged_in(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Authentication credentials were not provided', response.data['detail'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_logout_failure_no_csrf_token(self):
        self.client.post(self.login_url, self.user_data)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('CSRF Failed', response.data['detail'])
