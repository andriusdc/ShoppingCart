# -*- coding: utf-8 -*-
import pytest
from src.core.domain.models import CartItem, db
from src.adapters.cart_item_adapter import CartItemAdapter


@pytest.fixture
def cart_item_adapter():
    return CartItemAdapter()


def test_add_cart_item_success(test_client, cart_item_adapter):
    """
    Test adding a new cart item to the database.

    Ensures that a cart item can be added successfully to the database.

    This test checks:
    - If a cart item is added successfully to the database.
    """
    cart_item = CartItem(cart_id=1, product_id=1, quantity=3)
    cart_item_adapter.add_cart_item(cart_item)

    added_cart_item = (
        db.session.execute(db.select(CartItem).filter_by(cart_id=1, product_id=1))
        .scalars()
        .first()
    )
    assert added_cart_item is not None
    assert added_cart_item.cart_id == 1
    assert added_cart_item.product_id == 1
    assert added_cart_item.quantity == 3


def test_add_cart_item_failure(test_client, cart_item_adapter):
    """
    Test failure to add a cart item due to database error.

    Ensures that attempting to add a cart item when the database operation fails raises an exception.

    This test checks:
    - If an exception is raised when adding a cart item fails.
    """
    cart_item = CartItem(cart_id=1, product_id=1, quantity=3)
    cart_item_adapter.add_cart_item(cart_item)

    cart_item_duplicated_product = CartItem(cart_id=1, product_id=1, quantity=2)

    with pytest.raises(Exception, match="Failed to add cart item"):

        cart_item_adapter.add_cart_item(cart_item_duplicated_product)


def test_get_cart_item_success(test_client, cart_item_adapter):
    """
    Test retrieval of an existing cart item by ID.

    Ensures that a cart item can be retrieved successfully by its ID.

    This test checks:
    - If the cart item is retrieved successfully by its ID.
    - If the cart item's attributes are correctly set.
    """
    cart_item = CartItem(cart_id=1, product_id=1, quantity=3)
    cart_item_adapter.add_cart_item(cart_item)

    fetched_cart_item = cart_item_adapter.get_cart_item(cart_item.cart_item_id)
    assert fetched_cart_item is not None
    assert fetched_cart_item.cart_id == cart_item.cart_id
    assert fetched_cart_item.product_id == cart_item.product_id
    assert fetched_cart_item.quantity == cart_item.quantity


def test_get_cart_item_failure(test_client, cart_item_adapter):
    """
    Test retrieval of a non-existent cart item by ID.

    Ensures that attempting to retrieve a cart item that does not exist raises the appropriate exception.

    This test checks:
    - If attempting to retrieve a cart item with a non-existent ID raises a ValueError.
    """
    with pytest.raises(ValueError, match="CartItem with ID 999 does not exist"):
        cart_item_adapter.get_cart_item(999)


def test_update_cart_item_success(test_client, cart_item_adapter):
    """
    Test updating an existing cart item's details.

    Ensures that a cart item's details can be updated successfully.

    This test checks:
    - If the cart item's details are updated correctly.
    """
    cart_item = CartItem(cart_id=1, product_id=1, quantity=3)
    cart_item_adapter.add_cart_item(cart_item)

    cart_item.quantity = 5
    cart_item_adapter.update_cart_item(cart_item)

    updated_cart_item = db.session.get(CartItem, cart_item.cart_item_id)
    assert updated_cart_item is not None
    assert updated_cart_item.quantity == 5


def test_update_cart_item_failure(test_client, cart_item_adapter):
    """
    Test updating a non-existent cart item.

    Ensures that attempting to update a cart item that does not exist raises a ValueError.

    This test checks:
    - If attempting to update a cart item that does not exist raises a ValueError.
    """
    cart_item = CartItem(cart_id=9999, product_id=1, quantity=3)

    with pytest.raises(ValueError, match="CartItem Id does not exist"):
        cart_item_adapter.update_cart_item(cart_item)


def test_delete_cart_item_success(test_client, cart_item_adapter):
    """
    Test deletion of a cart item by ID.

    Ensures that a cart item can be deleted successfully by its ID.

    This test checks:
    - If the cart item is deleted successfully by its ID.
    """
    cart_item = CartItem(cart_id=1, product_id=1, quantity=3)
    cart_item_adapter.add_cart_item(cart_item)

    cart_item_adapter.delete_cart_item(cart_item.cart_item_id)

    deleted_cart_item = db.session.get(CartItem, cart_item.cart_item_id)
    assert deleted_cart_item is None


def test_delete_cart_item_failure(test_client, cart_item_adapter):
    """
    Test trying to delete a cart item with a non-existent ID.

    Ensures that attempting to delete a cart item that does not exist raises the appropriate exception.

    This test checks:
    - If attempting to delete a cart item with a non-existent ID raises a ValueError.
    """
    with pytest.raises(ValueError, match="CartItem with ID 999 does not exist"):
        cart_item_adapter.delete_cart_item(999)


def test_list_cart_items_success(test_client, cart_item_adapter):
    """
    Test listing all cart items.

    Ensures that all cart items can be listed successfully.

    This test checks:
    - If all cart items are retrieved successfully.
    """
    cart_item1 = CartItem(cart_id=1, product_id=1, quantity=3)
    cart_item2 = CartItem(cart_id=1, product_id=2, quantity=2)
    cart_item_adapter.add_cart_item(cart_item1)
    cart_item_adapter.add_cart_item(cart_item2)

    cart_items = cart_item_adapter.list_cart_items()
    assert len(cart_items) == 2
    assert any(item.product_id == 1 for item in cart_items)
    assert any(item.product_id == 2 for item in cart_items)
