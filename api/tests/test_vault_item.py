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

    def test_vault_item_create_user_not_logged_in(self):
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


class TestUpdateVaultItemAPIView(APITestCase):

    def setUp(self):
        self.vault_item_url = reverse('vault_item')

        self.user_data1 = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user1 = get_user_model().objects.create_user(**self.user_data1)
        self.vault_collection1 = VaultCollection.objects.create(
            name='folder1', user_id=self.user1.id)
        self.encrypted_data1 = 'encrypted data 1'
        self.vault_item1 = VaultItem.objects.create(
            encrypted_data=self.encrypted_data1, vault_collection_id=self.vault_collection1.id)

        self.user_data2 = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.user2 = get_user_model().objects.create_user(**self.user_data2)
        self.vault_collection2 = VaultCollection.objects.create(
            name='folder2', user_id=self.user2.id)
        self.encrypted_data2 = 'encrypted data 2'
        self.vault_item2 = VaultItem.objects.create(
            encrypted_data=self.encrypted_data2, vault_collection_id=self.vault_collection2.id)

    def test_vault_item_update_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        updated_data = 'encrypted data 1 update'
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': updated_data,
            'uuid': self.vault_item1.uuid
        })
        vault_item = VaultItem.objects.filter(
            id=self.vault_item1.id)
        uuid = str(vault_item.first().uuid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(uuid, response.data)
        self.assertEqual(
            response.data[uuid]['encrypted_data'], updated_data)

    def test_vault_item_update_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': 'encrypted data 1 update',
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_encrypted_data_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'uuid': self.vault_item1.uuid
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_encrypted_data_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {})
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_encrypted_data_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': '',
            'uuid': self.vault_item1.uuid
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'uuid': ''
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_encrypted_data__uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': '',
            'uuid': ''
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_vault_item_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_uuid_invalid(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'uuid': 'BADUUID!-69c9-44ed-ae4e-522150fcd840'
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)

    def test_vault_item_update_vault_item_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'uuid': self.vault_item2.uuid
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item2.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data2)

    def test_vault_item_update_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.put(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'uuid': self.vault_item1.uuid
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data1)


class TestDeleteVaultItemAPIView(APITestCase):

    def setUp(self):
        self.user_data1 = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user1 = get_user_model().objects.create_user(**self.user_data1)
        self.vault_collection1 = VaultCollection.objects.create(
            name='folder1', user_id=self.user1.id)
        self.encrypted_data1 = 'encrypted data 1'
        self.vault_item1 = VaultItem.objects.create(
            encrypted_data=self.encrypted_data1, vault_collection_id=self.vault_collection1.id)
        self.vault_item_url1 = reverse('vault_item_uuid', kwargs={
            'uuid': self.vault_item1.uuid})

        self.user_data2 = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.user2 = get_user_model().objects.create_user(**self.user_data2)
        self.vault_collection2 = VaultCollection.objects.create(
            name='folder2', user_id=self.user2.id)
        self.encrypted_data2 = 'encrypted data 2'
        self.vault_item2 = VaultItem.objects.create(
            encrypted_data=self.encrypted_data2, vault_collection_id=self.vault_collection2.id)
        self.vault_item_url2 = reverse('vault_item_uuid', kwargs={
            'uuid': self.vault_item2.uuid})

    def test_vault_item_delete_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.delete(self.vault_item_url1)
        vault_item = VaultItem.objects.filter(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(vault_item), 0)
        self.assertIn(str(self.vault_item1.uuid), response.data)

    def test_vault_item_delete_vault_item_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_item_url = reverse('vault_item_uuid', kwargs={
            'uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'})
        response = self.client.delete(vault_item_url)
        vault_item = VaultItem.objects.filter(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(vault_item), 1)

    def test_vault_item_delete_vault_item_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.delete(self.vault_item_url2)
        vault_item = VaultItem.objects.filter(
            id=self.vault_item2.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(vault_item), 1)

    def test_vault_item_delete_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.delete(self.vault_item_url1)
        vault_item = VaultItem.objects.filter(
            id=self.vault_item1.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(vault_item), 1)
