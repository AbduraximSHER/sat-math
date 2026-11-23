"use client";

import { RotateCcw } from "lucide-react";
import Link from "next/link";

export default function ErrorPage({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <article className="reading mx-auto max-w-2xl py-10 text-center">
      <h1 className="font-serif text-3xl text-heading">Nimadir buzildi</h1>
      <p className="prose-text mt-3 text-ink-muted">
        Sahifani ochishda xato bo&apos;ldi. Internet aloqasini tekshirib, qayta urinib ko&apos;ring.
      </p>
      <div className="mt-6 flex flex-wrap justify-center gap-3">
        <button type="button" onClick={reset} className="btn-primary h-10 px-4">
          <RotateCcw className="size-4" aria-hidden /> Qayta urinish
        </button>
        <Link href="/" className="btn h-10 px-4">
          Bosh sahifa
        </Link>
      </div>
    </article>
  );
}
