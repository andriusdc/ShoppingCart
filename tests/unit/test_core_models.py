# -*- coding: utf-8 -*-
import pytest
from datetime import datetime
from src.core.domain.models import User, Product, Cart, CartItem, Order, OrderItem


def test_user_instantiation():
    created_at = datetime(2024, 9, 11, 0, 0, 0)
    user = User(
        user_id=1, user_name="John", password="123", created_at=created_at, role="user"
    )

    assert user.user_id == 1
    assert user.user_name == "John"
    assert user.password == "123"
    assert user.created_at == created_at
    assert user.role == "user"


def test_user_id_validation():
    with pytest.raises(ValueError) as excinfo:
        User(user_id=0, user_name="John", password="123", role="user")
    assert str(excinfo.value) == "User ID must be greater than zero"


def test_user_name_validation():
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="", password="123", role="user")
    assert str(excinfo.value) == "User name cannot be empty"


def test_password_validation():
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="John", password="", role="user")
    assert str(excinfo.value) == "Password cannot be empty"


def test_created_at_validation():
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="John", password="123", created_at="0", role="user")
    assert str(excinfo.value) == "Created at must be a valid datetime object"


def test_role_validation():
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="John", password="123", role="king")
    assert str(excinfo.value) == "Role must be 'user' or 'admin'"


def test_product_instantiation():
    created_at = datetime(2024, 9, 11, 0, 0, 0)
    product = Product(
        product_id=1,
        product_name="Orange",
        description="Fruit unit",
        price=5,
        created_at=created_at,
    )

    assert product.product_id == 1
    assert product.product_name == "Orange"
    assert product.description == "Fruit unit"
    assert product.price == 5
    assert product.created_at == created_at


def test_product_id_validation():
    with pytest.raises(ValueError) as excinfo:
        Product(
            product_id=0,
            product_name="Orange",
            description="Fruit unit",
            price=5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Product ID must be greater than zero"


def test_product_name_validation():
    with pytest.raises(ValueError) as excinfo:
        Product(
            product_id=1,
            product_name="",
            description="Fruit unit",
            price=5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Product name cannot be empty"


def test_product_price_validation():
    with pytest.raises(ValueError) as excinfo:
        Product(
            product_id=1,
            product_name="Orange",
            description="Fruit unit",
            price=-5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Price must be a positive number"


def test_product_created_at_validation():
    with pytest.raises(ValueError) as excinfo:
        Product(
            product_id=1,
            product_name="Orange",
            description="Fruit unit",
            price=5.0,
            created_at="invalid_date",
        )
    assert str(excinfo.value) == "Created at must be a valid datetime object"


def test_cart_instantiation():
    created_at = datetime(2024, 9, 11, 0, 0, 0)
    cart = Cart(cart_id=1, user_id=1, created_at=created_at)

    assert cart.cart_id == 1
    assert cart.user_id == 1
    assert cart.created_at == created_at


def test_cart_items_instantiation():
    added_at = datetime(2024, 9, 11, 0, 0, 0)
    cartItems = CartItem(
        cart_item_id=1, cart_id=1, product_id=2, quantity=1, added_at=added_at
    )

    assert cartItems.cart_item_id == 1
    assert cartItems.cart_id == 1
    assert cartItems.product_id == 2
    assert cartItems.quantity == 1
    assert cartItems.added_at == added_at


def test_order_instantiation():
    created_at = datetime(2024, 9, 11, 0, 0, 0)
    order = Order(order_id=1, user_id=1, order_status=True, created_at=created_at)

    assert order.order_id == 1
    assert order.user_id == 1
    assert order.order_status == True
    assert order.created_at == created_at


def test_order_item_instantiation():
    created_at = datetime(2024, 9, 11, 0, 0, 0)
    order_item = OrderItem(
        order_item_id=1,
        order_id=2,
        product_id=3,
        quantity=2,
        price=2,
        created_at=created_at,
    )

    assert order_item.order_item_id == 1
    assert order_item.order_id == 2
    assert order_item.product_id == 3
    assert order_item.quantity == 2
    assert order_item.price == 2
    assert order_item.created_at == created_at
