from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import VaultItemAPIView

from .views import LoginAPIView, LogoutAPIView, TestView

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('test/', TestView.as_view(), name='test'),
    path('api/vault_item/', VaultItemAPIView.as_view(), name='vault_item'), path(
        'api/vault_item/<uuid:uuid>/', VaultItemAPIView.as_view(), name='vault_item_uuid'),
]

urlpatterns.extend(router.urls)
