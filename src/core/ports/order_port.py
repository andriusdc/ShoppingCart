# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.domain.models import Order


class OrderPort(ABC):
    @abstractmethod
    def add_order(self, order: Order) -> None:
        """
        Add a new order to the database.

        :param order: Order instance to be added.
        """
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> Optional[Order]:
        """
        Retrieve an order by its ID.

        :param order_id: ID of the order to retrieve.
        :return: Order instance if found, otherwise None.
        """
        pass

    @abstractmethod
    def update_order(self, order: Order) -> None:
        """
        Update an existing order's details in the database.

        :param order: Order instance with updated data.
        :raises ValueError: If the order does not exist.
        """
        pass

    @abstractmethod
    def delete_order(self, order_id: int) -> None:
        """
        Delete an order by its ID.

        :param order_id: ID of the order to delete.
        :raises ValueError: If the order does not exist.
        """
        pass

    @abstractmethod
    def list_orders(self) -> List[Order]:
        """
        List all orders in the database.

        :return: List of Order instances.
        """
        pass
