import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.fixture
def mock_user(db):
    username = 'test'
    email = 'test@test.co'
    password = '1234'
    user = User.objects.create_user(username, email=email, password=password)
    return user
