# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional
from src.core.domain.models import User


class UserPort(ABC):
    @abstractmethod
    def create_account(self, user: User) -> None:
        """
        Create a new user account.

        :param user: User instance to be created.
        :raises Exception: If account creation fails.
        """
        pass

    @abstractmethod
    def login_account(self, user: User) -> bool:
        """
        Log in the user with the provided credentials.

        :param user: User instance with login credentials.
        :return: True if login is successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        :param user_id: ID of the user to retrieve.
        :return: User instance if found, otherwise None.
        """
        pass

    @abstractmethod
    def update_user_name(self, user: User) -> None:
        """
        Update an existing user's name.

        :param user: User instance with the updated username.
        :raises Exception: If username update fails.
        """
        pass

    @abstractmethod
    def update_user_password(self, user: User) -> None:
        """
        Update an existing user's password.

        :param user: User instance with the updated password.
        :raises Exception: If password update fails.
        """
        pass
