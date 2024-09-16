# -*- coding: utf-8 -*-
import pytest

from src.core.application.order_service import OrderService

from src.core.domain.models import User, Product, Cart, CartItem, Order, OrderItem, db

from src.adapters import (
    UserAdapter,
    ProductAdapter,
    CartAdapter,
    CartItemAdapter,
    OrderAdapter,
    OrderItemAdapter,
)


@pytest.fixture
def order_service(password_service):
    user_adapter = UserAdapter(password_service=password_service)
    product_adapter = ProductAdapter()
    cart_adapter = CartAdapter()
    cart_item_adapter = CartItemAdapter()
    order_adapter = OrderAdapter()
    order_item_adapter = OrderItemAdapter()

    return OrderService(
        user_adapter,
        product_adapter,
        cart_adapter,
        cart_item_adapter,
        order_adapter,
        order_item_adapter,
    )


@pytest.fixture
def setup_data(test_client):
    # Create test data
    user = User(user_name="test_user", password="password", role="user")
    product = Product(product_name="test_product", price=10.0)
    cart = Cart(user_id=1)
    db.session.add(user)
    db.session.add(product)
    db.session.add(cart)
    db.session.commit()

    # Add items to cart
    cart_item = CartItem(cart_id=1, product_id=1, quantity=2)
    db.session.add(cart_item)
    db.session.commit()
    return user, product, cart


def test_place_order_success(order_service, setup_data, test_client):
    user, product, cart = setup_data

    # Place the order
    order_id = order_service.place_order(user_id=user.user_id)

    # Verify that the order was created

    order = db.session.get(Order, order_id)
    assert order is not None
    assert order.user_id == user.user_id

    # Verify that the order items match the cart items

    order_items = db.session.query(OrderItem).filter_by(order_id=order_id).all()
    assert len(order_items) == 1
    assert order_items[0].product_id == product.product_id
    assert order_items[0].quantity == 2

    # Verify that the cart is emptied

    cart_items = db.session.query(CartItem).filter_by(cart_id=cart.cart_id).all()
    assert len(cart_items) == 0


def test_place_order_empty_cart(order_service, setup_data, test_client):
    user, _, cart = setup_data

    db.session.query(CartItem).delete()
    db.session.commit()
    # Try to place an order with an empty cart
    with pytest.raises(Exception, match="Cart is empty"):
        order_service.place_order(user_id=user.user_id)

    # Verify no order was created
    orders = db.session.query(Order).filter_by(user_id=user.user_id).all()
    print(orders)
    assert len(orders) == 0


def test_place_order_nonexistent_user(order_service, test_client):
    # Try to place an order with a non-existent user
    with pytest.raises(Exception, match="User with ID not found"):
        order_service.place_order(user_id=9999)
