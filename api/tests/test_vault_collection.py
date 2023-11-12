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


class TestGetVaultCollectionViewSet(APITestCase):

    def setUp(self):
        self.vault_collections_url = reverse('vault_collection-list')

    def test_vault_collections_get_success(self):
        user_data = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        user = get_user_model().objects.create_user(**user_data)

        vc = VaultCollection.objects.create(
            name='folder1', user_id=user.id)
        VaultItem.objects.create(
            encrypted_data='encrypted data 1', vault_collection_id=vc.id)
        VaultItem.objects.create(
            encrypted_data='encrypted data 2', vault_collection_id=vc.id)
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.get(self.vault_collections_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]['vault_items']), 2)

        user_data = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        user = get_user_model().objects.create_user(**user_data)
        VaultCollection.objects.create(
            name='folder1', user_id=user.id)
        VaultCollection.objects.create(
            name='folder2', user_id=user.id)
        self.client.login(email='pippa2@gmail.com', password='super-password')
        response = self.client.get(self.vault_collections_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_vault_collections_get_user_not_authenticated(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.get(self.vault_collections_url)
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            'Authentication credentials were not provided.', response.data['detail'])


class TestUpdateVaultCollectionViewSet(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'pippa1@gmail.com',
            'password': 'super-password'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.collection_name = 'folder1'
        self.vault_collection = VaultCollection.objects.create(
            name=self.collection_name, user_id=self.user.id)
        self.vault_collection_url = reverse('vault_collection-detail', kwargs={
            'uuid': self.vault_collection.uuid})

        self.other_user_data = {
            'email': 'pippa2@gmail.com',
            'password': 'super-password'
        }
        self.other_user = get_user_model().objects.create_user(**self.other_user_data)
        self.other_user_cn = 'other user folder 1'
        self.other_user_vc = VaultCollection.objects.create(
            name=self.other_user_cn, user_id=self.other_user.id)
        self.other_user_vault_collection_url = reverse('vault_collection-detail', kwargs={
            'uuid': self.other_user_vc.uuid})

    def test_vault_collection_update_success(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        updated_collection_name = 'updated folder name'
        response = self.client.put(self.vault_collection_url, {
            'name': updated_collection_name,
        })
        self.assertEqual(response.status_code, 200)
        vault_collection = VaultCollection.objects.get(
            id=self.vault_collection.id)
        self.assertEqual(str(vault_collection.uuid), response.data['uuid'])
        self.assertEqual(
            response.data['name'], updated_collection_name)
        self.assertEqual(updated_collection_name,
                         response.data['name'])

    def test_vault_collection_update_collection_name_missing(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_collection_url, {})
        vault_collection = VaultCollection.objects.get(
            id=self.vault_collection.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(vault_collection.name, self.collection_name)

    def test_vault_collection_update_collection_name_blank(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.vault_collection_url, {
            'name': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field may not be blank.',
                      response.data['name'])
        vault_collection = VaultCollection.objects.get(
            id=self.vault_collection.id)
        self.assertEqual(
            vault_collection.name, self.collection_name)

    def test_vault_collection_update_collection_not_exist(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_collection_url = reverse('vault_collection-detail', kwargs={
            'uuid': '29dabaa2-69c9-44ed-ae4e-522150fcd840'})
        response = self.client.put(vault_collection_url, {
            'name': 'updated collection name',
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', response.data['detail'])

    def test_vault_collection_update_invalid_uuid(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        vault_collection_url = reverse('vault_collection-detail', kwargs={
            'uuid': 'BADUUID!-69c9-44ed-ae4e-522150fcd840'})
        updated_collection_name = 'updatedd collection name'
        response = self.client.put(vault_collection_url, {
            'name': updated_collection_name,
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', response.data['detail'])

    def test_vault_collection_update_collection_belongs_to_other_user(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        response = self.client.put(self.other_user_vault_collection_url, {
            'name': 'update other user collection name',
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found.', response.data['detail'])
        vault_collection = VaultCollection.objects.get(
            id=self.other_user_vc.id)
        self.assertEqual(
            vault_collection.name, self.other_user_cn)
        self.assertEqual(vault_collection.user, self.other_user)

    def test_vault_collection_update_user_not_logged_in(self):
        self.client.login(email='pippa1@gmail.com', password='super-password')
        self.client.logout()
        response = self.client.put(self.vault_collection_url, {
            'name': 'updated folder name'
        })
        vault_collection = VaultCollection.objects.get(
            id=self.vault_collection.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            vault_collection.name, self.collection_name)
