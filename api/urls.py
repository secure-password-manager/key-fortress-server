from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, LogoutAPIView, SignupAPIView, VaultItemAPIView

router = DefaultRouter()

urlpatterns = [
    path('api/vault_item/', VaultItemAPIView.as_view(), name='vault_item'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
]

urlpatterns.extend(router.urls)
