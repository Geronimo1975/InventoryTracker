"""
User management functionality for the Inventory Management System.
"""
from typing import Dict, Optional
from contextlib import contextmanager
from .user import User, UserRole
from .database import SessionLocal, DBUser
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    """
    Manages user accounts in the system using PostgreSQL database.
    """

    @contextmanager
    def get_db(self):
        """Get database session context."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def __init__(self):
        """Initialize with a default admin user."""
        with self.get_db() as db:
            # Create default admin user if not exists
            admin = db.query(DBUser).filter(DBUser.username == "admin").first()
            if not admin:
                admin_user = DBUser(
                    username="admin",
                    password_hash=generate_password_hash("admin123"),
                    role=UserRole.ADMIN.value,
                    is_active=1
                )
                db.add(admin_user)
                db.commit()

    def register_user(self, username: str, password: str, role: UserRole) -> None:
        """
        Register a new user.

        Args:
            username (str): Username
            password (str): Password
            role (UserRole): User role

        Raises:
            ValueError: If username already exists
        """
        with self.get_db() as db:
            if db.query(DBUser).filter(DBUser.username == username).first():
                raise ValueError(f"Username '{username}' already exists")

            user = DBUser(
                username=username,
                password_hash=generate_password_hash(password),
                role=role.value,
                is_active=1
            )
            db.add(user)
            db.commit()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username and password.

        Args:
            username (str): Username
            password (str): Password

        Returns:
            Optional[User]: User object if authentication successful, None otherwise
        """
        with self.get_db() as db:
            db_user = db.query(DBUser).filter(DBUser.username == username).first()
            if db_user and check_password_hash(db_user.password_hash, password):
                return User(
                    username=db_user.username,
                    password_hash=db_user.password_hash,
                    role=UserRole(db_user.role),
                    is_active=bool(db_user.is_active)
                )
        return None

    def get_user(self, username: str) -> Optional[User]:
        """Get user by username."""
        with self.get_db() as db:
            db_user = db.query(DBUser).filter(DBUser.username == username).first()
            if db_user:
                return User(
                    username=db_user.username,
                    password_hash=db_user.password_hash,
                    role=UserRole(db_user.role),
                    is_active=bool(db_user.is_active)
                )
        return None

    def get_all_users(self) -> Dict[str, Dict]:
        """Get all users as dictionary."""
        with self.get_db() as db:
            users = db.query(DBUser).all()
            return {
                user.username: {
                    "username": user.username,
                    "role": user.role,
                    "is_active": bool(user.is_active)
                } for user in users
            }