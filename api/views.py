from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import LoginSerializer, VaultItemSerializer
from api.models import VaultItem, VaultCollection


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class TestView(APIView):

    def get(self, request):  # noqa
        return Response(data={'detail': 'Congratulations! You are an authenticated user!'},
                        status=status.HTTP_200_OK)


class VaultItemViewSet(ModelViewSet):
    # setting this as serializer_class when allow the serializer
    # to be called for every API request
    serializer_class = VaultItemSerializer
    # Overridden by get_queryset() but still required
    queryset = VaultItem.objects.all()
    lookup_field = 'uuid'  # VaultItems are looked up by uuid rather than pk
    # Overrides the ViewSet queryset attribute to ensure users can only access their own VaultItems
    # Results in a 404 if a user tries to list, retrieve, put, or delete a VaultItem they don't own

    def get_queryset(self):
        queryset = super(VaultItemViewSet, self).get_queryset()
        return queryset.filter(vault_collection__user_id=self.request.user.id)

    def validate_vault_collection(self, serializer):
        try:
            if 'vault_collection' in serializer.validated_data:
                VaultCollection.objects.get(user_id=self.request.user.id,
                                            uuid=serializer.validated_data['vault_collection'].uuid)
        except ObjectDoesNotExist:
            raise PermissionDenied(
                detail='User does not own VaultCollection', code=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        self.validate_vault_collection(serializer)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        self.validate_vault_collection(serializer)
        super().perform_create(serializer)

    def perform_destroy(self, instance):
        if instance.vault_collection.user != self.request.user:
            raise PermissionDenied(
                detail='User does not own VaultCollection', code=status.HTTP_403_FORBIDDEN)
        instance.delete()

    # Formats the output of list GET requests as a dict instead of a list
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({item['uuid']: item for item in serializer.data})
