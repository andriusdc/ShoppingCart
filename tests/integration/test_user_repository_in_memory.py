# -*- coding: utf-8 -*-
import sqlite3
import pytest
from src.core.domain.models import User
from src.adapters.adapters import UserRepository
from datetime import datetime


@pytest.fixture
def in_memory_db():
    # Set up an in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def user_repository(in_memory_db):
    # Create a UserRepository with the in-memory database
    return UserRepository(in_memory_db)


def test_create_account(user_repository):
    user = User(
        user_id=1,
        user_name="John",
        password="123",
        created_at=datetime.now(),
        role="user",
    )
    user_repository.create_account(user)

    # Fetch the user to verify creation
    fetched_user = user_repository.get_user(1)
    assert fetched_user is not None
    assert fetched_user.user_name == user.user_name
    assert fetched_user.role == "user"


def test_update_username(user_repository):
    user = User(
        user_id=1,
        user_name="John",
        password="123",
        created_at=datetime.now(),
        role="user",
    )
    user_repository.create_account(user)

    # Update username
    user_repository.update_username(1, "new_username")

    # Fetch the updated user
    updated_user = user_repository.get_user(1)
    assert updated_user is not None
    assert updated_user.user_name == "new_username"


def test_update_password(user_repository):
    user = User(
        user_id=1,
        user_name="John",
        password="123",
        created_at=datetime.now(),
        role="user",
    )
    user_repository.create_account(user)

    # Update password
    user_repository.update_password(1, "new_password")

    # Log in with the new password
    logged_in_user = user_repository.login_account("John", "new_password")
    assert logged_in_user is not None
    assert logged_in_user.user_name == "John"


def test_login_account(user_repository):
    user = User(
        user_id=1,
        user_name="John",
        password="123",
        created_at=datetime.now(),
        role="user",
    )
    user_repository.create_account(user)

    # Attempt to log in with correct password
    logged_in_user = user_repository.login_account("John", "123")
    assert logged_in_user is not None
    assert logged_in_user.user_name == "John"

    # Attempt to log in with incorrect password
    logged_in_user = user_repository.login_account("John", "wrong_password")
    assert logged_in_user is None


def test_get_user(user_repository):
    user = User(
        user_id=1,
        user_name="John",
        password="123",
        created_at=datetime.now(),
        role="user",
    )
    user_repository.create_account(user)

    fetched_user = user_repository.get_user(1)
    assert fetched_user is not None
    assert fetched_user.user_name == "John"
