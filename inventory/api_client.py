"""
Unimall B2B API client for the Inventory Management System.
"""
from typing import Dict, List, Optional
import requests


class UnimallAPIClient:
    """
    Client for interacting with Unimall B2B API.
    
    Attributes:
        base_url (str): Base URL for the Unimall B2B API
        api_key (str): API key for authentication
    """
    
    def __init__(self, api_key: str):
        """Initialize the API client with authentication."""
        self.base_url = "https://b2b.unimall.lt/api/v1"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
    
    def get_product_quantities_and_prices(self) -> List[Dict]:
        """
        Fetch product quantities and prices from the API.
        
        Returns:
            List[Dict]: List of products with quantities and prices
        """
        endpoint = f"{self.base_url}/productsQuantitiesAndPrices"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_product_catalogue(self, page: int = 1, per_page: int = 100) -> Dict:
        """
        Fetch product catalog information from the API.
        
        Args:
            page (int): Page number for pagination
            per_page (int): Number of items per page
            
        Returns:
            Dict: Product catalog information
        """
        endpoint = f"{self.base_url}/productsCatalogue"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def sync_inventory(self, inventory_manager) -> None:
        """
        Synchronize local inventory with Unimall B2B data.
        
        Args:
            inventory_manager: InventoryManager instance to update
        """
        try:
            # Get product quantities and prices
            products_data = self.get_product_quantities_and_prices()
            
            # Get catalog information for additional details
            catalog_data = self.get_product_catalogue()
            
            # Create a mapping of product IDs to catalog information
            catalog_map = {
                item['id']: item for item in catalog_data.get('data', [])
            }
            
            # Update inventory with the latest data
            for product in products_data:
                product_id = product.get('id')
                catalog_info = catalog_map.get(product_id, {})
                
                try:
                    inventory_manager.add_product(
                        name=catalog_info.get('name', f"Product {product_id}"),
                        price=float(product.get('price', 0)),
                        quantity=int(product.get('quantity', 0))
                    )
                except ValueError:
                    # Product exists, update quantity and price
                    inventory_manager.update_quantity(
                        catalog_info.get('name', f"Product {product_id}"),
                        int(product.get('quantity', 0))
                    )
                    
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to sync with Unimall B2B API: {str(e)}")
