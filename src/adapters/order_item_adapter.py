# -*- coding: utf-8 -*-
from typing import Optional, List
from src.core.domain.models import OrderItem, db
from src.core.ports.order_item_port import OrderItemPort


class OrderItemAdapter(OrderItemPort):
    def add_order_item(self, order_item: OrderItem) -> None:
        """
        Add a new order item to the database.

        :param order_item: OrderItem instance to be added.
        :raises Exception: If the operation fails.
        """
        try:
            db.session.add(order_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to add order item: {e}")

    def get_order_item(self, order_item_id: int) -> Optional[OrderItem]:
        """
        Retrieve an order item by its ID.

        :param order_item_id: ID of the order item to retrieve.
        :return: OrderItem instance if found, otherwise None.
        :raises ValueError: If the order item does not exist.
        """
        try:
            order_item = db.session.get(OrderItem, order_item_id)
            if order_item is None:
                raise ValueError(f"OrderItem with ID {order_item_id} does not exist")
            return order_item
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to retrieve order item: {e}")

    def update_order_item(self, order_item: OrderItem) -> None:
        """
        Update an existing order item's details in the database.

        :param order_item: OrderItem instance with updated data.
        :raises ValueError: If the order item does not exist.
        """
        try:
            existing_order_item = db.session.get(OrderItem, order_item.order_item_id)
            if existing_order_item is None:
                raise ValueError(f"OrderItem ID does not exist")

            existing_order_item.product_id = order_item.product_id
            existing_order_item.quantity = order_item.quantity
            existing_order_item.price = order_item.price
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update order item: {e}")

    def delete_order_item(self, order_item_id: int) -> None:
        """
        Delete an order item by its ID.

        :param order_item_id: ID of the order item to delete.
        :raises ValueError: If the order item does not exist.
        """
        try:
            order_item = db.session.get(OrderItem, order_item_id)
            if order_item is None:
                raise ValueError(f"OrderItem with ID {order_item_id} does not exist")

            db.session.delete(order_item)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete order item: {e}")

    def list_order_items(self, order_id: int) -> List[OrderItem]:
        """
        List all order items in the database for a specific order_id.

        :param order_id: ID of the order to list items from.
        :return: List of OrderItem instances associated with the specified order.
        :raises Exception: If the operation fails.
        """
        try:
            # Fetch all order items for the given order_id
            return (
                db.session.execute(db.select(OrderItem).filter_by(order_id=order_id))
                .scalars()
                .all()
            )
        except Exception as e:
            raise Exception(f"Failed to list order items: {e}")
