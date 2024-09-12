# -*- coding: utf-8 -*-
from typing import Optional
from src.core.domain.models import User


class UserPort:
    def create_account(self, user: User) -> None:
        raise NotImplementedError

    def login_account(self, user: User) -> None:
        raise NotImplementedError

    def get_user(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    def update_user_name(self, user: User) -> None:
        raise NotImplementedError

    def update_user_password(self, user: User) -> None:
        raise NotImplementedError
