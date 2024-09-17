# -*- coding: utf-8 -*-
from src.core.domain.models import db, User  # ,migrate,app
from src.core.application.password_service import PasswordService
from src.core.application.routes import main
from flask import Flask
import os
from flask_migrate import Migrate, upgrade
from flask_jwt_extended import JWTManager


def add_admin_user(password_service=PasswordService):
    """
    Utility function to add an admin user if not already present.
    """
    admin_user = User.query.filter_by(role="admin").first()
    if not admin_user:
        admin_user = User(
            user_name="admin",
            password=password_service.hash_password("adminpassword"),
            role="admin",
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created")
    return admin_user


def create_app(test_config=None):
    """
    Create and configure the Flask application.

    :return: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    JWTManager().init_app(app)

    # Register blueprints
    app.register_blueprint(main)

    ## Create admin user if not exist
    # with app.app_context():
    #    add_admin_user(PasswordService())

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(debug=True, host="0.0.0.0", port=5000)
