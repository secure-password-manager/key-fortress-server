from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, CreateVaultItemSerializer, DeleteVaultItemSerializer, UpdateVaultItemSerializer, UUIDSerializer, VaultItemSerializer
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

    def post(self, request):
        serializer = CreateVaultItemSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        vault_item = VaultItemSerializer(serializer.save())

        return Response(
            {str(vault_item.data['uuid']): vault_item.data},
            status=status.HTTP_200_OK)

    def put(self, request):
        uuid_serializer = UUIDSerializer(data=request.data)
        uuid_serializer.is_valid(raise_exception=True)
        vault_item = get_object_or_404(VaultItem, uuid=request.data['uuid'])
        serializer = UpdateVaultItemSerializer(
            vault_item, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serialized_vault_item = VaultItemSerializer(serializer.save())

        return Response(
            {str(serialized_vault_item.data['uuid']): serialized_vault_item.data},
            status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        uuid_serializer = UUIDSerializer(data={'uuid': uuid})
        uuid_serializer.is_valid(raise_exception=True)
        serializer = DeleteVaultItemSerializer(
            data={'uuid': uuid}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.delete(serializer.validated_data)
        return Response({str(uuid): {}}, status=status.HTTP_200_OK)
