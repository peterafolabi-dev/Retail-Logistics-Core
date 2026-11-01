import Link from "next/link";
import { money, storeLinks, type ProductSummary } from "../lib/api";
import Stars from "./Stars";

export default function ProductCard({ product }: { product: ProductSummary }) {
  const onSale = product.sale_price !== null;
  return (
    <article className="group flex flex-col overflow-hidden rounded-xl border border-zinc-200 bg-white transition hover:shadow-card">
      <Link href={`/shop/${product.id}`} className="relative block aspect-square overflow-hidden bg-zinc-100">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={product.image}
          alt={product.name}
          loading="lazy"
          className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
        />
        {onSale && (
          <span className="absolute left-3 top-3 rounded-md bg-brand-600 px-2 py-1 text-xs font-bold text-white">
            −{product.discount_percentage}%
          </span>
        )}
        {!product.in_stock && (
          <span className="absolute inset-x-0 bottom-0 bg-ink/80 py-1.5 text-center text-xs font-semibold uppercase tracking-wide text-white">
            Out of stock
          </span>
        )}
      </Link>

      <div className="flex flex-1 flex-col p-4">
        <p className="text-xs font-medium uppercase tracking-wider text-ink-mute">{product.category_label}</p>
        <h3 className="mt-1 line-clamp-2 min-h-[2.75rem] font-semibold leading-snug text-ink">
          <Link href={`/shop/${product.id}`} className="hover:text-brand-600">{product.name}</Link>
        </h3>
        {product.review_count > 0 && <Stars rating={product.rating} count={product.review_count} className="mt-1.5" />}

        <div className="mt-auto pt-3">
          <div className="flex items-baseline gap-2">
            <span className="text-lg font-bold text-ink">{money(onSale ? product.sale_price! : product.price)}</span>
            {onSale && <span className="text-sm text-ink-mute line-through">{money(product.price)}</span>}
          </div>
          {product.low_stock && product.in_stock && <p className="mt-1 text-xs font-medium text-amber-700">Only a few left</p>}
          {product.in_stock ? (
            <a
              href={storeLinks.addToCart(product.id)}
              className="mt-3 block rounded-lg bg-brand-600 py-2.5 text-center text-sm font-semibold text-white transition hover:bg-brand-700"
            >
              Add to cart
            </a>
          ) : (
            <span className="mt-3 block rounded-lg bg-zinc-100 py-2.5 text-center text-sm font-semibold text-ink-mute">
              Unavailable
            </span>
          )}
        </div>
      </div>
    </article>
  );
}
