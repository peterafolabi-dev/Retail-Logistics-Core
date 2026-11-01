import Link from "next/link";
import Header from "./components/Header";

export default function NotFound() {
  return (
    <>
      <Header />
      <main className="mx-auto flex max-w-xl flex-col items-center px-4 py-24 text-center">
        <p className="text-sm font-bold uppercase tracking-widest text-brand-600">404</p>
        <h1 className="mt-2 text-3xl font-extrabold">We couldn&apos;t find that page</h1>
        <p className="mt-3 text-ink-mute">The product may have been removed, or the link is wrong.</p>
        <Link href="/shop" className="mt-6 rounded-lg bg-brand-600 px-5 py-3 font-semibold text-white hover:bg-brand-700">Browse products</Link>
      </main>
    </>
  );
}
