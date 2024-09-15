# -*- coding: utf-8 -*-
from typing import Optional, List
from src.core.domain.models import Cart, db
from src.core.ports.cart_port import CartPort


class CartAdapter(CartPort):
    def add_cart(self, cart: Cart) -> None:
        """
        Add a new cart to the database.

        :param cart: Cart instance to be added.
        :raises Exception: If adding the cart fails.
        """
        try:
            db.session.add(cart)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to add cart: {e}")

    def get_cart(self, cart_id: int) -> Optional[Cart]:
        """
        Retrieve a cart by its ID.

        :param cart_id: ID of the cart to retrieve.
        :return: Cart instance if found, otherwise None.
        :raises Exception: If retrieval fails.
        """
        try:
            cart = db.session.get(Cart, cart_id)
            if cart is None:
                raise ValueError(f"Cart with ID {cart_id} does not exist")
            return cart
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to retrieve cart: {e}")

    def update_cart(self, cart: Cart) -> None:
        """
        Update an existing cart's details in the database.

        :param cart: Cart instance with updated data.
        :raises ValueError: If the cart does not exist.
        :raises Exception: If updating the cart fails.
        """
        try:
            existing_cart = db.session.get(Cart, cart.cart_id)
            if not existing_cart:
                raise ValueError(f"Cart with ID {cart.cart_id} does not exist")

            existing_cart.user_id = cart.user_id
            existing_cart.created_at = cart.created_at
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update cart: {e}")

    def delete_cart(self, cart_id: int) -> None:
        """
        Delete a cart by its ID.

        :param cart_id: ID of the cart to delete.
        :raises ValueError: If the cart does not exist.
        :raises Exception: If deleting the cart fails.
        """
        try:
            cart = db.session.get(Cart, cart_id)
            if not cart:
                raise ValueError(f"Cart with ID {cart_id} does not exist")

            db.session.delete(cart)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete cart: {e}")

    def list_carts(self) -> List[Cart]:
        """
        List all carts in the database.

        :return: List of Cart instances.
        :raises Exception: If listing carts fails.
        """
        try:
            return db.session.execute(db.select(Cart)).scalars().all()
        except Exception as e:
            raise Exception(f"Failed to list carts: {e}")
