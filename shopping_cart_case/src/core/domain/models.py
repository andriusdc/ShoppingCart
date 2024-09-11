from datetime import datetime

class User():
    def __init__(self, user_id: int, user_name: str, password: str, created_at: datetime = None, role: str = 'user') -> None:
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.created_at = created_at or datetime.now()
        self.role = role
        
class Product:
    def __init__(self, product_id: int, product_name: str, description: str, price: int, created_at: datetime = None) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price
        self.created_at = created_at or datetime.now()

class Cart:
    def __init__(self, cart_id: int, user_id: int, created_at: datetime = None) -> None:
        self.cart_id = cart_id
        self.user_id = user_id
        self.created_at = created_at or datetime.now()

class CartItem:
    def __init__ (self, cart_item_id: int, cart_id: int, product_id: int, quantity: int, added_at: datetime = None) -> None:
        self.cart_item_id = cart_item_id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.added_at = added_at