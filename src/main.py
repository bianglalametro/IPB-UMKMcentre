"""
Main FastAPI Application

This is the entry point for the IPB Food & UMKM Student Hub API.

ARCHITECTURE SUMMARY:
==================

This application follows Clean Architecture with Layered Architecture:

LAYERS (from innermost to outermost):
--------------------------------------

1. DOMAIN LAYER (src/domain/)
   - Entities with business logic (User, UMKM, Product, Order, Review, Promo)
   - Repository interfaces (abstract base classes)
   - Pure business rules, no dependencies on other layers
   - Most stable, changes least frequently

2. APPLICATION LAYER (src/application/)
   - Use cases / Application services
   - Orchestrates domain objects and repositories
   - Implements business workflows
   - No UI or infrastructure concerns

3. INFRASTRUCTURE LAYER (src/infrastructure/)
   - Repository implementations (in-memory, will be PostgreSQL)
   - External service integrations (JWT, password hashing)
   - Technical details and frameworks
   - Most volatile, changes most frequently

4. INTERFACE LAYER (src/interface/)
   - FastAPI routes (thin controllers)
   - API schemas (Pydantic models)
   - HTTP concerns only
   - No business logic!

DEPENDENCY RULE:
----------------
- Inner layers NEVER depend on outer layers
- Outer layers depend on inner layers
- Domain is the core, everything else depends on it
- Infrastructure implements interfaces defined in domain

KEY BENEFITS:
-------------
1. Testable: Easy to mock repositories and services
2. Maintainable: Clear separation of concerns
3. Flexible: Easy to change infrastructure without touching domain
4. Scalable: Ready for growth and complexity
5. SOLID principles throughout

HOW TO EXTEND TO POSTGRESQL:
-----------------------------
1. Create new repository implementations in infrastructure/
2. Implement the same repository interfaces from domain/
3. Update dependency injection in interface/api/v1/dependencies/
4. NO changes needed in domain or application layers!

This is the power of Clean Architecture and Dependency Inversion.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.interface.api.v1.routes import auth, umkm, products, orders, reviews

# Create FastAPI application
app = FastAPI(
    title="IPB Food & UMKM Student Hub API",
    description="""
    Campus marketplace API for IPB University students.
    
    Features:
    - User authentication with JWT
    - Role-based access control (Buyer, Seller, Admin)
    - UMKM (merchant) management
    - Product/menu management
    - Preorder system
    - Rating & review system
    
    Architecture:
    - Clean Architecture with Layered Design
    - Domain-Driven Design principles
    - Repository pattern
    - Dependency injection
    - SOLID principles
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(umkm.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint
    
    Returns API information.
    """
    return {
        "name": "IPB Food & UMKM Student Hub API",
        "version": "1.0.0",
        "description": "Campus marketplace API with Clean Architecture",
        "docs": "/docs",
        "architecture": {
            "pattern": "Clean Architecture + Layered Architecture",
            "principles": "Domain-Driven Design, SOLID",
            "layers": [
                "Domain (entities, repositories interfaces)",
                "Application (use cases, services)",
                "Infrastructure (repository implementations, external services)",
                "Interface (API routes, schemas)"
            ]
        },
        "features": [
            "JWT Authentication",
            "Role-based access control",
            "UMKM management",
            "Product management",
            "Preorder system",
            "Rating & review system",
            "Admin moderation"
        ]
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Used for monitoring and deployment.
    """
    return {
        "status": "healthy",
        "message": "API is running"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # In production, use gunicorn with uvicorn workers
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Set to False in production
    )
