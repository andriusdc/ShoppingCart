# -*- coding: utf-8 -*-
import pytest
from flask_sqlalchemy import SQLAlchemy
from src.core.application.routes import app, db
from src.core.application.order_service import OrderService


# Fixtures
@pytest.fixture
def create_user(test_client):
    def _create_user(user_name, password, role):
        return test_client.post(
            "/users",
            json={"user_name": user_name, "password": password, "role": role},
        )

    return _create_user


@pytest.fixture
def login_user(test_client, create_user):
    def _login_user(user_name, password):
        create_user(user_name, password, "user")
        response = test_client.post(
            "/login", json={"user_name": user_name, "password": password}
        )
        return response.json.get("token")

    return _login_user


# User Endpoints Tests
def test_add_user_success(test_client, create_user):
    response = create_user("john_doe", "securepassword", "user")
    assert response.status_code == 201
    assert response.json == {"message": "User added successfully"}


def test_get_user_success(test_client, login_user):
    token = login_user("john_doe", "securepassword")

    response = test_client.get("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json == {"user_name": "john_doe", "role": "user"}


def test_add_user_missing_fields(test_client, create_user):
    response = test_client.post("/users", json={"user_name": "john_doe"})
    assert response.status_code == 400
    print(response.json["error"])
    assert response.json["error"] == "Password cannot be empty"


def test_login_success(test_client, create_user):
    create_user("john_doe", "securepassword", "user")

    response = test_client.post(
        "/login", json={"user_name": "john_doe", "password": "securepassword"}
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "token" in json_data


def test_login_missing_user_name(test_client, create_user):
    create_user("john_doe", "securepassword", "user")

    response = test_client.post("/login", json={"password": "securepassword"})

    assert response.status_code == 400
    json_data = response.get_json()
    print(json_data)
    assert json_data["error"] == "Username and password are required"


def test_login_missing_password(test_client, create_user):
    create_user("john_doe", "securepassword", "user")

    response = test_client.post("/login", json={"user_name": "john_doe"})

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "Username and password are required"


def test_login_invalid_credentials(test_client, create_user):
    create_user("john_doe", "securepassword", "user")

    response = test_client.post(
        "/login", json={"user_name": "john_doe", "password": "wrong_password"}
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["error"] == "Invalid username or password"


def test_login_non_existent_user(test_client):
    response = test_client.post(
        "/login", json={"user_name": "non_existent_user", "password": "some_password"}
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["error"] == "Invalid username or password"


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
def test_create_cart_success(test_client, login_user):
    token = login_user("john_doe", "securepassword")
    response = test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.json == {"message": "Cart created successfully"}


def test_get_cart_success(test_client, login_user):
    token = login_user("john_doe", "securepassword")
    test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})
    response = test_client.get("/carts/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json == {"cart_id": 1, "user_id": 1}


def test_get_cart_not_found(test_client, login_user):
    token = login_user("john_doe", "securepassword")
    test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})
    response = test_client.get(
        "/carts/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Cart with ID 999 does not exist"


# Cart Item Endpoints Tests
def test_add_cart_item_success(test_client, login_user):
    test_client.post("/products", json={"name": "Product1", "price": 5})

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/carts/1/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Item added to cart successfully"}


def test_list_cart_items_success(test_client, login_user):
    test_client.post("/products", json={"name": "Product1", "price": 5})

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/carts/1/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = test_client.get(
        "/carts/1/items", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == [{"product_id": 1, "quantity": 2}]


def test_add_cart_item_missing_product_id(test_client, login_user):
    test_client.post("/products", json={"name": "Product1", "price": 5})

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/carts/1/items",
        json={"quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json["error"] == "Product ID is required"


def test_remove_cart_item_success(test_client, login_user):
    test_client.post("/products", json={"name": "Product1", "price": 5})

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/carts/1/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = test_client.delete(
        "/cart_items/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Cart item removed successfully"}


# Order Endpoints Tests
def test_create_order_success(test_client, login_user):
    token = login_user("john_doe", "securepassword")

    response = test_client.post(
        "/orders",
        json={"order_status": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Order created successfully"}


def test_get_order_success(test_client, login_user):
    token = login_user("john_doe", "securepassword")

    response = test_client.post(
        "/orders",
        json={"order_status": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = test_client.get(
        "/orders/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == {"order_id": 1, "status": True}


def test_get_order_not_found(test_client, login_user):
    token = login_user("john_doe", "securepassword")

    response = test_client.post(
        "/orders",
        json={"order_status": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = test_client.get(
        "/orders/999", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json["error"] == "Order with ID 999 does not exist"


# Order Item Endpoints Tests
def test_add_order_item_success(test_client, login_user):
    product_price = 5
    test_client.post("/products", json={"name": "Product1", "price": product_price})

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/orders/1/items",
        json={"product_id": 1, "quantity": 2, "price": product_price},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Item added to order successfully"}


def test_list_order_items_success(test_client, login_user):
    product_price = 5
    test_client.post("/products", json={"name": "Product1", "price": product_price})

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/orders/1/items",
        json={"product_id": 1, "quantity": 2, "price": product_price},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = test_client.get(
        "/orders/1/items", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == [{"product_id": 1, "quantity": 2}]


# OrderService Endpoint Tests


def test_place_order_success(test_client, login_user):
    token = login_user("john_doe", "securepassword")

    test_client.post("/products", json={"name": "Product1", "price": 5})
    test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})
    test_client.post(
        "/carts/1/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    # Place the order
    response = test_client.post(
        "/orders/finish", headers={"Authorization": f"Bearer {token}"}
    )

    # Assert successful order placement
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Order placed successfully"
    assert "order_id" in data
