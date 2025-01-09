"""
Unit tests for the Inventory Management System.
"""
import unittest
from unittest.mock import patch
from inventory import Product, InventoryManager


class TestProduct(unittest.TestCase):
    """Test cases for the Product class."""

    def test_valid_product_creation(self):
        """Test creating a valid product."""
        product = Product("Test Product", 10.99, 5)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.quantity, 5)

    def test_invalid_product_creation(self):
        """Test creating products with invalid parameters."""
        with self.assertRaises(ValueError):
            Product("", 10.99, 5)  # Empty name
        with self.assertRaises(ValueError):
            Product("Test", -10, 5)  # Negative price
        with self.assertRaises(ValueError):
            Product("Test", 10.99, -5)  # Negative quantity

    def test_update_quantity(self):
        """Test updating product quantity."""
        product = Product("Test Product", 10.99, 5)
        product.update_quantity(10)
        self.assertEqual(product.quantity, 10)

        with self.assertRaises(ValueError):
            product.update_quantity(-1)

    def test_get_product_info(self):
        """Test retrieving product information."""
        product = Product("Test Product", 10.99, 5)
        info = product.get_product_info()
        self.assertEqual(info["name"], "Test Product")
        self.assertEqual(info["price"], 10.99)
        self.assertEqual(info["quantity"], 5)
        self.assertEqual(info["total_value"], 54.95)


class TestInventoryManager(unittest.TestCase):
    """Test cases for the InventoryManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = InventoryManager()
        self.manager.add_product("Test Product", 10.99, 5)

    def test_add_product(self):
        """Test adding products to inventory."""
        self.manager.add_product("New Product", 15.99, 3)
        self.assertIsNotNone(self.manager.retrieve_product_info("New Product"))

        with self.assertRaises(ValueError):
            self.manager.add_product("Test Product", 20.00, 1)  # Duplicate product

    def test_remove_product(self):
        """Test removing products from inventory."""
        self.manager.remove_product("Test Product")
        self.assertIsNone(self.manager.retrieve_product_info("Test Product"))

        with self.assertRaises(KeyError):
            self.manager.remove_product("Nonexistent Product")

    def test_update_quantity(self):
        """Test updating product quantities."""
        self.manager.update_quantity("Test Product", 10)
        product_info = self.manager.retrieve_product_info("Test Product")
        self.assertEqual(product_info["quantity"], 10)

        with self.assertRaises(KeyError):
            self.manager.update_quantity("Nonexistent Product", 5)

    def test_get_total_inventory_value(self):
        """Test calculating total inventory value."""
        self.manager.add_product("Second Product", 20.00, 3)
        expected_value = (10.99 * 5) + (20.00 * 3)
        self.assertEqual(self.manager.get_total_inventory_value(), expected_value)

    @patch('inventory.inventory_manager.Product')
    def test_mocked_product_creation(self, mock_product):
        """Test product creation with mocking."""
        mock_product.return_value.name = "Mocked Product"
        mock_product.return_value.price = 25.99
        mock_product.return_value.quantity = 2

        self.manager.add_product("Mocked Product", 25.99, 2)
        mock_product.assert_called_once_with(name="Mocked Product", price=25.99, quantity=2)


if __name__ == '__main__':
    unittest.main()
