from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView

urlpatterns = [
    path('register', RegisterUserView.as_view(), name='register_user'),
    path('login', TokenObtainPairView.as_view(), name='login_with_token'),
    path('refresh', TokenRefreshView.as_view(), name='refresh_token'),
]