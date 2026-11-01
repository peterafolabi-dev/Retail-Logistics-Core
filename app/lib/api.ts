// Talks to the Django read-only catalog API (products/api_v1.py).
// Cart, checkout, payments and accounts stay on Django: the storefront links there.

export const STORE_URL = (process.env.REDCART_API_URL || "https://retail-logistics-core-t0xz.onrender.com").replace(/\/$/, "");

export type ProductSummary = {
  id: number;
  name: string;
  category: string;
  category_label: string;
  price: number;
  sale_price: number | null;
  sale_ends_at: string | null;
  discount_percentage: number;
  image: string;
  in_stock: boolean;
  low_stock: boolean;
  rating: number;
  review_count: number;
};

export type Category = { value: string; label: string; count: number };

export type ProductPage = {
  results: ProductSummary[];
  count: number;
  page: number;
  pages: number;
  categories: Category[];
};

export type Review = { rating: number; text: string; author: string; verified_purchase: boolean; created_at: string };

export type ProductDetail = ProductSummary & {
  description: string;
  images: string[];
  stock: number;
  reviews: Review[];
  related: ProductSummary[];
};

export type ListParams = { q?: string; category?: string; sort?: string; page?: number; page_size?: number; on_sale?: boolean };

export const SORT_OPTIONS = [
  { value: "newest", label: "Newest" },
  { value: "price_asc", label: "Price: low to high" },
  { value: "price_desc", label: "Price: high to low" },
  { value: "name", label: "Name A–Z" },
];

async function getJson<T>(path: string): Promise<T | null> {
  const response = await fetch(`${STORE_URL}${path}`, {
    next: { revalidate: 60 },
    headers: { Accept: "application/json" },
  });
  if (response.status === 404) return null;
  if (!response.ok) throw new Error(`RedCart API returned ${response.status} for ${path}`);
  return (await response.json()) as T;
}

export async function listProducts(params: ListParams = {}): Promise<ProductPage> {
  const search = new URLSearchParams();
  if (params.q) search.set("q", params.q);
  if (params.category) search.set("category", params.category);
  if (params.sort) search.set("sort", params.sort);
  if (params.page && params.page > 1) search.set("page", String(params.page));
  if (params.page_size) search.set("page_size", String(params.page_size));
  if (params.on_sale) search.set("on_sale", "1");
  const query = search.toString();
  const data = await getJson<ProductPage>(`/products/api/v1/products/${query ? `?${query}` : ""}`);
  return data ?? { results: [], count: 0, page: 1, pages: 1, categories: [] };
}

export function getProduct(id: number): Promise<ProductDetail | null> {
  return getJson<ProductDetail>(`/products/api/v1/products/${id}/`);
}

// Links into the Django app for everything that changes state.
export const storeLinks = {
  addToCart: (id: number) => `${STORE_URL}/products/add-to-cart/${id}/`,
  productOnStore: (id: number) => `${STORE_URL}/products/product/${id}/`,
  cart: `${STORE_URL}/products/cart/`,
  wishlist: `${STORE_URL}/products/wishlist/`,
  login: `${STORE_URL}/products/login/`,
  register: `${STORE_URL}/products/register/`,
  account: `${STORE_URL}/account/`,
};

export const money = (value: number) =>
  `₦${value.toLocaleString("en-NG", { maximumFractionDigits: 0 })}`;

export function shopHref(current: ListParams, change: Partial<ListParams>) {
  const next = { ...current, ...change };
  const search = new URLSearchParams();
  if (next.q) search.set("q", next.q);
  if (next.category) search.set("category", next.category);
  if (next.sort && next.sort !== "newest") search.set("sort", next.sort);
  if (next.on_sale) search.set("deals", "1");
  if (next.page && next.page > 1) search.set("page", String(next.page));
  const query = search.toString();
  return `/shop${query ? `?${query}` : ""}`;
}
