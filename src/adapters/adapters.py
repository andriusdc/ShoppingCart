# -*- coding: utf-8 -*-

import sqlite3
from typing import Optional
from datetime import datetime
from src.core.domain.models import User
from src.core.ports.user_port import UserPort
import bcrypt


class UserRepository(UserPort):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        try:
            with self.conn:
                self.conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        user_name TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        created_at TEXT,
                        role TEXT NOT NULL DEFAULT 'user' CHECK("role" IN ('user', 'admin')
                    )
                """
                )
        except sqlite3.DatabaseError as e:
            print(f"Error creating table: {e}")

    def create_account(self, user: User) -> None:
        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO users (user_id, user_name, password, created_at, role)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        user.user_id,
                        user.user_name,
                        hashed_password.decode(),
                        user.created_at.isoformat(),
                        user.role,
                    ),
                )
        except sqlite3.IntegrityError as e:
            print(f"Error creating account: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")

    def get_user(self, user_id: int) -> Optional[User]:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row[0],
                    user_name=row[1],
                    password=row[2],
                    created_at=datetime.fromisoformat(row[3]),
                    role=row[4],
                )
            return None
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None

    def update_username(self, user_id: int, new_username: str) -> None:
        try:
            with self.conn:
                self.conn.execute(
                    """
                    UPDATE users
                    SET user_name = ?
                    WHERE user_id = ?
                """,
                    (new_username, user_id),
                )
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")

    def update_password(self, user_id: int, new_password: str) -> None:
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        try:
            with self.conn:
                self.conn.execute(
                    """
                    UPDATE users
                    SET password = ?
                    WHERE user_id = ?
                """,
                    (hashed_password.decode(), user_id),
                )
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")

    def login_account(self, username: str, password: str) -> Optional[User]:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_name = ?", (username,))
            row = cursor.fetchone()
            if row:
                stored_password_hash = row[2]
                if bcrypt.checkpw(password.encode(), stored_password_hash.encode()):
                    return User(
                        user_id=row[0],
                        user_name=row[1],
                        password=stored_password_hash,
                        created_at=datetime.fromisoformat(row[3]),
                        role=row[4],
                    )
            return None
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None
