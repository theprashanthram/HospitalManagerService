from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers.user_registration import UserRegistrationRequestSerializer, UserRegistrationResponseSerializer


class RegisterUserView(APIView):
    request_serializer_class = UserRegistrationRequestSerializer
    response_serializer_class = UserRegistrationResponseSerializer

    permission_classes = (IsAdminUser,)

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
