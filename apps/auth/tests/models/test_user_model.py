import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
def test_create_user_success():
    """
    1. Create user with the model
    2. Validate all fields after user creation
    """
    user = User.objects.create_user(
        email='test@example.com',
        password='securepassword123',
        full_name='Test User'
    )
    assert user.email == 'test@example.com'
    assert user.check_password('securepassword123')
    assert user.full_name == 'Test User'
    assert user.id is not None
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False

@pytest.mark.django_db
def test_create_superuser_success():
    """
    1. Create a super user with the model
    2. Validate relevant fields after su creation
    """
    superuser = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123',
        full_name='Admin User'
    )
    assert superuser.email == 'admin@example.com'
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.check_password('adminpass123')

@pytest.mark.django_db
def test_create_user_with_duplicate_id():
    """
    1. Create user 1 with const id
    2. Validate IntegrityError from DB
       for creation of another user with same id
    """
    test_id = uuid.uuid4()
    # Create user 1
    User.objects.create_superuser(
        email='user@example.com',
        password='afergpass123',
        full_name='Test User',
        id=test_id,
    )
    # Try creating user 2 with the same UUID
    with pytest.raises(IntegrityError):
        User.objects.create(
            id=test_id,
            email="user2@example.com",
            full_name="User Two",
            password="password456"
        )

@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(ValueError):
        User.objects.create_user(
            email=None,
            password='afergpass123',
            full_name='Test User')