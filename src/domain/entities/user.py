"""
Domain Layer - User Entity

This module contains the User entity with embedded business logic.
The User entity represents a user in the system with different roles (Buyer, Seller, Admin).

Key principles:
- Entities contain business logic, not just data
- Domain validation is enforced here
- Entity behavior is defined by its methods
- No infrastructure concerns (databases, APIs) in this layer
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class UserRole(str, Enum):
    """User roles in the system"""
    BUYER = "buyer"  # Regular student buyer
    SELLER = "seller"  # UMKM student merchant
    ADMIN = "admin"  # System administrator


class User:
    """
    User Entity - Core domain model for users
    
    This entity contains business logic for user operations.
    It's NOT just a data container - it validates and enforces business rules.
    """
    
    def __init__(
        self,
        email: str,
        username: str,
        hashed_password: str,
        role: UserRole,
        full_name: str,
        phone: Optional[str] = None,
        id: Optional[UUID] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.role = role
        self.full_name = full_name
        self.phone = phone
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        # Validate on creation
        self._validate()
    
    def _validate(self) -> None:
        """
        Business rule validation for User entity
        
        Domain-level validation ensures data integrity at the entity level.
        This is separate from API validation (Pydantic schemas).
        """
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")
        
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if not self.full_name or len(self.full_name) < 2:
            raise ValueError("Full name must be at least 2 characters")
    
    def can_sell_products(self) -> bool:
        """Business logic: Check if user can sell products"""
        return self.role == UserRole.SELLER and self.is_active
    
    def can_moderate(self) -> bool:
        """Business logic: Check if user can perform moderation actions"""
        return self.role == UserRole.ADMIN and self.is_active
    
    def can_make_orders(self) -> bool:
        """Business logic: Check if user can make orders"""
        return self.role in [UserRole.BUYER, UserRole.SELLER] and self.is_active
    
    def deactivate(self) -> None:
        """Business logic: Deactivate user account"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Business logic: Activate user account"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def update_profile(
        self, 
        full_name: Optional[str] = None,
        phone: Optional[str] = None
    ) -> None:
        """Business logic: Update user profile with validation"""
        if full_name is not None:
            if len(full_name) < 2:
                raise ValueError("Full name must be at least 2 characters")
            self.full_name = full_name
        
        if phone is not None:
            self.phone = phone
        
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, role={self.role})"
