# -*- coding: utf-8 -*-
import pytest
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import SQLAlchemy
from src.adapters.user_adapter import UserAdapter
from src.adapters.product_adapter import ProductAdapter
from src.adapters.cart_adapter import CartAdapter
from src.adapters.cart_item_adapter import CartItemAdapter
from src.adapters.order_adapter import OrderAdapter
from src.adapters.order_item_adapter import OrderItemAdapter
from src.core.application.routes import app, db


@pytest.fixture
def test_client():
    """
    Fixture for setting up a test client with an in-memory SQLite database.

    Configures the Flask app for testing and sets up an in-memory SQLite database.
    Provides a test client to be used in tests and ensures the database is cleaned up
    after each test.

    :return: Flask test client.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def user_adapter(password_service):
    return UserAdapter(password_service=password_service)


@pytest.fixture
def product_adapter():
    return ProductAdapter()


@pytest.fixture
def cart_adapter():
    return CartAdapter()


@pytest.fixture
def cart_item_adapter():
    return CartItemAdapter()


@pytest.fixture
def order_adapter():
    return OrderAdapter()


@pytest.fixture
def order_item_adapter():
    return OrderItemAdapter()


# User Endpoints Tests
def test_add_user_success(test_client, user_adapter):
    response = test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "User added successfully"}


def test_get_user_success(test_client, user_adapter):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    response = test_client.get("/users/1")
    assert response.status_code == 200
    assert response.json == {"user_name": "john_doe", "role": "user"}


def test_add_user_missing_fields(test_client):
    response = test_client.post("/users", json={"user_name": "john_doe"})
    assert response.status_code == 400
    print(response.json["error"])
    assert response.json["error"] == "Password cannot be empty"


def test_get_user_not_found(test_client):
    response = test_client.get("/users/999")
    assert response.status_code == 400
    assert response.json["error"] == "User with ID 999 not found"


# Product Endpoints Tests
def test_add_product_success(test_client, product_adapter):
    response = test_client.post("/products", json={"name": "Product1", "price": 10.0})
    assert response.status_code == 201
    assert response.json == {"message": "Product added successfully"}


def test_get_product_success(test_client, product_adapter):
    test_client.post("/products", json={"name": "Product1", "price": 10.0})
    response = test_client.get("/products/1")
    assert response.status_code == 200
    assert response.json == {"name": "Product1", "price": 10.0}


def test_add_product_invalid_price(test_client):
    response = test_client.post("/products", json={"name": "Product1", "price": -10.0})
    assert response.status_code == 400
    assert response.json["error"] == "Price must be a positive number"


def test_get_product_not_found(test_client):
    response = test_client.get("/products/999")
    assert response.status_code == 400
    assert response.json["error"] == "Product with ID 999 not found"


# Cart Endpoints Tests
def test_create_cart_success(test_client, cart_adapter):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    response = test_client.post("/carts", json={"user_id": 1})
    assert response.status_code == 201
    assert response.json == {"message": "Cart created successfully"}


def test_get_cart_success(test_client, cart_adapter):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    test_client.post("/carts", json={"user_id": 1})
    response = test_client.get("/carts/1")
    assert response.status_code == 200
    assert response.json == {"cart_id": 1, "user_id": 1}


def test_create_cart_missing_user_id(test_client):
    response = test_client.post("/carts", json={})
    assert response.status_code == 400
    assert response.json["error"] == "User ID is required"


def test_get_cart_not_found(test_client):
    response = test_client.get("/carts/999")
    assert response.status_code == 400
    assert response.json["error"] == "Cart with ID 999 does not exist"


# Cart Item Endpoints Tests
def test_add_cart_item_success(test_client, cart_item_adapter):
    test_client.post("/products", json={"name": "Product1", "price": 5})
    response = test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    assert response.json == {"message": "Item added to cart successfully"}


def test_list_cart_items_success(test_client, cart_item_adapter):
    test_client.post("/products", json={"name": "Product1", "price": 5})
    test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    response = test_client.get("/carts/1/items")
    assert response.status_code == 200
    assert response.json == [{"product_id": 1, "quantity": 2}]


def test_add_cart_item_missing_product_id(test_client):
    response = test_client.post("/carts/1/items", json={"quantity": 2})
    assert response.status_code == 400
    assert response.json["error"] == "Product ID is required"


def test_remove_cart_item_success(test_client, cart_item_adapter):
    test_client.post("/products", json={"name": "Product1", "price": 5})
    test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    response = test_client.delete("/cart_items/1")
    assert response.status_code == 200
    assert response.json == {"message": "Cart item removed successfully"}


# Order Endpoints Tests
def test_create_order_success(test_client, order_adapter):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    response = test_client.post("/orders", json={"user_id": 1, "order_status": True})
    assert response.status_code == 201
    assert response.json == {"message": "Order created successfully"}


def test_get_order_success(test_client, order_adapter):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    test_client.post("/orders", json={"user_id": 1, "order_status": True})
    response = test_client.get("/orders/1")
    assert response.status_code == 200
    assert response.json == {"order_id": 1, "status": True}


def test_create_order_missing_user_id(test_client):
    response = test_client.post("/orders", json={"order_status": True})
    assert response.status_code == 400
    assert response.json["error"] == "User ID is required"


def test_get_order_not_found(test_client):
    response = test_client.get("/orders/999")
    assert response.status_code == 400
    assert response.json["error"] == "Order with ID 999 does not exist"


# Order Item Endpoints Tests
def test_add_order_item_success(test_client, order_item_adapter):
    product_price = 5
    test_client.post("/products", json={"name": "Product1", "price": product_price})
    response = test_client.post(
        "/orders/1/items", json={"product_id": 1, "quantity": 2, "price": product_price}
    )
    assert response.status_code == 201
    assert response.json == {"message": "Item added to order successfully"}


def test_list_order_items_success(test_client, order_item_adapter):
    product_price = 5
    test_client.post("/products", json={"name": "Product1", "price": product_price})
    test_client.post(
        "/orders/1/items", json={"product_id": 1, "quantity": 2, "price": product_price}
    )
    response = test_client.get("/orders/1/items")
    assert response.status_code == 200
    assert response.json == [{"product_id": 1, "quantity": 2}]


def test_add_order_item_missing_product_id(test_client):
    test_client.post("/products", json={"name": "Product1", "price": 5})
    response = test_client.post("/orders/1/items", json={"quantity": 2})
    assert response.status_code == 400
    assert response.json["error"] == "Product ID is required"
