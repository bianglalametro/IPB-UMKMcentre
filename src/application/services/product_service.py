"""
Application Layer - Product Service

This module contains the application services for product management.
"""

from typing import List, Optional
from uuid import UUID

from src.domain.entities import Product, ProductCategory
from src.domain.repositories import ProductRepository, UMKMRepository


class ProductService:
    """
    Product Application Service
    
    Orchestrates product-related use cases:
    - Create product
    - Update product
    - Manage availability
    - List products
    """
    
    def __init__(
        self,
        product_repository: ProductRepository,
        umkm_repository: UMKMRepository
    ):
        self.product_repository = product_repository
        self.umkm_repository = umkm_repository
    
    async def create_product(
        self,
        seller_id: UUID,
        umkm_id: UUID,
        name: str,
        description: str,
        price: float,
        category: ProductCategory,
        image_url: Optional[str] = None,
        stock_quantity: Optional[int] = None,
        preorder_required: bool = False,
        min_preorder_hours: int = 0
    ) -> Product:
        """
        Use Case: Create new product
        
        Only UMKM owner can create products for their UMKM.
        """
        # Verify UMKM exists and seller owns it
        umkm = await self.umkm_repository.find_by_id(umkm_id)
        if not umkm:
            raise ValueError("UMKM not found")
        
        if umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this UMKM")
        
        # Create Product entity
        product = Product(
            umkm_id=umkm_id,
            name=name,
            description=description,
            price=price,
            category=category,
            image_url=image_url,
            stock_quantity=stock_quantity,
            preorder_required=preorder_required,
            min_preorder_hours=min_preorder_hours
        )
        
        # Persist
        saved_product = await self.product_repository.save(product)
        return saved_product
    
    async def get_product(self, product_id: UUID) -> Optional[Product]:
        """Use Case: Get product by ID"""
        return await self.product_repository.find_by_id(product_id)
    
    async def get_umkm_products(self, umkm_id: UUID) -> List[Product]:
        """Use Case: Get all products for a UMKM"""
        return await self.product_repository.find_by_umkm_id(umkm_id)
    
    async def get_all_products(self, available_only: bool = False) -> List[Product]:
        """Use Case: Get all products"""
        return await self.product_repository.find_all(available_only=available_only)
    
    async def update_product(
        self,
        product_id: UUID,
        seller_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[ProductCategory] = None,
        image_url: Optional[str] = None,
        preorder_required: Optional[bool] = None,
        min_preorder_hours: Optional[int] = None
    ) -> Product:
        """
        Use Case: Update product information
        
        Only owner can update their products.
        """
        product = await self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Verify seller owns the UMKM
        umkm = await self.umkm_repository.find_by_id(product.umkm_id)
        if not umkm or umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this product's UMKM")
        
        # Domain business logic: Update with validation
        product.update_info(
            name=name,
            description=description,
            category=category,
            image_url=image_url,
            preorder_required=preorder_required,
            min_preorder_hours=min_preorder_hours
        )
        
        # Persist
        await self.product_repository.save(product)
        return product
    
    async def update_product_price(
        self,
        product_id: UUID,
        seller_id: UUID,
        new_price: float
    ) -> Product:
        """Use Case: Update product price"""
        product = await self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Verify seller owns the UMKM
        umkm = await self.umkm_repository.find_by_id(product.umkm_id)
        if not umkm or umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this product's UMKM")
        
        # Domain business logic: Update price with validation
        product.update_price(new_price)
        
        # Persist
        await self.product_repository.save(product)
        return product
    
    async def update_product_stock(
        self,
        product_id: UUID,
        seller_id: UUID,
        new_stock: int
    ) -> Product:
        """Use Case: Update product stock quantity"""
        product = await self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Verify seller owns the UMKM
        umkm = await self.umkm_repository.find_by_id(product.umkm_id)
        if not umkm or umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this product's UMKM")
        
        # Update stock (simple assignment, validated on save)
        if new_stock < 0:
            raise ValueError("Stock cannot be negative")
        product.stock_quantity = new_stock
        
        # Persist
        await self.product_repository.save(product)
        return product
    
    async def toggle_product_availability(
        self,
        product_id: UUID,
        seller_id: UUID,
        available: bool
    ) -> Product:
        """Use Case: Make product available or unavailable"""
        product = await self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Verify seller owns the UMKM
        umkm = await self.umkm_repository.find_by_id(product.umkm_id)
        if not umkm or umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this product's UMKM")
        
        # Domain business logic: Toggle availability
        if available:
            product.mark_available()
        else:
            product.mark_unavailable()
        
        # Persist
        await self.product_repository.save(product)
        return product
    
    async def delete_product(
        self,
        product_id: UUID,
        seller_id: UUID
    ) -> bool:
        """Use Case: Delete product"""
        product = await self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Verify seller owns the UMKM
        umkm = await self.umkm_repository.find_by_id(product.umkm_id)
        if not umkm or umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this product's UMKM")
        
        # Delete
        return await self.product_repository.delete(product_id)
