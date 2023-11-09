from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, VaultCollection


@receiver(post_save, sender=User)
def create_default_vault_collection(sender, instance, created, **kwargs):
    if created:
        VaultCollection.objects.create(user=instance, name="Default")
