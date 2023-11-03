from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.serializers import Serializer, CharField, EmailField, UUIDField

from api.models import VaultItem, VaultCollection


class LoginSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'),
                            email=email,
                            password=password)
        if user is None:
            raise AuthenticationFailed('Invalid email or password')

        data['user'] = user
        return data


class VaultItemSerializer(Serializer):

    encrypted_data = CharField(required=True)
    vault_collection_uuid = UUIDField(required=True)

    def create(self, validated_data):
        return VaultItem.objects.create(**validated_data)

    def validate(self, data):
        current_user = self.context['request'].user

        vault_collection = get_object_or_404(
            VaultCollection,
            user_id=current_user.id,
            uuid=data.get('vault_collection_uuid')
        )

        return {
            'encrypted_data': data.get('encrypted_data'),
            'vault_collection_id': vault_collection.id
        }