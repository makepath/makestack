import pytest

from users.tests.factories import UserFactory


@pytest.fixture
def user():
    user = UserFactory(is_active=True)
    user.set_password("mypassword")
    user.save()
    return user
