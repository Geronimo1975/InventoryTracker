"""
User management functionality for the Inventory Management System.
"""
from typing import Dict, Optional
from .user import User, UserRole


class UserManager:
    """
    Manages user accounts in the system.
    
    Attributes:
        _users (Dict[str, User]): Dictionary storing users with username as key
    """

    def __init__(self):
        """Initialize with a default admin user."""
        self._users: Dict[str, User] = {}
        # Create default admin user if not exists
        if "admin" not in self._users:
            self.register_user("admin", "admin123", UserRole.ADMIN)

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
        if username in self._users:
            raise ValueError(f"Username '{username}' already exists")
        
        user = User.create(username, password, role)
        self._users[username] = user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username and password.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            Optional[User]: User object if authentication successful, None otherwise
        """
        user = self._users.get(username)
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self._users.get(username)

    def get_all_users(self) -> Dict[str, Dict]:
        """Get all users as dictionary."""
        return {username: user.to_dict() for username, user in self._users.items()}
