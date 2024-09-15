# -*- coding: utf-8 -*-
from typing import Optional, List
from src.core.domain.models import CartItem


class CartItemPort:
    def add_cart_item(self, cart_item: CartItem) -> None:
        """
        Add a new cart item to the database.

        :param cart_item: CartItem instance to be added.
        """
        raise NotImplementedError

    def get_cart_item(self, cart_item_id: int) -> Optional[CartItem]:
        """
        Retrieve a cart item by its ID.

        :param cart_item_id: ID of the cart item to retrieve.
        :return: CartItem instance if found, otherwise None.
        """
        raise NotImplementedError

    def update_cart_item(self, cart_item: CartItem) -> None:
        """
        Update an existing cart item's details in the database.

        :param cart_item: CartItem instance with updated data.
        :raises ValueError: If the cart item does not exist.
        """
        raise NotImplementedError

    def delete_cart_item(self, cart_item_id: int) -> None:
        """
        Delete a cart item by its ID.

        :param cart_item_id: ID of the cart item to delete.
        :raises ValueError: If the cart item does not exist.
        """
        raise NotImplementedError

    def list_cart_items(self) -> List[CartItem]:
        """
        List all cart items in the database.

        :return: List of CartItem instances.
        """
        raise NotImplementedError
