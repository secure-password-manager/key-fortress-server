from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, LogoutAPIView, SignupAPIView, UserKeyAPIView, \
    VaultCollectionViewSet, VaultItemViewSet

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('user_key/', UserKeyAPIView.as_view(), name='user_key'),
]

router.register(r'vault_items', VaultItemViewSet, basename='vault_item')
router.register(r'vault_collections', VaultCollectionViewSet,
                basename='vault_collection')
urlpatterns.extend(router.urls)
