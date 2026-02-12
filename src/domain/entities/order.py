"""
Domain Layer - Order Entity

This module contains the Order entity with business logic for the preorder system.
Orders represent customer purchases with state management and validation.

Key principles:
- Order state machine (placed -> confirmed -> ready -> completed)
- Business rules for order transitions
- Total calculation logic
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4


class OrderStatus(str, Enum):
    """Order status in the fulfillment workflow"""
    PLACED = "placed"  # Order placed by customer
    CONFIRMED = "confirmed"  # Confirmed by seller
    PREPARING = "preparing"  # Being prepared
    READY = "ready"  # Ready for pickup
    COMPLETED = "completed"  # Picked up and completed
    CANCELLED = "cancelled"  # Cancelled by customer or seller


class OrderItem:
    """
    Value Object: Represents an item in an order
    
    This is a value object, not an entity, because it has no identity
    outside of its parent Order. Two order items with the same values
    are considered equal.
    """
    
    def __init__(
        self,
        product_id: UUID,
        product_name: str,
        quantity: int,
        unit_price: float
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if unit_price <= 0:
            raise ValueError("Unit price must be positive")
    
    def subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self.quantity * self.unit_price
    
    def __repr__(self) -> str:
        return f"OrderItem(product={self.product_name}, qty={self.quantity}, price={self.unit_price})"


class Order:
    """
    Order Entity - Order/Preorder domain model
    
    Contains business logic for:
    - Order state transitions
    - Total calculation
    - Pickup time validation
    - Cancellation rules
    """
    
    def __init__(
        self,
        buyer_id: UUID,
        umkm_id: UUID,
        items: List[OrderItem],
        status: OrderStatus = OrderStatus.PLACED,
        id: Optional[UUID] = None,
        pickup_time: Optional[datetime] = None,
        notes: Optional[str] = None,
        total_amount: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        cancelled_at: Optional[datetime] = None,
        cancellation_reason: Optional[str] = None
    ):
        self.id = id or uuid4()
        self.buyer_id = buyer_id
        self.umkm_id = umkm_id
        self.items = items
        self.status = status
        self.pickup_time = pickup_time
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.cancelled_at = cancelled_at
        self.cancellation_reason = cancellation_reason
        
        # Calculate total if not provided
        self.total_amount = total_amount if total_amount is not None else self._calculate_total()
        
        self._validate()
    
    def _validate(self) -> None:
        """Domain validation for Order entity"""
        if not self.items:
            raise ValueError("Order must have at least one item")
        
        if self.pickup_time:
            if self.pickup_time <= datetime.utcnow():
                raise ValueError("Pickup time must be in the future")
        
        if self.total_amount <= 0:
            raise ValueError("Order total must be positive")
    
    def _calculate_total(self) -> float:
        """
        Business logic: Calculate order total
        
        This is pure business logic - calculating the total based on items.
        """
        return sum(item.subtotal() for item in self.items)
    
    def can_be_cancelled(self) -> bool:
        """
        Business logic: Check if order can be cancelled
        
        Business rule: Orders can only be cancelled if not yet completed.
        """
        return self.status not in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]
    
    def can_be_confirmed(self) -> bool:
        """Business logic: Check if order can be confirmed by seller"""
        return self.status == OrderStatus.PLACED
    
    def confirm(self) -> None:
        """
        Business logic: Confirm order (seller action)
        
        State transition with business rules enforcement.
        """
        if not self.can_be_confirmed():
            raise ValueError(f"Cannot confirm order in status: {self.status}")
        
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.utcnow()
    
    def mark_preparing(self) -> None:
        """Business logic: Mark order as being prepared"""
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Only confirmed orders can be marked as preparing")
        
        self.status = OrderStatus.PREPARING
        self.updated_at = datetime.utcnow()
    
    def mark_ready(self) -> None:
        """Business logic: Mark order as ready for pickup"""
        if self.status != OrderStatus.PREPARING:
            raise ValueError("Only preparing orders can be marked as ready")
        
        self.status = OrderStatus.READY
        self.updated_at = datetime.utcnow()
    
    def complete(self) -> None:
        """Business logic: Complete order (picked up)"""
        if self.status != OrderStatus.READY:
            raise ValueError("Only ready orders can be completed")
        
        self.status = OrderStatus.COMPLETED
        self.updated_at = datetime.utcnow()
    
    def cancel(self, reason: Optional[str] = None) -> None:
        """
        Business logic: Cancel order
        
        Business rules:
        - Cannot cancel completed or already cancelled orders
        - Cancellation must include timestamp
        """
        if not self.can_be_cancelled():
            raise ValueError(f"Cannot cancel order in status: {self.status}")
        
        self.status = OrderStatus.CANCELLED
        self.cancelled_at = datetime.utcnow()
        self.cancellation_reason = reason
        self.updated_at = datetime.utcnow()
    
    def is_preorder(self) -> bool:
        """Check if this is a preorder (has future pickup time)"""
        return self.pickup_time is not None and self.pickup_time > datetime.utcnow()
    
    def update_pickup_time(self, new_pickup_time: datetime) -> None:
        """Business logic: Update pickup time with validation"""
        if self.status not in [OrderStatus.PLACED, OrderStatus.CONFIRMED]:
            raise ValueError("Cannot update pickup time for orders in progress")
        
        if new_pickup_time <= datetime.utcnow():
            raise ValueError("Pickup time must be in the future")
        
        self.pickup_time = new_pickup_time
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"Order(id={self.id}, status={self.status}, total={self.total_amount})"
