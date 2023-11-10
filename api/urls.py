from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import LoginAPIView, LogoutAPIView, VaultItemViewSet, TestView

router = DefaultRouter()

urlpatterns = [
    # path('api/', include(router.urls,  namespace='api')),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('test/', TestView.as_view(), name='test'),
]

router.register(r'vault_items', VaultItemViewSet, basename='vault_item')
urlpatterns.extend(router.urls)
