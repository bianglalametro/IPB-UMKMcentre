# Frontend Architecture Documentation

## Overview

The IPB Food & UMKM Student Hub frontend is built using **Clean Architecture** combined with **Feature-Based Modular Architecture**.

## Why Clean Architecture for Frontend?

### Problems with Traditional React Apps

**Typical issues:**
- Components making direct API calls (tight coupling)
- Business logic mixed with UI code
- Hard to test (requires mocking HTTP)
- Difficult to change API endpoints
- State management scattered across components
- No clear structure as app grows

### Benefits of Clean Architecture

✅ **Separation of Concerns**: UI, API, and infrastructure are separated  
✅ **Testability**: Each layer can be tested independently  
✅ **Maintainability**: Clear structure makes code easy to understand  
✅ **Flexibility**: Easy to swap implementations (e.g., REST to GraphQL)  
✅ **Scalability**: Structure supports growth in features and team size  

## The Three Layers

### 1. UI Layer (Components)

**Location**: `src/features/*/components/` and `src/features/*/pages/`

**Purpose**: Handle user interface and user interactions

**Responsibilities**:
- Render UI elements
- Handle user input
- Display loading states
- Show error messages
- Call service layer methods

**Key Principles**:
- NO direct API calls
- NO business logic (that's in services)
- Only UI-related concerns
- Use React hooks for state

**Example - Login Component**:
```tsx
const LoginPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Call service layer - NO direct API call
      const response = await AuthService.login(formData);
      setUser(response.user);
      navigate('/dashboard');
    } catch (error) {
      // Handle error
    } finally {
      setIsLoading(false);
    }
  };
  
  return <form onSubmit={handleSubmit}>{/* JSX */}</form>;
};
```

**Why no API calls in components?**
- Components focus on UI only
- Services handle API details
- Easy to mock services for testing
- API changes don't affect components

### 2. Service Layer (API Communication)

**Location**: `src/features/*/services/`

**Purpose**: Handle all API communication and data transformation

**Responsibilities**:
- Make HTTP requests
- Transform API responses to domain types
- Handle API errors
- Provide typed interfaces

**Key Principles**:
- Use HTTP client from infrastructure layer
- Return typed data
- NO UI logic
- NO direct Axios usage (use http client)

**Example - Product Service**:
```tsx
export class ProductService {
  static async getProducts(params?: FilterParams): Promise<PaginatedResponse<Product>> {
    // Use infrastructure layer's HTTP client
    return await http.get<PaginatedResponse<Product>>(
      API_ENDPOINTS.PRODUCTS,
      { params }
    );
  }
  
  static async createProduct(data: CreateProductRequest): Promise<Product> {
    return await http.post<Product>(API_ENDPOINTS.PRODUCTS, data);
  }
}
```

**Benefits:**
- Centralized API logic
- Reusable across components
- Easy to mock for testing
- Type-safe interfaces

### 3. Infrastructure Layer (HTTP Client & Utilities)

**Location**: `src/infrastructure/`

**Purpose**: Handle technical implementation details

**Responsibilities**:
- Configure Axios
- Add request/response interceptors
- Inject JWT tokens
- Handle global errors
- Manage localStorage

**Key Principles**:
- Used by service layer
- Provides technical utilities
- No business logic
- No UI concerns

**Example - HTTP Client**:
```tsx
const httpClient = axios.create({
  baseURL: config.api.baseURL,
  timeout: config.api.timeout,
});

// Request interceptor - inject JWT token
httpClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle 401
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuth();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Feature-Based Module Organization

Each feature is self-contained with all its related code:

```
features/
├── auth/
│   ├── components/     # Auth-specific UI components
│   ├── services/       # Auth API calls
│   ├── pages/          # Login, Register pages
│   ├── hooks/          # Custom hooks for auth
│   └── types/          # Auth-specific types
│
├── products/
│   ├── components/     # ProductCard, ProductFilter, etc.
│   ├── services/       # Product API calls
│   ├── pages/          # ProductList, ProductDetail
│   └── types/          # Product-specific types
```

**Benefits:**
- Easy to locate related code
- Features can be developed independently
- Easy to add/remove features
- Clear ownership and responsibilities

## State Management (Zustand)

### Why Zustand?

- **Simple**: No boilerplate like Redux
- **Fast**: Optimized re-renders
- **TypeScript-friendly**: Great type inference
- **Flexible**: Works with any React pattern

### Store Structure

```tsx
// Auth Store
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
  hasRole: (role: UserRole) => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  logout: () => {
    clearAuth();
    set({ user: null, isAuthenticated: false });
  },
  hasRole: (role) => get().user?.role === role,
}));
```

### Usage in Components

```tsx
const MyComponent = () => {
  // Subscribe to specific state
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  
  return <button onClick={logout}>Logout {user?.full_name}</button>;
};
```

## Authentication Architecture

### JWT Token Flow

1. **Login:**
   - User submits credentials
   - AuthService calls `/auth/login`
   - Backend returns JWT token + user data
   - Token stored in localStorage
   - User stored in Zustand store

2. **Authenticated Requests:**
   - HTTP client reads token from localStorage
   - Adds `Authorization: Bearer <token>` header
   - Backend validates token

3. **Token Expiration:**
   - Backend returns 401 if token expired
   - HTTP interceptor catches 401
   - Clears auth data
   - Redirects to login

4. **Logout:**
   - Clear token from localStorage
   - Clear user from store
   - Redirect to login

### Role-Based Route Protection

```tsx
// ProtectedRoute Component
const ProtectedRoute = ({ children, allowedRoles = [] }) => {
  const { user, isAuthenticated } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (allowedRoles.length > 0) {
    if (!allowedRoles.includes(user.role)) {
      return <div>Access Denied</div>;
    }
  }
  
  return <>{children}</>;
};

// Usage
<Route
  path="/admin"
  element={
    <ProtectedRoute allowedRoles={[UserRole.ADMIN]}>
      <AdminDashboard />
    </ProtectedRoute>
  }
/>
```

## Data Flow Example: Create Order

Let's trace a complete order creation through all layers:

### 1. User Action (UI Layer)
```tsx
// OrderCheckout.tsx
const handleCheckout = async () => {
  setIsLoading(true);
  try {
    const order = await OrderService.createOrder({
      umkm_id: selectedUMKM.id,
      items: cartItems,
    });
    navigate(`/orders/${order.id}`);
  } catch (error) {
    showError(error.message);
  }
};
```

### 2. Service Call (Service Layer)
```tsx
// order.service.ts
export class OrderService {
  static async createOrder(data: CreateOrderRequest): Promise<Order> {
    return await http.post<Order>(API_ENDPOINTS.ORDERS, data);
  }
}
```

### 3. HTTP Request (Infrastructure Layer)
```tsx
// http-client.ts
export const http = {
  post: async (url, data) => {
    // Interceptor adds JWT token
    const response = await httpClient.post(url, data);
    return response.data;
  }
};
```

### 4. Backend Processing
- Validates token
- Validates order data
- Creates order in database
- Returns order data

### 5. Response Flow
- HTTP client receives response
- Service returns typed Order object
- Component updates UI
- User sees success message

## Testing Strategy

### Unit Tests - Service Layer
```tsx
describe('ProductService', () => {
  it('should fetch products', async () => {
    // Mock HTTP client
    jest.spyOn(http, 'get').mockResolvedValue(mockProducts);
    
    const products = await ProductService.getProducts();
    
    expect(products).toEqual(mockProducts);
    expect(http.get).toHaveBeenCalledWith(API_ENDPOINTS.PRODUCTS);
  });
});
```

### Component Tests - UI Layer
```tsx
describe('LoginPage', () => {
  it('should call AuthService on submit', async () => {
    // Mock service
    jest.spyOn(AuthService, 'login').mockResolvedValue(mockUser);
    
    render(<LoginPage />);
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.click(submitButton);
    
    expect(AuthService.login).toHaveBeenCalled();
  });
});
```

## Best Practices

### DO's ✅

1. **Separate concerns:**
   - UI in components
   - API in services
   - Config in infrastructure

2. **Use service layer:**
   - Always call services from components
   - Never make direct API calls

3. **Type everything:**
   - Use TypeScript interfaces
   - Define request/response types
   - Leverage type inference

4. **Handle errors:**
   - Try-catch in components
   - Display user-friendly messages
   - Log errors for debugging

5. **Keep components small:**
   - Single responsibility
   - Extract reusable components
   - Use composition

### DON'Ts ❌

1. **Don't make API calls in components:**
   ```tsx
   // ❌ Bad
   useEffect(() => {
     axios.get('/products').then(setProducts);
   }, []);
   
   // ✅ Good
   useEffect(() => {
     ProductService.getProducts().then(setProducts);
   }, []);
   ```

2. **Don't put business logic in components:**
   ```tsx
   // ❌ Bad
   const discountedPrice = product.price * (1 - promo.discount / 100);
   
   // ✅ Good
   const discountedPrice = PromoService.calculateDiscount(product, promo);
   ```

3. **Don't use axios directly:**
   ```tsx
   // ❌ Bad
   axios.get('/products');
   
   // ✅ Good
   http.get(API_ENDPOINTS.PRODUCTS);
   ```

## Conclusion

This architecture provides:
- ✅ **Clear separation of concerns**
- ✅ **Easy to test and maintain**
- ✅ **Scalable for team growth**
- ✅ **Type-safe throughout**
- ✅ **Production-ready**

The result is a **professional**, **maintainable**, and **scalable** frontend application that follows industry best practices.
