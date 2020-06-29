from django.urls import path, include
from .views import UserCreateAPIView, example_view, UserLoginAPIView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


urlpatterns = [
    path('login', CustomTokenObtainPairView.as_view()),
    path('refresh_token', TokenRefreshView.as_view()),
    path('register', UserCreateAPIView.as_view() ),
    path('teste', example_view)
]