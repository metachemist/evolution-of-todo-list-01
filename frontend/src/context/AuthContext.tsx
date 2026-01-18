'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';
import apiClient from '@/lib/api';

interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUserProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const router = useRouter();

  useEffect(() => {
    // Check if token exists on initial load
    const token = Cookies.get('token');
    if (token) {
      fetchUserProfile();
    } else {
      setIsLoading(false);
    }
  }, []);

  const fetchUserProfile = async () => {
    // Don't call API if no token
    if (!Cookies.get('token')) return;

    try {
      setIsLoading(true);
      const response = await apiClient.get('/api/v1/auth/me');
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error: any) {
      console.error('Failed to fetch user profile:', error);
      // If 401 error, simply set user to null and isAuthenticated to false
      if (error.response?.status === 401) {
        setUser(null);
        setIsAuthenticated(false);
      } else {
        // Clear invalid token for other errors
        Cookies.remove('token');
        setIsAuthenticated(false);
        setUser(null);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await apiClient.post('/api/v1/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      // Store the token in cookies
      Cookies.set('token', response.data.access_token, {
        expires: 7, // 7 days
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
      });

      // Fetch user profile after successful login
      await fetchUserProfile();

      router.push('/dashboard');
      router.refresh();
    } catch (error: any) {
      throw error;
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    try {
      const response = await apiClient.post('/api/v1/auth/signup', {
        email,
        name,
        password,
      });

      // Store the token in cookies
      Cookies.set('token', response.data.access_token, {
        expires: 7, // 7 days
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
      });

      // Fetch user profile after successful signup
      await fetchUserProfile();

      router.push('/dashboard');
      router.refresh();
    } catch (error: any) {
      throw error;
    }
  };

  const logout = () => {
    // Remove token from cookies
    Cookies.remove('token');

    // Clear user state
    setUser(null);
    setIsAuthenticated(false);

    // Redirect to login
    router.push('/login');
    router.refresh();
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    signup,
    logout,
    fetchUserProfile,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}