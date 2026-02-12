"""
Interface Layer - Order Routes

THIN CONTROLLERS for order management.
Demonstrates the Create Order use case with domain validation.
"""

from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.order_service import OrderService
from src.domain.entities import User
from src.interface.api.v1.schemas import (
    OrderCreateRequest,
    OrderResponse,
    OrderStatusUpdateRequest,
    OrderCancelRequest,
    MessageResponse
)
from src.interface.api.v1.dependencies import (
    get_order_service,
    get_current_user,
    get_current_seller
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: OrderCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    """
    Create a new order (preorder)
    
    CRITICAL EXAMPLE OF CLEAN ARCHITECTURE:
    - Route is THIN - just handles HTTP
    - Application service orchestrates
    - Domain entities enforce business rules
    - Infrastructure persists data
    
    Notice: NO business logic in this controller!
    All validation, stock management, total calculation happens in lower layers.
    """
    try:
        # Verify user can make orders (domain business rule)
        if not current_user.can_make_orders():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User cannot make orders"
            )
        
        # Convert request to format expected by service
        items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity
            }
            for item in request.items
        ]
        
        # Call application service - ALL the work happens here
        order = await order_service.create_order(
            buyer_id=current_user.id,
            umkm_id=request.umkm_id,
            items=items,
            pickup_time=request.pickup_time,
            notes=request.notes
        )
        
        # Format response
        return OrderResponse(
            id=order.id,
            buyer_id=order.buyer_id,
            umkm_id=order.umkm_id,
            status=order.status.value,
            total_amount=order.total_amount,
            pickup_time=order.pickup_time,
            notes=order.notes,
            created_at=order.created_at,
            items=[
                {
                    "product_id": str(item.product_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal()
                }
                for item in order.items
            ]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    """
    Get orders for current user (buyer view)
    """
    orders = await order_service.get_buyer_orders(current_user.id)
    
    return [
        OrderResponse(
            id=order.id,
            buyer_id=order.buyer_id,
            umkm_id=order.umkm_id,
            status=order.status.value,
            total_amount=order.total_amount,
            pickup_time=order.pickup_time,
            notes=order.notes,
            created_at=order.created_at,
            items=[
                {
                    "product_id": str(item.product_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal()
                }
                for item in order.items
            ]
        )
        for order in orders
    ]


@router.get("/umkm/{umkm_id}", response_model=List[OrderResponse])
async def get_umkm_orders(
    umkm_id: UUID,
    current_user: Annotated[User, Depends(get_current_seller)],
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    """
    Get orders for a UMKM (seller view)
    """
    orders = await order_service.get_umkm_orders(umkm_id)
    
    return [
        OrderResponse(
            id=order.id,
            buyer_id=order.buyer_id,
            umkm_id=order.umkm_id,
            status=order.status.value,
            total_amount=order.total_amount,
            pickup_time=order.pickup_time,
            notes=order.notes,
            created_at=order.created_at,
            items=[
                {
                    "product_id": str(item.product_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal()
                }
                for item in order.items
            ]
        )
        for order in orders
    ]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    """
    Get order details by ID
    
    Requires authentication.
    """
    order = await order_service.get_order(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return OrderResponse(
        id=order.id,
        buyer_id=order.buyer_id,
        umkm_id=order.umkm_id,
        status=order.status.value,
        total_amount=order.total_amount,
        pickup_time=order.pickup_time,
        notes=order.notes,
        created_at=order.created_at,
        items=[
            {
                "product_id": str(item.product_id),
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal()
            }
            for item in order.items
        ]
    )


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: UUID,
    request: OrderStatusUpdateRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    """
    Update order status (seller only)
    
    Demonstrates domain-driven state transitions.
    The domain entity enforces valid state transitions.
    """
    try:
        order = await order_service.update_order_status(
            order_id=order_id,
            seller_id=current_user.id,
            new_status=request.status
        )
        
        return OrderResponse(
            id=order.id,
            buyer_id=order.buyer_id,
            umkm_id=order.umkm_id,
            status=order.status.value,
            total_amount=order.total_amount,
            pickup_time=order.pickup_time,
            notes=order.notes,
            created_at=order.created_at,
            items=[
                {
                    "product_id": str(item.product_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal()
                }
                for item in order.items
            ]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/cancel", response_model=MessageResponse)
async def cancel_order(
    order_id: UUID,
    request: OrderCancelRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    """
    Cancel order
    
    Can be done by buyer or seller.
    Demonstrates complex business logic (stock restoration) in application layer.
    """
    try:
        await order_service.cancel_order(
            order_id=order_id,
            user_id=current_user.id,
            reason=request.reason
        )
        
        return MessageResponse(message="Order cancelled successfully")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/confirm", response_model=OrderResponse)
async def confirm_order(
    order_id: UUID,
    current_user: Annotated[User, Depends(get_current_seller)],
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    """
    Confirm order (seller only)
    
    Changes order status from 'pending' to 'confirmed'.
    This is a convenience endpoint for the frontend.
    """
    try:
        order = await order_service.update_order_status(
            order_id=order_id,
            seller_id=current_user.id,
            new_status="confirmed"
        )
        
        return OrderResponse(
            id=order.id,
            buyer_id=order.buyer_id,
            umkm_id=order.umkm_id,
            status=order.status.value,
            total_amount=order.total_amount,
            pickup_time=order.pickup_time,
            notes=order.notes,
            created_at=order.created_at,
            items=[
                {
                    "product_id": str(item.product_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal()
                }
                for item in order.items
            ]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
