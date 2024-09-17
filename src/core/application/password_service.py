# -*- coding: utf-8 -*-
import bcrypt


class PasswordService:
    def hash_password(self, password: str) -> str:
        """
        Hash a plain-text password using bcrypt.

        This method generates a salt and hashes the provided password using the bcrypt algorithm.

        :param password: The plain-text password to hash.
        :return: The hashed password as a string, encoded in UTF-8.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def check_password(self, hashed_password: str, password: str) -> bool:
        """
        Verify if a plain-text password matches its hashed version.

        This method checks if the provided password matches the given hashed password using bcrypt.

        :param hashed_password: The hashed password to check against.
        :param password: The plain-text password to verify.
        :return: True if the password matches the hashed password, otherwise False.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
