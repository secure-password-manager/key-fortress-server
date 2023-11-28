from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from api.models import VaultCollection, VaultItem


class TestCreateVaultItemViewSet(APITestCase):

    def setUp(self):
        self.vault_item_url = reverse('vault_item-list')

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
            'vault_collection': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 201)
        vault_item = VaultItem.objects.get(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(str(vault_item.uuid), response.data['uuid'])
        self.assertIn('vault_collection_name', response.data)
        self.assertEqual(response.data['vault_collection_name'], self.vault_collection.name)
        self.assertEqual(vault_item.vault_collection, self.vault_collection)

    def test_vault_item_create_vault_collection_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.',
                      response.data['vault_collection'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'vault_collection': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.',
                      response.data['encrypted_data'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.',
                      response.data['vault_collection'])
        self.assertIn('This field is required.',
                      response.data['encrypted_data'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.',
                      response.data['encrypted_data'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be null.',
                      response.data['vault_collection'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_encrypted_data_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be null.',
                      response.data['vault_collection'])
        self.assertIn('This field may not be blank.',
                      response.data['encrypted_data'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection': '29dabaa2-69c9-44ed-ae4e-522150fcd840'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Object with uuid=29dabaa2-69c9-44ed-ae4e-522150fcd840 does not exist.',
                      response.data['vault_collection'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_uuid_invalid(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection': 'BADUUID!-69c9-44ed-ae4e-522150fcd840'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('“BADUUID!-69c9-44ed-ae4e-522150fcd840” is not a valid UUID.',
                      response.data['vault_collection'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_vault_collection_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection': self.other_user_vc.uuid
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('User does not own VaultCollection',
                      response.data['detail'])
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.other_user_vc.id)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_create_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.post(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 403)
        vault_item = VaultItem.objects.filter(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(len(vault_item), 0)


class TestUpdateVaultItemViewSet(APITestCase):

    def setUp(self):
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
        self.vault_item_url = reverse('vault_item-detail', kwargs={
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
        self.other_user_vault_item_url = reverse('vault_item-detail', kwargs={
            'uuid': self.other_user_vi.uuid})

    def test_vault_item_update_encrypted_data_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        updated_encrypted_data = 'updated encrypted data'
        response = self.client.patch(self.vault_item_url, {
            'encrypted_data': updated_encrypted_data,
        })
        self.assertEqual(response.status_code, 200)
        vault_item = VaultItem.objects.get(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(str(vault_item.uuid), response.data['uuid'])
        self.assertEqual(
            response.data['encrypted_data'], updated_encrypted_data)
        self.assertEqual(self.vault_collection.uuid,
                         response.data['vault_collection'])

    def test_vault_item_update_vault_collection_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vc = VaultCollection.objects.create(
            name='collection', user_id=self.user.id)
        response = self.client.patch(self.vault_item_url, {
            'vault_collection': vc.uuid
        })
        vault_item = VaultItem.objects.get(id=self.vault_item.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(vault_item.uuid), response.data['uuid'])
        self.assertEqual(
            response.data['encrypted_data'], self.encrypted_data)
        self.assertEqual(vault_item.vault_collection, vc)

    def test_vault_item_update_encrypted_data_vault_collection_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vc = VaultCollection.objects.create(
            name='collection', user_id=self.user.id)
        updated_encrypted_data = 'UPDATED'
        response = self.client.patch(self.vault_item_url, {
            'encrypted_data': updated_encrypted_data,
            'vault_collection': vc.uuid
        })
        vault_item = VaultItem.objects.get(id=self.vault_item.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['encrypted_data'], updated_encrypted_data)
        self.assertEqual(vault_item.vault_collection, vc)

    def test_vault_item_update_encrypted_data_uuid_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.patch(self.vault_item_url, {})
        vault_item = VaultItem.objects.get(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(vault_item.encrypted_data, self.encrypted_data)
        self.assertEqual(vault_item.vault_collection,
                         self.vault_collection)

    def test_vault_item_update_encrypted_data_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.patch(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.',
                      response.data['encrypted_data'])
        vault_item = VaultItem.objects.get(
            id=self.vault_item.id)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)
        self.assertEqual(vault_item.vault_collection, self.vault_collection)

    def test_vault_item_update_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.patch(self.vault_item_url, {
            'encrypted_data': 'encrypted data',
            'vault_collection': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be null.',
                      response.data['vault_collection'])
        vault_item = VaultItem.objects.get(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)
        self.assertEqual(vault_item.vault_collection, self.vault_collection)

    def test_vault_item_update_encrypted_data_vault_collection_uuid_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.patch(self.vault_item_url, {
            'encrypted_data': '',
            'vault_collection': ''
        })
        self.assertEqual(response.status_code, 400)
        vault_item = VaultItem.objects.get(
            vault_collection_id=self.vault_collection.id)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)
        self.assertEqual(vault_item.vault_collection, self.vault_collection)

    def test_vault_item_update_vault_item_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_item_url = reverse('vault_item-detail', kwargs={
            'uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'})
        response = self.client.patch(vault_item_url, {
            'encrypted_data': 'encrypted data update',
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', response.data['detail'])

    def test_vault_item_update_invalid_uuid(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_item_url = reverse('vault_item-detail', kwargs={
            'uuid': 'BADUUID!-69c9-44ed-ae4e-522150fcd840'})
        updated_encrypted_data = 'encrypted data update'
        response = self.client.patch(vault_item_url, {
            'encrypted_data': updated_encrypted_data,
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', response.data['detail'])

    def test_vault_item_update_vault_item_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.patch(self.other_user_vault_item_url, {
            'encrypted_data': 'update other user vault item',
            'vault_collection': self.vault_collection.uuid
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', response.data['detail'])
        vault_item = VaultItem.objects.get(
            id=self.other_user_vi.id)
        self.assertEqual(
            vault_item.encrypted_data, self.other_user_encrypted_data)
        self.assertEqual(vault_item.vault_collection, self.other_user_vc)

    def test_vault_item_update_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.patch(self.vault_item_url, {
            'encrypted_data': 'encrypted data update',
        })
        vault_item = VaultItem.objects.get(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            vault_item.encrypted_data, self.encrypted_data)
        self.assertEqual(vault_item.vault_collection, self.vault_collection)


class TestGetVaultItemViewSet(APITestCase):

    def setUp(self):
        self.vault_items_url = reverse('vault_item-list')

        self.user_data = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.vault_collection = VaultCollection.objects.create(
            name='folder1', user_id=self.user.id)
        self.vault_item1 = VaultItem.objects.create(
            encrypted_data='encrypted data 1', vault_collection_id=self.vault_collection.id)
        self.vault_item2 = VaultItem.objects.create(
            encrypted_data='encrypted data 2', vault_collection_id=self.vault_collection.id)

        self.other_user_data = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.other_user = get_user_model().objects.create_user(**self.other_user_data)
        self.other_user_vc = VaultCollection.objects.create(
            name='folder2', user_id=self.other_user.id)
        self.vault_item3 = VaultItem.objects.create(
            encrypted_data='encrypted data 3', vault_collection_id=self.other_user_vc.id)

        self.no_vi_user_data = {
            'email': 'pippa3@gmail.com',
            'password': 'super-password'
        }
        self.no_vi_user = get_user_model().objects.create_user(**self.no_vi_user_data)
        self.no_vi_vault_collection = VaultCollection.objects.create(
            name='folder3', user_id=self.no_vi_user.id)

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
        self.client.login(email='pippa3@gmail.com', password='super-password')
        response = self.client.get(self.vault_items_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_vault_items_get_user_not_authenticated(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.get(self.vault_items_url)
        self.assertEqual(response.status_code, 403)


class TestDeleteVaultItemViewSet(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.vault_collection = VaultCollection.objects.create(
            name='folder1', user_id=self.user.id)
        self.vault_item = VaultItem.objects.create(
            encrypted_data='encrypted data', vault_collection_id=self.vault_collection.id)
        self.vault_item_url = reverse('vault_item-detail', kwargs={
            'uuid': self.vault_item.uuid})

        self.other_user_data = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.other_user = get_user_model().objects.create_user(**self.other_user_data)
        self.other_user_vc = VaultCollection.objects.create(
            name='folder2', user_id=self.other_user.id)
        self.other_user_vi = VaultItem.objects.create(
            encrypted_data='encrypted data other user', vault_collection_id=self.other_user_vc.id)
        self.other_user_vault_item_url = reverse('vault_item-detail', kwargs={
            'uuid': self.other_user_vi.uuid})

    def test_vault_item_delete_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.delete(self.vault_item_url)
        vault_item = VaultItem.objects.filter(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(vault_item), 0)

    def test_vault_item_delete_vault_item_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_item_url = reverse('vault_item-detail', kwargs={
            'uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'})
        response = self.client.delete(vault_item_url)
        vault_item = VaultItem.objects.filter(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(vault_item), 1)

    def test_vault_item_delete_uuid_invalid(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_item_url = reverse('vault_item-detail', kwargs={
            'uuid': 'BADUUID!-69c9-44ed-ae4e-522150fcd840'})
        response = self.client.delete(vault_item_url)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', response.data['detail'])

    def test_vault_item_delete_vault_item_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.delete(self.other_user_vault_item_url)
        vault_item = VaultItem.objects.get(
            id=self.other_user_vi.id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(vault_item.vault_collection.user, self.other_user)

    def test_vault_item_delete_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.delete(self.vault_item_url)
        vault_item = VaultItem.objects.filter(
            id=self.vault_item.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(vault_item), 1)
