"""
Infrastructure Layer - Authentication Service

This module provides authentication services including:
- Password hashing and verification
- JWT token generation and validation

WHY THIS IS IN INFRASTRUCTURE:
- Uses external libraries (passlib, python-jose)
- Deals with technical implementation details
- Application layer uses this service without knowing the details

The application layer calls these services to handle authentication,
but doesn't know HOW they work internally.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key-here-change-in-production"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    """
    Authentication Service
    
    Provides:
    - Password hashing and verification
    - JWT token creation and validation
    - Token payload extraction
    
    This is infrastructure because it deals with HOW authentication works,
    not the business logic of authentication.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password
        
        Uses bcrypt for secure password hashing.
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Returns True if password matches, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token
        
        Args:
            data: Dictionary of data to encode in the token
            expires_delta: Optional custom expiration time
        
        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token: str) -> Optional[dict]:
        """
        Decode and validate a JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def extract_user_id(token: str) -> Optional[str]:
        """
        Extract user ID from JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            User ID if token is valid, None otherwise
        """
        payload = AuthService.decode_access_token(token)
        if payload:
            return payload.get("sub")
        return None
