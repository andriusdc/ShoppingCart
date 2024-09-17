# -*- coding: utf-8 -*-
from flask import request, jsonify, Blueprint
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from werkzeug.exceptions import BadRequest, Forbidden
from flask_sqlalchemy import SQLAlchemy
from src.adapters.user_adapter import UserAdapter
from src.adapters.product_adapter import ProductAdapter
from src.adapters.cart_adapter import CartAdapter
from src.adapters.cart_item_adapter import CartItemAdapter
from src.adapters.order_adapter import OrderAdapter
from src.adapters.order_item_adapter import OrderItemAdapter
from src.core.application.password_service import PasswordService
from src.core.application.order_service import OrderService
from src.core.domain.models import (
    User,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)

from functools import wraps
import os
from datetime import datetime, timedelta


main = Blueprint("main", __name__)


def role_required(required_role):
    """
    Role-based authorization decorator.

    This decorator ensures that the current user has the required role to access a specific resource.
    If the user's role does not match the required role, an error response with a 403 status code is returned.

    :param required_role: The role required to access the resource (e.g., 'admin').
    :return: A decorator that checks user role before allowing access to the decorated function.
    """

    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_role = current_user.get("role")

            if user_role != required_role:
                return (
                    jsonify(
                        {"error": "You do not have permission to access this resource"}
                    ),
                    403,
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator


# Validation functions
def validate_user_name_password(data):
    """
    Validate user name and password input.

    This function checks whether the user_name and password fields are present in the input data and are not empty.

    :param data: The input dictionary containing 'user_name' and 'password' fields.
    :return: A tuple containing the validated user_name and password.
    :raises BadRequest: If user_name or password are missing or empty.
    """
    user_name = data.get("user_name", "").strip()
    password = data.get("password", "").strip()
    if not user_name:
        raise BadRequest("User name cannot be empty")
    if not password:
        raise BadRequest("Password cannot be empty")
    return user_name, password


def validate_role(data):
    """
    Validate the user's role.

    This function checks whether the provided role is either 'admin' or 'user'.

    :param data: The input dictionary containing the 'role' field.
    :return: The validated role.
    :raises BadRequest: If the role is not 'admin' or 'user'.
    """
    role = data.get("role")
    if role not in ["admin", "user"]:
        raise BadRequest('Invalid role value. Must be "admin" or "user".')
    return role


def validate_price(data):
    """
    Validate the price field.

    This function ensures that the price is a positive float value.

    :param data: The input dictionary containing the 'price' field.
    :return: The validated price as a float.
    :raises BadRequest: If the price is missing, not a valid number, or less than or equal to zero.
    """
    try:
        price = float(data.get("price"))
        if price <= 0:
            raise BadRequest("Price must be a positive number")
    except (TypeError, ValueError):
        raise BadRequest("Price must be a valid number")
    return price


def validate_name(data):
    """
    Validate the product name.

    This function checks whether the 'name' field is present and not empty.

    :param data: The input dictionary containing the 'name' field.
    :return: The validated product name.
    :raises BadRequest: If the name is missing or empty.
    """
    name = data.get("name", "").strip()
    if not name:
        raise BadRequest("Product name cannot be empty")
    return name


def validate_quantity(data):
    """
    Validate the quantity field.

    This function ensures that the quantity is a positive integer.

    :param data: The input dictionary containing the 'quantity' field.
    :return: The validated quantity as an integer.
    :raises BadRequest: If the quantity is missing, not a valid number, or less than or equal to zero.
    """
    try:
        quantity = int(data.get("quantity"))
        if quantity <= 0:
            raise BadRequest("Quantity must be a positive number")
    except (TypeError, ValueError):
        raise BadRequest("Quantity must be a valid number")
    return quantity


def validate_order_status(data):
    """
    Validate the order status field.

    This function ensures that the order status is either True or False.

    :param data: The input dictionary containing the 'order_status' field.
    :return: The validated order status as a boolean.
    :raises BadRequest: If the order status is not True or False.
    """
    status = data.get("order_status")
    if status not in [True, False]:
        raise BadRequest("Order status must be True or False")
    return status


# Adapters
user_adapter = UserAdapter(password_service=PasswordService())
product_adapter = ProductAdapter()
cart_adapter = CartAdapter()
cart_item_adapter = CartItemAdapter()
order_adapter = OrderAdapter()
order_item_adapter = OrderItemAdapter()
order_service = OrderService(
    user_adapter,
    product_adapter,
    cart_adapter,
    cart_item_adapter,
    order_adapter,
    order_item_adapter,
)


# User Endpoints


@main.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and generate a JWT token.

    This endpoint expects a JSON body containing the user's credentials:
    - `user_name` (string): The username of the user.
    - `password` (string): The password of the user.

    Returns:
        200: A JSON response containing the generated JWT token if authentication is successful.
        400: A JSON response with an error message if validation fails.
        401: A JSON response with an error message if authentication fails.
    """
    try:
        data = request.get_json()

        # Validate user credentials
        user_name = data.get("user_name")
        password = data.get("password")

        if not user_name or not password:
            raise BadRequest("Username and password are required")
        # Retrieve the user from the database
        user = user_adapter.login_account(user_name, password)
        # Generate JWT token with user ID and role
        token = create_access_token(
            identity={"user_id": user.user_id, "role": user.role},
            expires_delta=timedelta(hours=1),
        )
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    # Return the token in the response
    return jsonify({"token": token}), 200


@main.route("/users", methods=["POST"])
def add_user():
    """
    Create a new user.

    This endpoint expects a JSON body containing the user's details:
    - `user_name` (string): The username of the new user.
    - `password` (string): The password for the new user.
    - `role` (string): The role of the user ("admin" or "user").
    Only "user" can be created by regular users, but functionallity was mantained for future implementations which may permit admin users to create other admin users

    Returns:
        201: A JSON response with a success message if the user is created.
        400: A JSON response with an error message if validation or creation fails.
    """
    try:
        data = request.get_json()
        user_name, password = validate_user_name_password(data)
        role = validate_role(data)
        if role == "admin":
            raise BadRequest("You are not permited to create admin role user")
        user = User(user_name=user_name, password=password, role=role)
        user_adapter.create_account(user)
        return jsonify({"message": "User added successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    """
    Retrieve user information based on the user ID from the JWT.

    Returns:
        200: A JSON response with the user's information (username and role).
        400: A JSON response with an error message if the user is not found.
    """
    try:
        # Get the identity of the current user from the JWT token
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        # Fetch the user information
        user = user_adapter.get_user(user_id=user_id)
        if not user:
            raise BadRequest(f"User with ID {user_id} not found")

        return jsonify({"user_name": user.user_name, "role": user.role})
    except BadRequest as e:
        print(str(e.description))
        return jsonify({"error": str(e.description)}), 400


# Product Endpoints
@main.route("/products", methods=["POST"])
@role_required("admin")
def create_product():
    """
    Create a new product. (Admin only)

    This endpoint expects a JSON body containing the product's details:
    - `name` (string): The name of the product.
    - `price` (float): The price of the product.

    Returns:
        201: A JSON response with a success message if the product is created.
        400: A JSON response with an error message if validation or creation fails.
    """
    try:
        data = request.get_json()
        name = validate_name(data)
        price = validate_price(data)
        product = Product(product_name=name, price=price)
        product_adapter.create_product(product=product)
        return jsonify({"message": "Product added successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a product's information.

    Returns:
        200: A JSON response with the product's details (name and price).
        400: A JSON response with an error message if the product is not found.
    """
    try:
        product = product_adapter.get_product(product_id=product_id)
        if not product:
            raise BadRequest(f"Product with ID {product_id} not found")
        return jsonify({"name": product.product_name, "price": product.price})
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/products/<int:product_id>", methods=["PUT"])
@role_required("admin")
def update_product(product_id):
    """
    Update an existing product's details. (Admin only)

    This endpoint expects a JSON body containing the updated product details:
    - `name` (string): The new name of the product.
    - `price` (float): The new price of the product.

    Returns:
        200: A JSON response with a success message if the product is updated.
        400: A JSON response with an error message if validation or updating fails.
        500: A JSON response with an error message for internal errors.
    """
    try:
        data = request.get_json()
        name = validate_name(data)
        price = validate_price(data)

        # Fetch the existing product
        product = product_adapter.get_product(product_id=product_id)
        if not product:
            raise BadRequest(f"Product with ID {product_id} not found")

        # Update product details
        product.product_name = name
        product.price = price
        product_adapter.update_product(product=product)

        return jsonify({"message": "Product updated successfully"}), 200
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/products/<int:product_id>", methods=["DELETE"])
@role_required("admin")
def delete_product(product_id):
    """
    Delete a product by its ID. (Admin only)

    Returns:
        200: A JSON response with a success message if the product is deleted.
        400: A JSON response with an error message if the product is not found.
        500: A JSON response with an error message for internal errors.
    """
    try:
        # Fetch the existing product
        product = product_adapter.get_product(product_id=product_id)
        if not product:
            raise BadRequest(f"Product with ID {product_id} not found")

        # Delete the product
        product_adapter.delete_product(product_id=product_id)

        return jsonify({"message": "Product deleted successfully"}), 200
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Cart Endpoints
@main.route("/carts", methods=["POST"])
@jwt_required()
def add_cart():
    """
    Create a new cart for the logged-in user.

    Returns:
        201: A JSON response with a success message if the cart is created.
        400: A JSON response with an error message if the user ID is not valid.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        if not user_id:
            raise BadRequest("User ID is required")

        user = user_adapter.get_user(user_id=user_id)
        if not user:
            raise BadRequest(f"User with ID {user_id} not found")

        cart = Cart(user_id=user_id)
        cart_adapter.add_cart(cart=cart)
        return jsonify({"message": "Cart created successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/carts/<int:cart_id>", methods=["GET"])
@jwt_required()
def get_cart(cart_id):
    """
    Retrieve the details of a cart by its ID.

    Returns:
        200: A JSON response with the cart's details (cart ID and user ID).
        401: A JSON response with an error message if the user is unauthorized.
        404: A JSON response with an error message if the cart is not found.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        cart = cart_adapter.get_cart(cart_id=cart_id)
        if cart.user_id != user_id:
            raise BadRequest("Unauthorized access to this cart")

        return jsonify({"cart_id": cart.cart_id, "user_id": cart.user_id})
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 401
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Cart Item Endpoints
@main.route("/carts/<int:cart_id>/items", methods=["POST"])
@jwt_required()
def add_cart_item(cart_id):
    """
    Add an item to a cart.

    Args:
        cart_id (int) : ID of the cart for adding items

    This endpoint expects a JSON body containing:
    - `product_id` (int): The ID of the product to be added.
    - `quantity` (int): The quantity of the product.

    Returns:
        201: A JSON response with a success message if the item is added to the cart.
        400: A JSON response with an error message if the product or quantity is invalid.
    """
    try:
        data = request.get_json()
        product_id = data.get("product_id")
        if not product_id:
            raise BadRequest("Product ID is required")
        quantity = validate_quantity(data)
        product = product_adapter.get_product(product_id=product_id)
        if not product:
            raise BadRequest(f"Product with ID {product_id} not found")
        cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        cart_item_adapter.add_cart_item(cart_item=cart_item)
        return jsonify({"message": "Item added to cart successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/carts/<int:cart_id>/items", methods=["GET"])
@jwt_required()
def list_cart_items(cart_id):
    """
    Retrieve a list of items in a cart.

    Args:
    cart_item_id (int): The ID of the cart item to list.

    Returns:
        200: A JSON response containing a list of cart items.
        400: A JSON response with an error message if the cart is not found.
    """
    try:
        items = cart_item_adapter.list_cart_items(cart_id=cart_id)
        if not items:
            raise BadRequest("Cart ID not found")
        return jsonify(
            [
                {"product_id": item.product_id, "quantity": item.quantity}
                for item in items
            ]
        )
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/cart_items/<int:cart_item_id>", methods=["DELETE"])
@jwt_required()
def remove_cart_item(cart_item_id):
    """
    Remove an item from the user's cart.

    Deletes the specified cart item from the cart.

    Args:
        cart_item_id (int): The ID of the cart item to remove.

    Returns:
        200: A JSON response with a success message if the item is successfully removed.
        500: A JSON response with an error message if something goes wrong.
    """
    try:
        cart_item_adapter.delete_cart_item(cart_item_id=cart_item_id)
        return jsonify({"message": "Cart item removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Order Endpoints
@main.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    """
    Create a new order for the logged-in user.

    This endpoint expects a JSON body containing:
    - `order_status` (boolean): The status of the order (True or False).

    The order will be created for the logged-in user.

    Returns:
        201: A JSON response with a success message and the order ID if the order is created.
        400: A JSON response with an error message if validation fails or the user is not found.
    """
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        if not user_id:
            raise BadRequest("User ID is required")

        order_status = validate_order_status(data)
        user = user_adapter.get_user(user_id=user_id)
        if not user:
            raise BadRequest(f"User with ID {user_id} not found")

        order = Order(user_id=user_id, order_status=order_status)
        order_adapter.add_order(order=order)
        return jsonify({"message": "Order created successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    """
    Retrieve the details of a specific order.

    Args:
        order_id (int): The ID of the order to retrieve.

    Returns:
        200: A JSON response with the order ID and status if the order is found.
        400: A JSON response with an error message if the order is not found.
    """
    try:
        order = order_adapter.get_order(order_id=order_id)
        return jsonify({"order_id": order.order_id, "status": order.order_status})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Order Item Endpoints
@main.route("/orders/<int:order_id>/items", methods=["POST"])
@jwt_required()
def add_order_item(order_id):
    """
    Add an item to an existing order.

    This endpoint expects a JSON body containing:
    - `product_id` (int): The ID of the product to add.
    - `quantity` (int): The quantity of the product.
    - `price` (float): The price of the product.

    Args:
        order_id (int): The ID of the order to add the item to.

    Returns:
        201: A JSON response with a success message if the item is added.
        400: A JSON response with an error message if validation fails or the product is not found.
    """
    try:
        data = request.get_json()
        product_id = data.get("product_id")
        if not product_id:
            raise BadRequest("Product ID is required")
        quantity = validate_quantity(data)
        price = validate_price(data)
        product = product_adapter.get_product(product_id=product_id)
        if not product:
            raise BadRequest(f"Product with ID {product_id} not found")

        order_item = OrderItem(
            order_id=order_id, product_id=product_id, quantity=quantity, price=price
        )
        order_item_adapter.add_order_item(order_item=order_item)
        return jsonify({"message": "Item added to order successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@main.route("/orders/<int:order_id>/items", methods=["GET"])
@jwt_required()
def list_order_items(order_id):
    """
    List all items in a specific order.

    Args:
        order_id (int): The ID of the order to list items for.

    Returns:
        200: A JSON response with a list of order items.
        500: A JSON response with an error message if something goes wrong.
    """
    try:
        items = order_item_adapter.list_order_items(order_id=order_id)
        return jsonify(
            [
                {"product_id": item.product_id, "quantity": item.quantity}
                for item in items
            ]
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/orders/finish", methods=["POST"])
@jwt_required()
def place_order():
    """
    Finalize and place an order for the logged-in user.

    This endpoint expects a JSON body containing:
    - `cart_id` (int): The ID of the cart to place the order from.

    Returns:
        201: A JSON response with a success message and the order ID if the order is placed.
        400: A JSON response with an error message if validation fails or the cart is not found.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        if not user_id:
            raise BadRequest("User ID is required")
        data = request.get_json()
        cart_id = data.get("cart_id")
        if not cart_id:
            raise BadRequest("Cart ID is required")
        order_id = order_service.place_order(user_id=user_id, cart_id=cart_id)

        return (
            jsonify({"message": "Order placed successfully", "order_id": order_id}),
            201,
        )

    except ValueError as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400
