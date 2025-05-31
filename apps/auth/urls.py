from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserView, ObtainAuthTokenView

urlpatterns = [
    path('register', RegisterUserView.as_view(), name='register_user'),
    path('login', ObtainAuthTokenView.as_view(), name='obtain_access_token'),
    path('refresh', TokenRefreshView.as_view(), name='refresh_access_token'),
]