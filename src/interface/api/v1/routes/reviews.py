"""
Interface Layer - Review Routes

THIN CONTROLLERS for review management.
"""

from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.review_service import ReviewService
from src.domain.entities import User
from src.interface.api.v1.schemas import (
    ReviewCreateRequest,
    ReviewUpdateRequest,
    ReviewResponse,
    MessageResponse
)
from src.interface.api.v1.dependencies import (
    get_review_service,
    get_current_user,
    get_current_admin
)

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    request: ReviewCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    """
    Create a new review
    
    Requires authentication.
    """
    try:
        review = await review_service.create_review(
            user_id=current_user.id,
            umkm_id=request.umkm_id,
            rating=request.rating,
            comment=request.comment,
            order_id=request.order_id
        )
        
        return ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            umkm_id=review.umkm_id,
            order_id=review.order_id,
            rating=review.rating,
            comment=review.comment,
            is_visible=review.is_visible,
            is_flagged=review.is_flagged,
            created_at=review.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/umkm/{umkm_id}", response_model=List[ReviewResponse])
async def get_umkm_reviews(
    umkm_id: UUID,
    review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    """
    Get all reviews for a UMKM
    
    Public endpoint - shows only visible reviews.
    """
    reviews = await review_service.get_umkm_reviews(umkm_id, visible_only=True)
    
    return [
        ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            umkm_id=review.umkm_id,
            order_id=review.order_id,
            rating=review.rating,
            comment=review.comment,
            is_visible=review.is_visible,
            is_flagged=review.is_flagged,
            created_at=review.created_at
        )
        for review in reviews
    ]


@router.get("/my-reviews", response_model=List[ReviewResponse])
async def get_my_reviews(
    current_user: Annotated[User, Depends(get_current_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    """
    Get reviews written by current user
    """
    reviews = await review_service.get_user_reviews(current_user.id)
    
    return [
        ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            umkm_id=review.umkm_id,
            order_id=review.order_id,
            rating=review.rating,
            comment=review.comment,
            is_visible=review.is_visible,
            is_flagged=review.is_flagged,
            created_at=review.created_at
        )
        for review in reviews
    ]


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: UUID,
    request: ReviewUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    """
    Update review
    
    Only the review author can update it.
    """
    try:
        review = await review_service.update_review(
            review_id=review_id,
            user_id=current_user.id,
            new_rating=request.rating,
            new_comment=request.comment
        )
        
        return ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            umkm_id=review.umkm_id,
            order_id=review.order_id,
            rating=review.rating,
            comment=review.comment,
            is_visible=review.is_visible,
            is_flagged=review.is_flagged,
            created_at=review.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{review_id}/flag", response_model=MessageResponse)
async def flag_review(
    review_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    """
    Flag review for moderation
    
    Any authenticated user can flag inappropriate reviews.
    """
    try:
        await review_service.flag_review(review_id)
        return MessageResponse(message="Review flagged for moderation")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{review_id}/hide", response_model=MessageResponse)
async def hide_review(
    review_id: UUID,
    current_user: Annotated[User, Depends(get_current_admin)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    """
    Hide review (admin only)
    
    Admin moderation action.
    """
    try:
        await review_service.hide_review(review_id, current_user.id)
        return MessageResponse(message="Review hidden successfully")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{review_id}/show", response_model=MessageResponse)
async def show_review(
    review_id: UUID,
    current_user: Annotated[User, Depends(get_current_admin)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    """
    Show hidden review (admin only)
    
    Admin moderation action.
    """
    try:
        await review_service.show_review(review_id, current_user.id)
        return MessageResponse(message="Review shown successfully")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
