import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(
        email='test@example.com',
        password='securepassword123',
        full_name='Test User'
    )
    assert user.email == 'test@example.com'
    assert user.check_password('securepassword123')
    assert user.full_name == 'Test User'
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_without_email_raises_error():
    with pytest.raises(ValueError, match="Users must have an email address"):
        User.objects.create_user(
            email='',
            password='securepassword123',
            full_name='Test User'
        )


@pytest.mark.django_db
def test_create_superuser_success():
    superuser = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123',
        full_name='Admin User'
    )
    assert superuser.email == 'admin@example.com'
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.check_password('adminpass123')