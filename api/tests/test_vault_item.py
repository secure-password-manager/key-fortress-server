from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from api.models import VaultCollection, VaultItem


class TestCreateVaultItemAPIView(APITestCase):

    def setUp(self):
        self.vault_item_url = reverse('vault_item')

        self.user_data = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.vault_collection = VaultCollection.objects.create(
            name='folder1', user_id=self.user.id)

        self.other_user_data = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.other_user = get_user_model().objects.create_user(**self.other_user_data)
        self.other_user_vc = VaultCollection.objects.create(
            name='folder2', user_id=self.other_user.id)

    def test_vault_item_create_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': self.vault_collection.uuid
        })

        self.assertEqual(response.status_code, 200)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 1)
        self.assertIn(str(vault_item.first().uuid), response.data)

    def test_vault_item_create_vault_collection_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'vault_collection_uuid': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {})
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection_uuid': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': ''
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection_uuid': ''
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'
        })
        self.assertEqual(response.status_code, 404)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_uuid_invalid(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': 'BADUUID!-69c9-44ed-ae4e-522150fcd840'
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': self.other_user_vc.uuid
        })
        self.assertEqual(response.status_code, 404)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.other_user_vc.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection_uuid': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 403)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)


class TestUpdateVaultItemAPIView(APITestCase):

    def setUp(self):
        self.vault_item_url = reverse('vault_item')

        self.user_data = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.vault_collection = VaultCollection.objects.create(
            name='folder1', user_id=self.user.id)
        self.encrypted_data = 'encrypted data'
        self.vault_item = VaultItem.objects.create(
            encrypted_data=self.encrypted_data, vault_collection_id=self.vault_collection.id)
        self.vault_item_url = reverse('vault_item_uuid', kwargs={
            'uuid': self.vault_item.uuid})

        self.other_user_data = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.other_user = get_user_model().objects.create_user(**self.other_user_data)
        self.other_user_vc = VaultCollection.objects.create(
            name='folder2', user_id=self.other_user.id)
        self.other_user_encrypted_data = 'encrypted data other user'
        self.other_user_vi = VaultItem.objects.create(
            encrypted_data=self.other_user_encrypted_data, vault_collection_id=self.other_user_vc.id)
        self.other_user_vault_item_url = reverse('vault_item_uuid', kwargs={
            'uuid': self.other_user_vi.uuid})

    def test_vault_item_update_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        updated_data = 'encrypted data update'
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': updated_data,
        })
        vault_item = VaultItem.objects.filter(
            id=self.vault_item.id)
        uuid = str(vault_item.first().uuid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(uuid, response.data)
        self.assertEqual(
            response.data[uuid]['encrypted_data'], updated_data)

    def test_vault_item_update_encrypted_data_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {})
        vault_item = VaultItem.objects.get(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)

    def test_vault_item_update_encrypted_data_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': '',
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)

    def test_vault_item_update_vault_item_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_item_url = reverse('vault_item_uuid', kwargs={
            'uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'})
        response = self.client.put(vault_item_url, {
            'encrypted_data': 'encrypted data update',
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)

    def test_vault_item_update_vault_item_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.other_user_vault_item_url, {
            'encrypted_data': 'encrypted data update'
        })
        vault_item = VaultItem.objects.get(
            id=self.other_user_vi.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            vault_item.encrypted_data, self.other_user_encrypted_data)

    def test_vault_item_update_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': 'encrypted data update',
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)
