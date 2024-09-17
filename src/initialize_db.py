# -*- coding: utf-8 -*-
from src.main import create_app, add_admin_user
from src.core.application.password_service import PasswordService
from flask_migrate import Migrate, upgrade

app = create_app()

with app.app_context():
    # Apply migrations
    upgrade()

    # Create admin user if not exists
    add_admin_user(PasswordService())
