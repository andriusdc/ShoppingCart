# -*- coding: utf-8 -*-
from datetime import datetime


class User:
    def __init__(
        self,
        user_id: int,
        user_name: str,
        password: str,
        created_at: datetime = None,
        role: str = "user",
    ) -> None:
        if user_id <= 0:
            raise ValueError("User ID must be greater than zero")
        if not user_name:
            raise ValueError("User name cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a valid datetime object")
        if role not in {"admin", "user"}:
            raise ValueError("Role must be 'user' or 'admin'")

        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.created_at = created_at or datetime.now()
        self.role = role

        print("/n")
        print(f"created_at: {created_at}")
        print(f"role: {role}")


class Product:
    def __init__(
        self,
        product_id: int,
        product_name: str,
        description: str,
        price: int,
        created_at: datetime = None,
    ) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price
        self.created_at = created_at or datetime.now()


class Cart:
    def __init__(self, cart_id: int, user_id: int, created_at: datetime = None) -> None:
        self.cart_id = cart_id
        self.user_id = user_id
        self.created_at = created_at or datetime.now()


class CartItem:
    def __init__(
        self,
        cart_item_id: int,
        cart_id: int,
        product_id: int,
        quantity: int,
        added_at: datetime = None,
    ) -> None:
        self.cart_item_id = cart_item_id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.added_at = added_at


class Order:
    def __init__(
        self,
        order_id: int,
        user_id: int,
        order_status: bool,
        created_at: datetime = None,
    ) -> None:
        self.order_id = order_id
        self.user_id = user_id
        self.order_status = order_status
        self.created_at = created_at or datetime.now()


class OrderItem:
    def __init__(
        self,
        order_item_id: int,
        order_id: int,
        product_id: id,
        quantity: int,
        price: int,
        created_at: datetime = None,
    ) -> None:
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.created_at = created_at
