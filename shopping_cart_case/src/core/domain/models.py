from datetime import datetime

class User():
    def __init__(self, user_id: int, user_name: str, password: str, created_at: datetime = None, role: str = 'user') -> None:
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.created_at = created_at or datetime.now()
        self.role = role
        
class Product:
    def __init__(self, product_id: int, product_name: str, description: str, price: int, created_at: datetime = None):
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price
        self.created_at = created_at or datetime.now()