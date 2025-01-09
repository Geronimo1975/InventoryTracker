"""
InventoryManager class module for the Inventory Management System.
"""
from typing import Dict, Optional, List
from .product import Product


class InventoryManager:
    """
    Manages the inventory of products.
    
    Attributes:
        _products (Dict[str, Product]): Dictionary storing products with name as key
    """

    def __init__(self):
        """Initialize an empty inventory."""
        self._products: Dict[str, Product] = {}

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
        if name.strip() in self._products:
            raise ValueError(f"Product '{name}' already exists in inventory")
        
        product = Product(name=name, price=price, quantity=quantity)
        self._products[product.name] = product

    def remove_product(self, name: str) -> None:
        """
        Remove a product from the inventory.
        
        Args:
            name (str): Name of the product to remove
            
        Raises:
            KeyError: If product doesn't exist
        """
        if name.strip() not in self._products:
            raise KeyError(f"Product '{name}' not found in inventory")
        
        del self._products[name.strip()]

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
        if name.strip() not in self._products:
            raise KeyError(f"Product '{name}' not found in inventory")
        
        self._products[name.strip()].update_quantity(new_quantity)

    def retrieve_product_info(self, name: str) -> Optional[Dict[str, any]]:
        """
        Retrieve information about a specific product.
        
        Args:
            name (str): Product name
            
        Returns:
            Optional[Dict[str, any]]: Product information or None if not found
        """
        product = self._products.get(name.strip())
        return product.get_product_info() if product else None

    def get_total_inventory_value(self) -> float:
        """
        Calculate the total value of all products in inventory.
        
        Returns:
            float: Total value of inventory
        """
        return sum(product.price * product.quantity for product in self._products.values())

    def get_all_products(self) -> List[Dict[str, any]]:
        """
        Get information about all products in inventory.
        
        Returns:
            List[Dict[str, any]]: List of product information dictionaries
        """
        return [product.get_product_info() for product in self._products.values()]

    def __str__(self) -> str:
        """Return a string representation of the inventory."""
        if not self._products:
            return "Inventory is empty"
        
        return "\n".join(str(product) for product in self._products.values())
