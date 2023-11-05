from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from api.models import VaultCollection, VaultItem


class TestCreateVaultItemAPIView(APITestCase):

    def setUp(self):
        self.vault_item_url = reverse('vault_item')

        self.user_data1 = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user1 = get_user_model().objects.create_user(**self.user_data1)
        self.vault_collection1 = VaultCollection.objects.create(
            name='folder1', user_id=self.user1.id)

        self.user_data2 = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.user2 = get_user_model().objects.create_user(**self.user_data2)
        self.vault_collection2 = VaultCollection.objects.create(
            name='folder2', user_id=self.user2.id)

    def test_vault_item_create_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': self.vault_collection1.uuid
        })

        self.assertEqual(response.status_code, 200)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 1)
        self.assertIn(str(vault_item.first().uuid), response.data)

    def test_vault_item_create_vault_collection_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'vault_collection_uuid': self.vault_collection1.uuid
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {})
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection_uuid': self.vault_collection1.uuid
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': ''
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection_uuid': ''
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'
        })
        self.assertEqual(response.status_code, 404)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_uuid_invalid(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': 'BADUUID!-69c9-44ed-ae4e-522150fcd840'
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': self.vault_collection2.uuid
        })
        self.assertEqual(response.status_code, 404)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection2.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_user_not_authenticated(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': self.vault_collection1.uuid
        })
        self.assertEqual(response.status_code, 403)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection1.id)
        self.assertEqual(len(vault_item), 0)


class TestGetVaultItemAPIView(APITestCase):

    def setUp(self):
        self.vault_items_url = reverse('vault_items')

        self.user_data1 = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user1 = get_user_model().objects.create_user(**self.user_data1)
        self.vault_collection1 = VaultCollection.objects.create(
            name='folder1', user_id=self.user1.id)
        self.vault_item1 = VaultItem.objects.create(
            encrypted_data='encrypted data 1', vault_collection_id=self.vault_collection1.id)
        self.vault_item2 = VaultItem.objects.create(
            encrypted_data='encrypted data 2', vault_collection_id=self.vault_collection1.id)

        self.user_data2 = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.user2 = get_user_model().objects.create_user(**self.user_data2)
        self.vault_collection2 = VaultCollection.objects.create(
            name='folder2', user_id=self.user2.id)
        self.vault_item3 = VaultItem.objects.create(
            encrypted_data='encrypted data 3', vault_collection_id=self.vault_collection2.id)

        self.user_data3 = {
            'email': 'pippa3@gmail.com',
            'password': 'super-password'
        }
        self.user3 = get_user_model().objects.create_user(**self.user_data3)
        self.vault_collection3 = VaultCollection.objects.create(
            name='folder3', user_id=self.user3.id)

    def test_vault_items_get_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.get(self.vault_items_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(str(self.vault_item1.uuid), response.data)
        self.assertIn(str(self.vault_item2.uuid), response.data)
        self.client.login(email='pippa2@gmail.com', password='super-password')
        response = self.client.get(self.vault_items_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(str(self.vault_item3.uuid), response.data)

    def test_vault_items_get_no_vault_items(self):
        self.client.login(email='pippa3@gmail.com', password='super-password')
        response = self.client.get(self.vault_items_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_vault_items_get_user_not_authenticated(self):
        self.client.login(email='pippa3@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.get(self.vault_items_url)
        self.assertEqual(response.status_code, 403)
