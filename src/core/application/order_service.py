# -*- coding: utf-8 -*-
from src.core.domain.models import Order, OrderItem


class OrderService:
    def __init__(
        self,
        user_adapter,
        product_adapter,
        cart_adapter,
        cart_item_adapter,
        order_adapter,
        order_item_adapter,
    ):
        self.user_adapter = user_adapter
        self.product_adapter = product_adapter
        self.cart_adapter = cart_adapter
        self.cart_item_adapter = cart_item_adapter
        self.order_adapter = order_adapter
        self.order_item_adapter = order_item_adapter

    def place_order(self, user_id):
        user = self.user_adapter.get_user(user_id)
        if not user:
            raise ValueError("User with ID not found")

        cart = self.cart_adapter.get_cart(user_id)
        if not cart:
            raise ValueError("No cart found for the user")

        # Move items from cart to order
        cart_items = self.cart_item_adapter.list_cart_items(cart_id=cart.cart_id)
        if not cart_items:
            raise ValueError("Cart is empty")

        # Create the order
        order = Order(user_id=user_id, order_status=False)
        self.order_adapter.add_order(order)

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=self.product_adapter.get_product(item.product_id).price,
            )
            self.order_item_adapter.add_order_item(order_item)
            self.cart_item_adapter.delete_cart_item(item.cart_item_id)

        return order.order_id
