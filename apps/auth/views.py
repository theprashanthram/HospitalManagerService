import logging

from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers.auth_token import ObtainAuthTokenResponseSerializer, ObtainAuthTokenRequestSerializer
from .serializers.user_registration import UserRegistrationRequestSerializer, UserRegistrationResponseSerializer

logger = logging.getLogger(__name__)

class RegisterUserView(APIView):
    """
    Create a new user account.
    """
    request_serializer_class = UserRegistrationRequestSerializer
    response_serializer_class = UserRegistrationResponseSerializer

    permission_classes = (IsAdminUser,) # Registration can only be done by an admin

    @extend_schema(
        operation_id='registerNewUser',
        request=request_serializer_class,
        responses=response_serializer_class,
        description='User registration service',
    )
    def post(self, request):
        request_serializer = self.request_serializer_class(data=request.data)
        if request_serializer.is_valid():
            user = request_serializer.save()
            response_serializer = self.response_serializer_class(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenView(TokenObtainPairView):
    """
    Get Access Token (as json field) and Refresh Token (as cookie)
    """
    @extend_schema(
        operation_id='obtainAuthToken',
        request=ObtainAuthTokenRequestSerializer,
        responses=ObtainAuthTokenResponseSerializer,
        description='Obtain access token using username and password',
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            access_token = response.data.get('access')

            # Remove refresh token from response body
            response.data.pop('refresh', None)
            response.data.pop('access', None)

            # Set refresh token as HttpOnly cookie
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=7 * 24 * 60 * 60,  # 7 days in seconds
                path='/auth/refresh'  # restrict cookie to refresh token api calls
            )

            # Set access token in response body (unchanged)
            response.data['access_token'] = access_token

        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    Refresh access token using refresh token from HttpOnly cookie.
    """

    @extend_schema(
        operation_id='refreshAuthToken',
        responses=ObtainAuthTokenResponseSerializer,
        description='Refresh access token using http cookie',
    )
    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'message': 'Refresh token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken) as err:
            logger.error("Token refresh error: %s", err)
            return Response({'message': 'Invalid or expired or blacklisted token.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'access_token': serializer.validated_data['access']})