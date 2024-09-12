# -*- coding: utf-8 -*-
from datetime import datetime


class User:
    """
    User model for representing a user in the system. Handles basic data and acess control.

    The model validates all the attributes.

    Attributes:
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
        The role of the user, either 'admin' or 'user'. Defaults to less privilege role'user'

    Raises:
    ------
    ValueError:
        If user_id is not greater than zero.
        If user_name or password is empty.
        If created_at is not a valid datetime object.
        If role is not 'admin' or 'user'.

    """

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
    """
    Product model for representing a product available for purchase. Handles basic product data.

    The model validates all the attributes, apart from description.

    Attributes:
    ----------
    product_id : int
        A unique identifier for the product.
    product_name : str
        The name of the product.
    description : str
        A short description of the product.
    price : int
        The price of the product per unit.
    created_at : datetime
        The timestamp when the product was added to the system.

    Raises:
    ------
    ValueError:
        If product_id is not greater than zero.
        If product_name or description is empty.
        If price is not greater than zero.
        If created_at is not a valid datetime object.
    """

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

        if product_id <= 0:
            raise ValueError("Product ID must be greater than zero")
        if not product_name:
            raise ValueError("Product name cannot be empty")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a valid datetime object")


class Cart:
    """
    Cart model for representing a shopping cart associated with a user. Handles cart-level data.

    The model validates all the attributes to ensure proper cart structure.

    Attributes:
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
        If cart_id or user_id is not greater than zero.
        If created_at is not a valid datetime object.
    """

    def __init__(self, cart_id: int, user_id: int, created_at: datetime = None) -> None:
        if cart_id <= 0:
            raise ValueError("Cart ID must be greater than zero")
        if user_id <= 0:
            raise ValueError("User ID must be greater than zero")
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a valid datetime object")

        self.cart_id = cart_id
        self.user_id = user_id
        self.created_at = created_at or datetime.now()


class CartItem:
    """
    CartItem model for representing individual items in a shopping cart. Handles item-level data within a cart.

    The model validates all the attributes to ensure valid cart item structure.

    Attributes:
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
        If cart_item_id, cart_id, or product_id is not greater than zero.
        If quantity is not greater than zero.
        If added_at is not a valid datetime object.
    """

    def __init__(
        self,
        cart_item_id: int,
        cart_id: int,
        product_id: int,
        quantity: int,
        added_at: datetime = None,
    ) -> None:
        if cart_item_id <= 0:
            raise ValueError("Cart item ID must be greater than zero")
        if cart_id <= 0:
            raise ValueError("Cart ID must be greater than zero")
        if product_id <= 0:
            raise ValueError("Product ID must be greater than zero")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if added_at and not isinstance(added_at, datetime):
            raise ValueError("Added at must be a valid datetime object")

        self.cart_item_id = cart_item_id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.added_at = added_at


class Order:
    """
    Order model for representing a customer's order in the system. Handles order-level data.

    The model validates the attributes to ensure proper order structure.

    Attributes:
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
        If order_id or user_id is not greater than zero.
        If order_status is not True or False.
        If created_at is not a valid datetime object.
    """

    def __init__(
        self,
        order_id: int,
        user_id: int,
        order_status: bool,
        created_at: datetime = None,
    ) -> None:
        if order_id <= 0:
            raise ValueError("Order ID must be greater than zero")
        if user_id <= 0:
            raise ValueError("User ID must be greater than zero")
        if order_status not in {True, False}:
            raise ValueError("Order status must be true or false")
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a valid datetime object")

        self.order_id = order_id
        self.user_id = user_id
        self.order_status = order_status
        self.created_at = created_at or datetime.now()


class OrderItem:
    """
    OrderItem model for representing individual items in an order. Handles item-level data within an order.

    The model validates all the attributes to ensure valid order item structure.

    Attributes:
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
        If order_item_id, order_id, or product_id is not greater than zero.
        If quantity or price is not greater than zero.
        If created_at is not a valid datetime object.
    """

    def __init__(
        self,
        order_item_id: int,
        order_id: int,
        product_id: id,
        quantity: int,
        price: int,
        created_at: datetime = None,
    ) -> None:
        if order_item_id <= 0:
            raise ValueError("Order item ID must be greater than zero")

        if order_id <= 0:
            raise ValueError("Order ID must be greater than zero")

        if product_id <= 0:
            raise ValueError("Product ID must be greater than zero")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if price <= 0:
            raise ValueError("Price must be a positive number")
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a valid datetime object")

        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.created_at = created_at
