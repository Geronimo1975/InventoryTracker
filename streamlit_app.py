"""
Streamlit interface for the Inventory Management System.
"""
import streamlit as st
from inventory import InventoryManager

def main():
    st.title("Inventory Management System")
    
    # Initialize inventory manager in session state if not exists
    if 'inventory' not in st.session_state:
        st.session_state.inventory = InventoryManager()
        # Add sample products
        try:
            st.session_state.inventory.add_product("Laptop", 999.99, 5)
            st.session_state.inventory.add_product("Mouse", 29.99, 20)
            st.session_state.inventory.add_product("Keyboard", 59.99, 15)
        except ValueError:
            pass  # Products might already exist

    # Sidebar for adding new products
    with st.sidebar:
        st.header("Add New Product")
        with st.form("add_product_form"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0.01, step=0.01)
            quantity = st.number_input("Quantity", min_value=0, step=1)
            
            if st.form_submit_button("Add Product"):
                try:
                    st.session_state.inventory.add_product(name, price, quantity)
                    st.success(f"Added product: {name}")
                except ValueError as e:
                    st.error(str(e))

    # Main content area
    st.header("Current Inventory")
    
    # Display total inventory value
    total_value = st.session_state.inventory.get_total_inventory_value()
    st.metric("Total Inventory Value", f"${total_value:.2f}")
    
    # Display and manage products
    products = st.session_state.inventory.get_all_products()
    
    for product in products:
        with st.expander(f"{product['name']} - ${product['price']:.2f}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"Current Quantity: {product['quantity']}")
                st.write(f"Total Value: ${product['total_value']:.2f}")
            
            with col2:
                new_quantity = st.number_input(
                    "New Quantity",
                    min_value=0,
                    value=product['quantity'],
                    key=f"qty_{product['name']}"
                )
            
            with col3:
                if st.button("Update", key=f"update_{product['name']}"):
                    st.session_state.inventory.update_quantity(product['name'], new_quantity)
                    st.success("Quantity updated!")
                if st.button("Remove", key=f"remove_{product['name']}"):
                    st.session_state.inventory.remove_product(product['name'])
                    st.success("Product removed!")
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
