from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import CharField, EmailField, ModelSerializer, Serializer, UUIDField

from api.models import UserKey, VaultItem, VaultCollection


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


class SignupSerializer(ModelSerializer):
    encrypted_symmetric_key = CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'encrypted_symmetric_key']

    def save(self):
        user = get_user_model().objects.create_user(email=self.validated_data['email'],
                                                    password=self.validated_data['password'])
        UserKey.objects.create(
            user=user,
            encrypted_symmetric_key=self.validated_data['encrypted_symmetric_key']
        )
        return user


class VaultItemSerializer(ModelSerializer):
    class Meta:
        model = VaultItem
        fields = '__all__'
