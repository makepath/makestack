import pytest

from users.models import User


@pytest.mark.django_db
def test_main_create_user():
    email = "user@email.com"
    password = "mypassword"
    user = User.objects.create_user(email, password)

    assert isinstance(user, User)
    assert str(user) == email
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_main_create_superuser():
    email = "user@email.com"
    password = "mypassword"
    user = User.objects.create_superuser(email, password)

    assert isinstance(user, User)
    assert str(user) == email
    assert user.is_staff is True
    assert user.is_superuser is True


@pytest.mark.django_db
def test_main_create_user_unsuccessful_missing_email():
    password = "mypassword"

    with pytest.raises(ValueError):
        User.objects.create_user(email=None, password=password)


@pytest.mark.django_db
def test_main_create_superuser_unsuccessful_no_staff():
    email = "user@email.com"
    password = "mypassword"

    with pytest.raises(ValueError):
        User.objects.create_superuser(email, password, is_staff=False)


@pytest.mark.django_db
def test_main_create_superuser_unsuccessful_no_superuser():
    email = "user@email.com"
    password = "mypassword"

    with pytest.raises(ValueError):
        User.objects.create_superuser(email, password, is_superuser=False)
