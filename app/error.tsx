"use client";

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <main className="mx-auto flex max-w-xl flex-col items-center px-4 py-24 text-center">
      <h1 className="text-3xl font-extrabold">The store is waking up</h1>
      <p className="mt-3 text-slate-500">
        We couldn&apos;t reach the RedCart catalog just now. It can take up to a minute to start after a quiet spell.
      </p>
      <button onClick={reset} className="mt-6 rounded-lg bg-red-600 px-5 py-3 font-semibold text-white hover:bg-red-700">Try again</button>
    </main>
  );
}
