from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from api.models import UserKey


class TestUserKeyAPIView(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.user_key_url = reverse('user_key')
        self.user_data = {
            'email': 'marion@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.user_key = UserKey.objects.create(
            user=self.user,
            encrypted_symmetric_key='somelonggobbledegookthatlookslikeitsabase64encodedstring'
        )
        self.no_key_user_data = {
            'email': 'bob@example.com',
            'password': 'nobody-can-guess-this'
        }
        self.no_key_user = get_user_model().objects.create_user(**self.no_key_user_data)

    def test_user_key_success(self):
        self.client.post(self.login_url, self.user_data)
        response = self.client.get(self.user_key_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['encrypted_symmetric_key'],
                         self.user_key.encrypted_symmetric_key)

    def test_user_key_not_found(self):
        self.client.login(**self.no_key_user_data)
        response = self.client.get(self.user_key_url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('User\'s symmetric key not found', response.data['detail'])
