// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";
import { Providers } from "@/components/Providers";
// import { CherryBlossom } from "@/components/CherryBlossom";

export const metadata: Metadata = {
  title: "Todo Evolution",
  description: "Task Management App",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    // 👇 This prop fixes the extension error
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>
          <AuthProvider>
            {children}
          </AuthProvider>
        </Providers>
      </body>
    </html>
  );
}