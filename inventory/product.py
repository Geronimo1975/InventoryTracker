"""
Product class module for the Inventory Management System.
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class Product:
    """
    Represents a product in the inventory system.
    
    Attributes:
        name (str): The name of the product
        price (float): The price of the product
        quantity (int): The quantity in stock
    """
    # 
    name: str
    price: float
    quantity: int

    def __post_init__(self):
        """Validate the product attributes after initialization."""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Product name must be a non-empty string")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a non-negative number")
        if not isinstance(self.quantity, int) or self.quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")
        
        self.name = self.name.strip()

    def update_quantity(self, new_quantity: int) -> None:
        """
        Update the quantity of the product.
        
        Args:
            new_quantity (int): The new quantity value
            
        Raises:
            ValueError: If the new quantity is negative
        """
        if not isinstance(new_quantity, int) or new_quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")
        self.quantity = new_quantity

    def get_product_info(self) -> Dict[str, any]:
        """
        Get the product information as a dictionary.
        
        Returns:
            Dict[str, any]: Dictionary containing product details
        """
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "total_value": self.price * self.quantity
        }

    def __str__(self) -> str:
        """Return a string representation of the product."""
        return f"{self.name} - Price: ${self.price:.2f}, Quantity: {self.quantity}"
