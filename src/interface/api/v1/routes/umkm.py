"""
Interface Layer - UMKM Routes

THIN CONTROLLERS for UMKM management.
All business logic is in the application service layer.
"""

from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.umkm_service import UMKMService
from src.domain.entities import User
from src.interface.api.v1.schemas import (
    UMKMCreateRequest,
    UMKMUpdateRequest,
    UMKMResponse,
    MessageResponse
)
from src.interface.api.v1.dependencies import (
    get_umkm_service,
    get_current_user,
    get_current_seller,
    get_current_admin
)

router = APIRouter(prefix="/umkm", tags=["UMKM"])


@router.post("", response_model=UMKMResponse, status_code=status.HTTP_201_CREATED)
async def create_umkm(
    request: UMKMCreateRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    umkm_service: Annotated[UMKMService, Depends(get_umkm_service)]
):
    """
    Register a new UMKM (seller only)
    
    Creates a new UMKM for the authenticated seller.
    """
    try:
        umkm = await umkm_service.register_umkm(
            owner_id=current_user.id,
            name=request.name,
            description=request.description,
            location=request.location,
            phone=request.phone,
            operating_hours=request.operating_hours,
            image_url=request.image_url
        )
        
        return UMKMResponse(
            id=umkm.id,
            owner_id=umkm.owner_id,
            name=umkm.name,
            description=umkm.description,
            location=umkm.location,
            phone=umkm.phone,
            status=umkm.status.value,
            image_url=umkm.image_url,
            operating_hours=umkm.operating_hours,
            rating_average=umkm.rating_average,
            rating_count=umkm.rating_count,
            created_at=umkm.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[UMKMResponse])
async def list_umkms(
    active_only: bool = False,
    umkm_service: Annotated[UMKMService, Depends(get_umkm_service)]
):
    """
    List all UMKMs
    
    Public endpoint - no authentication required.
    Can filter to show only active UMKMs.
    """
    umkms = await umkm_service.get_all_umkms(active_only=active_only)
    
    return [
        UMKMResponse(
            id=umkm.id,
            owner_id=umkm.owner_id,
            name=umkm.name,
            description=umkm.description,
            location=umkm.location,
            phone=umkm.phone,
            status=umkm.status.value,
            image_url=umkm.image_url,
            operating_hours=umkm.operating_hours,
            rating_average=umkm.rating_average,
            rating_count=umkm.rating_count,
            created_at=umkm.created_at
        )
        for umkm in umkms
    ]


@router.get("/{umkm_id}", response_model=UMKMResponse)
async def get_umkm(
    umkm_id: UUID,
    umkm_service: Annotated[UMKMService, Depends(get_umkm_service)]
):
    """
    Get UMKM details by ID
    
    Public endpoint - no authentication required.
    """
    umkm = await umkm_service.get_umkm(umkm_id)
    
    if not umkm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UMKM not found"
        )
    
    return UMKMResponse(
        id=umkm.id,
        owner_id=umkm.owner_id,
        name=umkm.name,
        description=umkm.description,
        location=umkm.location,
        phone=umkm.phone,
        status=umkm.status.value,
        image_url=umkm.image_url,
        operating_hours=umkm.operating_hours,
        rating_average=umkm.rating_average,
        rating_count=umkm.rating_count,
        created_at=umkm.created_at
    )


@router.put("/{umkm_id}", response_model=UMKMResponse)
async def update_umkm(
    umkm_id: UUID,
    request: UMKMUpdateRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    umkm_service: Annotated[UMKMService, Depends(get_umkm_service)]
):
    """
    Update UMKM information (seller only)
    
    Only the UMKM owner can update their UMKM.
    """
    try:
        umkm = await umkm_service.update_umkm(
            umkm_id=umkm_id,
            owner_id=current_user.id,
            name=request.name,
            description=request.description,
            location=request.location,
            phone=request.phone,
            operating_hours=request.operating_hours,
            image_url=request.image_url
        )
        
        return UMKMResponse(
            id=umkm.id,
            owner_id=umkm.owner_id,
            name=umkm.name,
            description=umkm.description,
            location=umkm.location,
            phone=umkm.phone,
            status=umkm.status.value,
            image_url=umkm.image_url,
            operating_hours=umkm.operating_hours,
            rating_average=umkm.rating_average,
            rating_count=umkm.rating_count,
            created_at=umkm.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{umkm_id}/approve", response_model=MessageResponse)
async def approve_umkm(
    umkm_id: UUID,
    current_user: Annotated[User, Depends(get_current_admin)],
    umkm_service: Annotated[UMKMService, Depends(get_umkm_service)]
):
    """
    Approve UMKM (admin only)
    
    Changes UMKM status from PENDING to ACTIVE.
    """
    try:
        await umkm_service.approve_umkm(umkm_id, current_user.id)
        return MessageResponse(message="UMKM approved successfully")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{umkm_id}/suspend", response_model=MessageResponse)
async def suspend_umkm(
    umkm_id: UUID,
    current_user: Annotated[User, Depends(get_current_admin)],
    umkm_service: Annotated[UMKMService, Depends(get_umkm_service)]
):
    """
    Suspend UMKM (admin only)
    
    Temporarily suspends UMKM operations.
    """
    try:
        await umkm_service.suspend_umkm(umkm_id, current_user.id)
        return MessageResponse(message="UMKM suspended successfully")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
