"""
Domain Layer - UMKM Entity

This module contains the UMKM (merchant profile) entity with business logic.
UMKM represents a student-owned business/food stall on campus.

Key principles:
- Contains business rules for merchant operations
- Validates merchant data
- Enforces domain constraints
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class UMKMStatus(str, Enum):
    """UMKM operational status"""
    PENDING = "pending"  # Awaiting admin approval
    ACTIVE = "active"  # Approved and operational
    SUSPENDED = "suspended"  # Temporarily suspended
    CLOSED = "closed"  # Permanently closed


class UMKM:
    """
    UMKM Entity - Merchant profile domain model
    
    Represents a student-owned business with business logic for:
    - Approval workflow
    - Status management
    - Operating hours validation
    """
    
    def __init__(
        self,
        owner_id: UUID,
        name: str,
        description: str,
        location: str,
        phone: str,
        status: UMKMStatus = UMKMStatus.PENDING,
        id: Optional[UUID] = None,
        image_url: Optional[str] = None,
        operating_hours: Optional[str] = None,
        rating_average: float = 0.0,
        rating_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.owner_id = owner_id
        self.name = name
        self.description = description
        self.location = location
        self.phone = phone
        self.status = status
        self.image_url = image_url
        self.operating_hours = operating_hours
        self.rating_average = rating_average
        self.rating_count = rating_count
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        self._validate()
    
    def _validate(self) -> None:
        """Domain validation for UMKM entity"""
        if not self.name or len(self.name) < 3:
            raise ValueError("UMKM name must be at least 3 characters")
        
        if not self.description or len(self.description) < 10:
            raise ValueError("Description must be at least 10 characters")
        
        if not self.location:
            raise ValueError("Location is required")
        
        if not self.phone:
            raise ValueError("Phone number is required")
        
        if self.rating_average < 0 or self.rating_average > 5:
            raise ValueError("Rating must be between 0 and 5")
    
    def is_operational(self) -> bool:
        """Business logic: Check if UMKM is currently operational"""
        return self.status == UMKMStatus.ACTIVE
    
    def can_accept_orders(self) -> bool:
        """Business logic: Check if UMKM can accept orders"""
        return self.status == UMKMStatus.ACTIVE
    
    def approve(self) -> None:
        """Business logic: Approve UMKM (admin action)"""
        if self.status != UMKMStatus.PENDING:
            raise ValueError("Only pending UMKMs can be approved")
        self.status = UMKMStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def suspend(self, reason: Optional[str] = None) -> None:
        """Business logic: Suspend UMKM operations"""
        if self.status == UMKMStatus.CLOSED:
            raise ValueError("Cannot suspend a closed UMKM")
        self.status = UMKMStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
    
    def close(self) -> None:
        """Business logic: Permanently close UMKM"""
        self.status = UMKMStatus.CLOSED
        self.updated_at = datetime.utcnow()
    
    def reactivate(self) -> None:
        """Business logic: Reactivate a suspended UMKM"""
        if self.status == UMKMStatus.CLOSED:
            raise ValueError("Cannot reactivate a closed UMKM")
        self.status = UMKMStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def update_rating(self, new_rating: float) -> None:
        """
        Business logic: Update average rating when a new review is added
        
        This method demonstrates how business logic lives in the domain:
        The calculation of new average rating is a business rule.
        """
        if new_rating < 1 or new_rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        total_rating = self.rating_average * self.rating_count
        self.rating_count += 1
        self.rating_average = (total_rating + new_rating) / self.rating_count
        self.updated_at = datetime.utcnow()
    
    def update_info(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        phone: Optional[str] = None,
        operating_hours: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> None:
        """Business logic: Update UMKM information with validation"""
        if name is not None:
            if len(name) < 3:
                raise ValueError("UMKM name must be at least 3 characters")
            self.name = name
        
        if description is not None:
            if len(description) < 10:
                raise ValueError("Description must be at least 10 characters")
            self.description = description
        
        if location is not None:
            self.location = location
        
        if phone is not None:
            self.phone = phone
        
        if operating_hours is not None:
            self.operating_hours = operating_hours
        
        if image_url is not None:
            self.image_url = image_url
        
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"UMKM(id={self.id}, name={self.name}, status={self.status})"
