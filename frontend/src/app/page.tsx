'use client';

import Link from 'next/link';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

  // Optional: Auto-redirect to login after a delay
  // useEffect(() => {
  //   const timer = setTimeout(() => {
  //     router.push('/login');
  //   }, 3000); // Redirect after 3 seconds
  //   return () => clearTimeout(timer);
  // }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8 bg-background p-8 rounded-xl shadow-lg border border-border">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-foreground mb-4">
            Welcome to Todo Evolution
          </h1>
          <p className="text-lg text-muted-foreground mb-8">
            Manage your tasks efficiently with our intuitive platform
          </p>
        </div>

        <div className="flex flex-col gap-4">
          <Link
            href="/login"
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-accent-foreground bg-accent hover:bg-accent/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent transition-colors duration-200"
          >
            Sign In
          </Link>

          <Link
            href="/signup"
            className="w-full flex justify-center py-3 px-4 border border-border rounded-md shadow-sm text-sm font-medium text-foreground bg-background hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent transition-colors duration-200"
          >
            Create Account
          </Link>
        </div>

        <div className="mt-6 text-center text-sm text-muted-foreground">
          <p>By signing up, you agree to our Terms and Privacy Policy</p>
        </div>
      </div>
    </div>
  );
}