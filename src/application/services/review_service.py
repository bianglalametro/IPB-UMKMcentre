"""
Application Layer - Review Service

This module contains the application services for review management.
"""

from typing import List, Optional
from uuid import UUID

from src.domain.entities import Review
from src.domain.repositories import ReviewRepository, UMKMRepository, OrderRepository


class ReviewService:
    """
    Review Application Service
    
    Orchestrates review-related use cases:
    - Create review
    - Update review
    - Moderate reviews (admin)
    - List reviews
    """
    
    def __init__(
        self,
        review_repository: ReviewRepository,
        umkm_repository: UMKMRepository,
        order_repository: OrderRepository
    ):
        self.review_repository = review_repository
        self.umkm_repository = umkm_repository
        self.order_repository = order_repository
    
    async def create_review(
        self,
        user_id: UUID,
        umkm_id: UUID,
        rating: int,
        comment: str,
        order_id: Optional[UUID] = None
    ) -> Review:
        """
        Use Case: Create a review
        
        Business rules:
        - UMKM must exist
        - If linked to order, verify user made the order
        """
        # Verify UMKM exists
        umkm = await self.umkm_repository.find_by_id(umkm_id)
        if not umkm:
            raise ValueError("UMKM not found")
        
        # If order_id provided, verify user made the order
        if order_id:
            order = await self.order_repository.find_by_id(order_id)
            if not order:
                raise ValueError("Order not found")
            
            if order.buyer_id != user_id:
                raise ValueError("You can only review orders you made")
            
            if order.umkm_id != umkm_id:
                raise ValueError("Order does not belong to this UMKM")
        
        # Create Review entity
        review = Review(
            user_id=user_id,
            umkm_id=umkm_id,
            rating=rating,
            comment=comment,
            order_id=order_id
        )
        
        # Update UMKM rating
        # Domain business logic: UMKM calculates new average
        umkm.update_rating(rating)
        await self.umkm_repository.save(umkm)
        
        # Persist review
        saved_review = await self.review_repository.save(review)
        return saved_review
    
    async def get_review(self, review_id: UUID) -> Optional[Review]:
        """Use Case: Get review by ID"""
        return await self.review_repository.find_by_id(review_id)
    
    async def get_umkm_reviews(
        self,
        umkm_id: UUID,
        visible_only: bool = True
    ) -> List[Review]:
        """Use Case: Get all reviews for a UMKM"""
        return await self.review_repository.find_by_umkm_id(
            umkm_id,
            visible_only=visible_only
        )
    
    async def get_user_reviews(self, user_id: UUID) -> List[Review]:
        """Use Case: Get all reviews by a user"""
        return await self.review_repository.find_by_user_id(user_id)
    
    async def update_review(
        self,
        review_id: UUID,
        user_id: UUID,
        new_rating: int,
        new_comment: str
    ) -> Review:
        """
        Use Case: Update review
        
        Only the author can update their review.
        """
        review = await self.review_repository.find_by_id(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Authorization check
        if review.user_id != user_id:
            raise ValueError("Unauthorized: You can only update your own reviews")
        
        # Domain business logic: Update with validation
        review.update_content(new_rating, new_comment)
        
        # Persist
        await self.review_repository.save(review)
        return review
    
    async def flag_review(self, review_id: UUID) -> Review:
        """Use Case: Flag review for moderation"""
        review = await self.review_repository.find_by_id(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Domain business logic: Flag
        review.flag_for_moderation()
        
        # Persist
        await self.review_repository.save(review)
        return review
    
    async def hide_review(self, review_id: UUID, admin_id: UUID) -> Review:
        """Use Case: Hide review (admin action)"""
        # Note: In a real app, verify admin_id has admin role
        # For now, simplified
        
        review = await self.review_repository.find_by_id(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Domain business logic: Hide
        review.hide()
        
        # Persist
        await self.review_repository.save(review)
        return review
    
    async def show_review(self, review_id: UUID, admin_id: UUID) -> Review:
        """Use Case: Show hidden review (admin action)"""
        review = await self.review_repository.find_by_id(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Domain business logic: Show
        review.show()
        
        # Persist
        await self.review_repository.save(review)
        return review
