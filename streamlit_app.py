"""
Streamlit interface for the Inventory Management System.
"""
import streamlit as st
from inventory import InventoryManager
from inventory.user import UserRole
from inventory.user_manager import UserManager

def init_session_state():
    """Initialize session state variables."""
    if 'inventory' not in st.session_state:
        st.session_state.inventory = InventoryManager()
        # Add sample products
        try:
            st.session_state.inventory.add_product("Laptop", 999.99, 5)
            st.session_state.inventory.add_product("Mouse", 29.99, 20)
            st.session_state.inventory.add_product("Keyboard", 59.99, 15)
        except ValueError:
            pass

    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = UserManager()

    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

    if 'last_sync_time' not in st.session_state:
        st.session_state.last_sync_time = None

def login_page():
    """Display login form."""
    # Apply custom styles
    st.markdown("""
        <style>
        @import url('styles/styles.css');
        </style>
    """, unsafe_allow_html=True)

    st.title("🔐 Inventory Management System")
    st.markdown("### Welcome to the System")

    with st.form(key="login"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            user = st.session_state.user_manager.authenticate_user(username, password)
            if user:
                st.session_state.current_user = user
                # Role-based welcome message
                if user.role == UserRole.ADMIN:
                    st.markdown("""
                        <div class='welcome-admin'>
                            <h2>👋 Welcome, Administrator!</h2>
                            <p>You have full access to manage inventory and users.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class='welcome-partner'>
                            <h2>👋 Welcome, Partner!</h2>
                            <p>You can view and monitor inventory status.</p>
                        </div>
                    """, unsafe_allow_html=True)
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password")

    # Registration section
    st.markdown("---")
    st.markdown("### 📝 Create New Account")

    with st.form(key="register"):
        new_username = st.text_input("👤 New Username")
        new_password = st.text_input("🔑 New Password", type="password")
        role = st.selectbox("🎭 Account Type", ["partner", "admin"])
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            register = st.form_submit_button("Register", use_container_width=True)

        if register:
            try:
                st.session_state.user_manager.register_user(
                    new_username,
                    new_password,
                    UserRole.ADMIN if role == "admin" else UserRole.PARTNER
                )
                st.success("✅ Registration successful! Please login.")
            except ValueError as e:
                st.error(f"❌ {str(e)}")

def inventory_page():
    """Display inventory management interface."""
    st.title("Inventory Management System")
    user = st.session_state.current_user

    # Display user info and logout button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"Logged in as: {user.username} ({user.role.value})")
    with col2:
        # API sync status (only for admins)
        if user.role == UserRole.ADMIN:
            st.info("API Sync: Not configured")
    with col3:
        if st.button("Logout"):
            st.session_state.current_user = None
            st.experimental_rerun()

    # Admin-only section
    if user.role == UserRole.ADMIN:
        with st.sidebar:
            st.header("Admin Controls")

            # API Sync button (disabled for now)
            st.button("Sync with Unimall B2B", 
                     disabled=True, 
                     help="API key not configured. Please configure API key to enable synchronization.")

            st.markdown("---")

            # Add new product form
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

    # Display inventory
    st.header("Current Inventory")
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

            # Only allow quantity updates for admin users
            if user.role == UserRole.ADMIN:
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

def main():
    """Main application entry point."""
    init_session_state()

    if st.session_state.current_user is None:
        login_page()
    else:
        inventory_page()

if __name__ == "__main__":
    main()