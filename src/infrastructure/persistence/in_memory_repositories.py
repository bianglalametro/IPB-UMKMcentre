"""
Infrastructure Layer - In-Memory Repository Implementations

This module implements the repository interfaces defined in the domain layer
using in-memory storage (dictionaries).

WHY THIS IS IN INFRASTRUCTURE:
- These are IMPLEMENTATIONS of domain repository interfaces
- They contain infrastructure concerns (how data is stored)
- Domain layer defines WHAT, infrastructure defines HOW
- This can be easily swapped with PostgreSQL implementation later

KEY BENEFITS:
1. No database setup needed for development/testing
2. Fast execution
3. Easy to understand
4. Can be replaced with real database without changing domain or application layers

This demonstrates the power of the repository pattern and clean architecture:
- Domain logic remains unchanged regardless of storage mechanism
- Application services work with any repository implementation
- Infrastructure is pluggable
"""

from typing import Dict, List, Optional
from uuid import UUID
from copy import deepcopy

from src.domain.entities import User, UMKM, Product, Order, Review, Promo
from src.domain.repositories import (
    UserRepository,
    UMKMRepository,
    ProductRepository,
    OrderRepository,
    ReviewRepository,
    PromoRepository
)


class InMemoryUserRepository(UserRepository):
    """
    In-memory implementation of UserRepository
    
    Uses a dictionary to store users. In a real application,
    this would be replaced with a PostgreSQL implementation.
    """
    
    def __init__(self):
        self._users: Dict[UUID, User] = {}
    
    async def save(self, user: User) -> User:
        """Save user to in-memory storage"""
        self._users[user.id] = deepcopy(user)
        return user
    
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID"""
        user = self._users.get(user_id)
        return deepcopy(user) if user else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        for user in self._users.values():
            if user.email == email:
                return deepcopy(user)
        return None
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        for user in self._users.values():
            if user.username == username:
                return deepcopy(user)
        return None
    
    async def find_all(self) -> List[User]:
        """Get all users"""
        return [deepcopy(user) for user in self._users.values()]
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


class InMemoryUMKMRepository(UMKMRepository):
    """In-memory implementation of UMKMRepository"""
    
    def __init__(self):
        self._umkms: Dict[UUID, UMKM] = {}
    
    async def save(self, umkm: UMKM) -> UMKM:
        """Save UMKM to in-memory storage"""
        self._umkms[umkm.id] = deepcopy(umkm)
        return umkm
    
    async def find_by_id(self, umkm_id: UUID) -> Optional[UMKM]:
        """Find UMKM by ID"""
        umkm = self._umkms.get(umkm_id)
        return deepcopy(umkm) if umkm else None
    
    async def find_by_owner_id(self, owner_id: UUID) -> Optional[UMKM]:
        """Find UMKM by owner ID"""
        for umkm in self._umkms.values():
            if umkm.owner_id == owner_id:
                return deepcopy(umkm)
        return None
    
    async def find_all(self, status: Optional[str] = None) -> List[UMKM]:
        """Get all UMKMs, optionally filtered by status"""
        umkms = list(self._umkms.values())
        if status:
            umkms = [u for u in umkms if u.status.value == status]
        return [deepcopy(u) for u in umkms]
    
    async def delete(self, umkm_id: UUID) -> bool:
        """Delete UMKM by ID"""
        if umkm_id in self._umkms:
            del self._umkms[umkm_id]
            return True
        return False


class InMemoryProductRepository(ProductRepository):
    """In-memory implementation of ProductRepository"""
    
    def __init__(self):
        self._products: Dict[UUID, Product] = {}
    
    async def save(self, product: Product) -> Product:
        """Save product to in-memory storage"""
        self._products[product.id] = deepcopy(product)
        return product
    
    async def find_by_id(self, product_id: UUID) -> Optional[Product]:
        """Find product by ID"""
        product = self._products.get(product_id)
        return deepcopy(product) if product else None
    
    async def find_by_umkm_id(self, umkm_id: UUID) -> List[Product]:
        """Find all products for a specific UMKM"""
        products = [p for p in self._products.values() if p.umkm_id == umkm_id]
        return [deepcopy(p) for p in products]
    
    async def find_all(self, available_only: bool = False) -> List[Product]:
        """Get all products, optionally filtered by availability"""
        products = list(self._products.values())
        if available_only:
            products = [p for p in products if p.is_available]
        return [deepcopy(p) for p in products]
    
    async def delete(self, product_id: UUID) -> bool:
        """Delete product by ID"""
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of OrderRepository"""
    
    def __init__(self):
        self._orders: Dict[UUID, Order] = {}
    
    async def save(self, order: Order) -> Order:
        """Save order to in-memory storage"""
        self._orders[order.id] = deepcopy(order)
        return order
    
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID"""
        order = self._orders.get(order_id)
        return deepcopy(order) if order else None
    
    async def find_by_buyer_id(self, buyer_id: UUID) -> List[Order]:
        """Find all orders for a specific buyer"""
        orders = [o for o in self._orders.values() if o.buyer_id == buyer_id]
        return [deepcopy(o) for o in orders]
    
    async def find_by_umkm_id(self, umkm_id: UUID) -> List[Order]:
        """Find all orders for a specific UMKM"""
        orders = [o for o in self._orders.values() if o.umkm_id == umkm_id]
        return [deepcopy(o) for o in orders]
    
    async def find_all(self) -> List[Order]:
        """Get all orders"""
        return [deepcopy(order) for order in self._orders.values()]
    
    async def delete(self, order_id: UUID) -> bool:
        """Delete order by ID"""
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False


class InMemoryReviewRepository(ReviewRepository):
    """In-memory implementation of ReviewRepository"""
    
    def __init__(self):
        self._reviews: Dict[UUID, Review] = {}
    
    async def save(self, review: Review) -> Review:
        """Save review to in-memory storage"""
        self._reviews[review.id] = deepcopy(review)
        return review
    
    async def find_by_id(self, review_id: UUID) -> Optional[Review]:
        """Find review by ID"""
        review = self._reviews.get(review_id)
        return deepcopy(review) if review else None
    
    async def find_by_umkm_id(self, umkm_id: UUID, visible_only: bool = True) -> List[Review]:
        """Find all reviews for a specific UMKM"""
        reviews = [r for r in self._reviews.values() if r.umkm_id == umkm_id]
        if visible_only:
            reviews = [r for r in reviews if r.is_visible]
        return [deepcopy(r) for r in reviews]
    
    async def find_by_user_id(self, user_id: UUID) -> List[Review]:
        """Find all reviews by a specific user"""
        reviews = [r for r in self._reviews.values() if r.user_id == user_id]
        return [deepcopy(r) for r in reviews]
    
    async def find_all(self) -> List[Review]:
        """Get all reviews"""
        return [deepcopy(review) for review in self._reviews.values()]
    
    async def delete(self, review_id: UUID) -> bool:
        """Delete review by ID"""
        if review_id in self._reviews:
            del self._reviews[review_id]
            return True
        return False


class InMemoryPromoRepository(PromoRepository):
    """In-memory implementation of PromoRepository"""
    
    def __init__(self):
        self._promos: Dict[UUID, Promo] = {}
    
    async def save(self, promo: Promo) -> Promo:
        """Save promo to in-memory storage"""
        self._promos[promo.id] = deepcopy(promo)
        return promo
    
    async def find_by_id(self, promo_id: UUID) -> Optional[Promo]:
        """Find promo by ID"""
        promo = self._promos.get(promo_id)
        return deepcopy(promo) if promo else None
    
    async def find_by_code(self, code: str) -> Optional[Promo]:
        """Find promo by code"""
        for promo in self._promos.values():
            if promo.code == code:
                return deepcopy(promo)
        return None
    
    async def find_by_umkm_id(self, umkm_id: UUID, active_only: bool = False) -> List[Promo]:
        """Find all promos for a specific UMKM"""
        promos = [p for p in self._promos.values() if p.umkm_id == umkm_id]
        if active_only:
            promos = [p for p in promos if p.is_valid()]
        return [deepcopy(p) for p in promos]
    
    async def find_active_promos(self) -> List[Promo]:
        """Find all currently active promos"""
        promos = [p for p in self._promos.values() if p.is_valid()]
        return [deepcopy(p) for p in promos]
    
    async def find_all(self) -> List[Promo]:
        """Get all promos"""
        return [deepcopy(promo) for promo in self._promos.values()]
    
    async def delete(self, promo_id: UUID) -> bool:
        """Delete promo by ID"""
        if promo_id in self._promos:
            del self._promos[promo_id]
            return True
        return False
