"""
Interface Layer - Dependencies

This module sets up dependency injection for FastAPI.

DEPENDENCY INJECTION BENEFITS:
1. Loose coupling between layers
2. Easy testing (can inject mocks)
3. Centralized configuration
4. Easy to swap implementations

HOW IT WORKS:
- FastAPI's dependency injection system
- Dependencies are injected into route handlers
- Services get repositories injected
- Repositories are singletons (in-memory) for now

When switching to PostgreSQL:
- Only change the repository implementations here
- No changes needed in services or routes
- This is the power of dependency inversion!
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain.repositories import (
    UserRepository,
    UMKMRepository,
    ProductRepository,
    OrderRepository,
    ReviewRepository,
    PromoRepository
)
from src.infrastructure.persistence.in_memory_repositories import (
    InMemoryUserRepository,
    InMemoryUMKMRepository,
    InMemoryProductRepository,
    InMemoryOrderRepository,
    InMemoryReviewRepository,
    InMemoryPromoRepository
)
from src.application.services.auth_service import AuthenticationService
from src.application.services.umkm_service import UMKMService
from src.application.services.product_service import ProductService
from src.application.services.order_service import OrderService
from src.application.services.review_service import ReviewService
from src.domain.entities import User

# ============================================================================
# Repository Singletons
# ============================================================================
# In a real app with database, these would be scoped to request or session
# For in-memory implementation, we use singletons to persist data

_user_repo = InMemoryUserRepository()
_umkm_repo = InMemoryUMKMRepository()
_product_repo = InMemoryProductRepository()
_order_repo = InMemoryOrderRepository()
_review_repo = InMemoryReviewRepository()
_promo_repo = InMemoryPromoRepository()


# ============================================================================
# Repository Dependencies
# ============================================================================

def get_user_repository() -> UserRepository:
    """Dependency: Get user repository"""
    return _user_repo


def get_umkm_repository() -> UMKMRepository:
    """Dependency: Get UMKM repository"""
    return _umkm_repo


def get_product_repository() -> ProductRepository:
    """Dependency: Get product repository"""
    return _product_repo


def get_order_repository() -> OrderRepository:
    """Dependency: Get order repository"""
    return _order_repo


def get_review_repository() -> ReviewRepository:
    """Dependency: Get review repository"""
    return _review_repo


def get_promo_repository() -> PromoRepository:
    """Dependency: Get promo repository"""
    return _promo_repo


# ============================================================================
# Service Dependencies
# ============================================================================

def get_auth_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> AuthenticationService:
    """Dependency: Get authentication service"""
    return AuthenticationService(user_repo)


def get_umkm_service(
    umkm_repo: Annotated[UMKMRepository, Depends(get_umkm_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UMKMService:
    """Dependency: Get UMKM service"""
    return UMKMService(umkm_repo, user_repo)


def get_product_service(
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
    umkm_repo: Annotated[UMKMRepository, Depends(get_umkm_repository)]
) -> ProductService:
    """Dependency: Get product service"""
    return ProductService(product_repo, umkm_repo)


def get_order_service(
    order_repo: Annotated[OrderRepository, Depends(get_order_repository)],
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
    umkm_repo: Annotated[UMKMRepository, Depends(get_umkm_repository)]
) -> OrderService:
    """Dependency: Get order service"""
    return OrderService(order_repo, product_repo, umkm_repo)


def get_review_service(
    review_repo: Annotated[ReviewRepository, Depends(get_review_repository)],
    umkm_repo: Annotated[UMKMRepository, Depends(get_umkm_repository)],
    order_repo: Annotated[OrderRepository, Depends(get_order_repository)]
) -> ReviewService:
    """Dependency: Get review service"""
    return ReviewService(review_repo, umkm_repo, order_repo)


# ============================================================================
# Authentication Dependencies
# ============================================================================

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)]
) -> User:
    """
    Dependency: Get current authenticated user
    
    Extracts JWT token from Authorization header and validates it.
    Returns the User entity if valid, raises HTTPException otherwise.
    
    This is used to protect routes that require authentication.
    """
    token = credentials.credentials
    
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_seller(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Dependency: Get current user and verify they are a seller
    
    This is used to protect seller-only routes.
    """
    if not current_user.can_sell_products():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seller role required"
        )
    
    return current_user


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Dependency: Get current user and verify they are an admin
    
    This is used to protect admin-only routes.
    """
    if not current_user.can_moderate():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    
    return current_user


# ============================================================================
# Optional Authentication
# ============================================================================

async def get_current_user_optional(
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)],
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User | None:
    """
    Dependency: Get current user if authenticated, None otherwise
    
    This is used for routes that work differently for authenticated users
    but don't require authentication.
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    return user
