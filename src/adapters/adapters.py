# -*- coding: utf-8 -*-
from src.core.domain.models import User, db
from src.core.ports.user_port import UserPort
from src.core.application.password_service import PasswordService


class UserAdapter(UserPort):
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service

    def create_account(self, user: User) -> None:
        user.password = self.password_service.hash_password(user.password)
        db.session.add(user)
        db.session.commit()

    def login_account(self, user: User) -> bool:
        stored_user = (
            db.session.execute(db.select(User).filter_by(user_name=user.user_name))
            .scalars()
            .first()
        )
        if not stored_user or not self.password_service.check_password(
            stored_user.password, user.password
        ):
            return False
        return True

    def get_user(self, user_id: int) -> User:
        return db.session.get(User, user_id)

    def update_user_name(self, user: User) -> None:
        stored_user = db.session.get(User, user.user_id)
        if stored_user:
            stored_user.user_name = user.user_name
            db.session.commit()

    def update_user_password(self, user: User) -> None:
        stored_user = db.session.get(User, user.user_id)
        if stored_user:
            stored_user.password = self.password_service.hash_password(user.password)
            db.session.commit()
