# -*- coding: utf-8 -*-
import pytest
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import SQLAlchemy
from src.core.application.routes import app, db
from src.core.application.order_service import OrderService


# User Endpoints Tests
def test_add_user_success(test_client):
    response = test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "User added successfully"}


def test_get_user_success(test_client):
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
def test_add_product_success(test_client):
    response = test_client.post("/products", json={"name": "Product1", "price": 10.0})
    assert response.status_code == 201
    assert response.json == {"message": "Product added successfully"}


def test_get_product_success(test_client):
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
def test_create_cart_success(test_client):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    response = test_client.post("/carts", json={"user_id": 1})
    assert response.status_code == 201
    assert response.json == {"message": "Cart created successfully"}


def test_get_cart_success(test_client):
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
def test_add_cart_item_success(test_client):
    test_client.post("/products", json={"name": "Product1", "price": 5})
    response = test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    assert response.json == {"message": "Item added to cart successfully"}


def test_list_cart_items_success(test_client):
    test_client.post("/products", json={"name": "Product1", "price": 5})
    test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    response = test_client.get("/carts/1/items")
    assert response.status_code == 200
    assert response.json == [{"product_id": 1, "quantity": 2}]


def test_add_cart_item_missing_product_id(test_client):
    response = test_client.post("/carts/1/items", json={"quantity": 2})
    assert response.status_code == 400
    assert response.json["error"] == "Product ID is required"


def test_remove_cart_item_success(test_client):
    test_client.post("/products", json={"name": "Product1", "price": 5})
    test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    response = test_client.delete("/cart_items/1")
    assert response.status_code == 200
    assert response.json == {"message": "Cart item removed successfully"}


# Order Endpoints Tests
def test_create_order_success(test_client):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    response = test_client.post("/orders", json={"user_id": 1, "order_status": True})
    assert response.status_code == 201
    assert response.json == {"message": "Order created successfully"}


def test_get_order_success(test_client):
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
def test_add_order_item_success(test_client):
    product_price = 5
    test_client.post("/products", json={"name": "Product1", "price": product_price})
    response = test_client.post(
        "/orders/1/items", json={"product_id": 1, "quantity": 2, "price": product_price}
    )
    assert response.status_code == 201
    assert response.json == {"message": "Item added to order successfully"}


def test_list_order_items_success(test_client):
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


# OrderService Endpoint Tests


def test_place_order_success(test_client):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    test_client.post("/products", json={"name": "Product1", "price": 5})
    test_client.post("/carts", json={"user_id": 1})
    test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    # Place the order
    response = test_client.post("/orders/finish", json={"user_id": 1})

    # Assert successful order placement
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Order placed successfully"
    assert "order_id" in data


def test_place_order_missing_user_id(test_client):
    test_client.post(
        "/users",
        json={"user_name": "john_doe", "password": "securepassword", "role": "user"},
    )
    test_client.post("/products", json={"name": "Product1", "price": 5})
    test_client.post("/carts", json={"user_id": 1})
    test_client.post("/carts/1/items", json={"product_id": 1, "quantity": 2})
    # Missing user_id in request
    response = test_client.post("/orders/finish", json={})

    # Assert 400 error for missing user ID
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "User ID is required"


def test_place_order_invalid_user_id(test_client):
    # Invalid user_id that does not exist

    response = test_client.post("/orders/finish", json={"user_id": 999})

    # Assert 400 error for invalid user ID
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "User with ID not found"
