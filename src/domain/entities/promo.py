"""
Domain Layer - Promo Entity

This module contains the Promo entity for student promotions and discounts.

Key principles:
- Promo validation (dates, discount amounts)
- Active status management
- Business rules for promo application
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class PromoType(str, Enum):
    """Types of promotions"""
    PERCENTAGE = "percentage"  # Percentage discount (e.g., 10% off)
    FIXED_AMOUNT = "fixed_amount"  # Fixed amount discount (e.g., Rp 5000 off)
    BUY_ONE_GET_ONE = "buy_one_get_one"  # BOGO deals


class Promo:
    """
    Promo Entity - Promotion/Discount domain model
    
    Contains business logic for:
    - Validity period checking
    - Discount calculation
    - Usage limits
    """
    
    def __init__(
        self,
        umkm_id: UUID,
        title: str,
        description: str,
        promo_type: PromoType,
        discount_value: float,  # Percentage (0-100) or fixed amount
        valid_from: datetime,
        valid_until: datetime,
        id: Optional[UUID] = None,
        code: Optional[str] = None,  # Optional promo code
        min_purchase: Optional[float] = None,  # Minimum purchase for promo
        max_discount: Optional[float] = None,  # Max discount for percentage promos
        usage_limit: Optional[int] = None,  # Total usage limit
        usage_count: int = 0,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.umkm_id = umkm_id
        self.title = title
        self.description = description
        self.promo_type = promo_type
        self.discount_value = discount_value
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.code = code
        self.min_purchase = min_purchase
        self.max_discount = max_discount
        self.usage_limit = usage_limit
        self.usage_count = usage_count
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        self._validate()
    
    def _validate(self) -> None:
        """Domain validation for Promo entity"""
        if not self.title or len(self.title) < 3:
            raise ValueError("Promo title must be at least 3 characters")
        
        if not self.description:
            raise ValueError("Promo description is required")
        
        if self.valid_from >= self.valid_until:
            raise ValueError("Valid from date must be before valid until date")
        
        if self.promo_type == PromoType.PERCENTAGE:
            if self.discount_value <= 0 or self.discount_value > 100:
                raise ValueError("Percentage discount must be between 0 and 100")
        elif self.promo_type == PromoType.FIXED_AMOUNT:
            if self.discount_value <= 0:
                raise ValueError("Fixed discount amount must be positive")
        
        if self.usage_limit is not None and self.usage_limit < 0:
            raise ValueError("Usage limit cannot be negative")
    
    def is_valid(self, current_time: Optional[datetime] = None) -> bool:
        """
        Business logic: Check if promo is currently valid
        
        Business rules for promo validity:
        - Must be within validity period
        - Must be active
        - Must not exceed usage limit
        """
        now = current_time or datetime.utcnow()
        
        if not self.is_active:
            return False
        
        if now < self.valid_from or now > self.valid_until:
            return False
        
        if self.usage_limit is not None and self.usage_count >= self.usage_limit:
            return False
        
        return True
    
    def can_apply_to_order(self, order_amount: float) -> bool:
        """
        Business logic: Check if promo can be applied to an order
        
        Validates minimum purchase requirement.
        """
        if not self.is_valid():
            return False
        
        if self.min_purchase is not None and order_amount < self.min_purchase:
            return False
        
        return True
    
    def calculate_discount(self, order_amount: float) -> float:
        """
        Business logic: Calculate discount amount for an order
        
        This is core business logic - how discounts are calculated
        based on promo type.
        """
        if not self.can_apply_to_order(order_amount):
            return 0.0
        
        if self.promo_type == PromoType.PERCENTAGE:
            discount = order_amount * (self.discount_value / 100)
            if self.max_discount is not None:
                discount = min(discount, self.max_discount)
            return discount
        
        elif self.promo_type == PromoType.FIXED_AMOUNT:
            return min(self.discount_value, order_amount)
        
        # For BOGO and other types, custom logic would be needed
        return 0.0
    
    def increment_usage(self) -> None:
        """Business logic: Increment usage count when promo is used"""
        if self.usage_limit is not None and self.usage_count >= self.usage_limit:
            raise ValueError("Promo usage limit exceeded")
        
        self.usage_count += 1
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Business logic: Deactivate promo"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Business logic: Activate promo"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"Promo(id={self.id}, title={self.title}, type={self.promo_type})"
