# -*- coding: utf-8 -*-
from typing import Optional, List
from src.core.domain.models import CartItem, db
from src.core.ports.cart_item_port import CartItemPort


class CartItemAdapter(CartItemPort):
    def add_cart_item(self, cart_item: CartItem) -> None:
        """
        Add a new cart item to the database.

        :param cart_item: CartItem instance to be added.
        :raises Exception: If adding the cart item fails.
        """
        try:
            db.session.add(cart_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to add cart item: {e}")

    def get_cart_item(self, cart_item_id: int) -> Optional[CartItem]:
        """
        Retrieve a cart item by its ID.

        :param cart_item_id: ID of the cart item to retrieve.
        :return: CartItem instance if found, otherwise None.
        :raises Exception: If retrieval fails.
        """
        try:
            cart_item = db.session.get(CartItem, cart_item_id)
            if cart_item is None:
                raise ValueError(f"CartItem with ID {cart_item_id} does not exist")
            return cart_item
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to retrieve cart item: {e}")

    def update_cart_item(self, cart_item: CartItem) -> None:
        """
        Update an existing cart item's details in the database.

        :param cart_item: CartItem instance with updated data.
        :raises ValueError: If the cart item does not exist.
        :raises Exception: If updating the cart item fails.
        """
        try:
            existing_cart_item = db.session.get(CartItem, cart_item.cart_item_id)
            if not existing_cart_item:
                raise ValueError(f"CartItem Id does not exist")

            existing_cart_item.product_id = cart_item.product_id
            existing_cart_item.quantity = cart_item.quantity
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update cart item: {e}")

    def delete_cart_item(self, cart_item_id: int) -> None:
        """
        Delete a cart item by its ID.

        :param cart_item_id: ID of the cart item to delete.
        :raises ValueError: If the cart item does not exist.
        :raises Exception: If deleting the cart item fails.
        """
        try:
            cart_item = db.session.get(CartItem, cart_item_id)
            if not cart_item:
                raise ValueError(f"CartItem with ID {cart_item_id} does not exist")

            db.session.delete(cart_item)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete cart item: {e}")

    def list_cart_items(self, cart_id: int) -> List[CartItem]:
        """
        List all cart items in the database for a specific cart_id.

        :param cart_id: ID of the cart to list items from.
        :return: List of CartItem instances associated with the specified cart.
        :raises Exception: If listing cart items fails.
        """
        try:
            # Fetch all cart items for the given cart_id
            return (
                db.session.execute(db.select(CartItem).filter_by(cart_id=cart_id))
                .scalars()
                .all()
            )
        except Exception as e:
            raise Exception(f"Failed to list cart items: {e}")
