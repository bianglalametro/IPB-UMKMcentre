# Architecture Documentation

## Overview

The IPB Food & UMKM Student Hub backend is built using **Clean Architecture** combined with **Layered Architecture** and **Domain-Driven Design (DDD)** principles.

## Why Clean Architecture?

### Problems with Traditional Architecture

**Typical issues in monolithic applications:**
- Business logic mixed with framework code
- Hard to test (requires running full application)
- Difficult to change database or framework
- Coupling between layers makes maintenance hard
- Business rules scattered across controllers, services, and models

### Benefits of Clean Architecture

✅ **Testability**: Business logic can be tested without UI, database, or frameworks  
✅ **Maintainability**: Clear separation makes code easy to understand and modify  
✅ **Flexibility**: Swap infrastructure without touching business logic  
✅ **Independence**: Business rules don't depend on frameworks or databases  
✅ **Scalability**: Architecture supports growth in team size and codebase  

## The Four Layers

### 1. Domain Layer (Core)

**Location**: `src/domain/`

**Purpose**: Contains pure business logic and rules

**Contents**:
- **Entities**: Business objects with behavior (not just data)
- **Repository Interfaces**: Contracts for data access
- **Value Objects**: Immutable objects defined by their values

**Key Principles**:
- NO dependencies on other layers
- NO framework dependencies
- Pure Python business logic
- Most stable layer (changes least)

**Example - User Entity**:
```python
class User:
    def can_sell_products(self) -> bool:
        """Business logic: Check if user can sell products"""
        return self.role == UserRole.SELLER and self.is_active
    
    def deactivate(self) -> None:
        """Business logic: Deactivate user account"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
```

**Why entities have methods?**
- Entities are NOT just data containers
- They enforce business rules
- They contain domain logic
- This is the heart of Domain-Driven Design

### 2. Application Layer (Use Cases)

**Location**: `src/application/`

**Purpose**: Orchestrates business workflows

**Contents**:
- **Services**: Implement use cases
- **DTOs**: Data transfer objects (if needed)

**Key Principles**:
- Orchestrates domain objects
- Calls repositories
- NO business logic (that's in domain!)
- Coordinates between layers

**Example - Order Service**:
```python
async def create_order(self, buyer_id, umkm_id, items):
    # 1. Fetch UMKM
    umkm = await self.umkm_repository.find_by_id(umkm_id)
    
    # 2. Domain check: Can accept orders?
    if not umkm.can_accept_orders():  # Business logic in domain!
        raise ValueError("UMKM not accepting orders")
    
    # 3. Process items
    for item in items:
        product = await self.product_repository.find_by_id(item.product_id)
        if not product.can_be_ordered(item.quantity):  # Business logic!
            raise ValueError("Product unavailable")
        product.reduce_stock(item.quantity)  # Business logic!
    
    # 4. Create order entity
    order = Order(...)  # Domain validates in constructor
    
    # 5. Persist
    return await self.order_repository.save(order)
```

**Notice**: The service orchestrates, but business rules are in entities!

### 3. Infrastructure Layer (Technical Details)

**Location**: `src/infrastructure/`

**Purpose**: Implements technical details

**Contents**:
- **Repository Implementations**: Actual database access
- **External Services**: APIs, authentication, etc.
- **Framework Adapters**: Database connections, etc.

**Key Principles**:
- Implements interfaces from domain layer
- Contains framework-specific code
- Most volatile layer (changes most)
- Depends on domain abstractions

**Example - Repository Implementation**:
```python
class InMemoryUserRepository(UserRepository):  # Implements domain interface
    def __init__(self):
        self._users: Dict[UUID, User] = {}
    
    async def save(self, user: User) -> User:
        self._users[user.id] = deepcopy(user)
        return user
```

**Key Point**: Can be replaced with PostgreSQL without changing domain!

### 4. Interface Layer (API)

**Location**: `src/interface/`

**Purpose**: Handles external communication (HTTP)

**Contents**:
- **Routes**: FastAPI endpoints (thin controllers)
- **Schemas**: Pydantic models for API
- **Dependencies**: Dependency injection setup

**Key Principles**:
- THIN controllers (no business logic!)
- Handle HTTP concerns only
- Call application services
- Return formatted responses

**Example - Thin Controller**:
```python
@router.post("/orders")
async def create_order(
    request: OrderCreateRequest,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    # NO business logic here!
    # Just call service and return response
    order = await order_service.create_order(
        buyer_id=current_user.id,
        umkm_id=request.umkm_id,
        items=request.items
    )
    return OrderResponse.from_entity(order)
```

## The Dependency Rule

```
┌─────────────────────────────────────┐
│     Interface Layer (API)           │
│  Depends on: Application            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Application Layer (Services)    │
│  Depends on: Domain                 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Domain Layer (Entities)         │
│  Depends on: NOTHING                │
└──────────────▲──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│  Infrastructure Layer (Repos)       │
│  Depends on: Domain (interfaces)    │
└─────────────────────────────────────┘
```

**Critical Rule**: Dependencies point INWARD
- Outer layers depend on inner layers
- Inner layers NEVER depend on outer layers
- Domain layer has ZERO dependencies

## Key Design Patterns

### 1. Repository Pattern

**Purpose**: Abstract data access

**Domain**: Defines WHAT is needed
```python
class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
```

**Infrastructure**: Defines HOW it's done
```python
class InMemoryUserRepository(UserRepository):
    async def save(self, user: User) -> User:
        # Implementation details
```

**Benefits**:
- Domain doesn't know about database
- Easy to swap implementations
- Testable with mocks

### 2. Dependency Injection

**Purpose**: Loose coupling, testability

**FastAPI Integration**:
```python
def get_order_service(
    order_repo: Annotated[OrderRepository, Depends(get_order_repository)],
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)]
) -> OrderService:
    return OrderService(order_repo, product_repo)
```

**Benefits**:
- Services don't create dependencies
- Easy to inject mocks for testing
- Centralized configuration

### 3. Domain-Driven Design

**Entities with Behavior**:
```python
class Order:
    def confirm(self) -> None:
        """Business logic with validation"""
        if self.status != OrderStatus.PLACED:
            raise ValueError("Can only confirm placed orders")
        self.status = OrderStatus.CONFIRMED
```

**Why?**
- Business rules in one place
- Easy to understand
- Testable without infrastructure
- Reflects real business domain

## Example: Create Order Flow

Let's trace a complete request through all layers:

### 1. HTTP Request (Interface Layer)

```
POST /api/v1/orders
{
  "umkm_id": "...",
  "items": [{"product_id": "...", "quantity": 2}]
}
```

### 2. Route Handler (Interface Layer)

```python
@router.post("/orders")
async def create_order(request, order_service):
    # Just call service - NO business logic!
    order = await order_service.create_order(...)
    return format_response(order)
```

### 3. Application Service (Application Layer)

```python
async def create_order(self, ...):
    # 1. Fetch entities
    umkm = await self.umkm_repository.find_by_id(...)
    product = await self.product_repository.find_by_id(...)
    
    # 2. Call domain methods (business logic!)
    if not umkm.can_accept_orders():  # Domain logic
        raise ValueError("...")
    
    if not product.can_be_ordered(quantity):  # Domain logic
        raise ValueError("...")
    
    product.reduce_stock(quantity)  # Domain logic
    
    # 3. Create order (domain validates)
    order = Order(...)  # Constructor validates
    
    # 4. Persist
    await self.order_repository.save(order)
    await self.product_repository.save(product)
```

### 4. Domain Entities (Domain Layer)

```python
class Product:
    def reduce_stock(self, quantity: int) -> None:
        """Business logic for stock management"""
        if not self.can_be_ordered(quantity):
            raise ValueError("Insufficient stock")
        self.stock_quantity -= quantity
        self.updated_at = datetime.utcnow()
```

### 5. Repository (Infrastructure Layer)

```python
async def save(self, product: Product) -> Product:
    # Just persistence - no business logic
    self._products[product.id] = deepcopy(product)
    return product
```

## Testing Strategy

### Unit Tests - Domain Layer

```python
def test_product_reduce_stock():
    product = Product(stock_quantity=10, ...)
    product.reduce_stock(3)
    assert product.stock_quantity == 7  # Pure business logic test
```

**No mocks needed!** Domain is pure.

### Integration Tests - Application Layer

```python
async def test_create_order():
    mock_repo = Mock(OrderRepository)
    service = OrderService(mock_repo, ...)
    
    order = await service.create_order(...)
    
    assert mock_repo.save.called
```

**Easy to mock repositories!**

### E2E Tests - API Layer

```python
def test_create_order_endpoint():
    response = client.post("/api/v1/orders", json={...})
    assert response.status_code == 201
```

## Migration Strategy

### From In-Memory to PostgreSQL

Current setup uses in-memory repositories for development.

**To migrate to PostgreSQL:**

1. **Create SQLAlchemy models** (Infrastructure)
```python
class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    # ...
```

2. **Implement PostgreSQL repositories** (Infrastructure)
```python
class PostgresUserRepository(UserRepository):
    async def save(self, user: User) -> User:
        # SQLAlchemy implementation
```

3. **Update dependency injection** (Interface)
```python
def get_user_repository() -> UserRepository:
    return PostgresUserRepository(session)  # Changed!
```

4. **Done!** ✅
- No changes to domain layer
- No changes to application layer
- No changes to routes

This is the power of Clean Architecture!

## Common Pitfalls to Avoid

### ❌ DON'T: Put business logic in controllers

```python
@router.post("/orders")
async def create_order(...):
    if product.stock_quantity < quantity:  # NO!
        raise HTTPException(...)
    product.stock_quantity -= quantity  # NO!
```

### ✅ DO: Call domain methods

```python
@router.post("/orders")
async def create_order(...):
    order = await order_service.create_order(...)  # YES!
```

### ❌ DON'T: Mix domain with infrastructure

```python
class User:
    def save_to_db(self):  # NO! Database concern in domain
        db.session.add(self)
```

### ✅ DO: Use repositories

```python
user = User(...)  # Domain entity
await user_repository.save(user)  # Infrastructure
```

## SOLID Principles in Action

### Single Responsibility Principle (SRP)
- Each entity has one responsibility
- Each service handles one area
- Each repository manages one entity type

### Open/Closed Principle (OCP)
- Open for extension (new implementations)
- Closed for modification (interfaces stable)

### Liskov Substitution Principle (LSP)
- Any repository implementation works
- Can swap in-memory for PostgreSQL

### Interface Segregation Principle (ISP)
- Repository interfaces are focused
- Services depend only on what they need

### Dependency Inversion Principle (DIP)
- High-level (domain) doesn't depend on low-level (infrastructure)
- Both depend on abstractions (interfaces)

## Conclusion

This architecture provides:
- ✅ **Separation of Concerns**: Each layer has a clear purpose
- ✅ **Testability**: Easy to test each layer independently
- ✅ **Maintainability**: Changes are localized and predictable
- ✅ **Flexibility**: Easy to swap implementations
- ✅ **Scalability**: Architecture supports growth

The result is a **production-ready**, **maintainable**, and **professional** backend that follows industry best practices.
