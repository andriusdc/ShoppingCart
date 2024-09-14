# -*- coding: utf-8 -*-
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.orm import validates


app = Flask(__name__)


#

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    """
    User model for representing a user in the system. Handles basic data and access control.

    The model validates all the attributes.

    Columns:
    ----------
    user_id : int
        A unique identifier for the user.
    user_name : str
        The user's name.
    password : str
        The user's password for authentication.
    created_at : datetime
        The timestamp when the user account was created. If not given, will be generated automatically.
    role : str
        The role of the user, either 'admin' or 'user'. Defaults to less privilege role 'user'.

    Raises:
    ------
    ValueError:
        If user_name or password is empty.
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String, nullable=False, default="user")

    __table_args__ = (
        db.CheckConstraint("role IN ('user', 'admin')", name="check_role"),
    )

    @validates("user_name", "password")
    def validate_not_empty(self, key, value):
        if not value or value.strip() == "":
            raise ValueError(f"{key} cannot be empty")
        return value


class Product(db.Model):
    """
    Product model for representing a product available for purchase. Handles basic product data.

    The model validates all the attributes, apart from description.

    Columns:
    ----------
    product_id : int
        A unique identifier for the product.
    product_name : str
        The name of the product.
    description : str
        A short description of the product.
    price : float
        The price of the product per unit.
    created_at : datetime
        The timestamp when the product was added to the system.

    Raises:
    ------
    ValueError:
        If product_name is empty.
        If price is not greater than zero.
    """

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @validates("product_name")
    def validate_product_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Product name cannot be empty")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be greater than zero")
        return value


class Cart(db.Model):
    """
    Cart model for representing a shopping cart associated with a user. Handles cart-level data.

    The model validates all the attributes to ensure proper cart structure.

    Columns:
    ----------
    cart_id : int
        A unique identifier for the cart.
    user_id : int
        The unique identifier of the user who owns the cart.
    created_at : datetime
        The timestamp when the cart was created.

    Raises:
    ------
    ValueError:
        If user_id is not greater than zero.
    """

    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("carts", lazy=True))


class CartItem(db.Model):
    """
    CartItem model for representing individual items in a shopping cart. Handles item-level data within a cart.

    The model validates all the attributes to ensure valid cart item structure.

    Column:
    ----------
    cart_item_id : int
        A unique identifier for the cart item.
    cart_id : int
        The unique identifier of the associated cart.
    product_id : int
        The unique identifier of the product in the cart.
    quantity : int
        The quantity of the product in the cart.
    added_at : datetime
        The timestamp when the item was added to the cart.

    Raises:
    ------
    ValueError:
        If quantity is not greater than zero.
    """

    __tablename__ = "cart_items"

    cart_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.cart_id"), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart = db.relationship("Cart", backref=db.backref("cart_items", lazy=True))
    product = db.relationship("Product")

    @validates("quantity")
    def validate_quantity(self, key, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than zero")
        return value


class Order(db.Model):
    """
    Order model for representing a customer's order in the system. Handles order-level data.

    The model validates the attributes to ensure proper order structure.

    Columns:
    ----------
    order_id : int
        A unique identifier for the order.
    user_id : int
        The unique identifier of the user who placed the order.
    order_status : bool
        The current status of the order (True for completed, False for pending).
    created_at : datetime
        The timestamp when the order was created.

    Raises:
    ------
    ValueError:
        If order_status is not True or False.
    """

    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    order_status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("orders", lazy=True))

    @validates("order_status")
    def validate_order_status(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("Order status must be either True or False.")
        return value


class OrderItem(db.Model):
    """
    OrderItem model for representing individual items in an order. Handles item-level data within an order.

    The model validates all the attributes to ensure valid order item structure.

    Columns:
    ----------
    order_item_id : int
        A unique identifier for the order item.
    order_id : int
        The unique identifier of the associated order.
    product_id : int
        The unique identifier of the product in the order.
    quantity : int
        The quantity of the product in the order.
    price : float
        The price of the product per item at the time of ordering.
    created_at : datetime
        The timestamp when the item was added to the order.

    Raises:
    ------
    ValueError:
        If quantity or price is not greater than zero.
    """

    __tablename__ = "order_items"

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship("Order", backref=db.backref("order_items", lazy=True))
    product = db.relationship("Product")

    @validates("quantity", "price")
    def validate_quantity_and_price(self, key, value):
        if value <= 0:
            raise ValueError(f"{key} must be greater than zero")
        return value
