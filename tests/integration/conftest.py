# -*- coding: utf-8 -*-
import pytest
from src.core.application.password_service import PasswordService
from src.main import add_admin_user, create_app, db


@pytest.fixture
def test_client():
    """
    Fixture for setting up a test client with an in-memory SQLite database.

    Configures the Flask app for testing and sets up an in-memory SQLite database.
    Provides a test client to be used in tests and ensures the database is cleaned up
    after each test.

    :return: Flask test client.
    """
    test_config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
    }

    app = create_app(test_config)

    with app.app_context():

        db.create_all()
        with app.test_client() as testing_client:
            yield testing_client  # This is where the testing happens

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
    with test_client.application.app_context():
        admin_user = add_admin_user(password_service)
        return admin_user
