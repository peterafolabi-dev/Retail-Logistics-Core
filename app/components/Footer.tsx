import { ShieldCheck, Truck, Undo2 } from "lucide-react";
import Link from "next/link";
import { storeLinks } from "../lib/api";

export default function Footer() {
  return (
    <footer className="mt-16 bg-ink text-slate-300">
      <div className="border-b border-white/10">
        <div className="mx-auto grid max-w-7xl gap-6 px-4 py-8 sm:grid-cols-3">
          {[
            [Truck, "Nationwide delivery", "2–5 business days across Nigeria"],
            [ShieldCheck, "Buyer protection", "Payment held until your order arrives"],
            [Undo2, "7-day returns", "Unused items in original packaging"],
          ].map(([Icon, title, copy]) => {
            const I = Icon as typeof Truck;
            return (
              <div key={title as string} className="flex gap-3">
                <I className="mt-0.5 h-5 w-5 shrink-0 text-brand-500" />
                <div>
                  <p className="font-semibold text-white">{title as string}</p>
                  <p className="text-sm text-slate-400">{copy as string}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <div className="mx-auto grid max-w-7xl gap-8 px-4 py-10 text-sm sm:grid-cols-2 md:grid-cols-4">
        <div>
          <p className="text-lg font-extrabold text-white">Red<span className="text-brand-500">Cart</span></p>
          <p className="mt-2 max-w-xs text-slate-400">Phones, laptops, fashion and more, delivered across Nigeria.</p>
        </div>
        <div className="flex flex-col gap-2">
          <p className="font-semibold text-white">Shop</p>
          <Link href="/shop" className="hover:text-white">All products</Link>
          <Link href="/shop?category=Phones" className="hover:text-white">Phones</Link>
          <Link href="/shop?category=Laptops" className="hover:text-white">Laptops</Link>
        </div>
        <div className="flex flex-col gap-2">
          <p className="font-semibold text-white">Account</p>
          <a href={storeLinks.account} className="hover:text-white">My orders</a>
          <a href={storeLinks.wishlist} className="hover:text-white">Wishlist</a>
          <a href={storeLinks.cart} className="hover:text-white">Cart</a>
        </div>
        <div className="flex flex-col gap-2">
          <p className="font-semibold text-white">Payments</p>
          <p className="text-slate-400">Card, bank transfer and USSD, processed securely by Paystack.</p>
        </div>
      </div>
      <p className="border-t border-white/10 py-5 text-center text-xs text-slate-500">© {new Date().getFullYear()} RedCart</p>
    </footer>
  );
}
