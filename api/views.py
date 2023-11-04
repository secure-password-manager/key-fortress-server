from django.contrib.auth import login, logout
from django.db.models import F

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, CreateVaultItemSerializer, GetVaultItemsSerializer, VaultItemSerializer
from api.models import VaultItem


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


class VaultItemAPIView(APIView):
    model = VaultItem

    def get(self, request):
        result = VaultItem.objects.filter(
            vault_collection__user_id=request.user.id
        ).values('uuid', 'encrypted_data', 'created_at', 'modified_at', vault_collection_uuid=F('vault_collection__uuid'),)
        serializer = GetVaultItemsSerializer(result)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateVaultItemSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        vault_item = VaultItemSerializer(saved)
        return Response(
            {str(vault_item.data['uuid']): vault_item.data},
            status=status.HTTP_200_OK)
