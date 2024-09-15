# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.core.domain.models import OrderItem


class OrderItemPort(ABC):
    @abstractmethod
    def add_order_item(self, order_item: OrderItem) -> None:
        """
        Add a new order item to the database.

        :param order_item: The order item to add.
        :raises Exception: If the operation fails.
        """
        pass

    @abstractmethod
    def get_order_item(self, order_item_id: int) -> OrderItem:
        """
        Retrieve an order item by its ID.

        :param order_item_id: The ID of the order item to retrieve.
        :return: The retrieved order item.
        :raises ValueError: If no order item with the specified ID exists.
        """
        pass

    @abstractmethod
    def update_order_item(self, order_item: OrderItem) -> None:
        """
        Update an existing order item's details.

        :param order_item: The order item with updated details.
        :raises ValueError: If the order item does not exist.
        """
        pass

    @abstractmethod
    def delete_order_item(self, order_item_id: int) -> None:
        """
        Delete an order item by its ID.

        :param order_item_id: The ID of the order item to delete.
        :raises ValueError: If no order item with the specified ID exists.
        """
        pass

    @abstractmethod
    def list_order_items(self) -> List[OrderItem]:
        """
        List all order items.

        :return: A list of all order items.
        """
        pass
