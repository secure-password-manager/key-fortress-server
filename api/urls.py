from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, TestView

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('test/', TestView.as_view(), name='test')
]

urlpatterns.extend(router.urls)
