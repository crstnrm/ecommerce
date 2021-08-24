import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.fixture
def mock_user(db):
    username = 'test'
    email = 'test@test.co'
    password = mixer.faker.pystr()
    user = User.objects.create_user(username, email=email, password=password)
    user.plain_password = password
    return user


@pytest.fixture
def mock_send_communication(monkeypatch):
    monkeypatch.setattr(
        'utils.communications.Communication.send',
        lambda *args, **kwargs: None
    )
