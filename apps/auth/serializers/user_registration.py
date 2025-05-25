from rest_framework import serializers
from apps.auth.models.user import HospitalUser


class UserRegistrationRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = HospitalUser
        fields = ('email', 'full_name', 'password')

    def create(self, validated_data):
        return HospitalUser.objects.create_user(**validated_data)


class UserRegistrationResponseSerializer(serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)  # Custom field

    class Meta:
        model = HospitalUser
        fields = ('id', 'message')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['message'] = 'User registered successfully'
        return data