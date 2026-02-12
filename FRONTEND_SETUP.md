# IPB Food & UMKM Student Hub - Complete Project Documentation

## Project Overview

A complete full-stack application for connecting IPB students with local UMKM (Micro, Small, and Medium Enterprise) food vendors. Built with professional Clean Architecture principles on both frontend and backend.

## Repository Structure

```
IPB-UMKMcentre/
├── src/                          # Backend (Python/FastAPI)
│   ├── domain/                   # Domain layer (business logic)
│   ├── application/              # Application layer (use cases)
│   ├── infrastructure/           # Infrastructure layer (DB, external services)
│   └── interface/                # Interface layer (API routes)
│
├── frontend/                     # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── core/                 # Core configuration
│   │   ├── infrastructure/       # HTTP client, auth
│   │   ├── features/             # Feature modules
│   │   ├── shared/               # Reusable components
│   │   ├── store/                # State management
│   │   └── routes/               # Routing
│   ├── README.md                 # Frontend documentation
│   ├── ARCHITECTURE.md           # Frontend architecture details
│   └── PROJECT_SUMMARY.md        # Frontend implementation summary
│
├── ARCHITECTURE.md               # Backend architecture documentation
├── README.md                     # Backend documentation
└── FRONTEND_SETUP.md            # This file
```

## Architecture Overview

Both frontend and backend follow **Clean Architecture** principles:

### Backend Architecture (Python/FastAPI)

```
Interface Layer (API)
    ↓
Application Layer (Services)
    ↓
Domain Layer (Entities)
    ↑
Infrastructure Layer (Repositories)
```

**Key Features:**
- RESTful API with FastAPI
- JWT authentication
- In-memory repositories (ready for PostgreSQL)
- Role-based access control
- Domain-driven design

### Frontend Architecture (React/TypeScript)

```
UI Components
    ↓
Service Layer (API)
    ↓
Infrastructure (HTTP Client)
```

**Key Features:**
- React 18 + TypeScript
- Vite for build tooling
- Zustand for state management
- React Router for routing
- Tailwind CSS for styling
- Role-based route protection

## User Roles

The system supports three user roles:

### 1. Buyer (Student)
**Capabilities:**
- Browse products from UMKM vendors
- Place pre-orders
- Write reviews and ratings
- View student-exclusive promos
- Track order status

**Dashboard:**
- View order history
- Manage reviews
- Browse products

### 2. Seller (UMKM Merchant)
**Capabilities:**
- Register and manage UMKM profile
- Add and manage products
- Process customer orders
- View sales statistics

**Dashboard:**
- Product management (CRUD)
- Order management
- UMKM profile settings
- Sales overview

### 3. Admin (System Administrator)
**Capabilities:**
- Approve/reject UMKM registrations
- Moderate reviews
- Manage users
- System oversight

**Dashboard:**
- User management
- UMKM approval workflow
- Review moderation
- System statistics

## Core Features

### 1. Authentication System
- **Registration** with role selection
- **Login** with JWT tokens
- **Role-based access control**
- **Protected routes** in frontend
- **Token persistence** in localStorage
- **Auto logout** on token expiration

### 2. Product Management
- **Browse products** by category
- **Search and filter** functionality
- **Product details** with images
- **Stock management** for sellers
- **Product reviews** and ratings

### 3. Pre-Order System
- **Shopping cart** functionality
- **Order placement** with items
- **Order status tracking**
- **Pickup time selection**
- **Order history**

### 4. Review & Rating System
- **Product reviews** with ratings (1-5 stars)
- **UMKM reviews** for overall service
- **Review moderation** by admins
- **Average rating** calculations

### 5. Student Promo System
- **Exclusive discounts** for students
- **Promo listings** on dedicated page
- **Discount calculation** at checkout
- **Time-limited** promotions

## Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **python-jose** - JWT handling
- **passlib** - Password hashing
- **uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router v6** - Routing
- **Zustand** - State management
- **Axios** - HTTP client
- **Tailwind CSS** - Styling

## Getting Started

### Backend Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the server:**
```bash
cd src
python main.py
```

3. **Access the API:**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment:**
Create `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

4. **Run development server:**
```bash
npm run dev
```

5. **Access the app:**
- Frontend: http://localhost:5173

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Products
- `GET /api/v1/products` - List products
- `GET /api/v1/products/:id` - Get product details
- `POST /api/v1/products` - Create product (seller)
- `PUT /api/v1/products/:id` - Update product (seller)
- `DELETE /api/v1/products/:id` - Delete product (seller)

### Orders
- `GET /api/v1/orders` - List orders
- `GET /api/v1/orders/:id` - Get order details
- `POST /api/v1/orders` - Create order (buyer)
- `POST /api/v1/orders/:id/confirm` - Confirm order (seller)
- `POST /api/v1/orders/:id/cancel` - Cancel order

### Reviews
- `GET /api/v1/reviews` - List reviews
- `GET /api/v1/products/:id/reviews` - Get product reviews
- `POST /api/v1/reviews` - Create review (buyer)
- `PUT /api/v1/reviews/:id` - Update review
- `DELETE /api/v1/reviews/:id` - Delete review

### UMKM
- `GET /api/v1/umkm` - List UMKM
- `GET /api/v1/umkm/:id` - Get UMKM details
- `POST /api/v1/umkm` - Register UMKM (seller)
- `POST /api/v1/umkm/:id/approve` - Approve UMKM (admin)
- `POST /api/v1/umkm/:id/suspend` - Suspend UMKM (admin)

## Frontend Routes

### Public Routes
- `/` - Home page
- `/login` - Login page
- `/register` - Registration page
- `/products` - Product listing
- `/umkm` - UMKM listing
- `/promos` - Student promos

### Protected Routes (Buyer)
- `/buyer` - Buyer dashboard
- `/buyer/orders` - Order history
- `/buyer/reviews` - My reviews
- `/cart` - Shopping cart
- `/checkout` - Checkout page

### Protected Routes (Seller)
- `/seller` - Seller dashboard
- `/seller/products` - Manage products
- `/seller/orders` - Manage orders
- `/seller/umkm` - UMKM profile

### Protected Routes (Admin)
- `/admin` - Admin dashboard
- `/admin/users` - User management
- `/admin/umkm` - UMKM approval
- `/admin/reviews` - Review moderation

## Key Architectural Patterns

### 1. Clean Architecture
- **Separation of concerns** at each layer
- **Dependency inversion** - inner layers don't depend on outer
- **Testability** - easy to mock and test
- **Flexibility** - easy to swap implementations

### 2. Repository Pattern
- **Abstracts data access** from business logic
- **Interface defined** in domain layer
- **Implementation** in infrastructure layer
- **Easy to swap** (in-memory → PostgreSQL)

### 3. Service Layer Pattern (Frontend)
- **No direct API calls** in components
- **All HTTP requests** through service classes
- **Type-safe** interfaces
- **Centralized error** handling

### 4. Dependency Injection
- **Services injected** into routes (backend)
- **Hooks consume** services (frontend)
- **Loose coupling** between layers
- **Easy to mock** for testing

### 5. State Management (Frontend)
- **Zustand stores** for global state
- **Auth store** for user/session
- **Cart store** with persistence
- **Optimized re-renders**

## Security Features

✅ **JWT Authentication** - Secure token-based auth
✅ **Password Hashing** - BCrypt for passwords
✅ **Role-Based Access** - Granular permissions
✅ **Input Validation** - Pydantic models
✅ **XSS Protection** - React escaping
✅ **CORS Configuration** - Restricted origins
✅ **Token Expiration** - Auto-logout
✅ **Protected Routes** - Frontend guards

## Testing Strategy

### Backend Testing
- **Unit tests** - Test domain logic
- **Integration tests** - Test services with mocked repos
- **E2E tests** - Test API endpoints

### Frontend Testing
- **Unit tests** - Test utility functions
- **Component tests** - Test UI components in isolation
- **Integration tests** - Test feature flows
- **E2E tests** - Test full user journeys

## Deployment Considerations

### Backend
- **Production server**: Gunicorn with Uvicorn workers
- **Database**: Migrate to PostgreSQL
- **Environment variables**: Use .env files
- **Logging**: Configure proper logging
- **Monitoring**: Add health checks

### Frontend
- **Build**: `npm run build`
- **Static hosting**: Vercel, Netlify, or S3
- **Environment**: Configure API URL
- **CDN**: Use for static assets
- **Analytics**: Add tracking

## Database Migration (Future)

Currently using in-memory storage. To migrate to PostgreSQL:

1. **Install SQLAlchemy:**
```bash
pip install sqlalchemy psycopg2-binary
```

2. **Create models** in `infrastructure/persistence/`
3. **Implement repository** interfaces with SQLAlchemy
4. **Update dependency injection** to use new repos
5. **No changes needed** in domain or application layers!

## Documentation

### Backend
- `README.md` - Quick start and overview
- `ARCHITECTURE.md` - Detailed architecture explanation
- API docs available at `/docs` endpoint

### Frontend
- `frontend/README.md` - Quick start guide
- `frontend/ARCHITECTURE.md` - Detailed architecture docs
- `frontend/PROJECT_SUMMARY.md` - Implementation summary
- Inline comments throughout code

## Learning Value

This project demonstrates:

✅ **Clean Architecture** in practice (both backend and frontend)
✅ **Domain-Driven Design** principles
✅ **SOLID principles** application
✅ **Repository pattern** implementation
✅ **Service layer pattern** (frontend)
✅ **Dependency injection** usage
✅ **Role-based access control**
✅ **JWT authentication** flow
✅ **RESTful API design**
✅ **Modern React** patterns
✅ **TypeScript** best practices
✅ **State management** with Zustand
✅ **Professional code** organization

Perfect for learning professional full-stack development! 🚀

## License

This project is licensed under the MIT License.

## Contributors

Developed as an educational example of Clean Architecture in full-stack development.

---

**Note:** This is a complete, production-ready application structure. However, some features like actual database integration, payment processing, and advanced error handling would need to be added for a real production deployment.
