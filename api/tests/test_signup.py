from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from api.models import UserKey


class TestSignupAPIView(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.user_data = {
            'email': 'bob@example.com',
            'password': 'super-password',
            'encrypted_symmetric_key': 'aV7XEg4EaWIivTcS76QcXPg7qD/'
                                       'Kox7MdAU44pQwKrfPKqb2Yl5/7CcAzC7dqQf9PyelHwM0oSeY52T7'
        }

    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, 201)
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 1)
        user_keys = UserKey.objects.filter(user=users[0])
        self.assertEqual(len(user_keys), 1)
        user_key = user_keys[0]
        self.assertEqual(user_key.encrypted_symmetric_key,
                         self.user_data['encrypted_symmetric_key'])

    def test_signed_up_user_can_log_in(self):
        self.client.post(self.signup_url, self.user_data)
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 200)

    def test_signup_email_already_exists(self):
        self.client.post(self.signup_url, self.user_data)
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('user with this email already exists.', response.data['email'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 1)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 1)

    def test_signup_email_missing(self):
        response = self.client.post(self.signup_url, {
            'password': self.user_data['password'],
            'encrypted_symmetric_key': self.user_data['encrypted_symmetric_key']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['email'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 0)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 0)

    def test_signup_password_missing(self):
        response = self.client.post(self.signup_url, {
            'email': self.user_data['email'],
            'encrypted_symmetric_key': self.user_data['encrypted_symmetric_key']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['password'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 0)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 0)

    def test_signup_encrypted_symmetric_key_missing(self):
        response = self.client.post(self.signup_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['encrypted_symmetric_key'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 0)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 0)

    def test_signup_email_invalid(self):
        response = self.client.post(self.signup_url, {
            'email': 'bob',
            'password': self.user_data['password'],
            'encrypted_symmetric_key': self.user_data['encrypted_symmetric_key']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Enter a valid email address.', response.data['email'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 0)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 0)

    def test_signup_email_blank(self):
        response = self.client.post(self.signup_url, {
            'email': '',
            'password': self.user_data['password'],
            'encrypted_symmetric_key': self.user_data['encrypted_symmetric_key']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.', response.data['email'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 0)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 0)

    def test_signup_password_blank(self):
        response = self.client.post(self.signup_url, {
            'email': self.user_data['email'],
            'password': '',
            'encrypted_symmetric_key': self.user_data['encrypted_symmetric_key']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.', response.data['password'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 0)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 0)

    def test_signup_encrypted_symmetric_key_blank(self):
        response = self.client.post(self.signup_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'encrypted_symmetric_key': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.', response.data['encrypted_symmetric_key'])
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 0)
        user_keys = UserKey.objects.all()
        self.assertEqual(len(user_keys), 0)
