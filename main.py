"""
Main entry point for the Inventory Management System.
"""
from inventory import InventoryManager


def main():
    """Main function to demonstrate the Inventory Management System."""
    # Create inventory manager instance
    inventory = InventoryManager()

    try:
        # Add sample products
        inventory.add_product("Laptop", 999.99, 5)
        inventory.add_product("Mouse", 29.99, 20)
        inventory.add_product("Keyboard", 59.99, 15)
        inventory.add_product("Monitor", 299.99, 8)

        # Display all products
        print("Current Inventory:")
        print(inventory)
        print("\nTotal Inventory Value: ${:.2f}".format(inventory.get_total_inventory_value()))

        # Demonstrate updating quantity
        print("\nUpdating Laptop quantity to 7...")
        inventory.update_quantity("Laptop", 7)

        # Demonstrate removing a product
        print("Removing Mouse from inventory...")
        inventory.remove_product("Mouse")

        # Display updated inventory
        print("\nUpdated Inventory:")
        print(inventory)
        print("\nUpdated Total Inventory Value: ${:.2f}".format(inventory.get_total_inventory_value()))

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
