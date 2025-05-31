from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ObtainAuthTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.pop('refresh', None)  # remove refresh token from response JSON
        return data