# IPB Food & UMKM Student Hub - Backend API

A production-ready FastAPI backend for a campus marketplace application, built with **Clean Architecture** and **Domain-Driven Design** principles.

## 🏗️ Architecture

This project follows **Clean Architecture** with **Layered Architecture**:

```
┌─────────────────────────────────────────┐
│         Interface Layer                 │
│  (FastAPI Routes, API Schemas)          │
│  - Thin controllers                     │
│  - HTTP concerns only                   │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│      Application Layer                  │
│  (Use Cases, Services)                  │
│  - Business workflows                   │
│  - Orchestration logic                  │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│         Domain Layer                    │
│  (Entities, Repository Interfaces)      │
│  - Business logic                       │
│  - Domain rules                         │
│  - Pure, no dependencies                │
└─────────────────▲───────────────────────┘
                  │ implements
┌─────────────────┴───────────────────────┐
│      Infrastructure Layer               │
│  (Repository Implementations)           │
│  - Database access                      │
│  - External services                    │
└─────────────────────────────────────────┘
```

### Why This Architecture?

**Key Benefits:**
- ✅ **Testability**: Easy to test with mocked dependencies
- ✅ **Maintainability**: Clear separation of concerns
- ✅ **Flexibility**: Swap implementations without changing business logic
- ✅ **Scalability**: Ready for growth and complexity
- ✅ **SOLID Principles**: Enforced throughout

**The Dependency Rule:**
- Inner layers NEVER depend on outer layers
- Domain layer is pure business logic
- Infrastructure details are isolated

## 📁 Project Structure

```
src/
├── domain/                          # Domain Layer (Core Business Logic)
│   ├── entities/                    # Domain entities with business logic
│   │   ├── user.py                  # User entity with role-based methods
│   │   ├── umkm.py                  # UMKM (merchant) entity
│   │   ├── product.py               # Product entity with inventory logic
│   │   ├── order.py                 # Order entity with state machine
│   │   ├── review.py                # Review entity
│   │   └── promo.py                 # Promo entity with validation logic
│   └── repositories/                # Repository interfaces (abstract)
│       └── __init__.py              # All repository ABCs
│
├── application/                     # Application Layer (Use Cases)
│   └── services/                    # Application services
│       ├── auth_service.py          # Authentication use cases
│       ├── umkm_service.py          # UMKM management use cases
│       ├── product_service.py       # Product management use cases
│       ├── order_service.py         # Order processing use cases
│       └── review_service.py        # Review management use cases
│
├── infrastructure/                  # Infrastructure Layer (Technical Details)
│   ├── persistence/                 # Data persistence implementations
│   │   └── in_memory_repositories.py  # In-memory implementation (for now)
│   └── security/                    # Security implementations
│       └── auth_service.py          # JWT & password hashing
│
├── interface/                       # Interface Layer (API)
│   └── api/
│       └── v1/
│           ├── routes/              # FastAPI route handlers (thin controllers)
│           │   ├── auth.py          # Authentication endpoints
│           │   ├── umkm.py          # UMKM endpoints
│           │   ├── products.py      # Product endpoints
│           │   ├── orders.py        # Order endpoints
│           │   └── reviews.py       # Review endpoints
│           ├── schemas/             # Pydantic schemas for API
│           │   └── __init__.py      # Request/response models
│           └── dependencies/        # Dependency injection
│               └── __init__.py      # DI container setup
│
└── main.py                          # FastAPI application entry point
```

## 🎯 Key Features

### Domain Layer (Business Logic)

**Entities with Business Methods:**
- `User`: Role-based permissions (`can_sell_products()`, `can_moderate()`)
- `UMKM`: Status management (`approve()`, `suspend()`, `can_accept_orders()`)
- `Product`: Inventory management (`reduce_stock()`, `can_be_ordered()`)
- `Order`: State machine (`confirm()`, `cancel()`, `complete()`)
- `Review`: Rating validation and moderation
- `Promo`: Discount calculation logic

### Application Layer (Use Cases)

**Services orchestrate business workflows:**
- `AuthenticationService`: User registration, login, JWT token management
- `UMKMService`: UMKM registration, approval, updates
- `ProductService`: Product CRUD, inventory management
- `OrderService`: **Create Order with domain validation** (critical example!)
- `ReviewService`: Review creation, moderation

### Infrastructure Layer

**Current Implementation:**
- In-memory repositories (for development/testing)
- JWT authentication with `python-jose`
- Password hashing with `bcrypt` via `passlib`

**Ready for PostgreSQL:**
- Just implement repository interfaces
- No changes to domain or application layers needed!

### Interface Layer (API)

**Thin Controllers:**
- Routes handle HTTP concerns only
- No business logic in controllers
- Call application services for operations
- Return formatted responses

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/bianglalametro/IPB-UMKMcentre.git
cd IPB-UMKMcentre
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

**Development mode:**
```bash
cd src
python main.py
```

Or using uvicorn directly:
```bash
cd src
uvicorn main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

## 📖 API Documentation

### Authentication

**Register User:**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword",
  "full_name": "John Doe",
  "role": "buyer",
  "phone": "081234567890"
}
```

**Login:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response: {"access_token": "eyJ...", "token_type": "bearer"}
```

## 🔐 Role-Based Access Control

| Role   | Permissions |
|--------|-------------|
| Buyer  | Make orders, write reviews |
| Seller | Register UMKM, manage products, manage orders |
| Admin  | Approve UMKMs, moderate reviews, suspend merchants |

## 💡 Key Architectural Patterns

### 1. Repository Pattern
Separates data access logic from business logic.

### 2. Dependency Injection
Services and repositories are injected, promoting loose coupling.

### 3. Domain-Driven Design
Business logic lives in domain entities, not in controllers or services.

## 🔄 Migrating to PostgreSQL

When ready to use PostgreSQL, simply implement the repository interfaces with SQLAlchemy - no changes needed in domain or application layers!

## 🧪 Testing

The architecture makes testing easy with mock repositories and services.

## 📝 License

This project is licensed under the MIT License.

## 🎓 Educational Value

This project demonstrates:
- ✅ Clean Architecture in practice
- ✅ Domain-Driven Design principles
- ✅ SOLID principles application
- ✅ Repository pattern
- ✅ Dependency injection
- ✅ Role-based access control
- ✅ JWT authentication
- ✅ RESTful API design

Perfect for learning professional backend development! 🚀