# Quick Start Guide

This guide will help you get started with the IPB Food & UMKM Student Hub backend.

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Test Demo

```bash
python test_architecture.py
```

This demonstrates the entire Clean Architecture working together!

### 3. Start the API Server

```bash
# From project root directory
python -m uvicorn src.main:app --reload
```

The API will be available at: http://localhost:8000

### 4. Explore the API

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Root Endpoint**: http://localhost:8000/

## 📖 Example API Workflow

### 1. Register a Seller

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seller@ipb.ac.id",
    "username": "seller1",
    "password": "password123",
    "full_name": "Jane Seller",
    "role": "seller"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seller@ipb.ac.id",
    "password": "password123"
  }'
```

Save the `access_token` from the response.

### 3. Create UMKM

```bash
TOKEN="your-token-here"

curl -X POST http://localhost:8000/api/v1/umkm \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Warung Makan Barokah",
    "description": "Makanan rumahan enak dan murah",
    "location": "Gedung Rektorat IPB",
    "phone": "081234567890",
    "operating_hours": "08:00-17:00"
  }'
```

### 4. Create Product

```bash
UMKM_ID="your-umkm-id-here"

curl -X POST "http://localhost:8000/api/v1/products?umkm_id=$UMKM_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nasi Goreng Special",
    "description": "Nasi goreng dengan telur dan ayam",
    "price": 15000,
    "category": "food",
    "stock_quantity": 50
  }'
```

### 5. List Products

```bash
curl http://localhost:8000/api/v1/products
```

## 🏗️ Architecture Overview

### Project Structure

```
src/
├── domain/           # Business logic & entities
├── application/      # Use cases & services
├── infrastructure/   # Repositories & external services
└── interface/        # API routes & schemas
```

### Key Principles

1. **Domain Layer**: Contains business logic, NO dependencies
2. **Application Layer**: Orchestrates use cases
3. **Infrastructure Layer**: Implements technical details
4. **Interface Layer**: Thin controllers for HTTP

### The Dependency Rule

```
Interface → Application → Domain ← Infrastructure
```

- Inner layers never depend on outer layers
- Domain is pure business logic
- Infrastructure implements domain interfaces

## 🧪 Testing

The `test_architecture.py` script demonstrates:
- ✅ User registration and authentication
- ✅ UMKM registration
- ✅ Product creation
- ✅ Order creation with validation
- ✅ Domain business rules
- ✅ State transitions
- ✅ Stock management

Run it with:
```bash
python test_architecture.py
```

## 🔐 Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-token>
```

### User Roles

- **Buyer**: Can make orders and write reviews
- **Seller**: Can create UMKM, manage products, fulfill orders
- **Admin**: Can approve UMKMs, moderate content

## 📝 API Documentation

### Available Endpoints

**Authentication**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user info

**UMKM Management**
- `POST /api/v1/umkm` - Create UMKM (seller)
- `GET /api/v1/umkm` - List all UMKMs
- `GET /api/v1/umkm/{id}` - Get UMKM details
- `PUT /api/v1/umkm/{id}` - Update UMKM (owner)
- `POST /api/v1/umkm/{id}/approve` - Approve UMKM (admin)

**Product Management**
- `POST /api/v1/products` - Create product (seller)
- `GET /api/v1/products` - List all products
- `GET /api/v1/products/umkm/{id}` - List UMKM products
- `GET /api/v1/products/{id}` - Get product details
- `PUT /api/v1/products/{id}` - Update product (owner)
- `PATCH /api/v1/products/{id}/price` - Update price
- `PATCH /api/v1/products/{id}/stock` - Update stock
- `PATCH /api/v1/products/{id}/availability` - Toggle availability

**Order Management**
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders/my-orders` - Get buyer's orders
- `GET /api/v1/orders/umkm/{id}` - Get UMKM's orders (seller)
- `GET /api/v1/orders/{id}` - Get order details
- `PATCH /api/v1/orders/{id}/status` - Update order status (seller)
- `POST /api/v1/orders/{id}/cancel` - Cancel order

**Review Management**
- `POST /api/v1/reviews` - Create review
- `GET /api/v1/reviews/umkm/{id}` - Get UMKM reviews
- `GET /api/v1/reviews/my-reviews` - Get user's reviews
- `PUT /api/v1/reviews/{id}` - Update review (author)
- `POST /api/v1/reviews/{id}/flag` - Flag for moderation
- `POST /api/v1/reviews/{id}/hide` - Hide review (admin)

## 🔄 Extending to PostgreSQL

When ready for production with PostgreSQL:

1. Install dependencies:
```bash
pip install asyncpg sqlalchemy[asyncio] alembic
```

2. Create SQLAlchemy models in `src/infrastructure/persistence/models.py`

3. Implement PostgreSQL repositories in `src/infrastructure/persistence/postgres_repositories.py`

4. Update dependency injection in `src/interface/api/v1/dependencies/__init__.py`

5. **No changes needed in domain or application layers!** ✅

## 💡 Tips

- Use the interactive docs at `/docs` for easy testing
- Check `test_architecture.py` for usage examples
- All business logic is in domain entities
- Routes are thin - they just call services
- Services orchestrate - they don't contain business logic

## 🆘 Common Issues

**Import errors when running directly:**
- Use: `python -m uvicorn src.main:app`
- Don't use: `python src/main.py`

**Port already in use:**
- Change port: `--port 8001`
- Or kill the process using port 8000

**Authentication errors:**
- Make sure to include `Bearer` prefix in Authorization header
- Check token hasn't expired (30 min default)

## 📚 Learn More

- See `README.md` for detailed architecture explanation
- Read inline comments in source code for layer responsibilities
- Check `src/domain/entities/` for business logic examples
- Review `src/application/services/order_service.py` for orchestration examples

## 🎓 Educational Value

This project demonstrates:
- Clean Architecture principles
- Domain-Driven Design
- SOLID principles
- Repository pattern
- Dependency injection
- JWT authentication
- Role-based access control

Perfect for learning professional backend development!

## 📞 Support

For questions or issues, refer to:
- README.md for architecture details
- Source code comments for implementation details
- test_architecture.py for usage examples
