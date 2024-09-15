# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.domain.models import Product


class ProductPort(ABC):
    @abstractmethod
    def create_product(self, product: Product) -> None:

        pass

    @abstractmethod
    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Retrieve a product by its ID.

        :param product_id: ID of the product.
        :return: Product instance if found, otherwise None.
        """
        pass

    @abstractmethod
    def update_product(self, product: Product) -> None:
        """
        Update an existing product.

        :param product: Product instance with updated data.
        """
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        """
        Delete a product by its ID.

        :param product_id: ID of the product.
        """
        pass

    @abstractmethod
    def list_products(self) -> List[Product]:
        """
        List all products.

        :return: List of Product instances.
        """
        pass
