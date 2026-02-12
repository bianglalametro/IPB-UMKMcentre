"""
Domain Layer - Review Entity

This module contains the Review entity for rating and reviewing UMKMs and products.

Key principles:
- Rating validation
- Review moderation
- Business rules for reviews
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Review:
    """
    Review Entity - Rating and review domain model
    
    Contains business logic for:
    - Rating validation (1-5 scale)
    - Review text validation
    - Moderation status
    """
    
    def __init__(
        self,
        user_id: UUID,
        umkm_id: UUID,
        rating: int,
        comment: str,
        order_id: Optional[UUID] = None,  # Review can be linked to an order
        id: Optional[UUID] = None,
        is_visible: bool = True,
        is_flagged: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.umkm_id = umkm_id
        self.order_id = order_id
        self.rating = rating
        self.comment = comment
        self.is_visible = is_visible
        self.is_flagged = is_flagged
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        self._validate()
    
    def _validate(self) -> None:
        """Domain validation for Review entity"""
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        if not self.comment or len(self.comment) < 5:
            raise ValueError("Review comment must be at least 5 characters")
        
        if len(self.comment) > 1000:
            raise ValueError("Review comment cannot exceed 1000 characters")
    
    def is_positive(self) -> bool:
        """Business logic: Check if review is positive (4-5 stars)"""
        return self.rating >= 4
    
    def flag_for_moderation(self) -> None:
        """Business logic: Flag review for admin moderation"""
        self.is_flagged = True
        self.updated_at = datetime.utcnow()
    
    def hide(self) -> None:
        """Business logic: Hide review (admin action)"""
        self.is_visible = False
        self.updated_at = datetime.utcnow()
    
    def show(self) -> None:
        """Business logic: Show previously hidden review (admin action)"""
        self.is_visible = True
        self.is_flagged = False
        self.updated_at = datetime.utcnow()
    
    def update_content(self, new_rating: int, new_comment: str) -> None:
        """Business logic: Update review content with validation"""
        if new_rating < 1 or new_rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        if not new_comment or len(new_comment) < 5:
            raise ValueError("Review comment must be at least 5 characters")
        
        if len(new_comment) > 1000:
            raise ValueError("Review comment cannot exceed 1000 characters")
        
        self.rating = new_rating
        self.comment = new_comment
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"Review(id={self.id}, rating={self.rating}, umkm_id={self.umkm_id})"
