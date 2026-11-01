import { BadgeCheck, ShieldCheck, Truck, Undo2 } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Header from "../../components/Header";
import ProductCard from "../../components/ProductCard";
import Stars from "../../components/Stars";
import { getProduct, money, storeLinks } from "../../lib/api";
import Gallery from "./Gallery";

type Params = Promise<{ id: string }>;

async function load(params: Params) {
  const { id } = await params;
  const numeric = Number.parseInt(id, 10);
  if (!Number.isFinite(numeric) || String(numeric) !== id) return null;
  return getProduct(numeric);
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const product = await load(params);
  if (!product) return { title: "Product not found" };
  return {
    title: product.name,
    description: product.description.slice(0, 160) || `Buy ${product.name} on RedCart.`,
    openGraph: { images: [product.image] },
  };
}

export default async function ProductPage({ params }: { params: Params }) {
  const product = await load(params);
  if (!product) notFound();

  const onSale = product.sale_price !== null;
  const price = onSale ? product.sale_price! : product.price;
  const saleEnds = product.sale_ends_at
    ? new Date(product.sale_ends_at).toLocaleDateString("en-NG", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })
    : null;

  return (
    <>
      <Header activeCategory={product.category} />
      <main className="mx-auto max-w-7xl px-4">
        <nav className="py-4 text-sm text-ink-mute" aria-label="Breadcrumb">
          <Link href="/" className="hover:text-ink">Home</Link> <span className="mx-1">/</span>
          <Link href={`/shop?category=${encodeURIComponent(product.category)}`} className="hover:text-ink">{product.category_label}</Link>
          <span className="mx-1">/</span> <span className="text-ink">{product.name}</span>
        </nav>

        <div className="grid gap-8 lg:grid-cols-2">
          <Gallery images={product.images} name={product.name} />

          <section className="rounded-2xl border border-zinc-200 bg-white p-6 md:p-8">
            <p className="text-sm font-medium uppercase tracking-wider text-ink-mute">{product.category_label}</p>
            <h1 className="mt-2 text-3xl font-extrabold tracking-tight">{product.name}</h1>
            {product.review_count > 0 ? (
              <Stars rating={product.rating} count={product.review_count} className="mt-2" />
            ) : (
              <p className="mt-2 text-sm text-ink-mute">No reviews yet</p>
            )}

            <div className="mt-6 flex flex-wrap items-baseline gap-3">
              <span className="text-3xl font-bold">{money(price)}</span>
              {onSale && (
                <>
                  <span className="text-lg text-ink-mute line-through">{money(product.price)}</span>
                  <span className="rounded-md bg-brand-50 px-2 py-1 text-sm font-bold text-brand-600">Save {product.discount_percentage}%</span>
                </>
              )}
            </div>
            {saleEnds && <p className="mt-1 text-sm font-medium text-brand-600">Deal ends {saleEnds}</p>}

            <p className={`mt-4 text-sm font-semibold ${!product.in_stock ? "text-ink-mute" : product.low_stock ? "text-amber-700" : "text-emerald-700"}`}>
              {!product.in_stock ? "Out of stock" : product.low_stock ? `Only ${product.stock} left in stock` : "In stock, ready to ship"}
            </p>

            {product.in_stock ? (
              <a href={storeLinks.addToCart(product.id)} className="mt-5 block rounded-xl bg-brand-600 py-4 text-center text-lg font-semibold text-white transition hover:bg-brand-700">
                Add to cart
              </a>
            ) : (
              <span className="mt-5 block rounded-xl bg-zinc-100 py-4 text-center text-lg font-semibold text-ink-mute">Currently unavailable</span>
            )}
            <p className="mt-2 text-center text-xs text-ink-mute">You&apos;ll sign in to RedCart to finish checkout securely.</p>

            <ul className="mt-6 grid gap-3 border-t border-zinc-200 pt-6 text-sm">
              <li className="flex gap-3"><Truck className="h-5 w-5 shrink-0 text-brand-600" /> Delivery in 2–5 business days across Nigeria</li>
              <li className="flex gap-3"><ShieldCheck className="h-5 w-5 shrink-0 text-brand-600" /> Buyer protection: payment held until delivery</li>
              <li className="flex gap-3"><Undo2 className="h-5 w-5 shrink-0 text-brand-600" /> Return unused items within 7 days</li>
            </ul>

            {product.description && (
              <div className="mt-6 border-t border-zinc-200 pt-6">
                <h2 className="font-bold">About this product</h2>
                <p className="mt-2 whitespace-pre-line leading-7 text-ink-soft">{product.description}</p>
              </div>
            )}
          </section>
        </div>

        {product.reviews.length > 0 && (
          <section className="mt-10" aria-labelledby="reviews-heading">
            <h2 id="reviews-heading" className="text-xl font-bold">Customer reviews</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {product.reviews.map((r, i) => (
                <article key={i} className="rounded-xl border border-zinc-200 bg-white p-5">
                  <div className="flex items-center justify-between gap-3">
                    <Stars rating={r.rating} />
                    <time className="text-xs text-ink-mute" dateTime={r.created_at}>
                      {new Date(r.created_at).toLocaleDateString("en-NG", { day: "numeric", month: "short", year: "numeric" })}
                    </time>
                  </div>
                  {r.text && <p className="mt-3 leading-6 text-ink-soft">{r.text}</p>}
                  <p className="mt-3 flex items-center gap-1.5 text-sm font-semibold">
                    {r.author}
                    {r.verified_purchase && <span className="flex items-center gap-1 text-xs font-medium text-emerald-700"><BadgeCheck className="h-4 w-4" /> Verified purchase</span>}
                  </p>
                </article>
              ))}
            </div>
          </section>
        )}

        {product.related.length > 0 && (
          <section className="mt-10" aria-labelledby="related-heading">
            <h2 id="related-heading" className="text-xl font-bold">More in {product.category_label}</h2>
            <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-4 md:gap-4">
              {product.related.map((p) => <ProductCard key={p.id} product={p} />)}
            </div>
          </section>
        )}
      </main>
    </>
  );
}
