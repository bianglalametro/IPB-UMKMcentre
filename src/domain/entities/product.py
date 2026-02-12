"""
Domain Layer - Product Entity

This module contains the Product entity with business logic.
Products are items/menus sold by UMKMs.

Key principles:
- Inventory management logic
- Price validation
- Availability rules
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class ProductCategory(str, Enum):
    """Product categories for campus marketplace"""
    FOOD = "food"
    BEVERAGE = "beverage"
    SNACK = "snack"
    MERCHANDISE = "merchandise"
    OTHER = "other"


class Product:
    """
    Product Entity - Product/Menu item domain model
    
    Contains business logic for:
    - Price management
    - Stock/availability tracking
    - Product status
    """
    
    def __init__(
        self,
        umkm_id: UUID,
        name: str,
        description: str,
        price: float,
        category: ProductCategory,
        id: Optional[UUID] = None,
        image_url: Optional[str] = None,
        stock_quantity: Optional[int] = None,  # None means unlimited
        is_available: bool = True,
        preorder_required: bool = False,
        min_preorder_hours: int = 0,  # Minimum hours needed for preorder
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.umkm_id = umkm_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.stock_quantity = stock_quantity
        self.is_available = is_available
        self.preorder_required = preorder_required
        self.min_preorder_hours = min_preorder_hours
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        self._validate()
    
    def _validate(self) -> None:
        """Domain validation for Product entity"""
        if not self.name or len(self.name) < 2:
            raise ValueError("Product name must be at least 2 characters")
        
        if not self.description:
            raise ValueError("Product description is required")
        
        if self.price <= 0:
            raise ValueError("Price must be greater than 0")
        
        if self.stock_quantity is not None and self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        if self.min_preorder_hours < 0:
            raise ValueError("Minimum preorder hours cannot be negative")
    
    def can_be_ordered(self, quantity: int = 1) -> bool:
        """
        Business logic: Check if product can be ordered
        
        This encapsulates the business rule for product availability.
        """
        if not self.is_available:
            return False
        
        # Unlimited stock
        if self.stock_quantity is None:
            return True
        
        # Check if enough stock
        return self.stock_quantity >= quantity
    
    def reduce_stock(self, quantity: int) -> None:
        """
        Business logic: Reduce stock when order is placed
        
        This is a critical business operation that must maintain data integrity.
        """
        if self.stock_quantity is None:
            # Unlimited stock, no reduction needed
            return
        
        if not self.can_be_ordered(quantity):
            raise ValueError(f"Insufficient stock. Available: {self.stock_quantity}, Requested: {quantity}")
        
        self.stock_quantity -= quantity
        self.updated_at = datetime.utcnow()
    
    def increase_stock(self, quantity: int) -> None:
        """Business logic: Increase stock (e.g., when order is cancelled)"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if self.stock_quantity is not None:
            self.stock_quantity += quantity
            self.updated_at = datetime.utcnow()
    
    def mark_available(self) -> None:
        """Business logic: Mark product as available"""
        self.is_available = True
        self.updated_at = datetime.utcnow()
    
    def mark_unavailable(self) -> None:
        """Business logic: Mark product as unavailable"""
        self.is_available = False
        self.updated_at = datetime.utcnow()
    
    def update_price(self, new_price: float) -> None:
        """Business logic: Update product price with validation"""
        if new_price <= 0:
            raise ValueError("Price must be greater than 0")
        self.price = new_price
        self.updated_at = datetime.utcnow()
    
    def update_info(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[ProductCategory] = None,
        image_url: Optional[str] = None,
        preorder_required: Optional[bool] = None,
        min_preorder_hours: Optional[int] = None
    ) -> None:
        """Business logic: Update product information with validation"""
        if name is not None:
            if len(name) < 2:
                raise ValueError("Product name must be at least 2 characters")
            self.name = name
        
        if description is not None:
            if not description:
                raise ValueError("Product description cannot be empty")
            self.description = description
        
        if category is not None:
            self.category = category
        
        if image_url is not None:
            self.image_url = image_url
        
        if preorder_required is not None:
            self.preorder_required = preorder_required
        
        if min_preorder_hours is not None:
            if min_preorder_hours < 0:
                raise ValueError("Minimum preorder hours cannot be negative")
            self.min_preorder_hours = min_preorder_hours
        
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
