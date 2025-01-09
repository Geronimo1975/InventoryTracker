"""
InventoryManager class module for the Inventory Management System.
"""
from typing import Dict, Optional, List
from contextlib import contextmanager
from .product import Product
from .database import SessionLocal, DBProduct

class InventoryManager:
    """
    Manages the inventory of products using PostgreSQL database.
    """

    @contextmanager
    def get_db(self):
        """Get database session context."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def add_product(self, name: str, price: float, quantity: int) -> None:
        """
        Add a new product to the inventory.

        Args:
            name (str): Product name
            price (float): Product price
            quantity (int): Initial quantity

        Raises:
            ValueError: If product already exists or invalid input
        """
        with self.get_db() as db:
            # Check if product exists
            existing = db.query(DBProduct).filter(DBProduct.name == name.strip()).first()
            if existing:
                raise ValueError(f"Product '{name}' already exists in inventory")

            # Create new product
            db_product = DBProduct(
                name=name.strip(),
                price=price,
                quantity=quantity
            )
            db.add(db_product)
            db.commit()

    def remove_product(self, name: str) -> None:
        """
        Remove a product from the inventory.

        Args:
            name (str): Name of the product to remove

        Raises:
            KeyError: If product doesn't exist
        """
        with self.get_db() as db:
            product = db.query(DBProduct).filter(DBProduct.name == name.strip()).first()
            if not product:
                raise KeyError(f"Product '{name}' not found in inventory")

            db.delete(product)
            db.commit()

    def update_quantity(self, name: str, new_quantity: int) -> None:
        """
        Update the quantity of an existing product.

        Args:
            name (str): Product name
            new_quantity (int): New quantity value

        Raises:
            KeyError: If product doesn't exist
            ValueError: If quantity is invalid
        """
        if not isinstance(new_quantity, int) or new_quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")

        with self.get_db() as db:
            product = db.query(DBProduct).filter(DBProduct.name == name.strip()).first()
            if not product:
                raise KeyError(f"Product '{name}' not found in inventory")

            product.quantity = new_quantity
            db.commit()

    def retrieve_product_info(self, name: str) -> Optional[Dict[str, any]]:
        """
        Retrieve information about a specific product.

        Args:
            name (str): Product name

        Returns:
            Optional[Dict[str, any]]: Product information or None if not found
        """
        with self.get_db() as db:
            product = db.query(DBProduct).filter(DBProduct.name == name.strip()).first()
            if not product:
                return None

            return {
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "total_value": product.price * product.quantity
            }

    def get_total_inventory_value(self) -> float:
        """
        Calculate the total value of all products in inventory.

        Returns:
            float: Total value of inventory
        """
        with self.get_db() as db:
            products = db.query(DBProduct).all()
            return sum(product.price * product.quantity for product in products)

    def get_all_products(self) -> List[Dict[str, any]]:
        """
        Get information about all products in inventory.

        Returns:
            List[Dict[str, any]]: List of product information dictionaries
        """
        with self.get_db() as db:
            products = db.query(DBProduct).all()
            return [{
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "total_value": product.price * product.quantity
            } for product in products]

    def __str__(self) -> str:
        """Return a string representation of the inventory."""
        products = self.get_all_products()
        if not products:
            return "Inventory is empty"

        return "\n".join(
            f"{product['name']} - Price: ${product['price']:.2f}, Quantity: {product['quantity']}"
            for product in products
        )