# -*- coding: utf-8 -*-
import pytest
from src.core.domain.models import Order, db
from src.adapters.order_adapter import OrderAdapter


@pytest.fixture
def order_adapter():
    return OrderAdapter()


def test_add_order_success(test_client, order_adapter):
    """
    Test adding a new order to the database.

    Ensures that an order can be added successfully to the database with the correct order_status.
    """
    order = Order(user_id=1, order_status=True)
    order_adapter.add_order(order)

    added_order = (
        db.session.execute(db.select(Order).filter_by(user_id=1, order_status=True))
        .scalars()
        .first()
    )
    assert added_order is not None
    assert added_order.user_id == 1
    assert added_order.order_status is True


def test_get_order_success(test_client, order_adapter):
    """
    Test retrieving an existing order by ID.

    Ensures that an order can be retrieved successfully by its ID.
    """
    order = Order(user_id=1, order_status=True)
    order_adapter.add_order(order)

    fetched_order = order_adapter.get_order(order.order_id)
    assert fetched_order is not None
    assert fetched_order.user_id == order.user_id
    assert fetched_order.order_status is True


def test_get_order_failure(test_client, order_adapter):
    """
    Test retrieval of a non-existent order by ID.

    Ensures that attempting to retrieve an order that does not exist raises a ValueError.
    """
    with pytest.raises(ValueError, match="Order with ID 999 does not exist"):
        order_adapter.get_order(999)


def test_update_order_success(test_client, order_adapter):
    """
    Test updating an existing order's details.

    Ensures that an order's details can be updated successfully.
    """
    order = Order(user_id=1, order_status=True)
    order_adapter.add_order(order)

    order.order_status = False
    order_adapter.update_order(order)

    updated_order = db.session.get(Order, order.order_id)
    assert updated_order is not None
    assert updated_order.order_status is False


def test_update_order_failure(test_client, order_adapter):
    """
    Test updating a non-existent order.

    Ensures that attempting to update an order that does not exist raises a ValueError.
    """
    order = Order(order_id=9999, user_id=1, order_status=True)

    with pytest.raises(ValueError, match="Order Id does not exist"):
        order_adapter.update_order(order)


def test_delete_order_success(test_client, order_adapter):
    """
    Test deleting an order by ID.

    Ensures that an order can be deleted successfully by its ID.
    """
    order = Order(user_id=1, order_status=True)
    order_adapter.add_order(order)

    order_adapter.delete_order(order.order_id)

    deleted_order = db.session.get(Order, order.order_id)
    assert deleted_order is None


def test_delete_order_failure(test_client, order_adapter):
    """
    Test trying to delete an order with a non-existent ID.

    Ensures that attempting to delete an order that does not exist raises a ValueError.
    """
    with pytest.raises(ValueError, match="Order with ID 999 does not exist"):
        order_adapter.delete_order(999)


def test_list_orders_success(test_client, order_adapter):
    """
    Test listing all orders.

    Ensures that all orders are retrieved successfully.
    """
    order1 = Order(user_id=1, order_status=True)
    order2 = Order(user_id=2, order_status=False)
    order_adapter.add_order(order1)
    order_adapter.add_order(order2)

    orders = order_adapter.list_orders()
    assert len(orders) == 2
    assert any(order.user_id == 1 for order in orders)
    assert any(order.user_id == 2 for order in orders)
