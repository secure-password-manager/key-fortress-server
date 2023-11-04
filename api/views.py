from django.contrib.auth import get_user_model, login, logout

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, CreateVaultItemSerializer, SignupSerializer,\
    VaultItemSerializer


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


class SignupAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    model = get_user_model()
    serializer_class = SignupSerializer


class VaultItemAPIView(APIView):
    def post(self, request):
        serializer = CreateVaultItemSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        vault_item = VaultItemSerializer(saved)
        return Response({str(vault_item.data['uuid']): vault_item.data}, status=status.HTTP_200_OK)
