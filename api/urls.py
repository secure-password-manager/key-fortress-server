from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, LogoutAPIView, TestView

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('test/', TestView.as_view(), name='test')
]

urlpatterns.extend(router.urls)
