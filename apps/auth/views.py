from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers.auth_token import ObtainAuthTokenSerializer
from .serializers.user_registration import UserRegistrationRequestSerializer, UserRegistrationResponseSerializer


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
        operation_id='obtainAccessToken',
        responses=ObtainAuthTokenSerializer,
        description='Obtain access token using username and password',
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            access_token = response.data.get('access')

            # Remove refresh token from response body
            response.data.pop('refresh', None)

            print(f"refresh --> {refresh_token}")

            # Set refresh token as HttpOnly cookie
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=7 * 24 * 60 * 60,  # 7 days in seconds
                path='/auth/'  # restrict cookie to refresh token api calls
            )

            # Set access token in response body (unchanged)
            response.data['access'] = access_token

        return response
