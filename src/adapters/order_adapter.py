# -*- coding: utf-8 -*-
from typing import Optional, List
from src.core.domain.models import Order, db
from src.core.ports.order_port import OrderPort


class OrderAdapter(OrderPort):
    def add_order(self, order: Order) -> None:
        """
        Add a new order to the database.

        :param order: Order instance to be added.
        """
        try:
            db.session.add(order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to add order: {e}")

    def get_order(self, order_id: int) -> Optional[Order]:
        """
        Retrieve an order by its ID.

        :param order_id: ID of the order to retrieve.
        :return: Order instance if found, otherwise None.
        :raises ValueError: If the order does not exist.
        """
        try:
            order = db.session.get(Order, order_id)
            if order is None:
                raise ValueError(f"Order with ID {order_id} does not exist")
            return order
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to retrieve order: {e}")

    def update_order(self, order: Order) -> None:
        """
        Update an existing order's details in the database.

        :param order: Order instance with updated data.
        :raises ValueError: If the order does not exist.
        """
        try:
            existing_order = db.session.get(Order, order.order_id)
            if existing_order is None:
                raise ValueError(f"Order Id does not exist")

            existing_order.order_status = order.order_status
            existing_order.created_at = order.created_at
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update order: {e}")

    def delete_order(self, order_id: int) -> None:
        """
        Delete an order by its ID.

        :param order_id: ID of the order to delete.
        :raises ValueError: If the order does not exist.
        """
        try:
            order = db.session.get(Order, order_id)
            if order is None:
                raise ValueError(f"Order with ID {order_id} does not exist")

            db.session.delete(order)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete order: {e}")

    def list_orders(self) -> List[Order]:
        """
        List all orders in the database.

        :return: List of Order instances.
        """
        try:
            return db.session.execute(db.select(Order)).scalars().all()
        except Exception as e:
            raise Exception(f"Failed to list orders: {e}")
