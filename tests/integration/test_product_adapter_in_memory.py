# -*- coding: utf-8 -*-
import pytest
from src.core.domain.models import Product, db
from src.adapters.product_adapter import ProductAdapter


@pytest.fixture
def product_adapter():
    """
    Fixture for providing an instance of ProductAdapter.

    :return: ProductAdapter instance.
    """
    return ProductAdapter()


def test_create_product(test_client, product_adapter):
    """
    Test addition of a new product to the database.

    Ensures that a product is added successfully and that it can be retrieved
    correctly from the database.

    This test checks:
    - If the product is successfully added to the database.
    - If the product's attributes are correctly saved and retrieved.
    """
    product = Product(product_name="Test Product", price=10.0)
    product_adapter.create_product(product)

    added_product = (
        db.session.execute(db.select(Product).filter_by(product_name="Test Product"))
        .scalars()
        .first()
    )
    assert added_product is not None
    assert added_product.product_name == "Test Product"
    assert added_product.price == 10.0


def test_create_existing_product(test_client, product_adapter):
    """
    Test trying to add a product with a name that already exists.

    Ensures that attempting to add a duplicate product raises the appropriate exception.

    This test checks:
    - If an exception is raised when trying to add a product with a duplicate name.
    """
    product1 = Product(product_name="Unique Product", price=10.0)
    product_adapter.create_product(product1)

    duplicate_product = Product(product_name="Unique Product", price=15.0)
    with pytest.raises(Exception):
        product_adapter.create_product(duplicate_product)


def test_get_product(test_client, product_adapter):
    """
    Test retrieval of an existing product by its ID.

    Ensures that a product can be retrieved successfully by its ID. Verifies that
    the retrieved product has the correct attributes.

    This test checks:
    - If the product is retrieved successfully by its ID.
    - If the product attributes match the originally added values.
    """
    product = Product(product_name="Test Product", price=10.0)
    product_adapter.create_product(product)

    fetched_product = product_adapter.get_product(product.product_id)
    assert fetched_product is not None
    assert fetched_product.product_id == product.product_id
    assert fetched_product.product_name == "Test Product"


def test_get_non_existent_product(test_client, product_adapter):
    """
    Test retrieving a product with a non-existent ID.

    Ensures that attempting to retrieve a product that does not exist returns None.

    This test checks:
    - If retrieving a product with a non-existent ID returns None.
    """
    non_existent_product_id = 9999
    fetched_product = product_adapter.get_product(non_existent_product_id)
    assert fetched_product is None


def test_update_product(test_client, product_adapter):
    """
    Test updating an existing product's details.

    Ensures that an existing product's details are updated successfully in the database.

    This test checks:
    - If the product's attributes are updated correctly in the database.
    - If the updated attributes match the new values provided.
    """
    product = Product(product_name="Test Product", price=10.0)
    product_adapter.create_product(product)

    product.product_name = "Updated Product"
    product.price = 20.0
    product_adapter.update_product(product)

    updated_product = db.session.get(Product, product.product_id)
    assert updated_product is not None
    assert updated_product.product_name == "Updated Product"
    assert updated_product.price == 20.0


def test_delete_product(test_client, product_adapter):
    """
    Test deletion of an existing product by its ID.

    Ensures that a product is deleted successfully and can no longer be retrieved.

    This test checks:
    - If the product is deleted from the database.
    - If attempting to retrieve the deleted product returns None.
    """
    product = Product(product_name="Test Product", price=10.0)
    product_adapter.create_product(product)

    product_adapter.delete_product(product.product_id)

    deleted_product = db.session.get(Product, product.product_id)
    assert deleted_product is None


def test_delete_non_existent_product(test_client, product_adapter):
    """
    Test trying to delete a product with a non-existent ID.

    Ensures that attempting to delete a product that does not exist raises the appropriate exception.

    This test checks:
    - If attempting to delete a product with a non-existent ID raises a ValueError.
    """
    non_existent_product_id = 9999
    with pytest.raises(ValueError):
        product_adapter.delete_product(non_existent_product_id)


def test_list_products(test_client, product_adapter):
    """
    Test listing all products in the database.

    Ensures that all added products are listed correctly.

    This test checks:
    - If the list of products includes all added products.
    - If the products in the list match the attributes of the added products.
    """
    product1 = Product(product_name="Product 1", price=10.0)
    product2 = Product(product_name="Product 2", price=20.0)
    product_adapter.create_product(product1)
    product_adapter.create_product(product2)

    products = product_adapter.list_products()
    assert len(products) == 2
    assert any(p.product_name == "Product 1" for p in products)
    assert any(p.product_name == "Product 2" for p in products)
