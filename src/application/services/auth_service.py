"""
Application Layer - Authentication Use Cases

This module contains the application services for authentication operations.

WHY THIS IS IN APPLICATION LAYER:
- Orchestrates domain entities and repositories
- Implements use cases (business workflows)
- Coordinates between domain and infrastructure
- Contains application-specific business logic

KEY PRINCIPLES:
1. No business logic in controllers/routes
2. Use cases orchestrate domain objects
3. Thin, focused use cases for each operation
4. Use dependency injection for repositories and services

The application layer is the "glue" that connects:
- Domain (business rules in entities)
- Infrastructure (repositories, external services)
- Interface (API routes)
"""

from typing import Optional
from uuid import UUID

from src.domain.entities import User, UserRole
from src.domain.repositories import UserRepository
from src.infrastructure.security.auth_service import AuthService


class AuthenticationService:
    """
    Authentication Application Service
    
    Orchestrates authentication use cases:
    - User registration
    - User login
    - Token validation
    
    This service uses:
    - Domain entities (User)
    - Domain repository interfaces (UserRepository)
    - Infrastructure services (AuthService)
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Dependency Injection: Repository is injected, not created here
        
        This allows:
        - Easy testing with mock repositories
        - Swapping implementations without changing this code
        - Loose coupling between layers
        """
        self.user_repository = user_repository
    
    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
        full_name: str,
        role: UserRole,
        phone: Optional[str] = None
    ) -> User:
        """
        Use Case: Register a new user
        
        Orchestration steps:
        1. Check if user already exists (application logic)
        2. Hash password (infrastructure service)
        3. Create User entity (domain logic validates)
        4. Persist user (repository)
        
        This is application logic - it coordinates different components
        but doesn't contain the actual business rules (those are in the domain).
        """
        # Check if user already exists
        existing_email = await self.user_repository.find_by_email(email)
        if existing_email:
            raise ValueError("Email already registered")
        
        existing_username = await self.user_repository.find_by_username(username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Hash password using infrastructure service
        hashed_password = AuthService.hash_password(password)
        
        # Create domain entity (this validates business rules)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            phone=phone
        )
        
        # Persist using repository
        saved_user = await self.user_repository.save(user)
        
        return saved_user
    
    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Use Case: Authenticate user with email and password
        
        Orchestration steps:
        1. Find user by email
        2. Verify password
        3. Check if user is active
        4. Return user if authentication successful
        
        Returns None if authentication fails.
        """
        # Find user
        user = await self.user_repository.find_by_email(email)
        if not user:
            return None
        
        # Verify password
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        
        # Check if user is active (business rule from domain)
        if not user.is_active:
            return None
        
        return user
    
    async def create_access_token(self, user: User) -> str:
        """
        Use Case: Create access token for authenticated user
        
        Creates a JWT token with user information.
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value
        }
        
        token = AuthService.create_access_token(data=token_data)
        return token
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Use Case: Get current user from token
        
        Validates token and retrieves user.
        """
        user_id_str = AuthService.extract_user_id(token)
        if not user_id_str:
            return None
        
        try:
            user_id = UUID(user_id_str)
            user = await self.user_repository.find_by_id(user_id)
            return user
        except (ValueError, AttributeError):
            return None
