from django.urls import path
from .views import RegisterUserView, ObtainAuthTokenView, CookieTokenRefreshView

urlpatterns = [
    path('register', RegisterUserView.as_view(), name='register_user'),
    path('login', ObtainAuthTokenView.as_view(), name='obtain_access_token'),
    path('refresh', CookieTokenRefreshView.as_view(), name='refresh_access_token'),
]