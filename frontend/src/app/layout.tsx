// frontend/src/app/layout.tsx
import type { Metadata } from "next";
// import "./globals.css"; // Uncomment this if you have a globals.css file

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
        {children}
      </body>
    </html>
  );
}