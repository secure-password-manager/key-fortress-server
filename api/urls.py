from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, LogoutAPIView, SignupAPIView, VaultItemViewSet

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
]

router.register(r'vault_items', VaultItemViewSet, basename='vault_item')
urlpatterns.extend(router.urls)
