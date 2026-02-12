/**
 * Main Application Component
 * 
 * This is the root component that sets up:
 * - Authentication state initialization
 * - Routing configuration
 * - Global providers
 * 
 * STATE FLOW IN THE APP:
 * 1. App mounts
 * 2. useEffect initializes auth state from localStorage
 * 3. Auth state is stored in Zustand (useAuthStore)
 * 4. Components access auth state via useAuthStore hook
 * 5. Protected routes check auth state to allow/deny access
 * 
 * WHY THIS ARCHITECTURE:
 * - Centralized auth initialization
 * - Single source of truth (Zustand store)
 * - Components don't manage auth logic
 * - Easy to test and maintain
 */

import { useEffect } from 'react';
import { AppRoutes } from './routes';
import { useAuthStore } from './store/auth.store';

function App() {
  const initializeAuth = useAuthStore((state) => state.initializeAuth);

  // Initialize auth state on app mount
  // This restores the user session from localStorage
  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return <AppRoutes />;
}

export default App;
