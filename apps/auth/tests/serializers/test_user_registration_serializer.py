import pytest

from django.contrib.auth import get_user_model
from apps.auth.serializers.user_registration import (
    UserRegistrationRequestSerializer,
    UserRegistrationResponseSerializer,
)

User = get_user_model()

@pytest.mark.django_db
def test_user_registration_request():
    """
    1. Save new request
    2. Validate creation of new model for the request
    """
    data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "securepass123"
    }

    serializer = UserRegistrationRequestSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()
    assert User.objects.count() == 1
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.check_password("securepass123")
    assert not hasattr(serializer.data, "password")  # write_only


def test_user_registration_request_negative():
    """
    1. Request without email
    2. Validate failure
    """
    data = {
        "full_name": "User Without Email",
        "password": "somepass"
    }

    serializer = UserRegistrationRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors

@pytest.mark.django_db
def test_user_registration_response():
    """
    1. Create new user with model
    2. Validate serialised response for creation with expected message
    """
    user = User.objects.create_user(
        email="resptest@example.com",
        full_name="Response Test",
        password="resppass"
    )

    serializer = UserRegistrationResponseSerializer(instance=user)
    data = serializer.data

    assert "id" in data
    assert "message" in data
    assert data["message"] == "User registered successfully"
