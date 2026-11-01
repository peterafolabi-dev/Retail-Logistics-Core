import { ArrowRight, Laptop, Smartphone, Watch, Gamepad2, Shirt, Footprints } from "lucide-react";
import Link from "next/link";
import Header from "./components/Header";
import ProductCard from "./components/ProductCard";
import { listProducts } from "./lib/api";

// Render on request so a sleeping API never breaks the build; fetches are still cached for 60s.
export const dynamic = "force-dynamic";

const FEATURED_CATEGORIES = [
  { value: "Phones", label: "Phones", Icon: Smartphone },
  { value: "Laptops", label: "Laptops", Icon: Laptop },
  { value: "Gaming", label: "Gaming", Icon: Gamepad2 },
  { value: "Watches", label: "Watches", Icon: Watch },
  { value: "Sneakers", label: "Sneakers", Icon: Footprints },
  { value: "Fashion", label: "Fashion", Icon: Shirt },
];

export default async function HomePage() {
  const [deals, newest] = await Promise.all([
    listProducts({ on_sale: true, page_size: 4 }),
    listProducts({ sort: "newest", page_size: 8 }),
  ]);
  const counts = Object.fromEntries(newest.categories.map((c) => [c.value, c.count]));

  return (
    <>
      <Header />
      <main className="mx-auto max-w-7xl px-4">
        <section className="mt-6 grid overflow-hidden rounded-2xl bg-ink text-white md:grid-cols-[1.2fr_1fr]">
          <div className="p-8 md:p-12">
            <p className="text-sm font-semibold uppercase tracking-widest text-brand-500">Delivered across Nigeria</p>
            <h1 className="mt-3 text-4xl font-extrabold leading-tight tracking-tight md:text-5xl">
              The gadgets and gear you want, <span className="text-brand-500">paid for safely.</span>
            </h1>
            <p className="mt-4 max-w-md text-slate-300">
              {newest.count} products from phones to sneakers. Pay by card, transfer or USSD; your money is held until your order arrives.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link href="/shop" className="inline-flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-3 font-semibold hover:bg-brand-700">
                Shop all products <ArrowRight className="h-4 w-4" />
              </Link>
              {deals.count > 0 && (
                <Link href="#deals" className="rounded-lg border border-white/25 px-5 py-3 font-semibold hover:bg-white/10">
                  See today&apos;s deals
                </Link>
              )}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2 p-2 md:p-3">
            {newest.results.slice(0, 4).map((p) => (
              <Link key={p.id} href={`/shop/${p.id}`} className="relative aspect-square overflow-hidden rounded-xl bg-white/5">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={p.image} alt={p.name} className="h-full w-full object-cover opacity-90 transition hover:opacity-100" />
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-10" aria-labelledby="categories-heading">
          <h2 id="categories-heading" className="text-xl font-bold">Shop by category</h2>
          <div className="mt-4 grid grid-cols-3 gap-3 sm:grid-cols-6">
            {FEATURED_CATEGORIES.map(({ value, label, Icon }) => (
              <Link
                key={value}
                href={`/shop?category=${encodeURIComponent(value)}`}
                className="flex flex-col items-center gap-2 rounded-xl border border-zinc-200 bg-white px-3 py-5 text-center transition hover:border-brand-600 hover:text-brand-600"
              >
                <Icon className="h-7 w-7" strokeWidth={1.6} />
                <span className="text-sm font-semibold">{label}</span>
                {counts[value] ? <span className="text-xs text-ink-mute">{counts[value]} items</span> : null}
              </Link>
            ))}
          </div>
        </section>

        {deals.count > 0 && (
          <section id="deals" className="mt-10 scroll-mt-40" aria-labelledby="deals-heading">
            <div className="flex items-end justify-between">
              <h2 id="deals-heading" className="text-xl font-bold">Flash deals</h2>
              <Link href="/shop?deals=1" className="text-sm font-semibold text-brand-600 hover:underline">View all</Link>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-4 md:gap-4">
              {deals.results.map((p) => <ProductCard key={p.id} product={p} />)}
            </div>
          </section>
        )}

        <section className="mt-10" aria-labelledby="new-heading">
          <div className="flex items-end justify-between">
            <h2 id="new-heading" className="text-xl font-bold">New arrivals</h2>
            <Link href="/shop" className="text-sm font-semibold text-brand-600 hover:underline">View all</Link>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-4 md:gap-4">
            {newest.results.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>
      </main>
    </>
  );
}
