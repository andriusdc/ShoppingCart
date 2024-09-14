# -*- coding: utf-8 -*-
import pytest
from src.core.domain.models import Cart, db
from src.adapters.cart_adapter import CartAdapter


@pytest.fixture
def cart_adapter():
    """
    Fixture for providing an instance of CartAdapter.

    :return: CartAdapter instance.
    """
    return CartAdapter()


def test_add_cart(test_client, cart_adapter):
    """
    Test adding a new cart to the database.

    Ensures that a cart can be added successfully and is retrievable.
    This test checks:
    - If a cart is added successfully.
    - If the added cart's attributes are correctly set.
    """
    cart = Cart(user_id=1)
    cart_adapter.add_cart(cart)

    added_cart = (
        db.session.execute(db.select(Cart).filter_by(user_id=1)).scalars().first()
    )
    assert added_cart is not None
    assert added_cart.user_id == 1


def test_get_cart(test_client, cart_adapter):
    """
    Test retrieving an existing cart by ID.

    Ensures that a cart can be successfully retrieved by its ID.
    This test checks:
    - If a cart can be retrieved by its ID.
    - If the retrieved cart's attributes are correctly set.
    """
    cart = Cart(user_id=1)
    cart_adapter.add_cart(cart)

    fetched_cart = cart_adapter.get_cart(cart.cart_id)
    assert fetched_cart is not None
    assert fetched_cart.cart_id == cart.cart_id
    assert fetched_cart.user_id == 1


def test_update_cart(test_client, cart_adapter):
    """
    Test updating an existing cart's details.

    Ensures that a cart's details can be updated successfully.
    This test checks:
    - If a cart's details can be updated.
    - If the updated cart's attributes reflect the new data.
    """
    cart = Cart(user_id=1)
    cart_adapter.add_cart(cart)

    cart.user_id = 2
    cart_adapter.update_cart(cart)

    updated_cart = db.session.get(Cart, cart.cart_id)
    assert updated_cart is not None
    assert updated_cart.user_id == 2


def test_delete_cart(test_client, cart_adapter):
    """
    Test deleting a cart by ID.

    Ensures that a cart can be successfully deleted by its ID.
    This test checks:
    - If a cart is deleted successfully.
    - If the deleted cart cannot be retrieved.
    """
    cart = Cart(user_id=1)
    cart_adapter.add_cart(cart)

    cart_adapter.delete_cart(cart.cart_id)

    deleted_cart = db.session.get(Cart, cart.cart_id)
    assert deleted_cart is None


def test_list_carts(test_client, cart_adapter):
    """
    Test listing all carts in the database.

    Ensures that all carts can be retrieved from the database.
    This test checks:
    - If all added carts are listed.
    - If the listed carts include all previously added carts.
    """
    cart1 = Cart(user_id=1)
    cart2 = Cart(user_id=2)
    cart_adapter.add_cart(cart1)
    cart_adapter.add_cart(cart2)

    carts = cart_adapter.list_carts()
    assert len(carts) >= 2
    assert any(c.user_id == 1 for c in carts)
    assert any(c.user_id == 2 for c in carts)


def test_add_cart_with_existing_user(test_client, cart_adapter):
    """
    Test adding a cart with an existing user ID.

    Ensures that adding a cart with a user ID that already exists raises a ValueError.
    This test checks:
    - If attempting to add a cart with an existing user ID raises a ValueError.
    """
    cart = Cart(user_id=1)
    cart_adapter.add_cart(cart)

    duplicate_cart = Cart(user_id=1)
    with pytest.raises(Exception, match="Failed to add cart"):
        cart_adapter.add_cart(duplicate_cart)


def test_get_non_existent_cart(test_client, cart_adapter):
    """
    Test trying to retrieve a non-existent cart by ID.

    Ensures that attempting to retrieve a cart that does not exist raises an appropriate exception.
    This test checks:
    - If attempting to get a cart with a non-existent ID returns None.
    """
    with pytest.raises(ValueError, match="Cart with ID 9999 does not exist"):
        cart_adapter.get_cart(9999)


def test_delete_non_existent_cart(test_client, cart_adapter):
    """
    Test trying to delete a cart with a non-existent ID.

    Ensures that attempting to delete a cart that does not exist raises an appropriate exception.
    This test checks:
    - If attempting to delete a cart with a non-existent ID raises a ValueError.
    """
    with pytest.raises(ValueError, match="Cart with ID 9999 does not exist"):
        cart_adapter.delete_cart(9999)
