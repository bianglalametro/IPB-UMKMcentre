"""
Domain Layer - Repository Interfaces

Repository Pattern: These are abstract interfaces that define operations
for persisting and retrieving domain entities.

WHY REPOSITORIES ARE IN THE DOMAIN LAYER:
- Repositories are part of the domain's contract
- They define WHAT operations are needed, not HOW they're implemented
- The domain layer declares its needs without depending on infrastructure
- Infrastructure layer implements these interfaces with actual database logic

KEY PRINCIPLES:
1. Repository interfaces belong to the domain
2. Repository implementations belong to infrastructure
3. This inverts the dependency: Infrastructure depends on Domain, not vice versa
4. This is the Dependency Inversion Principle (DIP) from SOLID

BENEFITS:
- Domain logic doesn't depend on database details
- Easy to swap database implementations (in-memory, PostgreSQL, MongoDB, etc.)
- Testable with mock repositories
- Clear separation of concerns
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities import (
    User, UMKM, Product, Order, Review, Promo
)


class UserRepository(ABC):
    """
    Abstract repository interface for User entity
    
    This interface defines all operations needed to persist and retrieve users.
    The actual implementation (in-memory, PostgreSQL, etc.) is in infrastructure layer.
    """
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Create or update a user"""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email (used for login)"""
        pass
    
    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[User]:
        """Get all users"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID"""
        pass


class UMKMRepository(ABC):
    """Abstract repository interface for UMKM entity"""
    
    @abstractmethod
    async def save(self, umkm: UMKM) -> UMKM:
        """Create or update a UMKM"""
        pass
    
    @abstractmethod
    async def find_by_id(self, umkm_id: UUID) -> Optional[UMKM]:
        """Find UMKM by ID"""
        pass
    
    @abstractmethod
    async def find_by_owner_id(self, owner_id: UUID) -> Optional[UMKM]:
        """Find UMKM by owner (seller) ID"""
        pass
    
    @abstractmethod
    async def find_all(self, status: Optional[str] = None) -> List[UMKM]:
        """Get all UMKMs, optionally filtered by status"""
        pass
    
    @abstractmethod
    async def delete(self, umkm_id: UUID) -> bool:
        """Delete UMKM by ID"""
        pass


class ProductRepository(ABC):
    """Abstract repository interface for Product entity"""
    
    @abstractmethod
    async def save(self, product: Product) -> Product:
        """Create or update a product"""
        pass
    
    @abstractmethod
    async def find_by_id(self, product_id: UUID) -> Optional[Product]:
        """Find product by ID"""
        pass
    
    @abstractmethod
    async def find_by_umkm_id(self, umkm_id: UUID) -> List[Product]:
        """Find all products for a specific UMKM"""
        pass
    
    @abstractmethod
    async def find_all(self, available_only: bool = False) -> List[Product]:
        """Get all products, optionally filtered by availability"""
        pass
    
    @abstractmethod
    async def delete(self, product_id: UUID) -> bool:
        """Delete product by ID"""
        pass


class OrderRepository(ABC):
    """Abstract repository interface for Order entity"""
    
    @abstractmethod
    async def save(self, order: Order) -> Order:
        """Create or update an order"""
        pass
    
    @abstractmethod
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID"""
        pass
    
    @abstractmethod
    async def find_by_buyer_id(self, buyer_id: UUID) -> List[Order]:
        """Find all orders for a specific buyer"""
        pass
    
    @abstractmethod
    async def find_by_umkm_id(self, umkm_id: UUID) -> List[Order]:
        """Find all orders for a specific UMKM"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Order]:
        """Get all orders"""
        pass
    
    @abstractmethod
    async def delete(self, order_id: UUID) -> bool:
        """Delete order by ID"""
        pass


class ReviewRepository(ABC):
    """Abstract repository interface for Review entity"""
    
    @abstractmethod
    async def save(self, review: Review) -> Review:
        """Create or update a review"""
        pass
    
    @abstractmethod
    async def find_by_id(self, review_id: UUID) -> Optional[Review]:
        """Find review by ID"""
        pass
    
    @abstractmethod
    async def find_by_umkm_id(self, umkm_id: UUID, visible_only: bool = True) -> List[Review]:
        """Find all reviews for a specific UMKM"""
        pass
    
    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> List[Review]:
        """Find all reviews by a specific user"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Review]:
        """Get all reviews"""
        pass
    
    @abstractmethod
    async def delete(self, review_id: UUID) -> bool:
        """Delete review by ID"""
        pass


class PromoRepository(ABC):
    """Abstract repository interface for Promo entity"""
    
    @abstractmethod
    async def save(self, promo: Promo) -> Promo:
        """Create or update a promo"""
        pass
    
    @abstractmethod
    async def find_by_id(self, promo_id: UUID) -> Optional[Promo]:
        """Find promo by ID"""
        pass
    
    @abstractmethod
    async def find_by_code(self, code: str) -> Optional[Promo]:
        """Find promo by code"""
        pass
    
    @abstractmethod
    async def find_by_umkm_id(self, umkm_id: UUID, active_only: bool = False) -> List[Promo]:
        """Find all promos for a specific UMKM"""
        pass
    
    @abstractmethod
    async def find_active_promos(self) -> List[Promo]:
        """Find all currently active promos"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Promo]:
        """Get all promos"""
        pass
    
    @abstractmethod
    async def delete(self, promo_id: UUID) -> bool:
        """Delete promo by ID"""
        pass
