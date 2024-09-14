# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.domain.models import Cart


class CartPort(ABC):
    @abstractmethod
    def add_cart(self, cart: Cart) -> None:
        """
        Add a new cart to the database.

        :param cart: Cart instance to be added.
        """
        pass

    @abstractmethod
    def get_cart(self, cart_id: int) -> Optional[Cart]:
        """
        Retrieve a cart by its ID.

        :param cart_id: ID of the cart to retrieve.
        :return: Cart instance if found, otherwise None.
        """
        pass

    @abstractmethod
    def update_cart(self, cart: Cart) -> None:
        """
        Update an existing cart's details in the database.

        :param cart: Cart instance with updated data.
        """
        pass

    @abstractmethod
    def delete_cart(self, cart_id: int) -> None:
        """
        Delete a cart by its ID.

        :param cart_id: ID of the cart to delete.
        """
        pass

    @abstractmethod
    def list_carts(self) -> List[Cart]:
        """
        List all carts in the database.

        :return: List of Cart instances.
        """
        pass
