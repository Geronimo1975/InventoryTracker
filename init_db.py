"""
Initialize the database with tables and default admin user.
"""
from inventory.database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
