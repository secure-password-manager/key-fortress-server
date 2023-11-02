from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase


class TestLoginAPIView(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'marion@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_login_success(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('csrftoken', response.cookies)
        self.assertIn('sessionid', response.cookies)

    def test_login_failure_user_does_not_exist(self):
        response = self.client.post(self.login_url, {
            'email': 'somedude@gmail.com',
            'password': 'super-secure-and-safe'
        })
        self.assertEqual(response.status_code, 403)
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_failure_bad_password(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': 'wrong-password'
        })
        self.assertEqual(response.status_code, 403)
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_email_missing(self):
        response = self.client.post(self.login_url, {
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['email'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_password_missing(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data['email']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['password'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_email_and_password_missing(self):
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['email'])
        self.assertIn('This field is required.', response.data['password'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_email_invalid(self):
        response = self.client.post(self.login_url, {
            'email': 'marion',
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Enter a valid email address.', response.data['email'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_email_blank(self):
        response = self.client.post(self.login_url, {
            'email': '',
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.', response.data['email'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_password_blank(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.', response.data['password'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)

    def test_login_email_and_password_blank(self):
        response = self.client.post(self.login_url, {
            'email': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.', response.data['email'])
        self.assertIn('This field may not be blank.', response.data['password'])
        self.assertNotIn('csrftoken', response.cookies)
        self.assertNotIn('sessionid', response.cookies)
