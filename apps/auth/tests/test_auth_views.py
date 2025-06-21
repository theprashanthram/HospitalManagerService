import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def admin_user(db):
    """
    Create and return a superuser for tests.
    """
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass",
        full_name="Admin User"
    )

@pytest.fixture
def regular_user():
    """
    Create and return a user for tests.
    """
    return User.objects.create_user(
        email="normal@example.com",
        password="normalpass",
        full_name="Normal User"
    )

@pytest.mark.django_db
def test_create_user(admin_user):
    """
    1. Positive flow of user creation
    2. Validate serialized response
    """
    client = APIClient()
    client.force_authenticate(admin_user)

    url = reverse('register_user')
    data = {
        "email": "newuser@example.com",
        "full_name": "New User",
        "password": "newuserpass"
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['message'] == 'User registered successfully'
    assert User.objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_create_user_without_admin(admin_user, regular_user):
    """
    1. Create user without admin user
    2. Validate the failure (403 Forbidden)
    """
    client = APIClient()
    client.force_authenticate(regular_user)

    url = reverse('register_user')
    data = {
        "email": "unauthuser@example.com",
        "full_name": "Unauth User",
        "password": "password123"
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_create_user_duplicate_email_id_uuid(admin_user):
    """
    1. Create user with duplicate email ID
    2. Validate the failure
    3. Create user with duplicate id (uuid)
    4. Validate the failure
    """
    admin = admin_user
    client = APIClient()
    client.force_authenticate(admin)

    url = reverse('register_user')

    # Create initial user
    data = {
        "email": "duplicate@example.com",
        "full_name": "Original User",
        "password": "originalpass"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Try duplicate email and validate serialiser error
    duplicate_email_id = "duplicate@example.com"
    dup_email_data = {
        "email": duplicate_email_id,
        "full_name": "Duplicate User",
        "password": "newpass"
    }
    response = client.post(url, dup_email_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data
    assert 'already exists' in str(response.data['email'][0]).lower()

    # Directly create a user with duplicate UUID (simulate)
    # Not a perfect place to test this edge case but does the job
    original_user = User.objects.get(email=duplicate_email_id)
    with pytest.raises(IntegrityError):
        User.objects.create(
            email="unique2@example.com",
            full_name="Duplicate UUID User",
            password="dummy",
            id=original_user.id)


@pytest.mark.django_db
def test_obtain_auth_token_and_request_token_cookie(regular_user):
    """
    1. Get auth token and refresh token cookie
    2. No refresh token in response body but in cookie
    3. Serialized output in response body
    """
    # regular_user cannot be used because we password for the validation
    # So creating new user
    user = User.objects.create_user(
        email="normal2@example.com",
        password="normalpass",
        full_name="Normal User"
    )
    client = APIClient()

    url = reverse('obtain_access_token')
    data = {
        "email": "normal2@example.com",
        "password": "normalpass",
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

    # Refresh token should NOT be in body, but access_token should
    assert 'access_token' in response.data
    assert 'refresh_token' in response.cookies
    assert 'refresh' not in response.data
    assert 'access' not in response.data
    cookie = response.cookies['refresh_token']
    assert cookie.get('httponly')
    assert cookie.value != ""

@pytest.mark.django_db
def test_auth_token_refresh_with_cookie(regular_user):
    """
    Test auth token refresh with valid refresh token cookie
    """
    user = regular_user
    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.cookies['refresh_token'] = str(refresh)

    url = reverse('refresh_access_token')

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.data

@pytest.mark.django_db
def test_auth_token_refresh_without_cookie():
    """
    Test auth token refresh without valid refresh token cookie
    """
    client = APIClient()

    url = reverse('refresh_access_token')  # Replace with your actual URL name/path

    # Make GET request without setting refresh_token cookie
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['message'] == 'Refresh token missing'

@pytest.mark.django_db
def test_auth_token_refresh_with_invalid_cookie():
    """
    Test auth token refresh with invalid refresh token cookie
    """
    client = APIClient()
    client.cookies['refresh_token'] = 'invalid.token.value'

    url = reverse('refresh_access_token')

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['message'] == 'Invalid or expired or blacklisted token.'
