import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sarwar AI",
  description: "One interface for multiple AI models. Premium Apple-inspired minimalist design.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen selection:bg-primary/20 bg-background text-foreground">
        {children}
      </body>
    </html>
  );
}
