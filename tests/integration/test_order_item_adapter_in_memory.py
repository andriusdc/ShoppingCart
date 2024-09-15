# -*- coding: utf-8 -*-
import pytest
from src.core.domain.models import OrderItem, db
from src.adapters.order_item_adapter import OrderItemAdapter


@pytest.fixture
def order_item_adapter():
    return OrderItemAdapter()


def test_add_order_item_success(test_client, order_item_adapter):
    """
    Test adding a new order item to the database.

    Ensures that an order item can be added successfully to the database.
    """
    order_item = OrderItem(order_id=1, product_id=1, quantity=2, price=100.00)
    order_item_adapter.add_order_item(order_item)

    added_order_item = (
        db.session.execute(db.select(OrderItem).filter_by(order_id=1, product_id=1))
        .scalars()
        .first()
    )
    assert added_order_item is not None
    assert added_order_item.order_id == 1
    assert added_order_item.product_id == 1
    assert added_order_item.quantity == 2
    assert added_order_item.price == 100.00


def test_get_order_item_success(test_client, order_item_adapter):
    """
    Test retrieving an existing order item by ID.

    Ensures that an order item can be retrieved successfully by its ID.
    """
    order_item = OrderItem(order_id=1, product_id=1, quantity=2, price=100.00)
    order_item_adapter.add_order_item(order_item)

    fetched_order_item = order_item_adapter.get_order_item(order_item.order_item_id)
    assert fetched_order_item is not None
    assert fetched_order_item.order_id == order_item.order_id
    assert fetched_order_item.product_id == order_item.product_id
    assert fetched_order_item.quantity == order_item.quantity
    assert fetched_order_item.price == order_item.price


def test_get_order_item_failure(test_client, order_item_adapter):
    """
    Test retrieval of a non-existent order item by ID.

    Ensures that attempting to retrieve an order item that does not exist raises a ValueError.
    """
    with pytest.raises(ValueError, match="OrderItem with ID 999 does not exist"):
        order_item_adapter.get_order_item(999)


def test_update_order_item_success(test_client, order_item_adapter):
    """
    Test updating an existing order item's details.

    Ensures that an order item's details can be updated successfully.
    """
    order_item = OrderItem(order_id=1, product_id=1, quantity=2, price=100.00)
    order_item_adapter.add_order_item(order_item)

    order_item.quantity = 5
    order_item.price = 150.00
    order_item_adapter.update_order_item(order_item)

    updated_order_item = db.session.get(OrderItem, order_item.order_item_id)
    assert updated_order_item is not None
    assert updated_order_item.quantity == 5
    assert updated_order_item.price == 150.00


def test_update_order_item_failure(test_client, order_item_adapter):
    """
    Test updating a non-existent order item.

    Ensures that attempting to update an order item that does not exist raises a ValueError.
    """
    order_item = OrderItem(
        order_item_id=9999, order_id=1, product_id=1, quantity=2, price=100.00
    )

    with pytest.raises(ValueError, match="OrderItem ID does not exist"):
        order_item_adapter.update_order_item(order_item)


def test_delete_order_item_success(test_client, order_item_adapter):
    """
    Test deleting an order item by ID.

    Ensures that an order item can be deleted successfully by its ID.
    """
    order_item = OrderItem(order_id=1, product_id=1, quantity=2, price=100.00)
    order_item_adapter.add_order_item(order_item)

    order_item_adapter.delete_order_item(order_item.order_item_id)

    deleted_order_item = db.session.get(OrderItem, order_item.order_item_id)
    assert deleted_order_item is None


def test_delete_order_item_failure(test_client, order_item_adapter):
    """
    Test trying to delete an order item with a non-existent ID.

    Ensures that attempting to delete an order item that does not exist raises a ValueError.
    """
    with pytest.raises(ValueError, match="OrderItem with ID 999 does not exist"):
        order_item_adapter.delete_order_item(999)


def test_list_order_items_success(test_client, order_item_adapter):
    """
    Test listing all order items.

    Ensures that all order items are retrieved successfully.
    """
    order_item1 = OrderItem(order_id=1, product_id=1, quantity=2, price=100.00)
    order_item2 = OrderItem(order_id=1, product_id=2, quantity=3, price=200.00)
    order_item_adapter.add_order_item(order_item1)
    order_item_adapter.add_order_item(order_item2)

    order_items = order_item_adapter.list_order_items()
    assert len(order_items) == 2
    assert any(item.product_id == 1 for item in order_items)
    assert any(item.product_id == 2 for item in order_items)
