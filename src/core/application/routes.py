# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
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
    app,
    db,
    User,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# Validation functions
def validate_user_name_password(data):
    user_name = data.get("user_name", "").strip()
    password = data.get("password", "").strip()
    if not user_name:
        raise BadRequest("User name cannot be empty")
    if not password:
        raise BadRequest("Password cannot be empty")
    return user_name, password


def validate_role(data):
    role = data.get("role")
    if role not in ["admin", "user"]:
        raise BadRequest('Invalid role value. Must be "admin" or "user".')
    return role


def validate_price(data):
    try:
        price = float(data.get("price"))
        if price <= 0:
            raise BadRequest("Price must be a positive number")
    except (TypeError, ValueError):
        raise BadRequest("Price must be a valid number")
    return price


def validate_name(data):
    name = data.get("name", "").strip()
    if not name:
        raise BadRequest("Product name cannot be empty")
    return name


def validate_quantity(data):
    try:
        quantity = int(data.get("quantity"))
        if quantity <= 0:
            raise BadRequest("Quantity must be a positive number")
    except (TypeError, ValueError):
        raise BadRequest("Quantity must be a valid number")
    return quantity


def validate_order_status(data):
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
@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.get_json()
        user_name, password = validate_user_name_password(data)
        role = validate_role(data)
        user = User(user_name=user_name, password=password, role=role)
        user_adapter.create_account(user)
        return jsonify({"message": "User added successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = user_adapter.get_user(user_id=user_id)
        if not user:
            raise BadRequest(f"User with ID {user_id} not found")
        return jsonify({"user_name": user.user_name, "role": user.role})
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


# Product Endpoints
@app.route("/products", methods=["POST"])
def create_product():
    try:
        data = request.get_json()
        name = validate_name(data)
        price = validate_price(data)
        product = Product(product_name=name, price=price)
        product_adapter.create_product(product=product)
        return jsonify({"message": "Product added successfully"}), 201
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = product_adapter.get_product(product_id=product_id)
        if not product:
            raise BadRequest(f"Product with ID {product_id} not found")
        return jsonify({"name": product.product_name, "price": product.price})
    except BadRequest as e:
        return jsonify({"error": str(e.description)}), 400


# Cart Endpoints
@app.route("/carts", methods=["POST"])
def add_cart():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            raise BadRequest("User ID is required")
        user = user_adapter.get_user(user_id=user_id)
        print(user)
        if not user:
            raise BadRequest(f"User with ID {user_id} not found")
        cart = Cart(user_id=user_id)
        cart_adapter.add_cart(cart=cart)
        return jsonify({"message": "Cart created successfully"}), 201
    except BadRequest as e:
        print(str(e))
        return jsonify({"error": str(e.description)}), 400


@app.route("/carts/<int:cart_id>", methods=["GET"])
def get_cart(cart_id):
    try:
        cart = cart_adapter.get_cart(cart_id=cart_id)
        return jsonify({"cart_id": cart.cart_id, "user_id": cart.user_id})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Cart Item Endpoints
@app.route("/carts/<int:cart_id>/items", methods=["POST"])
def add_cart_item(cart_id):
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
        print(str(e))
        return jsonify({"error": str(e.description)}), 400


@app.route("/carts/<int:cart_id>/items", methods=["GET"])
def list_cart_items(cart_id):
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


@app.route("/cart_items/<int:cart_item_id>", methods=["DELETE"])
def remove_cart_item(cart_item_id):
    try:
        cart_item_adapter.delete_cart_item(cart_item_id=cart_item_id)
        return jsonify({"message": "Cart item removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Order Endpoints
@app.route("/orders", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
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


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order = order_adapter.get_order(order_id=order_id)
        return jsonify({"order_id": order.order_id, "status": order.order_status})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Order Item Endpoints
@app.route("/orders/<int:order_id>/items", methods=["POST"])
def add_order_item(order_id):
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
        print(e)
        return jsonify({"error": str(e.description)}), 400


@app.route("/orders/<int:order_id>/items", methods=["GET"])
def list_order_items(order_id):
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


@app.route("/orders/finish", methods=["POST"])
def place_order():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            raise BadRequest("User ID is required")

        order_id = order_service.place_order(user_id=user_id)
        return (
            jsonify({"message": "Order placed successfully", "order_id": order_id}),
            201,
        )

    except ValueError as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400
    except BadRequest as e:
        print(str(e))
        return jsonify({"error": str(e.description)}), 400


if __name__ == "__main__":
    app.run(debug=True)
