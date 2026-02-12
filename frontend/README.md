# IPB Food & UMKM Student Hub - Frontend

A production-ready React + TypeScript frontend built with **Clean Architecture** principles, featuring a feature-based modular structure.

## 🏗️ Architecture

This project follows **Clean Architecture** with **Feature-Based Layered Architecture**:

```
┌─────────────────────────────────────────┐
│         UI Layer (Components)           │
│  - React components                     │
│  - UI logic only                        │
│  - No direct API calls                  │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│      Service Layer (API)                │
│  - API communication                    │
│  - Data transformation                  │
│  - HTTP requests                        │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│   Infrastructure Layer (HTTP Client)    │
│  - Axios configuration                  │
│  - Interceptors                         │
│  - Token management                     │
└─────────────────────────────────────────┘
```

### Why This Architecture?

**Key Benefits:**
- ✅ **Separation of Concerns**: UI, business logic, and API are separated
- ✅ **Testability**: Easy to test with mocked services
- ✅ **Maintainability**: Clear structure, easy to navigate
- ✅ **Scalability**: Feature-based modules scale well
- ✅ **Reusability**: Components and services are reusable

**The Dependency Rule:**
- UI components NEVER make direct API calls
- Components use services (service layer)
- Services use HTTP client (infrastructure layer)
- Clear separation of concerns at each layer

## 📁 Project Structure

See full structure in the repo. Key directories:

- `core/` - Configuration, constants, types
- `infrastructure/` - HTTP client, auth utilities
- `features/` - Feature modules (auth, products, orders, etc.)
- `shared/` - Reusable components and layouts
- `store/` - State management (Zustand)
- `routes/` - Route configuration with protection

## 🎯 Key Features

### 1. Authentication System
- JWT token-based authentication
- Login and registration
- Role-based access control (Buyer, Seller, Admin)
- Protected routes based on user roles
- Persistent sessions (localStorage)

### 2. User Roles
- **Buyer (Student)**: Browse products, place orders, write reviews
- **Seller (UMKM Merchant)**: Manage products, handle orders, manage business profile
- **Admin**: Moderate content, manage users, approve UMKM

### 3. Feature Modules
- **Products**: Browse, search, view details
- **Orders**: Pre-order system with status tracking
- **Reviews**: Rating and review system
- **Promos**: Student-exclusive promotional offers
- **Dashboards**: Role-specific dashboards

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
Create `.env` file in frontend directory:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Running the Application

**Development mode:**
```bash
npm run dev
```

The app will be available at: http://localhost:5173

**Build for production:**
```bash
npm run build
```

## 🔐 Authentication Flow

1. User logs in via LoginPage
2. AuthService makes API call to backend
3. Token stored in localStorage, user in Zustand
4. HTTP client auto-injects token in requests
5. Protected routes check auth status
6. On 401, user redirected to login

## 🛡️ Role-Based Route Protection

Routes are protected using `ProtectedRoute` component:

```tsx
<ProtectedRoute allowedRoles={[UserRole.ADMIN]}>
  <AdminDashboard />
</ProtectedRoute>
```

## 📦 Service Layer Pattern

Components never make direct API calls. They use service classes:

```tsx
// Component
const products = await ProductService.getProducts();

// Service
class ProductService {
  static async getProducts() {
    return await http.get('/products');
  }
}
```

## 🔧 Tech Stack

- React 18
- TypeScript
- Vite
- React Router v6
- Zustand (State Management)
- Axios (HTTP Client)
- Tailwind CSS

## 📄 License

MIT License
