# -*- coding: utf-8 -*-
import pytest
from src.core.domain.models import User, db
from src.adapters.user_adapter import UserAdapter


@pytest.fixture
def user_adapter(password_service):
    """
    Fixture for providing an instance of UserAdapter with PasswordService.

    :param password_service: Instance of PasswordService.
    :return: UserAdapter instance.
    """
    return UserAdapter(password_service=password_service)


def test_create_account_success(test_client, user_adapter):
    """
    Test the creation of a user account with valid data.

    Ensures that a new user account can be created successfully. Verifies that the user
    is created in the database with the correct attributes and that the password is hashed.

    This test checks:
    - If the user is created successfully and retrieved from the database.
    - If the user name and created_at attributes are correctly set.
    - If the password is hashed and matches the provided password when checked.
    """
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
    """
    Test account creation with a duplicate user name.

    Ensures that attempting to create a user account with an existing user name raises
    an exception due to the uniqueness constraint on the user name.

    This test checks:
    - If an exception is raised when trying to create a duplicate user.
    """
    user = User(user_name="test_user", password="secure_password")
    user_adapter.create_account(user)

    duplicate_user = User(user_name="test_user", password="another_password")
    with pytest.raises(Exception):
        user_adapter.create_account(duplicate_user)


def test_login_account_success(test_client, user_adapter):
    """
    Test successful user login.

    Ensures that a user can successfully log in with valid credentials. Verifies that
    the login attempt returns True when the correct username and password are provided.

    This test checks:
    - If the login attempt is successful with the correct username and password.
    """
    user_name = "test_user"
    password = "secure_password"
    user = User(user_name=user_name, password=password)
    user_adapter.create_account(user)

    result = user_adapter.login_account(user_name, password)
    assert result.user_name == user_name


def test_login_account_failure(test_client, user_adapter):
    """
    Test failed user login due to incorrect password.

    Ensures that a login attempt fails when an incorrect password is provided for a
    valid username. Verifies that the login attempt returns False.

    This test checks:
    - If the login attempt returns False with an incorrect password.
    """
    user_name = "test_user"
    password = "secure_password"
    user = User(user_name=user_name, password=password)
    user_adapter.create_account(user)

    wrong_password = "wrong_password"

    with pytest.raises(Exception):
        user_adapter.login_account(user_name, wrong_password)


def test_get_user(test_client, user_adapter):
    """
    Test retrieval of an existing user by ID.

    Ensures that a user can be retrieved successfully by their ID. Verifies that the
    retrieved user has the correct attributes and that the password is hashed.

    This test checks:
    - If the user is retrieved successfully by their ID.
    - If the user attributes, including hashed password, are correctly set.
    """
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
    """
    Test retrieval of a non-existent user by ID.

    Ensures that retrieving a user by an ID that does not exist returns None,
    confirming that no such user is present in the database.

    This test checks:
    - If fetching a user by a non-existent ID returns None.
    """
    non_existent_user_id = 9999
    fetched_user = user_adapter.get_user(non_existent_user_id)

    assert fetched_user is None  # Ensure that no user is returned


def test_update_user_name(test_client, user_adapter):
    """
    Test updating the username of an existing user.

    Ensures that the username of an existing user can be updated successfully. Verifies
    that the new username is saved in the database and that the password remains hashed.

    This test checks:
    - If the username is updated correctly in the database.
    - If the password remains hashed and unchanged.
    """
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
    """
    Test updating the password of an existing user.

    Ensures that the password of an existing user can be updated successfully. Verifies
    that the new password is hashed and saved in the database correctly.

    This test checks:
    - If the password is updated and hashed correctly in the database.
    - If the new password is correctly validated.
    """
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
