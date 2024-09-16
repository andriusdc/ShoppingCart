# -*- coding: utf-8 -*-
import pytest
from src.core.application.password_service import PasswordService
from src.core.domain.models import db, app, User
from src.adapters.user_adapter import UserAdapter


@pytest.fixture
def test_client():
    """
    Fixture for setting up a test client with an in-memory SQLite database.

    Configures the Flask app for testing and sets up an in-memory SQLite database.
    Provides a test client to be used in tests and ensures the database is cleaned up
    after each test.

    :return: Flask test client.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def password_service():
    """
    Fixture for providing an instance of PasswordService.

    :return: PasswordService instance.
    """
    return PasswordService()


@pytest.fixture
def create_admin_user(test_client, password_service):
    """
    Fixture to create an admin user for testing purposes.
    This is useful for setting up an initial state where an admin user exists
    in the database.

    :return: None
    """
    with app.app_context():
        # Directly add admin user to the database
        admin_user = User(
            user_name="admin",
            password=password_service.hash_password("adminpassword"),
            role="admin",
        )
        db.session.add(admin_user)
        db.session.commit()
