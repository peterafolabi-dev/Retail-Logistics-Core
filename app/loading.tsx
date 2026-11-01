export default function Loading() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-10" aria-busy="true" aria-label="Loading products">
      <div className="h-8 w-56 animate-pulse rounded bg-zinc-200" />
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        {Array.from({ length: 8 }, (_, i) => (
          <div key={i} className="overflow-hidden rounded-xl border border-zinc-200 bg-white">
            <div className="aspect-square animate-pulse bg-zinc-100" />
            <div className="space-y-2 p-4"><div className="h-3 w-1/3 rounded bg-zinc-200" /><div className="h-4 w-4/5 rounded bg-zinc-200" /><div className="h-9 rounded bg-zinc-100" /></div>
          </div>
        ))}
      </div>
    </main>
  );
}
