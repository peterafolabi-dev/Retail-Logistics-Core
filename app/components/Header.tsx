import { Heart, Search, ShoppingCart, User } from "lucide-react";
import Link from "next/link";
import { storeLinks } from "../lib/api";

const CATEGORY_LINKS = [
  ["Phones", "Phones"],
  ["Laptops", "Laptops"],
  ["Electronics", "Electronics"],
  ["Gaming", "Gaming"],
  ["Watches", "Watches"],
  ["Sneakers", "Sneakers"],
  ["Fashion", "Fashion"],
  ["Accessories", "Accessories"],
  ["Home Appliances", "Appliances"],
  ["Home", "Home & Kitchen"],
  ["Fitness", "Fitness"],
];

export default function Header({ query = "", activeCategory = "" }: { query?: string; activeCategory?: string }) {
  return (
    <header className="sticky top-0 z-40 bg-white shadow-[0_1px_0_#e4e4e7]">
      <div className="bg-ink text-[13px] text-slate-200">
        <div className="mx-auto flex max-w-7xl items-center justify-center gap-6 px-4 py-2">
          <span>Free delivery across Nigeria in 2–5 business days</span>
          <span className="hidden sm:inline">Buyer protection on every order</span>
        </div>
      </div>

      <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3 md:gap-8">
        <Link href="/" className="flex shrink-0 items-center gap-2" aria-label="RedCart home">
          <span className="grid h-9 w-9 place-items-center rounded-lg bg-brand-600 text-white">
            <ShoppingCart className="h-5 w-5" strokeWidth={2.4} />
          </span>
          <span className="text-xl font-extrabold tracking-tight">
            Red<span className="text-brand-600">Cart</span>
          </span>
        </Link>

        <form action="/shop" method="get" role="search" className="hidden flex-1 md:flex">
          <label htmlFor="site-search" className="sr-only">Search products</label>
          <input
            id="site-search"
            name="q"
            defaultValue={query}
            placeholder="Search products, brands and categories"
            className="min-w-0 flex-1 rounded-l-lg border-2 border-r-0 border-brand-600 px-4 py-2.5 text-[15px] outline-none placeholder:text-slate-400 focus:bg-brand-50/40"
          />
          <button className="flex items-center gap-2 rounded-r-lg bg-brand-600 px-5 font-semibold text-white transition hover:bg-brand-700">
            <Search className="h-4 w-4" /> Search
          </button>
        </form>

        <nav className="ml-auto flex items-center gap-1 text-[15px] text-ink-soft md:gap-3" aria-label="Account">
          <a href={storeLinks.login} className="flex items-center gap-1.5 rounded-lg px-2 py-2 hover:bg-surface hover:text-ink">
            <User className="h-5 w-5" /> <span className="hidden lg:inline">Sign in</span>
          </a>
          <a href={storeLinks.wishlist} className="flex items-center gap-1.5 rounded-lg px-2 py-2 hover:bg-surface hover:text-ink">
            <Heart className="h-5 w-5" /> <span className="hidden lg:inline">Wishlist</span>
          </a>
          <a href={storeLinks.cart} className="flex items-center gap-1.5 rounded-lg px-2 py-2 hover:bg-surface hover:text-ink">
            <ShoppingCart className="h-5 w-5" /> <span className="hidden lg:inline">Cart</span>
          </a>
        </nav>
      </div>

      <form action="/shop" method="get" role="search" className="flex px-4 pb-3 md:hidden">
        <input
          name="q"
          defaultValue={query}
          aria-label="Search products"
          placeholder="Search RedCart"
          className="min-w-0 flex-1 rounded-l-lg border-2 border-r-0 border-brand-600 px-3 py-2 text-[15px] outline-none"
        />
        <button className="rounded-r-lg bg-brand-600 px-4 text-white" aria-label="Search">
          <Search className="h-4 w-4" />
        </button>
      </form>

      <div className="border-t border-zinc-200">
        <nav className="scrollbar-none mx-auto flex max-w-7xl gap-1 overflow-x-auto px-4 text-[15px]" aria-label="Categories">
          <Link
            href="/shop"
            className={`shrink-0 border-b-2 px-3 py-3 ${!activeCategory ? "border-brand-600 font-medium text-brand-600" : "border-transparent text-ink-soft hover:text-ink"}`}
          >
            All products
          </Link>
          {CATEGORY_LINKS.map(([value, label]) => (
            <Link
              key={value}
              href={`/shop?category=${encodeURIComponent(value)}`}
              className={`shrink-0 border-b-2 px-3 py-3 ${activeCategory === value ? "border-brand-600 font-medium text-brand-600" : "border-transparent text-ink-soft hover:text-ink"}`}
            >
              {label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
