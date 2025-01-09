"""
User management module for the Inventory Management System.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from werkzeug.security import generate_password_hash, check_password_hash


class UserRole(Enum):
    """User role types in the system."""
    ADMIN = "admin"
    PARTNER = "partner"


@dataclass
class User:
    """
    Represents a user in the system.
    
    Attributes:
        username (str): User's username
        password_hash (str): Hashed password
        role (UserRole): User's role (admin or partner)
        is_active (bool): Whether the user account is active
    """
    username: str
    password_hash: str
    role: UserRole
    is_active: bool = True

    @staticmethod
    def create(username: str, password: str, role: UserRole) -> 'User':
        """Create a new user with a hashed password."""
        return User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )

    def check_password(self, password: str) -> bool:
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> Dict:
        """Convert user to dictionary representation."""
        return {
            "username": self.username,
            "role": self.role.value,
            "is_active": self.is_active
        }
