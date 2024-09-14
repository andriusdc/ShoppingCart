# -*- coding: utf-8 -*-
import pytest
import bcrypt
from src.core.application.password_service import PasswordService


@pytest.fixture
def password_service():
    return PasswordService()


def test_hash_password(password_service):
    password = "securepassword"
    hashed_password = password_service.hash_password(password)

    assert hashed_password != password

    assert bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def test_check_password_correct(password_service):
    password = "securepassword"
    hashed_password = password_service.hash_password(password)

    assert password_service.check_password(hashed_password, password) is True


def test_check_password_incorrect(password_service):
    correct_password = "securepassword"
    incorrect_password = "wrongpassword"
    hashed_password = password_service.hash_password(correct_password)

    assert password_service.check_password(hashed_password, incorrect_password) is False
