from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from api.models import VaultCollection, VaultItem


class TestCreateVaultCollectionViewSet(APITestCase):

    def setUp(self):
        self.vault_collection_url = reverse('vault_collection-list')

        self.user_data = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_vault_collection_create_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')

        response = self.client.post(self.vault_collection_url, {
            'name': 'Work'
        })
        self.assertEqual(response.status_code, 201)
        vault_collection = VaultCollection.objects.filter(
            user=self.user)
        self.assertEqual(len(vault_collection), 1)
        self.assertEqual(str(vault_collection.first().uuid),
                         response.data['uuid'])

    def test_vault_collection_create_name_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_collection_url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['name'])
        vault_collection = VaultCollection.objects.filter(
            user=self.user)
        self.assertEqual(len(vault_collection), 0)

    def test_vault_collection_create_name_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_collection_url, {
            'name': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.', response.data['name'])
        vault_collection = VaultCollection.objects.filter(
            user=self.user)
        self.assertEqual(len(vault_collection), 0)

    def test_vault_collection_create_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.post(self.vault_collection_url, {
            'name': 'Work'
        })
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            'Authentication credentials were not provided.', response.data['detail'])
        vault_collection = VaultCollection.objects.filter(
            user=self.user)
        self.assertEqual(len(vault_collection), 0)
