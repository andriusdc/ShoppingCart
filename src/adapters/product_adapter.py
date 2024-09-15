# -*- coding: utf-8 -*-
from typing import Optional, List
from src.core.domain.models import Product, db
from src.core.ports.product_port import ProductPort


class ProductAdapter(ProductPort):
    def create_product(self, product: Product) -> None:
        """
        Add a new product to the database.

        :param product: Product instance to be added.
        :raises Exception: If an error occurs while adding the product.
        """
        try:
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to add product: {e}")

    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Retrieve a product by its ID.

        :param product_id: ID of the product to retrieve.
        :return: Product instance if found, otherwise None.
        :raises Exception: If an error occurs while retrieving the product.
        """
        try:
            return db.session.get(Product, product_id)
        except Exception as e:
            raise Exception(f"Failed to retrieve product: {e}")

    def update_product(self, product: Product) -> None:
        """
        Update an existing product's details in the database.

        :param product: Product instance with updated data.
        :raises ValueError: If the product does not exist.
        :raises Exception: If an error occurs while updating the product.
        """
        try:
            existing_product = db.session.get(Product, product.product_id)
            if not existing_product:
                raise ValueError(f"Product with ID {product.product_id} does not exist")

            existing_product.product_name = product.product_name
            existing_product.description = product.description
            existing_product.price = product.price
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update product: {e}")

    def delete_product(self, product_id: int) -> None:
        """
        Delete a product by its ID.

        :param product_id: ID of the product to delete.
        :raises ValueError: If the product does not exist.
        :raises Exception: If an error occurs while deleting the product.
        """
        try:
            product = db.session.get(Product, product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} does not exist")

            db.session.delete(product)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete product: {e}")

    def list_products(self) -> List[Product]:
        """
        List all products in the database.

        :return: List of Product instances.
        :raises Exception: If an error occurs while listing products.
        """
        try:
            return db.session.execute(db.select(Product)).scalars().all()
        except Exception as e:
            raise Exception(f"Failed to list products: {e}")
