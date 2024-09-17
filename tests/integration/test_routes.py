# -*- coding: utf-8 -*-
import pytest
from src.core.application.order_service import OrderService


# Fixtures
@pytest.fixture
def create_user(test_client):
    """
    Fixture to create a user via the /users endpoint.

    Provides a function that can be used to make a POST request to add a user with the specified
    user_name, password, and role. Returns the response object of the POST request.

    Args:
        test_client (FlaskClient): The Flask test client instance.

    Returns:
        function: A function to create a user with specified details.
    """

    def _create_user(user_name, password, role):
        return test_client.post(
            "/users",
            json={"user_name": user_name, "password": password, "role": role},
        )

    return _create_user


@pytest.fixture
def login_user(test_client, create_user):
    """
    Fixture to log in a user and obtain an authentication token.

    Uses the create_user fixture to create a user and then makes a POST request to the /login endpoint
    to obtain a JWT token for the user. Returns the token as a string.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_user (function): The fixture function to create a user.

    Returns:
        function: A function to log in a user and return an authentication token.
    """

    def _login_user(user_name, password):
        create_user(user_name, password, "user")
        response = test_client.post(
            "/login", json={"user_name": user_name, "password": password}
        )
        return response.json.get("token")

    return _login_user


@pytest.fixture
def admin_token(test_client, create_admin_user):
    """
    Fixture to obtain an admin token.

    Uses the create_admin_user fixture to create an admin user and then makes a POST request to the
    /login endpoint to obtain an authentication token for the admin user. Returns the token as a string.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_admin_user (function): The fixture function to create an admin user.

    Returns:
        str: The authentication token for the admin user.
    """
    response = test_client.post(
        "/login", json={"user_name": "admin", "password": "adminpassword"}
    )
    return response.json.get("token")


# User Endpoints Tests
def test_add_user_success(test_client, create_user):
    """
    Test the successful creation of a user.

    Verifies that a POST request to the /users endpoint with valid user data
    results in a 201 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_user (function): Fixture function to create a user.
    """
    response = create_user("john_doe", "securepassword", "user")
    assert response.status_code == 201
    assert response.json == {"message": "User added successfully"}


def test_get_user_success(test_client, login_user):
    """
    Test retrieving user details successfully.

    Verifies that a GET request to the /users/{id} endpoint with a valid token
    returns the user details with a 200 status code.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
    token = login_user("john_doe", "securepassword")

    response = test_client.get("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json == {"user_name": "john_doe", "role": "user"}


def test_add_user_missing_fields(test_client, create_user):
    """
    Test user creation with missing fields.

    Verifies that a POST request to the /users endpoint with missing required fields
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_user (function): Fixture function to create a user.
    """
    response = test_client.post("/users", json={"user_name": "john_doe"})
    assert response.status_code == 400
    print(response.json["error"])
    assert response.json["error"] == "Password cannot be empty"


def test_login_success(test_client, create_user):
    """
    Test successful user login.

    Verifies that a POST request to the /login endpoint with valid credentials
    returns a 200 status code and a token.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_user (function): Fixture function to create a user.
    """
    create_user("john_doe", "securepassword", "user")

    response = test_client.post(
        "/login", json={"user_name": "john_doe", "password": "securepassword"}
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "token" in json_data


def test_login_missing_user_name(test_client, create_user):
    """
    Test login with missing username.

    Verifies that a POST request to the /login endpoint with missing username
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_user (function): Fixture function to create a user.
    """
    create_user("john_doe", "securepassword", "user")

    response = test_client.post("/login", json={"password": "securepassword"})

    assert response.status_code == 400
    json_data = response.get_json()
    print(json_data)
    assert json_data["error"] == "Username and password are required"


def test_login_missing_password(test_client, create_user):
    """
    Test login with missing password.

    Verifies that a POST request to the /login endpoint with missing password
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_user (function): Fixture function to create a user.
    """
    create_user("john_doe", "securepassword", "user")

    response = test_client.post("/login", json={"user_name": "john_doe"})

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "Username and password are required"


def test_login_invalid_credentials(test_client, create_user):
    """
    Test login with invalid credentials.

    Verifies that a POST request to the /login endpoint with incorrect password
    results in a 401 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_user (function): Fixture function to create a user.
    """

    create_user("john_doe", "securepassword", "user")

    response = test_client.post(
        "/login", json={"user_name": "john_doe", "password": "wrong_password"}
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["error"] == "Invalid username or password"


def test_login_non_existent_user(test_client):
    """
    Test login for a non-existent user.

    Verifies that a POST request to the /login endpoint with a non-existent username
    results in a 401 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
    """
    response = test_client.post(
        "/login", json={"user_name": "non_existent_user", "password": "some_password"}
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["error"] == "Invalid username or password"


def test_get_product_success(test_client, admin_token):
    """
    Test retrieving product details successfully.

    Verifies that a GET request to the /products/{id} endpoint with a valid admin token
    returns the product details with a 200 status code.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        admin_token (str): The admin token obtained via login.
    """

    test_client.post(
        "/products",
        json={"name": "Product1", "price": 10.0},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = test_client.get("/products/1")
    assert response.status_code == 200
    assert response.json == {"name": "Product1", "price": 10.0}


def test_get_product_not_found(test_client):
    """
    Test retrieving a non-existent product.

    Verifies that a GET request to the /products/{id} endpoint for a non-existent product
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
    """
    response = test_client.get("/products/999")
    assert response.status_code == 400
    assert response.json["error"] == "Product with ID 999 not found"


# Cart Endpoints Tests
def test_create_cart_success(test_client, login_user):
    """
    Test successful cart creation.

    Verifies that a POST request to the /carts endpoint with a valid user token
    results in a 201 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
    token = login_user("john_doe", "securepassword")
    response = test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.json == {"message": "Cart created successfully"}


def test_get_cart_success(test_client, login_user):
    """
    Test retrieving cart details successfully.

    Verifies that a GET request to the /carts/{id} endpoint with a valid token
    returns the cart details with a 200 status code.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
    token = login_user("john_doe", "securepassword")
    test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})
    response = test_client.get("/carts/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json == {"cart_id": 1, "user_id": 1}


def test_get_cart_not_found(test_client, login_user):
    """
    Test retrieving a non-existent cart.

    Verifies that a GET request to the /carts/{id} endpoint for a non-existent cart
    results in a 404 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
    token = login_user("john_doe", "securepassword")
    test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})
    response = test_client.get(
        "/carts/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Cart with ID 999 does not exist"


# Cart Item Endpoints Tests
def test_add_cart_item_success(test_client, login_user, admin_token):
    """
    Test successfully adding an item to a cart.

    Verifies that a POST request to the /carts/{id}/items endpoint with valid data and a token
    results in a 201 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
        admin_token (str): The admin token obtained via login.
    """
    test_client.post(
        "/products",
        json={"name": "Product1", "price": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/carts/1/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Item added to cart successfully"}


def test_list_cart_items_success(test_client, login_user, admin_token):
    """
    Test listing items in a cart successfully.

    Verifies that a GET request to the /carts/{id}/items endpoint with a valid token
    returns the cart items with a 200 status code.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
        admin_token (str): The admin token obtained via login.
    """

    test_client.post(
        "/products",
        json={"name": "Product1", "price": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

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
    """
    Test adding an item to the cart with missing product ID.

    Verifies that a POST request to the /carts/{id}/items endpoint with missing product ID
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
    test_client.post("/products", json={"name": "Product1", "price": 5})

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/carts/1/items",
        json={"quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json["error"] == "Product ID is required"


def test_remove_cart_item_success(test_client, login_user, admin_token):
    """
    Test successfully removing an item from the cart.

    Verifies that a DELETE request to the /cart_items/{id} endpoint with a valid token
    results in a 200 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
        admin_token (str): The admin token obtained via login.
    """
    test_client.post(
        "/products",
        json={"name": "Product1", "price": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

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
    """
    Test successful order creation.

    Verifies that a POST request to the /orders endpoint with a valid order status and token
    results in a 201 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
    token = login_user("john_doe", "securepassword")

    response = test_client.post(
        "/orders",
        json={"order_status": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Order created successfully"}


def test_get_order_success(test_client, login_user):
    """
    Test retrieving order details successfully.

    Verifies that a GET request to the /orders/{id} endpoint with a valid token
    returns the order details with a 200 status code.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
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
    """
    Test retrieving a non-existent order.

    Verifies that a GET request to the /orders/{id} endpoint for a non-existent order
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
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
def test_add_order_item_success(test_client, login_user, admin_token):
    """
    Test successfully adding an item to an order.

    Verifies that a POST request to the /orders/{id}/items endpoint with valid product ID, quantity, and price
    results in a 201 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
        admin_token (str): The admin token obtained via login.
    """
    product_price = 5
    test_client.post(
        "/products",
        json={"name": "Product1", "price": product_price},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    token = login_user("john_doe", "securepassword")
    response = test_client.post(
        "/orders/1/items",
        json={"product_id": 1, "quantity": 2, "price": product_price},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Item added to order successfully"}


def test_list_order_items_success(test_client, login_user, admin_token):
    """
    Test listing items in an order successfully.

    Verifies that a GET request to the /orders/{id}/items endpoint with a valid token
    returns the order items with a 200 status code.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
        admin_token (str): The admin token obtained via login.
    """
    product_price = 5
    test_client.post(
        "/products",
        json={"name": "Product1", "price": product_price},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

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


def test_place_order_success(test_client, login_user, admin_token):
    """
    Test successful placement of an order.

    Verifies that a POST request to the /orders/finish endpoint with a valid cart ID and token
    results in a 201 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
        admin_token (str): The admin token obtained via login.
    """
    test_client.post(
        "/products",
        json={"name": "Product1", "price": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    token = login_user("john_doe", "securepassword")
    test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})
    test_client.post(
        "/carts/1/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Place the order
    response = test_client.post(
        "/orders/finish",
        json={"cart_id": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert successful order placement
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Order placed successfully"
    assert "order_id" in data


def test_place_order_wrong_cart_id(test_client, login_user, admin_token):
    """
    Test placing an order with an incorrect cart ID.

    Verifies that a POST request to the /orders/finish endpoint with a non-existent cart ID
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
        admin_token (str): The admin token obtained via login.
    """
    test_client.post(
        "/products",
        json={"name": "Product1", "price": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    token = login_user("john_doe", "securepassword")
    test_client.post("/carts", headers={"Authorization": f"Bearer {token}"})
    test_client.post(
        "/carts/1/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Place the order
    cart_id = 2
    response = test_client.post(
        "/orders/finish",
        json={"cart_id": cart_id},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert successful order placement
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == f"Cart with ID {cart_id} does not exist"


# Admin acess related Tests


def test_create_product_success(test_client, admin_token):
    """
    Test successful product creation by an admin user.

    Verifies that a POST request to the /products endpoint with valid product data and admin token
    results in a 201 status code.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        admin_token (str): The admin token obtained via login.
    """
    response = test_client.post(
        "/products",
        json={"name": "Test Product", "price": 10.0},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201


def test_create_product_unauthorized(test_client, login_user):
    """
    Test failure when a non-admin user tries to create a product.

    Verifies that a POST request to the /products endpoint with a non-admin token
    results in a 403 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        login_user (function): Fixture function to log in a user and get a token.
    """
    token = login_user("john_doe", "password")

    response = test_client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Product", "price": 10.0},
    )
    assert response.status_code == 403
    assert response.json == {
        "error": "You do not have permission to access this resource"
    }


def test_create_product_invalid_data(test_client, create_admin_user):
    """
    Test failure when creating a product with invalid data.

    Verifies that a POST request to the /products endpoint with missing or invalid product data
    results in a 400 status code and appropriate error messages.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_admin_user (function): Fixture function to create an admin user and get a token.
    """
    response = test_client.post(
        "/login", json={"user_name": "admin", "password": "adminpassword"}
    )

    token = response.json.get("token")
    # Test with missing name
    response = test_client.post(
        "/products", headers={"Authorization": f"Bearer {token}"}, json={"price": 10.0}
    )

    assert response.status_code == 400
    assert response.json == {"error": "Product name cannot be empty"}

    # Test with invalid price
    response = test_client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Product", "price": -10.0},
    )
    assert response.status_code == 400
    assert response.json == {"error": "Price must be a positive number"}


def test_update_product_success(test_client, create_admin_user):
    """
    Test successful product update by an admin user.

    Verifies that a PUT request to the /products/{id} endpoint with valid update data and admin token
    results in a 200 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_admin_user (function): Fixture function to create an admin user and get a token.
    """
    response = test_client.post(
        "/login", json={"user_name": "admin", "password": "adminpassword"}
    )

    token = response.json.get("token")
    # Create a product to update
    test_client.post(
        "/products",
        json={"name": "Old Product", "price": 10.0},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Update the product
    response = test_client.put(
        "/products/1",
        json={"name": "Updated Product", "price": 20.0},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json == {"message": "Product updated successfully"}


def test_update_product_not_found(test_client, create_admin_user):
    """
    Test updating a non-existing product.

    Verifies that a PUT request to the /products/{id} endpoint for a non-existent product
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_admin_user (function): Fixture function to create an admin user and get a token.
    """
    response = test_client.post(
        "/login", json={"user_name": "admin", "password": "adminpassword"}
    )

    token = response.json.get("token")
    # Attempt to update a non-existing product
    response = test_client.put(
        "/products/999",
        json={"name": "Non-Existent Product", "price": 20.0},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Product with ID 999 not found"}


def test_update_product_invalid_data(test_client, create_admin_user):
    """
    Test updating a product with invalid data.

    Verifies that a PUT request to the /products/{id} endpoint with invalid product data
    results in a 400 status code and appropriate error messages.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_admin_user (function): Fixture function to create an admin user and get a token.
    """
    response = test_client.post(
        "/login", json={"user_name": "admin", "password": "adminpassword"}
    )

    token = response.json.get("token")
    # Create a product to update
    test_client.post(
        "/products",
        json={"name": "Valid Product", "price": 10.0},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Attempt to update the product with invalid price
    response = test_client.put(
        "/products/1",
        json={"name": "Updated Product", "price": "invalid_price"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Price must be a valid number"}


def test_delete_product_success(test_client, create_admin_user):
    """
    Test successful product deletion by an admin user.

    Verifies that a DELETE request to the /products/{id} endpoint with a valid product ID and admin token
    results in a 200 status code and the appropriate success message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_admin_user (function): Fixture function to create an admin user and get a token.
    """
    response = test_client.post(
        "/login", json={"user_name": "admin", "password": "adminpassword"}
    )

    token = response.json.get("token")
    # Create a product to delete
    test_client.post(
        "/products",
        json={"name": "Product to Delete", "price": 10.0},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Delete the product
    response = test_client.delete(
        "/products/1", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json == {"message": "Product deleted successfully"}


def test_delete_product_not_found(test_client, create_admin_user):
    """
    Test deleting a non-existing product.

    Verifies that a DELETE request to the /products/{id} endpoint for a non-existent product
    results in a 400 status code and an appropriate error message.

    Args:
        test_client (FlaskClient): The Flask test client instance.
        create_admin_user (function): Fixture function to create an admin user and get a token.
    """
    response = test_client.post(
        "/login", json={"user_name": "admin", "password": "adminpassword"}
    )

    token = response.json.get("token")
    # Attempt to delete a non-existing product
    response = test_client.delete(
        "/products/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json == {"error": "Product with ID 999 not found"}
