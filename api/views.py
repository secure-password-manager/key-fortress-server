from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import LoginSerializer, SignupSerializer, UserKeySerializer, \
    VaultCollectionSerializer, VaultItemSerializer
from .throttling import SignupAnonRateThrottle

from api.models import UserKey, VaultItem, VaultCollection


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        payload = serializer.validated_data['user_key']

        return Response(data=payload, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class SignupAPIView(CreateAPIView):
    throttle_classes = [SignupAnonRateThrottle]
    authentication_classes = []
    permission_classes = [AllowAny]

    model = get_user_model()
    serializer_class = SignupSerializer


class UserKeyAPIView(APIView):

    def get(self, request):
        try:
            user_key = UserKey.objects.get(user=request.user.id)
        except ObjectDoesNotExist:
            raise PermissionDenied("User's symmetric key not found")

        serializer = UserKeySerializer(user_key)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


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
            raise NotFound(
                detail='User does not own VaultCollection')

    def perform_create(self, serializer):
        self.validate_vault_collection(serializer)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        self.validate_vault_collection(serializer)
        super().perform_create(serializer)

    # Formats the output of list GET requests as a dict instead of a list
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({item['uuid']: item for item in serializer.data})


class VaultCollectionViewSet(ModelViewSet):
    # setting this as serializer_class when allow the serializer
    # to be called for every API request
    serializer_class = VaultCollectionSerializer
    # Overridden by get_queryset() but still required
    queryset = VaultCollection.objects.prefetch_related('vault_items').all()
    lookup_field = 'uuid'  # VaultCollections are looked up by uuid rather than pk

    # Overrides the ViewSet queryset attribute to ensure users can only access their own VaultItems
    # Results in a 404 if a user tries to list, retrieve, put, or delete a VaultItem they don't own

    def get_queryset(self):
        queryset = super(VaultCollectionViewSet, self).get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(context={'request': self.request})
