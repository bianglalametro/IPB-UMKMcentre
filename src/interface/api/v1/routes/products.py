"""
Interface Layer - Product Routes

THIN CONTROLLERS for product management.
"""

from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.product_service import ProductService
from src.domain.entities import User, ProductCategory
from src.interface.api.v1.schemas import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductPriceUpdateRequest,
    ProductStockUpdateRequest,
    ProductAvailabilityRequest,
    ProductResponse,
    MessageResponse
)
from src.interface.api.v1.dependencies import (
    get_product_service,
    get_current_seller
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    umkm_id: UUID,
    request: ProductCreateRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    Create a new product (seller only)
    
    Adds a new product to the seller's UMKM.
    """
    try:
        category = ProductCategory(request.category)
        
        product = await product_service.create_product(
            seller_id=current_user.id,
            umkm_id=umkm_id,
            name=request.name,
            description=request.description,
            price=request.price,
            category=category,
            image_url=request.image_url,
            stock_quantity=request.stock_quantity,
            preorder_required=request.preorder_required,
            min_preorder_hours=request.min_preorder_hours
        )
        
        return ProductResponse(
            id=product.id,
            umkm_id=product.umkm_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.value,
            image_url=product.image_url,
            stock_quantity=product.stock_quantity,
            is_available=product.is_available,
            preorder_required=product.preorder_required,
            min_preorder_hours=product.min_preorder_hours,
            created_at=product.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[ProductResponse])
async def list_products(
    available_only: bool = False,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    List all products
    
    Public endpoint - can filter to show only available products.
    """
    products = await product_service.get_all_products(available_only=available_only)
    
    return [
        ProductResponse(
            id=product.id,
            umkm_id=product.umkm_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.value,
            image_url=product.image_url,
            stock_quantity=product.stock_quantity,
            is_available=product.is_available,
            preorder_required=product.preorder_required,
            min_preorder_hours=product.min_preorder_hours,
            created_at=product.created_at
        )
        for product in products
    ]


@router.get("/umkm/{umkm_id}", response_model=List[ProductResponse])
async def list_umkm_products(
    umkm_id: UUID,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    List all products for a specific UMKM
    
    Public endpoint.
    """
    products = await product_service.get_umkm_products(umkm_id)
    
    return [
        ProductResponse(
            id=product.id,
            umkm_id=product.umkm_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.value,
            image_url=product.image_url,
            stock_quantity=product.stock_quantity,
            is_available=product.is_available,
            preorder_required=product.preorder_required,
            min_preorder_hours=product.min_preorder_hours,
            created_at=product.created_at
        )
        for product in products
    ]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    Get product details by ID
    
    Public endpoint.
    """
    product = await product_service.get_product(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return ProductResponse(
        id=product.id,
        umkm_id=product.umkm_id,
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category.value,
        image_url=product.image_url,
        stock_quantity=product.stock_quantity,
        is_available=product.is_available,
        preorder_required=product.preorder_required,
        min_preorder_hours=product.min_preorder_hours,
        created_at=product.created_at
    )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    request: ProductUpdateRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    Update product information (seller only)
    """
    try:
        category = ProductCategory(request.category) if request.category else None
        
        product = await product_service.update_product(
            product_id=product_id,
            seller_id=current_user.id,
            name=request.name,
            description=request.description,
            category=category,
            image_url=request.image_url,
            preorder_required=request.preorder_required,
            min_preorder_hours=request.min_preorder_hours
        )
        
        return ProductResponse(
            id=product.id,
            umkm_id=product.umkm_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.value,
            image_url=product.image_url,
            stock_quantity=product.stock_quantity,
            is_available=product.is_available,
            preorder_required=product.preorder_required,
            min_preorder_hours=product.min_preorder_hours,
            created_at=product.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{product_id}/price", response_model=ProductResponse)
async def update_product_price(
    product_id: UUID,
    request: ProductPriceUpdateRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    Update product price (seller only)
    """
    try:
        product = await product_service.update_product_price(
            product_id=product_id,
            seller_id=current_user.id,
            new_price=request.price
        )
        
        return ProductResponse(
            id=product.id,
            umkm_id=product.umkm_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.value,
            image_url=product.image_url,
            stock_quantity=product.stock_quantity,
            is_available=product.is_available,
            preorder_required=product.preorder_required,
            min_preorder_hours=product.min_preorder_hours,
            created_at=product.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_product_stock(
    product_id: UUID,
    request: ProductStockUpdateRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    Update product stock quantity (seller only)
    """
    try:
        product = await product_service.update_product_stock(
            product_id=product_id,
            seller_id=current_user.id,
            new_stock=request.stock_quantity
        )
        
        return ProductResponse(
            id=product.id,
            umkm_id=product.umkm_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.value,
            image_url=product.image_url,
            stock_quantity=product.stock_quantity,
            is_available=product.is_available,
            preorder_required=product.preorder_required,
            min_preorder_hours=product.min_preorder_hours,
            created_at=product.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{product_id}/availability", response_model=ProductResponse)
async def toggle_product_availability(
    product_id: UUID,
    request: ProductAvailabilityRequest,
    current_user: Annotated[User, Depends(get_current_seller)],
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    Toggle product availability (seller only)
    """
    try:
        product = await product_service.toggle_product_availability(
            product_id=product_id,
            seller_id=current_user.id,
            available=request.available
        )
        
        return ProductResponse(
            id=product.id,
            umkm_id=product.umkm_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.value,
            image_url=product.image_url,
            stock_quantity=product.stock_quantity,
            is_available=product.is_available,
            preorder_required=product.preorder_required,
            min_preorder_hours=product.min_preorder_hours,
            created_at=product.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(
    product_id: UUID,
    current_user: Annotated[User, Depends(get_current_seller)],
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    """
    Delete product (seller only)
    """
    try:
        await product_service.delete_product(product_id, current_user.id)
        return MessageResponse(message="Product deleted successfully")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
