import type { Metadata } from "next";
import "./globals.css";
import Footer from "./components/Footer";

export const metadata: Metadata = {
  title: { default: "RedCart: shop phones, laptops & more in Nigeria", template: "%s | RedCart" },
  description: "Shop phones, laptops, gaming, fashion and home essentials with nationwide delivery and buyer protection.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col font-sans">
        <div className="flex-1">{children}</div>
        <Footer />
      </body>
    </html>
  );
}
