from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from api.models import VaultCollection


class TestCreateDefaultVaultCollection(APITestCase):
    def test_default_vault_collection_created(self):
        get_user_model().objects.create_user(email="bob@example.com", password="super-secret")
        all_users = get_user_model().objects.all()
        self.assertEqual(len(all_users), 1)
        bob = all_users[0]
        self.assertEqual(bob.vaultcollection_set.count(), 1)
        self.assertEqual(VaultCollection.objects.first().name, "Default")

    def test_default_vault_collection_created_signup_api(self):
        self.client.post(reverse('signup'), {
            "email": "bob@example.com",
            "password": "super-secret",
            "encrypted_symmetric_key": "as0env8as7e0r9akse098a0e98r7aev"
        })
        all_users = get_user_model().objects.all()
        self.assertEqual(len(all_users), 1)
        bob = all_users[0]
        self.assertEqual(bob.vaultcollection_set.count(), 1)
        self.assertEqual(VaultCollection.objects.first().name, "Default")
