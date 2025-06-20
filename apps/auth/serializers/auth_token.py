from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ObtainAuthTokenRequestSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ObtainAuthTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
