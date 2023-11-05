from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from rest_framework.serializers import Serializer, ModelSerializer, CharField, EmailField, UUIDField

from api.models import User, VaultItem, VaultCollection


class UUIDSerializer(Serializer):
    uuid = UUIDField(required=True)


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


class VaultItemSerializer(ModelSerializer):
    class Meta:
        model = VaultItem
        fields = '__all__'


class CreateVaultItemSerializer(Serializer):
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


class UpdateVaultItemSerializer(ModelSerializer):
    uuid = UUIDField(required=True)
    encrypted_data = CharField(required=True)

    class Meta:
        model = VaultItem
        fields = ['uuid', 'encrypted_data']

    def update(self, instance, validated_data):
        instance.encrypted_data = validated_data['encrypted_data']
        instance.save()
        return instance

    def validate(self, data):
        user = get_object_or_404(User, pk=self.context['request'].user.id)
        vault_item = get_object_or_404(VaultItem, uuid=data.get('uuid'))

        if vault_item.vault_collection.user != user:
            raise NotFound()

        return {
            'id': vault_item.id,
            'encrypted_data': data.get('encrypted_data'),
            'vault_collection_id': vault_item.vault_collection_id
        }


class DeleteVaultItemSerializer(Serializer):
    uuid = UUIDField(required=True)

    def delete(self, validated_data):
        vault_item = get_object_or_404(VaultItem, pk=validated_data.get('id'))
        vault_item.delete()

    def validate(self, data):
        user = get_object_or_404(User, pk=self.context['request'].user.id)
        vault_item = get_object_or_404(VaultItem, uuid=data.get('uuid'))

        if vault_item.vault_collection.user != user:
            raise NotFound()

        return {'id': vault_item.id}
