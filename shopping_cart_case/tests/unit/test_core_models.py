import pytest
from datetime import datetime
from src.core.domain.models import User,Product,Cart,CartItem,Order,OrderItem

def test_user_model():
    created_at=datetime(2024,9,11,0,0,0)
    user=User(user_id=1,user_name="John",password="123",created_at=created_at,role="user")

    assert user.user_id==1
    assert user.user_name=="John"
    assert user.password=="123"
    assert user.created_at==created_at
    assert user.role=="user"

def test_product_model():
    created_at=datetime(2024,9,11,0,0,0)
    product=Product(product_id=1,product_name="Orange",description="Fruit unit",price=5,created_at=created_at)

    assert product.product_id==1
    assert product.product_name=="Orange"
    assert product.description=="Fruit unit"
    assert product.price==5
    assert product.created_at==created_at

def test_cart_model():
    created_at=datetime(2024,9,11,0,0,0)
    cart=Cart(cart_id=1,user_id=1,created_at=created_at)

    assert cart.cart_id==1
    assert cart.user_id==1
    assert cart.created_at==created_at

def test_cart_items_model():
    added_at=datetime(2024,9,11,0,0,0)
    cartItems=CartItem(cart_item_id=1, cart_id=1, product_id =2, quantity=1,added_at=added_at)

    assert cartItems.cart_item_id == 1
    assert cartItems.cart_id == 1
    assert cartItems.product_id == 2
    assert cartItems.quantity == 1
    assert cartItems.added_at == added_at

def test_order_model():
    created_at=datetime(2024,9,11,0,0,0)
    order=Order(order_id=1,user_id=1, order_status=True, created_at=created_at)

    assert order.order_id==1
    assert order.user_id==1
    assert order.order_status==True
    assert order.created_at==created_at

def test_order_item_model():
    created_at=datetime(2024,9,11,0,0,0)
    order_item=OrderItem(order_item_id=1, order_id= 2, product_id=3, quantity= 2, price=2, created_at=created_at)

    assert order_item.order_item_id == 1
    assert order_item.order_id == 2
    assert order_item.product_id == 3
    assert order_item.quantity == 2
    assert order_item.price == 2
    assert order_item.created_at == created_at
