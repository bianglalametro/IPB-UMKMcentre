"""
Application Layer - Order Service

This module contains the application services for order management.

Demonstrates:
- Complex use case with domain validation
- Orchestration of multiple entities
- Transaction-like operations
- Business workflow coordination
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.entities import Order, OrderItem, OrderStatus, Product
from src.domain.repositories import OrderRepository, ProductRepository, UMKMRepository


class OrderService:
    """
    Order Application Service
    
    Orchestrates order-related use cases:
    - Create order (with inventory management)
    - Update order status
    - Cancel order
    - List orders
    
    This is a CRITICAL example of how business logic stays in the domain
    while the application layer orchestrates the workflow.
    """
    
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        umkm_repository: UMKMRepository
    ):
        """
        Dependency Injection: Multiple repositories injected
        
        This service needs to coordinate between orders, products, and UMKMs.
        """
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.umkm_repository = umkm_repository
    
    async def create_order(
        self,
        buyer_id: UUID,
        umkm_id: UUID,
        items: List[dict],  # List of {product_id, quantity}
        pickup_time: Optional[datetime] = None,
        notes: Optional[str] = None
    ) -> Order:
        """
        Use Case: Create Order with Domain Validation
        
        This is a PERFECT example of Clean Architecture:
        
        APPLICATION LAYER (this method):
        - Orchestrates the workflow
        - Fetches products
        - Prepares data
        - Coordinates between entities
        
        DOMAIN LAYER (entities):
        - Order entity validates business rules
        - Product entity checks availability
        - Product entity manages inventory
        
        INFRASTRUCTURE LAYER:
        - Repositories handle persistence
        
        Notice: NO business logic here, just orchestration!
        """
        
        # 1. Validate UMKM exists and can accept orders
        umkm = await self.umkm_repository.find_by_id(umkm_id)
        if not umkm:
            raise ValueError("UMKM not found")
        
        # Domain business logic: UMKM must be operational
        if not umkm.can_accept_orders():
            raise ValueError("UMKM is not accepting orders")
        
        # 2. Validate and prepare order items
        order_items: List[OrderItem] = []
        
        for item_data in items:
            product_id = item_data["product_id"]
            quantity = item_data["quantity"]
            
            # Fetch product
            product = await self.product_repository.find_by_id(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            # Verify product belongs to this UMKM
            if product.umkm_id != umkm_id:
                raise ValueError(f"Product {product_id} does not belong to this UMKM")
            
            # Domain business logic: Check if product can be ordered
            if not product.can_be_ordered(quantity):
                raise ValueError(
                    f"Product {product.name} is not available in requested quantity"
                )
            
            # Create OrderItem value object
            order_item = OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price
            )
            order_items.append(order_item)
            
            # Domain business logic: Reduce stock
            # This is a domain operation - the Product entity knows how to manage its stock
            product.reduce_stock(quantity)
            
            # Persist updated product
            await self.product_repository.save(product)
        
        # 3. Create Order entity
        # Domain validates: must have items, valid pickup time, etc.
        order = Order(
            buyer_id=buyer_id,
            umkm_id=umkm_id,
            items=order_items,
            pickup_time=pickup_time,
            notes=notes
        )
        
        # 4. Persist order
        saved_order = await self.order_repository.save(order)
        
        return saved_order
    
    async def get_order(self, order_id: UUID) -> Optional[Order]:
        """Use Case: Get order by ID"""
        return await self.order_repository.find_by_id(order_id)
    
    async def get_buyer_orders(self, buyer_id: UUID) -> List[Order]:
        """Use Case: Get all orders for a buyer"""
        return await self.order_repository.find_by_buyer_id(buyer_id)
    
    async def get_umkm_orders(self, umkm_id: UUID) -> List[Order]:
        """Use Case: Get all orders for a UMKM (seller view)"""
        return await self.order_repository.find_by_umkm_id(umkm_id)
    
    async def confirm_order(self, order_id: UUID, seller_id: UUID) -> Order:
        """
        Use Case: Seller confirms order
        
        Authorization check + domain operation
        """
        order = await self.order_repository.find_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        
        # Verify seller owns the UMKM
        umkm = await self.umkm_repository.find_by_id(order.umkm_id)
        if not umkm or umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this UMKM")
        
        # Domain business logic: State transition
        order.confirm()
        
        # Persist
        await self.order_repository.save(order)
        return order
    
    async def update_order_status(
        self,
        order_id: UUID,
        seller_id: UUID,
        new_status: str
    ) -> Order:
        """
        Use Case: Update order status (seller action)
        
        Demonstrates domain-driven state transitions.
        """
        order = await self.order_repository.find_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        
        # Verify seller owns the UMKM
        umkm = await self.umkm_repository.find_by_id(order.umkm_id)
        if not umkm or umkm.owner_id != seller_id:
            raise ValueError("Unauthorized: You don't own this UMKM")
        
        # Domain business logic: State transitions with validation
        if new_status == "confirmed":
            order.confirm()
        elif new_status == "preparing":
            order.mark_preparing()
        elif new_status == "ready":
            order.mark_ready()
        elif new_status == "completed":
            order.complete()
        else:
            raise ValueError(f"Invalid status: {new_status}")
        
        # Persist
        await self.order_repository.save(order)
        return order
    
    async def cancel_order(
        self,
        order_id: UUID,
        user_id: UUID,
        reason: Optional[str] = None
    ) -> Order:
        """
        Use Case: Cancel order
        
        Can be done by buyer or seller with proper authorization.
        Demonstrates domain validation and stock restoration.
        """
        order = await self.order_repository.find_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        
        # Authorization: buyer or seller can cancel
        is_buyer = order.buyer_id == user_id
        umkm = await self.umkm_repository.find_by_id(order.umkm_id)
        is_seller = umkm and umkm.owner_id == user_id
        
        if not (is_buyer or is_seller):
            raise ValueError("Unauthorized: You cannot cancel this order")
        
        # Domain business logic: Check if can be cancelled
        if not order.can_be_cancelled():
            raise ValueError("Order cannot be cancelled")
        
        # Restore product stock
        for item in order.items:
            product = await self.product_repository.find_by_id(item.product_id)
            if product:
                # Domain business logic: Increase stock
                product.increase_stock(item.quantity)
                await self.product_repository.save(product)
        
        # Domain business logic: Cancel order
        order.cancel(reason)
        
        # Persist
        await self.order_repository.save(order)
        return order
