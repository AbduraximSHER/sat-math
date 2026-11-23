import { Search } from "lucide-react";
import Link from "next/link";

export default function NotFound() {
  return (
    <article className="reading mx-auto max-w-2xl py-10 text-center">
      <p className="font-serif text-7xl text-heading">404</p>
      <h1 className="mt-4 font-serif text-3xl text-heading">Bu sahifa yo&apos;q</h1>
      <p className="prose-text mt-3 text-ink-muted">
        Manzil noto&apos;g&apos;ri yozilgan yoki dars hali kitobga kirmagan. Darsni ro&apos;yxatdan yoki qidiruvdan toping.
      </p>
      <div className="mt-6 flex flex-wrap justify-center gap-3">
        <Link href="/" className="btn-primary h-10 px-4">
          Bosh sahifa
        </Link>
        <Link href="/dars/0.1" className="btn h-10 px-4">
          <Search className="size-4" aria-hidden /> Birinchi dars
        </Link>
      </div>
    </article>
  );
}
