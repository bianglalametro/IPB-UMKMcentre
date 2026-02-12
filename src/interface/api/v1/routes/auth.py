"""
Interface Layer - Authentication Routes

THIN CONTROLLERS:
- Routes are THIN - they only handle HTTP concerns
- No business logic here!
- Call application services for all operations
- Handle request/response formatting
- Error handling

This demonstrates the separation of concerns:
- Routes: HTTP protocol, request/response
- Application: Business workflows
- Domain: Business rules
- Infrastructure: Technical details
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.auth_service import AuthenticationService
from src.domain.entities import User, UserRole
from src.interface.api.v1.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse
)
from src.interface.api.v1.dependencies import (
    get_auth_service,
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterRequest,
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)]
):
    """
    Register a new user
    
    Creates a new user account with the specified role.
    
    THIN CONTROLLER:
    - Validates request (Pydantic)
    - Calls application service
    - Returns response
    - No business logic!
    """
    try:
        # Convert role string to enum
        role = UserRole(request.role)
        
        # Call application service - THIS is where the work happens
        user = await auth_service.register_user(
            email=request.email,
            username=request.username,
            password=request.password,
            full_name=request.full_name,
            role=role,
            phone=request.phone
        )
        
        # Return response
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role.value,
            phone=user.phone,
            is_active=user.is_active,
            created_at=user.created_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: UserLoginRequest,
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)]
):
    """
    Login with email and password
    
    Returns a JWT access token on successful authentication.
    
    THIN CONTROLLER:
    - Receives credentials
    - Calls authentication service
    - Returns token
    - No authentication logic here!
    """
    # Call application service
    user = await auth_service.authenticate_user(
        email=request.email,
        password=request.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Create token
    token = await auth_service.create_access_token(user)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Get current user information
    
    Requires authentication (JWT token in Authorization header).
    
    THIN CONTROLLER:
    - Authentication handled by dependency injection
    - Just returns user info
    - No logic needed!
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role.value,
        phone=current_user.phone,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )
