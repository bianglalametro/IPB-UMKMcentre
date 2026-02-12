"""
Interface Layer - Pydantic Schemas

These schemas define the API contract (request/response formats).

WHY SCHEMAS ARE IN THE INTERFACE LAYER:
- They are API-specific, not domain models
- Handle serialization/deserialization
- API validation (different from domain validation)
- Separate from domain entities for flexibility

DOMAIN ENTITIES vs API SCHEMAS:
- Domain entities: Business logic and rules
- API schemas: API contract and validation

This separation allows:
- Domain to evolve independently from API
- Multiple API versions with same domain
- Different representations for different clients
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# Authentication Schemas
# ============================================================================

class UserRegisterRequest(BaseModel):
    """Request schema for user registration"""
    email: EmailStr
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    role: str = Field(..., pattern="^(buyer|seller|admin)$")
    phone: Optional[str] = None


class UserLoginRequest(BaseModel):
    """Request schema for user login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Response schema for user information"""
    id: UUID
    email: str
    username: str
    full_name: str
    role: str
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# UMKM Schemas
# ============================================================================

class UMKMCreateRequest(BaseModel):
    """Request schema for creating UMKM"""
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    location: str
    phone: str
    operating_hours: Optional[str] = None
    image_url: Optional[str] = None


class UMKMUpdateRequest(BaseModel):
    """Request schema for updating UMKM"""
    name: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=10)
    location: Optional[str] = None
    phone: Optional[str] = None
    operating_hours: Optional[str] = None
    image_url: Optional[str] = None


class UMKMResponse(BaseModel):
    """Response schema for UMKM information"""
    id: UUID
    owner_id: UUID
    name: str
    description: str
    location: str
    phone: str
    status: str
    image_url: Optional[str]
    operating_hours: Optional[str]
    rating_average: float
    rating_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Product Schemas
# ============================================================================

class ProductCreateRequest(BaseModel):
    """Request schema for creating product"""
    name: str = Field(..., min_length=2)
    description: str
    price: float = Field(..., gt=0)
    category: str = Field(..., pattern="^(food|beverage|snack|merchandise|other)$")
    image_url: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    preorder_required: bool = False
    min_preorder_hours: int = Field(0, ge=0)


class ProductUpdateRequest(BaseModel):
    """Request schema for updating product"""
    name: Optional[str] = Field(None, min_length=2)
    description: Optional[str] = None
    category: Optional[str] = Field(None, pattern="^(food|beverage|snack|merchandise|other)$")
    image_url: Optional[str] = None
    preorder_required: Optional[bool] = None
    min_preorder_hours: Optional[int] = Field(None, ge=0)


class ProductPriceUpdateRequest(BaseModel):
    """Request schema for updating product price"""
    price: float = Field(..., gt=0)


class ProductStockUpdateRequest(BaseModel):
    """Request schema for updating product stock"""
    stock_quantity: int = Field(..., ge=0)


class ProductAvailabilityRequest(BaseModel):
    """Request schema for toggling product availability"""
    available: bool


class ProductResponse(BaseModel):
    """Response schema for product information"""
    id: UUID
    umkm_id: UUID
    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str]
    stock_quantity: Optional[int]
    is_available: bool
    preorder_required: bool
    min_preorder_hours: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Order Schemas
# ============================================================================

class OrderItemRequest(BaseModel):
    """Request schema for order item"""
    product_id: UUID
    quantity: int = Field(..., gt=0)


class OrderCreateRequest(BaseModel):
    """Request schema for creating order"""
    umkm_id: UUID
    items: List[OrderItemRequest] = Field(..., min_items=1)
    pickup_time: Optional[datetime] = None
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Response schema for order item"""
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Response schema for order information"""
    id: UUID
    buyer_id: UUID
    umkm_id: UUID
    status: str
    total_amount: float
    pickup_time: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    items: List[dict]  # Simplified for now
    
    class Config:
        from_attributes = True


class OrderStatusUpdateRequest(BaseModel):
    """Request schema for updating order status"""
    status: str = Field(..., pattern="^(confirmed|preparing|ready|completed)$")


class OrderCancelRequest(BaseModel):
    """Request schema for cancelling order"""
    reason: Optional[str] = None


# ============================================================================
# Review Schemas
# ============================================================================

class ReviewCreateRequest(BaseModel):
    """Request schema for creating review"""
    umkm_id: UUID
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=1000)
    order_id: Optional[UUID] = None


class ReviewUpdateRequest(BaseModel):
    """Request schema for updating review"""
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=1000)


class ReviewResponse(BaseModel):
    """Response schema for review information"""
    id: UUID
    user_id: UUID
    umkm_id: UUID
    order_id: Optional[UUID]
    rating: int
    comment: str
    is_visible: bool
    is_flagged: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Generic Schemas
# ============================================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
