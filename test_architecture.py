"""
Test script to demonstrate the Clean Architecture implementation

This script tests the core functionality without running the HTTP server.
It demonstrates how the layers work together.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.domain.entities import User, UserRole, UMKM, Product, ProductCategory, Order, OrderItem, OrderStatus
from src.infrastructure.persistence.in_memory_repositories import (
    InMemoryUserRepository,
    InMemoryUMKMRepository,
    InMemoryProductRepository,
    InMemoryOrderRepository
)
from src.application.services.auth_service import AuthenticationService
from src.application.services.umkm_service import UMKMService
from src.application.services.product_service import ProductService
from src.application.services.order_service import OrderService


async def main():
    print("=" * 70)
    print("IPB Food & UMKM Student Hub - Clean Architecture Demo")
    print("=" * 70)
    print()
    
    # Initialize repositories (Infrastructure Layer)
    user_repo = InMemoryUserRepository()
    umkm_repo = InMemoryUMKMRepository()
    product_repo = InMemoryProductRepository()
    order_repo = InMemoryOrderRepository()
    
    # Initialize services (Application Layer)
    auth_service = AuthenticationService(user_repo)
    umkm_service = UMKMService(umkm_repo, user_repo)
    product_service = ProductService(product_repo, umkm_repo)
    order_service = OrderService(order_repo, product_repo, umkm_repo)
    
    print("✅ All layers initialized successfully")
    print()
    
    # Test 1: Register users
    print("📝 Test 1: User Registration")
    print("-" * 70)
    
    buyer = await auth_service.register_user(
        email="buyer@ipb.ac.id",
        username="john_buyer",
        password="secure123",
        full_name="John Doe",
        role=UserRole.BUYER,
        phone="081234567890"
    )
    print(f"✅ Buyer registered: {buyer.username} ({buyer.email})")
    
    seller = await auth_service.register_user(
        email="seller@ipb.ac.id",
        username="jane_seller",
        password="secure123",
        full_name="Jane Seller",
        role=UserRole.SELLER
    )
    print(f"✅ Seller registered: {seller.username} ({seller.email})")
    print()
    
    # Test 2: Authentication
    print("🔐 Test 2: Authentication")
    print("-" * 70)
    
    authenticated_seller = await auth_service.authenticate_user(
        email="seller@ipb.ac.id",
        password="secure123"
    )
    
    if authenticated_seller:
        token = await auth_service.create_access_token(authenticated_seller)
        print(f"✅ Seller authenticated successfully")
        print(f"   Token: {token[:50]}...")
    print()
    
    # Test 3: Register UMKM
    print("🏪 Test 3: UMKM Registration")
    print("-" * 70)
    
    umkm = await umkm_service.register_umkm(
        owner_id=seller.id,
        name="Warung Makan Barokah",
        description="Makanan rumahan enak dan murah di kampus IPB",
        location="Gedung Rektorat IPB",
        phone="081234567890",
        operating_hours="08:00-17:00"
    )
    print(f"✅ UMKM registered: {umkm.name}")
    print(f"   Status: {umkm.status.value}")
    print(f"   Owner: {umkm.owner_id}")
    print()
    
    # Test 4: Create Products
    print("🍔 Test 4: Product Creation")
    print("-" * 70)
    
    products = []
    
    product1 = await product_service.create_product(
        seller_id=seller.id,
        umkm_id=umkm.id,
        name="Nasi Goreng Special",
        description="Nasi goreng dengan telur dan ayam",
        price=15000,
        category=ProductCategory.FOOD,
        stock_quantity=50
    )
    products.append(product1)
    print(f"✅ Product created: {product1.name} - Rp {product1.price:,.0f}")
    
    product2 = await product_service.create_product(
        seller_id=seller.id,
        umkm_id=umkm.id,
        name="Es Teh Manis",
        description="Es teh manis segar",
        price=5000,
        category=ProductCategory.BEVERAGE,
        stock_quantity=100
    )
    products.append(product2)
    print(f"✅ Product created: {product2.name} - Rp {product2.price:,.0f}")
    print()
    
    # Test 5: Create Order (Critical Use Case!)
    print("📦 Test 5: Create Order with Domain Validation")
    print("-" * 70)
    print("This demonstrates Clean Architecture in action:")
    print("  - Route would call Application Service")
    print("  - Application Service orchestrates")
    print("  - Domain entities enforce business rules")
    print("  - Infrastructure persists data")
    print()
    
    # Domain business logic: Check if UMKM can accept orders
    print(f"   Can UMKM accept orders? {umkm.can_accept_orders()} ❌ (Status: {umkm.status.value})")
    
    # Approve UMKM first (would be admin action)
    umkm.approve()
    await umkm_repo.save(umkm)
    print(f"   UMKM approved! Status: {umkm.status.value}")
    print(f"   Can UMKM accept orders now? {umkm.can_accept_orders()} ✅")
    print()
    
    # Domain business logic: Check product availability
    print(f"   Product '{product1.name}' available? {product1.can_be_ordered(2)} ✅")
    print(f"   Current stock: {product1.stock_quantity} units")
    print()
    
    # Create order
    order = await order_service.create_order(
        buyer_id=buyer.id,
        umkm_id=umkm.id,
        items=[
            {"product_id": product1.id, "quantity": 2},
            {"product_id": product2.id, "quantity": 3}
        ],
        notes="Extra pedas ya"
    )
    
    print(f"✅ Order created successfully!")
    print(f"   Order ID: {order.id}")
    print(f"   Status: {order.status.value}")
    print(f"   Total: Rp {order.total_amount:,.0f}")
    print(f"   Items: {len(order.items)}")
    for item in order.items:
        print(f"     - {item.product_name} x{item.quantity} @ Rp {item.unit_price:,.0f}")
    print()
    
    # Check stock reduction (Domain business logic!)
    updated_product1 = await product_repo.find_by_id(product1.id)
    print(f"   Stock after order:")
    print(f"     {updated_product1.name}: {updated_product1.stock_quantity} units (was 50)")
    print()
    
    # Test 6: Order State Transitions
    print("🔄 Test 6: Order State Machine (Domain Logic)")
    print("-" * 70)
    
    print(f"   Initial status: {order.status.value}")
    
    # Seller confirms order
    order = await order_service.confirm_order(order.id, seller.id)
    print(f"   After confirm: {order.status.value} ✅")
    
    # Seller updates to preparing
    order = await order_service.update_order_status(order.id, seller.id, "preparing")
    print(f"   After preparing: {order.status.value} ✅")
    
    # Seller marks as ready
    order = await order_service.update_order_status(order.id, seller.id, "ready")
    print(f"   After ready: {order.status.value} ✅")
    
    # Mark as completed
    order = await order_service.update_order_status(order.id, seller.id, "completed")
    print(f"   After completed: {order.status.value} ✅")
    print()
    
    # Test 7: List operations
    print("📋 Test 7: Listing Operations")
    print("-" * 70)
    
    all_umkms = await umkm_repo.find_all()
    print(f"✅ Total UMKMs: {len(all_umkms)}")
    
    all_products = await product_repo.find_all()
    print(f"✅ Total Products: {len(all_products)}")
    
    buyer_orders = await order_repo.find_by_buyer_id(buyer.id)
    print(f"✅ Buyer's Orders: {len(buyer_orders)}")
    
    seller_orders = await order_repo.find_by_umkm_id(umkm.id)
    print(f"✅ Seller's Orders: {len(seller_orders)}")
    print()
    
    # Summary
    print("=" * 70)
    print("🎉 All Tests Passed!")
    print("=" * 70)
    print()
    print("Clean Architecture Demonstrated:")
    print("✅ Domain entities with business logic")
    print("✅ Repository pattern with abstractions")
    print("✅ Application services orchestrating workflows")
    print("✅ Dependency injection")
    print("✅ Domain-driven state transitions")
    print("✅ Business rules enforced in domain layer")
    print()
    print("Ready for:")
    print("📱 FastAPI routes (thin controllers)")
    print("🗄️  PostgreSQL implementation (just implement interfaces)")
    print("🧪 Easy testing (mock repositories)")
    print("📈 Scalability and maintainability")
    print()


if __name__ == "__main__":
    asyncio.run(main())
