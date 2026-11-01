import { ChevronLeft, ChevronRight, SearchX } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import Header from "../components/Header";
import ProductCard from "../components/ProductCard";
import { listProducts, shopHref, SORT_OPTIONS, type ListParams } from "../lib/api";

type SearchParams = Promise<Record<string, string | string[] | undefined>>;

const one = (value: string | string[] | undefined) => (Array.isArray(value) ? value[0] : value) ?? "";

async function readParams(searchParams: SearchParams): Promise<ListParams> {
  const sp = await searchParams;
  return {
    q: one(sp.q).trim().slice(0, 100),
    category: one(sp.category),
    sort: one(sp.sort) || "newest",
    page: Math.max(1, Number.parseInt(one(sp.page), 10) || 1),
    on_sale: one(sp.deals) === "1",
  };
}

export async function generateMetadata({ searchParams }: { searchParams: SearchParams }): Promise<Metadata> {
  const params = await readParams(searchParams);
  if (params.q) return { title: `Results for “${params.q}”` };
  if (params.on_sale) return { title: "Flash deals" };
  return { title: params.category || "Shop all products" };
}

export default async function ShopPage({ searchParams }: { searchParams: SearchParams }) {
  const params = await readParams(searchParams);
  const data = await listProducts({ ...params, page_size: 24 });
  const activeLabel = data.categories.find((c) => c.value === params.category)?.label;
  const heading = params.q ? `Results for “${params.q}”` : params.on_sale ? "Flash deals" : activeLabel || "All products";

  return (
    <>
      <Header query={params.q} activeCategory={params.category} />
      <main className="mx-auto max-w-7xl px-4">
        <nav className="py-4 text-sm text-ink-mute" aria-label="Breadcrumb">
          <Link href="/" className="hover:text-ink">Home</Link> <span className="mx-1">/</span>
          <span className="text-ink">Shop</span>
        </nav>

        <div className="grid gap-6 lg:grid-cols-[240px_1fr]">
          <aside className="h-fit rounded-xl border border-zinc-200 bg-white p-4 lg:sticky lg:top-48">
            <p className="px-2 text-xs font-bold uppercase tracking-widest text-ink-mute">Category</p>
            <ul className="mt-2 flex gap-1 overflow-x-auto lg:flex-col">
              <li>
                <Link
                  href={shopHref(params, { category: "", page: 1 })}
                  className={`flex justify-between whitespace-nowrap rounded-lg px-3 py-2 text-[15px] ${!params.category ? "bg-brand-50 font-semibold text-brand-600" : "hover:bg-surface"}`}
                >
                  All categories
                </Link>
              </li>
              {data.categories.map((c) => (
                <li key={c.value}>
                  <Link
                    href={shopHref(params, { category: c.value, page: 1 })}
                    className={`flex justify-between gap-4 whitespace-nowrap rounded-lg px-3 py-2 text-[15px] ${params.category === c.value ? "bg-brand-50 font-semibold text-brand-600" : "hover:bg-surface"}`}
                  >
                    {c.label} <span className="text-ink-mute">{c.count}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </aside>

          <section aria-labelledby="results-heading">
            <div className="flex flex-wrap items-end justify-between gap-3">
              <div>
                <h1 id="results-heading" className="text-2xl font-bold tracking-tight">{heading}</h1>
                <p className="mt-1 text-sm text-ink-mute">
                  {data.count} item{data.count === 1 ? "" : "s"}
                  {data.pages > 1 && ` · Page ${data.page} of ${data.pages}`}
                </p>
              </div>
              <form action="/shop" method="get" className="flex items-center gap-2 text-sm">
                {params.q && <input type="hidden" name="q" value={params.q} />}
                {params.category && <input type="hidden" name="category" value={params.category} />}
                {params.on_sale && <input type="hidden" name="deals" value="1" />}
                <label htmlFor="sort" className="text-ink-mute">Sort by</label>
                <select id="sort" name="sort" defaultValue={params.sort} className="rounded-lg border border-zinc-300 bg-white px-3 py-2">
                  {SORT_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                </select>
                <button className="rounded-lg bg-ink px-3 py-2 font-semibold text-white">Apply</button>
              </form>
            </div>

            {data.results.length === 0 ? (
              <div className="mt-6 flex flex-col items-center rounded-xl border border-dashed border-zinc-300 bg-white px-6 py-16 text-center">
                <SearchX className="h-10 w-10 text-ink-mute" />
                <p className="mt-3 text-lg font-semibold">No products match that search</p>
                <p className="mt-1 text-ink-mute">Try a shorter search, or browse a category.</p>
                <Link href="/shop" className="mt-5 rounded-lg bg-brand-600 px-5 py-2.5 font-semibold text-white hover:bg-brand-700">
                  Browse all products
                </Link>
              </div>
            ) : (
              <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-3 md:gap-4 xl:grid-cols-4">
                {data.results.map((p) => <ProductCard key={p.id} product={p} />)}
              </div>
            )}

            {data.pages > 1 && (
              <nav className="mt-8 flex items-center justify-center gap-2" aria-label="Pagination">
                {data.page > 1 ? (
                  <Link href={shopHref(params, { page: data.page - 1 })} className="flex items-center gap-1 rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm font-semibold hover:border-ink">
                    <ChevronLeft className="h-4 w-4" /> Previous
                  </Link>
                ) : null}
                {Array.from({ length: data.pages }, (_, i) => i + 1).map((n) => (
                  <Link
                    key={n}
                    href={shopHref(params, { page: n })}
                    aria-current={n === data.page ? "page" : undefined}
                    className={`grid h-9 min-w-9 place-items-center rounded-lg px-2 text-sm font-semibold ${n === data.page ? "bg-brand-600 text-white" : "border border-zinc-300 bg-white hover:border-ink"}`}
                  >
                    {n}
                  </Link>
                ))}
                {data.page < data.pages ? (
                  <Link href={shopHref(params, { page: data.page + 1 })} className="flex items-center gap-1 rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm font-semibold hover:border-ink">
                    Next <ChevronRight className="h-4 w-4" />
                  </Link>
                ) : null}
              </nav>
            )}
          </section>
        </div>
      </main>
    </>
  );
}
