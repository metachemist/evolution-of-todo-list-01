'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { ThemeToggle } from '@/components/ThemeToggle';
import Cookies from 'js-cookie';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      // Call login from context which handles the API call and token storage
      await login(email, password);
    } catch (err: any) {
      // Handle different error response formats
      if (err.response?.data?.detail) {
        // Handle string error messages
        setError(typeof err.response.data.detail === 'string'
          ? err.response.data.detail
          : JSON.stringify(err.response.data.detail));
      } else if (Array.isArray(err.response?.data)) {
        // Handle Pydantic validation errors which come as arrays
        const validationErrors = err.response.data;
        const errorMessage = validationErrors.map((e: any) => e.msg || e.detail || 'Validation error').join(', ');
        setError(errorMessage || 'Validation error occurred');
      } else if (typeof err.response?.data === 'object') {
        // Handle other object responses by extracting message if possible
        const errorObj = err.response.data;
        if (errorObj.message) {
          setError(errorObj.message);
        } else if (errorObj.detail) {
          setError(Array.isArray(errorObj.detail)
            ? errorObj.detail.map((item: any) => item.msg || item.detail || 'Error').join(', ')
            : String(errorObj.detail));
        } else {
          setError('An error occurred during login');
        }
      } else {
        setError(err.response?.data || 'Login failed');
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background py-12 px-4 sm:px-6 lg:px-8">
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>
      <div className="flex-grow flex items-center justify-center">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-foreground">
              Sign in to your account
            </h2>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-md bg-red-50 p-4 dark:bg-red-950">
                <div className="text-sm text-red-700 dark:text-red-300">{error}</div>
              </div>
            )}
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-border placeholder-muted-foreground text-foreground rounded-t-md focus:outline-none focus:ring-accent focus:border-accent focus:z-10 sm:text-sm bg-background"
                  placeholder="Email address"
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-border placeholder-muted-foreground text-foreground rounded-b-md focus:outline-none focus:ring-accent focus:border-accent focus:z-10 sm:text-sm bg-background"
                  placeholder="Password"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-accent-foreground bg-accent hover:bg-accent/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent"
              >
                Sign in
              </button>
            </div>

            <div className="text-sm text-center">
              <a href="/signup" className="font-medium text-accent hover:text-accent-foreground">
                Don't have an account? Sign up
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}