# Backend-Frontend Integration Guide

This document describes how the backend and frontend work together in the IPB UMKM Centre application.

## Architecture Overview

The application uses a **clean architecture** approach with clear separation between backend (FastAPI) and frontend (React + TypeScript):

```
┌─────────────────────────────────────────┐
│         Frontend (React + TS)           │
│  - Vite build system                    │
│  - Zustand state management             │
│  - Axios HTTP client                    │
│  - Service layer for API calls          │
└─────────────┬───────────────────────────┘
              │ HTTP/REST API
              │ (JSON over HTTP)
┌─────────────▼───────────────────────────┐
│         Backend (FastAPI)               │
│  - Clean Architecture layers            │
│  - JWT authentication                   │
│  - Role-based access control            │
│  - Domain-driven design                 │
└─────────────────────────────────────────┘
```

## API Endpoints

### Base URL
- **Development**: `http://localhost:8000/api/v1`
- **Production**: Configure via `VITE_API_BASE_URL` environment variable

### Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword",
  "full_name": "John Doe",
  "role": "buyer",
  "phone": "081234567890"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "buyer",
    "phone": "081234567890",
    "is_active": true,
    "created_at": "2026-02-12T09:00:00"
  }
}
```

#### POST /auth/login
Authenticate existing user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:** Same as register response (token + user)

#### GET /auth/me
Get current user information (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "buyer",
  "phone": "081234567890",
  "is_active": true,
  "created_at": "2026-02-12T09:00:00"
}
```

#### POST /auth/logout
Logout current user (requires authentication).

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

### Product Endpoints

#### GET /products
List all products.

**Query Parameters:**
- `available_only`: boolean (optional)

#### GET /products/{id}
Get single product by ID.

#### GET /products/{id}/reviews
Get all reviews for a product.

#### POST /products
Create new product (seller only).

#### PUT /products/{id}
Update product (seller only).

#### DELETE /products/{id}
Delete product (seller only).

### Order Endpoints

#### POST /orders
Create new order.

#### GET /orders/my-orders
Get current user's orders.

#### GET /orders/{id}
Get order details.

#### POST /orders/{id}/confirm
Confirm order (seller only) - convenience endpoint.

#### POST /orders/{id}/cancel
Cancel order.

### Review Endpoints

#### POST /reviews
Create new review.

#### GET /reviews/umkm/{umkm_id}
Get reviews for a UMKM.

### UMKM Endpoints

#### POST /umkm
Register new UMKM.

#### GET /umkm
List all UMKMs.

#### GET /umkm/{id}
Get UMKM details.

## Frontend Configuration

### Environment Variables

Create a `.env` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### HTTP Client

The frontend uses a centralized HTTP client (`src/infrastructure/http/http-client.ts`) that:
- Automatically injects JWT tokens
- Handles authentication errors (401)
- Provides consistent error handling
- Returns data directly (unwraps Axios responses)

### Service Layer Pattern

All API calls go through service classes:

```typescript
// Example: AuthService
import { AuthService } from '@/features/auth/services/auth.service';

// Login
const response = await AuthService.login({
  email: 'user@example.com',
  password: 'password'
});
// Returns: { access_token, token_type, user }

// Get current user
const user = await AuthService.getCurrentUser();
```

## Running the Application

### Backend (FastAPI)

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
cd src
python main.py

# Or using uvicorn
uvicorn src.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend (React)

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

The frontend will be available at: http://localhost:5173

### Running Both Together

1. **Terminal 1 - Backend:**
   ```bash
   cd /path/to/project
   python -m uvicorn src.main:app --reload
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd /path/to/project/frontend
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Authentication Flow

```
┌──────────┐                           ┌──────────┐
│          │  1. Login Request         │          │
│ Frontend ├──────────────────────────>│  Backend │
│          │  (email, password)        │          │
│          │                           │          │
│          │  2. Auth Response         │          │
│          │<──────────────────────────┤          │
│          │  (token + user)           │          │
└────┬─────┘                           └──────────┘
     │
     │ 3. Store token in localStorage
     │    Store user in Zustand store
     │
     │ 4. All subsequent requests
     │    include token in header:
     │    Authorization: Bearer <token>
     │
```

## CORS Configuration

The backend is configured to allow CORS for development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**⚠️ Production Note:** Update `allow_origins` to specify your production frontend URL.

## Error Handling

### Backend
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing or invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Internal Server Error

### Frontend
The HTTP client automatically:
- Redirects to login on 401
- Logs errors to console
- Propagates errors to components for display

## Data Types and Schemas

### User Roles
```typescript
enum UserRole {
  BUYER = 'buyer',
  SELLER = 'seller',
  ADMIN = 'admin'
}
```

### Product Categories
```typescript
enum ProductCategory {
  FOOD = 'food',
  BEVERAGE = 'beverage',
  SNACK = 'snack',
  MERCHANDISE = 'merchandise',
  OTHER = 'other'
}
```

### Order Status
```typescript
enum OrderStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  PREPARING = 'preparing',
  READY = 'ready',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
}
```

## Testing

### Integration Test Script

Run the integration test to verify backend-frontend connectivity:

```bash
# Start backend
python -m uvicorn src.main:app --reload

# Start frontend (in another terminal)
cd frontend
npm run dev

# Run integration tests (in another terminal)
./test_integration.sh
```

### Manual Testing

1. **Test Authentication:**
   - Register a new user
   - Login with credentials
   - Check if token is stored
   - Access protected routes

2. **Test Products:**
   - View product list
   - View product details
   - Create product (as seller)

3. **Test Orders:**
   - Create order (as buyer)
   - View order list
   - Confirm order (as seller)

## Troubleshooting

### Issue: CORS errors
**Solution:** Ensure backend CORS middleware is properly configured and backend is running.

### Issue: 401 Unauthorized
**Solution:** Check if token is stored in localStorage and not expired.

### Issue: Module not found in frontend
**Solution:** Check import paths - use `../../../` for imports from features to core/infrastructure.

### Issue: API endpoints not matching
**Solution:** Verify `API_ENDPOINTS` constants in `frontend/src/core/constants/index.ts` match backend routes.

## Next Steps

### Backend Enhancements
- [ ] Add PostgreSQL database
- [ ] Implement refresh tokens
- [ ] Add rate limiting
- [ ] Add pagination for large datasets
- [ ] Add search and filtering

### Frontend Enhancements
- [ ] Add loading states
- [ ] Add error boundaries
- [ ] Implement real-time updates (WebSocket)
- [ ] Add offline support
- [ ] Improve accessibility (a11y)

## Contributing

When making changes that affect both backend and frontend:

1. **Update API schemas** first in backend
2. **Update TypeScript types** in frontend
3. **Update service methods** if endpoints change
4. **Test both** backend and frontend
5. **Update this documentation**

## Support

For issues or questions:
- Check API docs: http://localhost:8000/docs
- Review integration tests
- Check console logs in browser/server
