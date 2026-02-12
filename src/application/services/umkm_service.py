"""
Application Layer - UMKM Service

This module contains the application services for UMKM management.
"""

from typing import List, Optional
from uuid import UUID

from src.domain.entities import UMKM, UMKMStatus, UserRole
from src.domain.repositories import UMKMRepository, UserRepository


class UMKMService:
    """
    UMKM Application Service
    
    Orchestrates UMKM-related use cases:
    - Register UMKM
    - Approve/suspend UMKM (admin)
    - Update UMKM info
    - List UMKMs
    """
    
    def __init__(
        self,
        umkm_repository: UMKMRepository,
        user_repository: UserRepository
    ):
        self.umkm_repository = umkm_repository
        self.user_repository = user_repository
    
    async def register_umkm(
        self,
        owner_id: UUID,
        name: str,
        description: str,
        location: str,
        phone: str,
        operating_hours: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> UMKM:
        """
        Use Case: Register new UMKM
        
        Business rules:
        - Owner must be a seller
        - Owner can only have one UMKM
        """
        # Verify owner exists and is a seller
        owner = await self.user_repository.find_by_id(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        if not owner.can_sell_products():
            raise ValueError("User must have seller role to register UMKM")
        
        # Check if owner already has a UMKM
        existing_umkm = await self.umkm_repository.find_by_owner_id(owner_id)
        if existing_umkm:
            raise ValueError("Owner already has a UMKM registered")
        
        # Create UMKM entity (starts in PENDING status)
        umkm = UMKM(
            owner_id=owner_id,
            name=name,
            description=description,
            location=location,
            phone=phone,
            operating_hours=operating_hours,
            image_url=image_url,
            status=UMKMStatus.PENDING
        )
        
        # Persist
        saved_umkm = await self.umkm_repository.save(umkm)
        return saved_umkm
    
    async def get_umkm(self, umkm_id: UUID) -> Optional[UMKM]:
        """Use Case: Get UMKM by ID"""
        return await self.umkm_repository.find_by_id(umkm_id)
    
    async def get_all_umkms(
        self,
        status: Optional[str] = None,
        active_only: bool = False
    ) -> List[UMKM]:
        """
        Use Case: List all UMKMs
        
        Can filter by status or show only active UMKMs.
        """
        if active_only:
            status = "active"
        
        return await self.umkm_repository.find_all(status=status)
    
    async def update_umkm(
        self,
        umkm_id: UUID,
        owner_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        phone: Optional[str] = None,
        operating_hours: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> UMKM:
        """
        Use Case: Update UMKM information
        
        Only owner can update their UMKM.
        """
        umkm = await self.umkm_repository.find_by_id(umkm_id)
        if not umkm:
            raise ValueError("UMKM not found")
        
        # Authorization check
        if umkm.owner_id != owner_id:
            raise ValueError("Unauthorized: You don't own this UMKM")
        
        # Domain business logic: Update with validation
        umkm.update_info(
            name=name,
            description=description,
            location=location,
            phone=phone,
            operating_hours=operating_hours,
            image_url=image_url
        )
        
        # Persist
        await self.umkm_repository.save(umkm)
        return umkm
    
    async def approve_umkm(self, umkm_id: UUID, admin_id: UUID) -> UMKM:
        """
        Use Case: Approve UMKM (admin action)
        
        Admin must have moderation capability.
        """
        # Verify admin
        admin = await self.user_repository.find_by_id(admin_id)
        if not admin or not admin.can_moderate():
            raise ValueError("Unauthorized: Admin access required")
        
        umkm = await self.umkm_repository.find_by_id(umkm_id)
        if not umkm:
            raise ValueError("UMKM not found")
        
        # Domain business logic: Approve
        umkm.approve()
        
        # Persist
        await self.umkm_repository.save(umkm)
        return umkm
    
    async def suspend_umkm(
        self,
        umkm_id: UUID,
        admin_id: UUID,
        reason: Optional[str] = None
    ) -> UMKM:
        """Use Case: Suspend UMKM (admin action)"""
        # Verify admin
        admin = await self.user_repository.find_by_id(admin_id)
        if not admin or not admin.can_moderate():
            raise ValueError("Unauthorized: Admin access required")
        
        umkm = await self.umkm_repository.find_by_id(umkm_id)
        if not umkm:
            raise ValueError("UMKM not found")
        
        # Domain business logic: Suspend
        umkm.suspend(reason)
        
        # Persist
        await self.umkm_repository.save(umkm)
        return umkm
