# Inventory Management System Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Components](#key-components)
3. [Project Structure](#project-structure)
4. [Setup and Installation](#setup-and-installation)
5. [Usage Guide](#usage-guide)
6. [Technical Details](#technical-details)
7. [Challenges and Solutions](#challenges-and-solutions)
8. [Future Enhancements](#future-enhancements)

## Project Overview

The Inventory Management System is a comprehensive Python-based solution designed for efficient product tracking and business operations management. It provides a robust platform for managing inventory, user authentication, and real-time data visualization.

### Key Features
- Product inventory tracking with real-time updates
- Multi-user support with role-based access control
- Streamlit-powered web interface
- PostgreSQL database integration
- PDF and Excel export functionality
- Real-time notifications
- RESTful API integration with Unimall B2B platform

## Key Components

### 1. Inventory Management (`inventory_manager.py`)
The core component handling product management and inventory operations.

```python
class InventoryManager:
    """
    Key methods:
    - add_product(name, price, quantity)
    - remove_product(name)
    - update_quantity(name, new_quantity)
    - get_total_inventory_value()
    """
```

### 2. User Management (`user_manager.py`)
Handles user authentication and authorization with role-based access control.

```python
class UserManager:
    """
    Features:
    - User registration and authentication
    - Role-based access (Admin/Partner)
    - Secure password handling
    """
```

### 3. API Integration (`api_client.py`)
Provides integration with the Unimall B2B API for product synchronization.

```python
class UnimallAPIClient:
    """
    Capabilities:
    - Product catalog synchronization
    - Real-time price and quantity updates
    - Automated inventory synchronization
    """
```

### 4. Web Interface (`streamlit_app.py`)
Interactive web interface built with Streamlit, featuring:
- Dashboard with real-time inventory status
- User authentication system
- Product management interface
- Export functionality
- Customizable themes

## Project Structure

```
project/
├── inventory/               # Core package directory
│   ├── __init__.py         # Package initialization
│   ├── api_client.py       # B2B API integration
│   ├── database.py         # Database configurations
│   ├── export_manager.py   # Export functionality
│   ├── inventory_manager.py # Core inventory logic
│   ├── product.py          # Product model
│   ├── user.py             # User model
│   └── user_manager.py     # User management
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_inventory_manager.py
├── main.py                 # CLI entry point
└── streamlit_app.py        # Web interface
```

## Setup and Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- Required Python packages

### Installation Steps

1. Clone the repository
2. Install dependencies:
```bash
pip install streamlit pandas sqlalchemy psycopg2-binary reportlab openpyxl flask-login flask-wtf
```

3. Set up environment variables:
```bash
DATABASE_URL=postgresql://username:password@host:port/dbname
```

4. Initialize the database:
```bash
python init_db.py
```

## Usage Guide

### Starting the Application

1. Run the web interface:
```bash
python -m streamlit run streamlit_app.py
```

2. Access the application at `http://localhost:8501`

### User Roles and Permissions

1. **Admin Users**
   - Full access to all features
   - Can add/remove products
   - Can manage other users
   - Access to export functionality

2. **Partner Users**
   - View-only access to inventory
   - Can view product details
   - Cannot modify inventory

### Basic Operations

1. **Adding Products**
```python
inventory.add_product("Laptop", 999.99, 5)
```

2. **Updating Quantities**
```python
inventory.update_quantity("Laptop", 7)
```

3. **Generating Reports**
   - Use the export functionality in the web interface
   - Supports PDF and Excel formats

## Technical Details

### Database Schema
- Products table: name, price, quantity
- Users table: username, password_hash, role, is_active

### API Integration
The system integrates with Unimall B2B API for:
- Product catalog synchronization
- Real-time price updates
- Inventory synchronization

### Security Features
- Password hashing using Werkzeug
- Role-based access control
- Session management
- Protected API endpoints

## Challenges and Solutions

1. **Real-time Updates**
   - Challenge: Maintaining data consistency across multiple users
   - Solution: Implemented real-time notification system and database session management

2. **Data Synchronization**
   - Challenge: Keeping local inventory in sync with B2B API
   - Solution: Automated synchronization with error handling and retry mechanism

3. **User Authentication**
   - Challenge: Secure user management with different access levels
   - Solution: Implemented role-based access control with Flask-Login

## Future Enhancements

1. **Planned Features**
   - Advanced analytics dashboard
   - Automated inventory alerts
   - Mobile application support
   - Batch import/export functionality

2. **Technical Improvements**
   - Enhanced caching mechanism
   - API rate limiting
   - Advanced search functionality
   - Real-time chat support

---

## Contributing
Please refer to CONTRIBUTING.md for guidelines on how to contribute to this project.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
