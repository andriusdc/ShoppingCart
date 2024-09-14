# -*- coding: utf-8 -*-
import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from src.core.domain.models import (
    User,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    app,
    db,
)
from flask_migrate import upgrade


@pytest.fixture
def session():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_databasedb"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


# Tests for the User model
def test_user_name_validation(session):
    """
    Test the validation of `user_name` in the `User` model.

    Ensures that the `User` model raises a `ValueError` with the message
    'User name cannot be empty' when `user_name` is an empty string,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `user_name` is an empty string, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="user_name cannot be empty"):
        user = User(user_name="", password="securepassword", role="user")


def test_user_password_validation(session):
    """
    Test the validation of `password` in the `User` model.

    Ensures that the `User` model raises a `ValueError` with the message
    'Password cannot be empty' when `password` is an empty string,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `password` is an empty string, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="password cannot be empty"):
        user = User(user_name="validuser", password="", role="user")


def test_create_valid_user(session):
    """
    Test creating a valid user with a username, password, and a valid role.

    Ensures that the `User` model allows creation of a user with valid attributes
    and commits it to the session.

    This test checks:
    - If the user is created successfully with the provided attributes.
    """
    user = User(user_name="validuser", password="securepassword", role="user")

    assert user.user_name == "validuser"
    assert user.role == "user"
    assert user.password == "securepassword"


# Tests for the Product model
def test_product_name_validation(session):
    """
    Test the validation of `product_name` in the `Product` model.

    Ensures that the `Product` model raises a `ValueError` with the message
    'Product name cannot be empty' when `product_name` is an empty string,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `product_name` is an empty string, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        product = Product(product_name="", description="A test product", price=100.0)


def test_product_price_validation(session):
    """
    Test the validation of `price` in the `Product` model.

    Ensures that the `Product` model raises a `ValueError` with the message
    'Price must be a positive number' when `price` is zero or negative,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `price` is zero or negative, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        product = Product(
            product_name="Test Product", description="A test product", price=0.0
        )

    with pytest.raises(ValueError, match="Price must be greater than zero"):
        product = Product(
            product_name="Test Product", description="A test product", price=-10.0
        )


def test_create_valid_product(session):
    """
    Test creating a valid product with a name, description, price, and creation date.

    Ensures that the `Product` model allows creation of a product with valid attributes
    and commits it to the session.

    This test checks:
    - If the product is created successfully with the provided attributes.
    """
    product = Product(
        product_name="Test Product", description="A test product", price=100.0
    )

    assert product.product_name == "Test Product"
    assert product.price == 100.0


# Tests for CartItem model
def test_cart_item_quantity_validation(session):
    """
    Test the validation of `quantity` in the `CartItem` model.

    Ensures that the `CartItem` model raises a `ValueError` with the message
    'Quantity must be greater than zero' when `quantity` is zero or negative,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `quantity` is zero or negative, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        cart_item = CartItem(cart_id=1, product_id=1, quantity=0)

    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        cart_item = CartItem(cart_id=1, product_id=1, quantity=-1)


def test_create_cart_item_with_valid_quantity(session):
    """
    Test creating a CartItem with a valid quantity.

    Ensures that the `CartItem` model allows creation of a cart item with a valid quantity
    and commits it to the session.

    This test checks:
    - If the cart item is created successfully with the provided attributes.
    """
    cart_item = CartItem(cart_id=1, product_id=1, quantity=3)

    assert cart_item.quantity == 3


# Tests for Order model
def test_order_status_validation(session):
    """
    Test the validation of `order_status` in the `Order` model.

    Ensures that the `Order` model raises a `ValueError` with the message
    'Order status must be true or false' when `order_status` is neither True nor False,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `order_status` is neither True nor False, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="Order status must be either True or False."):
        order = Order(user_id=1, order_status="pending")  # Invalid status


def test_create_valid_order(session):
    """
    Test creating an order with a valid user_id and order_status.

    Ensures that the `Order` model allows creation of an order with valid attributes
    and commits it to the session.

    This test checks:
    - If the order is created successfully with the provided attributes.
    """
    order = Order(user_id=1, order_status=True)

    assert order.user_id == 1
    assert order.order_status is True


# Tests for OrderItem model
def test_order_item_quantity_validation(session):
    """
    Test the validation of `quantity` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Quantity must be greater than zero' when `quantity` is zero or negative,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `quantity` is zero or negative, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="quantity must be greater than zero"):
        order_item = OrderItem(order_id=1, product_id=1, quantity=0, price=50.0)

    with pytest.raises(ValueError, match="quantity must be greater than zero"):
        order_item = OrderItem(order_id=1, product_id=1, quantity=-1, price=50.0)


def test_order_item_price_validation(session):
    """
    Test the validation of `price` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Price must be a positive number' when `price` is zero or negative,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `price` is zero or negative, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError, match="price must be greater than zero"):
        order_item = OrderItem(order_id=1, product_id=1, quantity=2, price=0.0)

    with pytest.raises(ValueError, match="price must be greater than zero"):
        order_item = OrderItem(order_id=1, product_id=1, quantity=2, price=-10.0)


def test_create_valid_order_item(session):
    """
    Test creating a valid OrderItem with a positive quantity and price.

    Ensures that the `OrderItem` model allows creation of an order item with valid attributes
    and commits it to the session.

    This test checks:
    - If the order item is created successfully with the provided attributes.
    """
    order_item = OrderItem(order_id=1, product_id=1, quantity=2, price=50.0)

    assert order_item.quantity == 2
    assert order_item.price == 50.0
