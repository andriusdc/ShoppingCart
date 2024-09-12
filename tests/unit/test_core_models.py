# -*- coding: utf-8 -*-
import pytest
from datetime import datetime
from src.core.domain.models import User, Product, Cart, CartItem, Order, OrderItem


def test_user_instantiation():
    """
    Test User class instantiation with valid inputs.

    Ensures that the attributes are assigned correctly while instantiating the User
    object and validates them according do pre defined valid values.

    This test checks:
    - If the `User` model is instantiated correctly with valid input values.
    """
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
    """
    Test the validation of user_id in the User model.

    Ensures that the User model throws the 'User ID must be greater than zero' ValueError
    when user_id is less than or equal to zero, ensuring adherence to
    the model's constraints.

    This test checks:
    - If 'user_id' is 0, a 'ValueError' is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        User(user_id=0, user_name="John", password="123", role="user")
    assert str(excinfo.value) == "User ID must be greater than zero"


def test_user_name_validation():
    """
    Test the validation of `user_name` in the `User` model.

    Ensures that the `User` model raises a `ValueError` with the message
    'User name cannot be empty' when `user_name` is an empty string,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `user_name` is an empty string, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="", password="123", role="user")
    assert str(excinfo.value) == "User name cannot be empty"


def test_password_validation():
    """
    Test the validation of `password` in the `User` model.

    Ensures that the `User` model raises a `ValueError` with the message
    'Password cannot be empty' when `password` is an empty string,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `password` is an empty string, a `ValueError` is raised with
      the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="John", password="", role="user")
    assert str(excinfo.value) == "Password cannot be empty"


def test_created_at_validation():
    """
    Test the validation of `created_at` in the `User` model.

    Ensures that the `User` model raises a `ValueError` with the message
    'Created at must be a valid datetime object' when `created_at` is
    not an instance of `datetime`, ensuring adherence to the model's
    constraints.

    This test checks:
    - If `created_at` is not a `datetime` instance, a `ValueError` is raised
      with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="John", password="123", created_at="0", role="user")
    assert str(excinfo.value) == "Created at must be a valid datetime object"


def test_role_validation():
    """
    Test the validation of `role` in the `User` model.

    Ensures that the `User` model raises a `ValueError` with the message
    'Role must be 'user' or 'admin'' when `role` is not one of the allowed values,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `role` is set to 'king', a `ValueError` is raised with the correct
      error message.
    """
    with pytest.raises(ValueError) as excinfo:
        User(user_id=1, user_name="John", password="123", role="king")
    assert str(excinfo.value) == "Role must be 'user' or 'admin'"


def test_product_instantiation():
    """
    Test Product class instantiation with valid inputs.

    Ensures that the attributes are assigned correctly while instantiating the Product
    object and validates them according do pre defined valid values.

    This test checks:
    - If the `Product` model is instantiated correctly with valid input values.
    """
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
    """
    Test the validation of `product_id` in the `Product` model.

    Ensures that the `Product` model raises a `ValueError` with the message
    'Product ID must be greater than zero' when `product_id` is less than
    or equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `product_id` is 0, a `ValueError` is raised with the correct error
      message.
    """
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
    """
    Test the validation of `product_name` in the `Product` model.

    Ensures that the `Product` model raises a `ValueError` with the message
    'Product name cannot be empty' when `product_name` is an empty string,
    ensuring adherence to the model's constraints.

    This test checks:
    - If `product_name` is an empty string, a `ValueError` is raised with
      the correct error message.
    """
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
    """
    Test the validation of `price` in the `Product` model.

    Ensures that the `Product` model raises a `ValueError` with the message
    'Price must be greater than zero' when `price` is less than or equal
    to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `price` is 0, a `ValueError` is raised with the correct error message.
    """
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
    """
    Test the validation of `created_at` in the `Product` model.

    Ensures that the `Product` model raises a `ValueError` with the message
    'Created at must be a valid datetime object' when `created_at` is
    not an instance of `datetime`, ensuring adherence to the model's
    constraints.

    This test checks:
    - If `created_at` is not a `datetime` instance, a `ValueError` is raised
      with the correct error message.
    """
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
    """
    Test Cart class instantiation with valid inputs.

    Ensures that the attributes are assigned correctly while instantiating the Cart
    object and validates them according do pre defined valid values.

    This test checks:
    - If the `Cart` model is instantiated correctly with valid input values.
    """

    created_at = datetime(2024, 9, 11, 0, 0, 0)
    cart = Cart(cart_id=1, user_id=1, created_at=created_at)

    assert cart.cart_id == 1
    assert cart.user_id == 1
    assert cart.created_at == created_at


def test_cart_id_validation():
    """
    Test the validation of `cart_id` in the `Cart` model.

    Ensures that the `Cart` model raises a `ValueError` with the message
    'Cart ID must be greater than zero' when `cart_id` is less than or
    equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `cart_id` is -1, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        Cart(cart_id=-1, user_id=1, created_at=datetime.now())
    assert str(excinfo.value) == "Cart ID must be greater than zero"


def test_cart_user_id_validation():
    """
    Test the validation of `user_id` in the `Cart` model.

    Ensures that the `Cart` model raises a `ValueError` with the message
    'User ID must be greater than zero' when `user_id` is less than or
    equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `user_id` is -1, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        Cart(cart_id=1, user_id=-1, created_at=datetime.now())
    assert str(excinfo.value) == "User ID must be greater than zero"


def test_cart_created_at_validation():
    """
    Test the validation of `created_at` in the `Cart` model.

    Ensures that the `Cart` model raises a `ValueError` with the message
    'Created at must be a valid datetime object' when `created_at` is
    not an instance of `datetime`, ensuring adherence to the model's
    constraints.

    This test checks:
    - If `created_at` is not a `datetime` instance, a `ValueError` is raised
      with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        Cart(cart_id=1, user_id=1, created_at="invalid_date")
    assert str(excinfo.value) == "Created at must be a valid datetime object"


def test_cart_items_instantiation():
    """
    Test CartItems class instantiation with valid inputs.

    Ensures that the attributes are assigned correctly while instantiating the CartItems
    object and validates them according do pre defined valid values.

    This test checks:
    - If the `CartItems` model is instantiated correctly with valid input values.
    """
    added_at = datetime(2024, 9, 11, 0, 0, 0)
    cartItems = CartItem(
        cart_item_id=1, cart_id=1, product_id=2, quantity=1, added_at=added_at
    )

    assert cartItems.cart_item_id == 1
    assert cartItems.cart_id == 1
    assert cartItems.product_id == 2
    assert cartItems.quantity == 1
    assert cartItems.added_at == added_at


def test_cart_item_id_validation():
    """
    Test the validation of `cart_item_id` in the `CartItem` model.

    Ensures that the `CartItem` model raises a `ValueError` with the message
    'Cart Item ID must be greater than zero' when `cart_item_id` is less
    than or equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `cart_item_id` is -1, a `ValueError` is raised with the correct error
      message.
    """
    with pytest.raises(ValueError) as excinfo:
        CartItem(
            cart_item_id=-1,
            cart_id=1,
            product_id=1,
            quantity=1,
            added_at=datetime.now(),
        )
    assert str(excinfo.value) == "Cart item ID must be greater than zero"


def test_cart_item_quantity_validation():
    """
    Test the validation of `quantity` in the `CartItem` model.

    Ensures that the `CartItem` model raises a `ValueError` with the message
    'Quantity must be greater than zero' when `quantity` is less than or
    equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `quantity` is -1, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        CartItem(
            cart_item_id=1,
            cart_id=1,
            product_id=1,
            quantity=-1,
            added_at=datetime.now(),
        )
    assert str(excinfo.value) == "Quantity must be greater than zero"


def test_cart_item_added_at_validation():
    """
    Test the validation of `added_at` in the `CartItem` model.

    Ensures that the `CartItem` model raises a `ValueError` with the message
    'Added at must be a valid datetime object' when `added_at` is
    not an instance of `datetime`, ensuring adherence to the model's
    constraints.

    This test checks:
    - If `added_at` is not a `datetime` instance, a `ValueError` is raised
      with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        CartItem(
            cart_item_id=1, cart_id=1, product_id=1, quantity=1, added_at="invalid_date"
        )
    assert str(excinfo.value) == "Added at must be a valid datetime object"


def test_order_instantiation():
    """
    Test Order class instantiation with valid inputs.

    Ensures that the attributes are assigned correctly while instantiating the Order
    object and validates them according do pre defined valid values.

    This test checks:
    - If the `Order` model is instantiated correctly with valid input values.
    """
    created_at = datetime(2024, 9, 11, 0, 0, 0)
    order = Order(order_id=1, user_id=1, order_status=True, created_at=created_at)

    assert order.order_id == 1
    assert order.user_id == 1
    assert order.order_status == True
    assert order.created_at == created_at


def test_order_id_validation():
    """
    Test the validation of `order_id` in the `Order` model.

    Ensures that the `Order` model raises a `ValueError` with the message
    'Order ID must be greater than zero' when `order_id` is less than
    or equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `order_id` is -1, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        Order(order_id=-1, user_id=1, order_status=True, created_at=datetime.now())
    assert str(excinfo.value) == "Order ID must be greater than zero"


def test_order_user_id_validation():
    """
    Test the validation of `user_id` in the `Order` model.

    Ensures that the `Order` model raises a `ValueError` with the message
    'User ID must be greater than zero' when `user_id` is less than or
    equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `user_id` is -1, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        Order(order_id=1, user_id=-1, order_status=True, created_at=datetime.now())
    assert str(excinfo.value) == "User ID must be greater than zero"


def test_order_order_status_validation():
    """
    Test the validation of `order_status` in the `Order` model.

    Ensures that the `Order` model raises a `ValueError` with the message
    'Order status must be a boolean value' when `order_status` is not a
    boolean value, ensuring adherence to the model's constraints.

    This test checks:
    - If `order_status` is not a boolean, a `ValueError` is raised with the
      correct error message.
    """

    with pytest.raises(ValueError) as excinfo:
        Order(order_id=1, user_id=1, order_status="", created_at=datetime.now())
    assert str(excinfo.value) == "Order status must be true or false"


def test_order_created_at_validation():
    """
    Test the validation of `created_at` in the `Order` model.

    Ensures that the `Order` model raises a `ValueError` with the message
    'Created at must be a valid datetime object' when `created_at` is
    not an instance of `datetime`, ensuring adherence to the model's
    constraints.

    This test checks:
    - If `created_at` is not a `datetime` instance, a `ValueError` is raised
      with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        Order(order_id=1, user_id=1, order_status=True, created_at="invalid_date")
    assert str(excinfo.value) == "Created at must be a valid datetime object"


def test_order_item_instantiation():
    """
    Test OrderItem class instantiation with valid inputs.

    Ensures that the attributes are assigned correctly while instantiating the OrderItem
    object and validates them according do pre defined valid values.

    This test checks:
    - If the `OrderItem` model is instantiated correctly with valid input values.
    """

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


def test_order_item_id_validation():
    """
    Test the validation of `order_item_id` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Order Item ID must be greater than zero' when `order_item_id` is less
    than or equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `order_item_id` is 0, a `ValueError` is raised with the correct
      error message.
    """
    with pytest.raises(ValueError) as excinfo:
        OrderItem(
            order_item_id=-1,
            order_id=1,
            product_id=1,
            quantity=2,
            price=5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Order item ID must be greater than zero"


def test_order_item_order_id_validation():
    """
    Test the validation of `order_id` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Order ID must be greater than zero' when `order_id` is less than or
    equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `order_id` is -1, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        OrderItem(
            order_item_id=1,
            order_id=-1,
            product_id=1,
            quantity=2,
            price=5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Order ID must be greater than zero"


def test_order_item_product_id_validation():
    """
    Test the validation of `product_id` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Product ID must be greater than zero' when `product_id` is less than
    or equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `product_id` is -1, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        OrderItem(
            order_item_id=1,
            order_id=1,
            product_id=-1,
            quantity=2,
            price=5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Product ID must be greater than zero"


def test_order_item_quantity_validation():
    """
    Test the validation of `quantity` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Quantity must be greater than zero' when `quantity` is less than or
    equal to zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `quantity` is 0, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        OrderItem(
            order_item_id=1,
            order_id=1,
            product_id=1,
            quantity=0,
            price=5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Quantity must be greater than zero"


def test_order_item_price_validation():
    """
    Test the validation of `price` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Price must be greater than zero' when `price` is less than or equal to
    zero, ensuring adherence to the model's constraints.

    This test checks:
    - If `price` is -5, a `ValueError` is raised with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        OrderItem(
            order_item_id=1,
            order_id=1,
            product_id=1,
            quantity=2,
            price=-5.0,
            created_at=datetime.now(),
        )
    assert str(excinfo.value) == "Price must be a positive number"


def test_order_item_created_at_validation():
    """
    Test the validation of `created_at` in the `OrderItem` model.

    Ensures that the `OrderItem` model raises a `ValueError` with the message
    'Created at must be a valid datetime object' when `created_at` is not
    an instance of `datetime`, ensuring adherence to the model's constraints.

    This test checks:
    - If `created_at` is not a `datetime` instance, a `ValueError` is raised
      with the correct error message.
    """
    with pytest.raises(ValueError) as excinfo:
        OrderItem(
            order_item_id=1,
            order_id=1,
            product_id=1,
            quantity=2,
            price=5.0,
            created_at="invalid_date",
        )
    assert str(excinfo.value) == "Created at must be a valid datetime object"
