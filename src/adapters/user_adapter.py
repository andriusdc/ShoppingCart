# -*- coding: utf-8 -*-
from src.core.domain.models import User, db
from src.core.ports.user_port import UserPort
from src.core.application.password_service import PasswordService
from typing import Optional


class UserAdapter(UserPort):
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service

    def create_account(self, user: User) -> None:
        """
        Create a new user account by hashing the password and saving the user to the database.
        """
        try:
            user.password = self.password_service.hash_password(user.password)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to create account: {e}")

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        :param user_id: ID of the user to retrieve.
        :return: The User instance if found, otherwise None.
        """
        return db.session.get(User, user_id)

    def update_user_name(self, user: User) -> None:
        """
        Update the username of an existing user.
        """
        try:
            stored_user = db.session.get(User, user.user_id)
            if stored_user:
                stored_user.user_name = user.user_name
                db.session.commit()
            else:
                raise Exception(f"User with ID {user.user_id} not found")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update username: {e}")

    def update_user_password(self, user: User) -> None:
        """
        Update the password of an existing user after hashing it.
        """
        try:
            stored_user = db.session.get(User, user.user_id)
            if stored_user:
                stored_user.password = self.password_service.hash_password(
                    user.password
                )
                db.session.commit()
            else:
                raise Exception(f"User with ID {user.user_id} not found")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update password: {e}")

    def login_account(self, user: User) -> bool:
        """
        Validate user login credentials by checking the hashed password.

        :return: True if the login credentials are correct, False otherwise.
        """
        stored_user = User.query.filter_by(user_name=user.user_name).first()
        if not stored_user:
            return False
        return self.password_service.check_password(stored_user.password, user.password)
