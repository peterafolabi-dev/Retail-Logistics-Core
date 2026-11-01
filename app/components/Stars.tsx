import { Star } from "lucide-react";

export default function Stars({ rating, count, className = "" }: { rating: number; count?: number; className?: string }) {
  const rounded = Math.round(rating);
  return (
    <div className={`flex items-center gap-1 text-sm ${className}`} aria-label={`Rated ${rating} out of 5`}>
      <span className="flex">
        {[1, 2, 3, 4, 5].map((i) => (
          <Star key={i} className={`h-4 w-4 ${i <= rounded ? "fill-amber-400 text-amber-400" : "text-zinc-300"}`} />
        ))}
      </span>
      {count !== undefined && <span className="text-ink-mute">({count})</span>}
    </div>
  );
}
