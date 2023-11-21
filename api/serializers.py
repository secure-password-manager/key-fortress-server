from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.serializers import Serializer, ModelSerializer, CharField, EmailField, \
    SlugRelatedField

from api.models import UserKey, VaultItem, VaultCollection


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

        try:
            user_key = UserKey.objects.get(user=user)
        except ObjectDoesNotExist:
            raise PermissionDenied("User's symmetric key not found")

        data['user'] = user
        serializer = UserKeySerializer(user_key)
        data['user_key'] = serializer.data

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


class UserKeySerializer(ModelSerializer):
    class Meta:
        model = UserKey
        fields = ['encrypted_symmetric_key', 'created_at', 'modified_at']


class VaultItemSerializer(ModelSerializer):
    # This automatically looks up related VaultCollections when both serializing and deserializing
    # JSON payloads would use 'vault_collection' for the uuid field, not 'vault_collection_uuid'
    vault_collection = SlugRelatedField(
        slug_field='uuid', queryset=VaultCollection.objects.all())

    class Meta:
        model = VaultItem
        fields = ['encrypted_data', 'uuid',
                  'vault_collection', 'created_at', 'modified_at']

        # Means that these fields are not expected on write requests but are returned on reads
        read_only_fields = ['created_at', 'modified_at']


class VaultCollectionSerializer(ModelSerializer):
    class Meta:
        model = VaultCollection
        fields = ['name', 'uuid']

    def save(self, **kwargs):
        self.validated_data['user_id'] = self.context['request'].user.id
        return super().save()
