# -*- coding: utf-8 -*-
import pytest

from src.core.domain.models import db, User, app
from src.core.application.password_service import PasswordService
from src.adapters.adapters import UserAdapter


@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def password_service():
    return PasswordService()


@pytest.fixture
def user_adapter(password_service):
    return UserAdapter(password_service=password_service)


def test_create_account_success(test_client, user_adapter):
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    created_user = (
        db.session.execute(db.select(User).filter_by(user_name="test_user"))
        .scalars()
        .first()
    )

    assert created_user is not None
    assert created_user.user_name == "test_user"
    assert (
        created_user.password != "secure_password"
    )  # Check that the password is hashed
    assert user_adapter.password_service.check_password(
        created_user.password, "secure_password"
    )
    assert created_user.created_at is not None


def test_create_account_existing_user_name(test_client, user_adapter):
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    # Trying to create a user with the same username should fail
    duplicate_user = User(user_name="test_user", password="another_password")
    with pytest.raises(Exception):
        user_adapter.create_account(duplicate_user)


def test_login_account_success(test_client, user_adapter):
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    login_user = User(user_name="test_user", password="secure_password")
    result = user_adapter.login_account(login_user)
    assert result is True


def test_login_account_failure(test_client, user_adapter):
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    wrong_password_user = User(user_name="test_user", password="wrong_password")
    result = user_adapter.login_account(wrong_password_user)
    assert result is False


def test_get_user(test_client, user_adapter):
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    fetched_user = user_adapter.get_user(user.user_id)
    assert fetched_user is not None
    assert fetched_user.user_id == user.user_id
    assert fetched_user.user_name == "test_user"
    assert fetched_user.password != "secure_password"
    assert user_adapter.password_service.check_password(
        fetched_user.password, "secure_password"
    )
    assert fetched_user.created_at is not None


def test_get_non_existent_user(test_client, user_adapter):
    non_existent_user_id = 9999
    fetched_user = user_adapter.get_user(non_existent_user_id)

    assert fetched_user is None  # Ensure that no user is returned


def test_update_user_name(test_client, user_adapter):
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    user.user_name = "new_user_name"
    user_adapter.update_user_name(user)

    updated_user = db.session.get(User, user.user_id)
    assert updated_user is not None
    assert updated_user.user_id == user.user_id
    assert updated_user.user_name == "new_user_name"
    assert updated_user.password != "secure_password"
    assert user_adapter.password_service.check_password(
        updated_user.password, "secure_password"
    )
    assert updated_user.created_at is not None


def test_update_user_password(test_client, user_adapter):
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    new_password = "new_secure_password"
    user.password = new_password
    user_adapter.update_user_password(user)

    updated_user = db.session.get(User, user.user_id)
    assert updated_user is not None
    assert updated_user.user_id == user.user_id
    assert updated_user.user_name == "test_user"
    assert updated_user.password != new_password
    assert user_adapter.password_service.check_password(
        updated_user.password, new_password
    )
    assert updated_user.created_at is not None
