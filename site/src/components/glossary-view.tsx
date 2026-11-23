"use client";

import { Search, X } from "lucide-react";
import { Fragment, useMemo, useState } from "react";
import { fold, slug } from "@/lib/search";

type Row = { en: string; uz: string; hint: string };

function Highlight({ text, needle }: { text: string; needle: string }) {
  if (!needle) return text;
  const folded = fold(text);
  const at = folded.indexOf(needle);
  if (at < 0 || folded.length !== text.length) return text;
  return (
    <Fragment>
      {text.slice(0, at)}
      <mark className="rounded bg-warn-bg px-0.5 text-ink">{text.slice(at, at + needle.length)}</mark>
      {text.slice(at + needle.length)}
    </Fragment>
  );
}

export function GlossaryView({ rows }: { rows: Row[] }) {
  const [query, setQuery] = useState("");
  const needle = fold(query);
  const filtered = useMemo(
    () => (needle ? rows.filter((row) => fold(`${row.en} ${row.uz} ${row.hint}`).includes(needle)) : rows),
    [needle, rows],
  );

  return (
    <article className="reading mx-auto max-w-3xl">
      <p className="text-sm font-bold tracking-wide text-brand">LUG&apos;AT</p>
      <h1 className="mt-1 font-serif text-[2.3rem] leading-tight text-heading">Atamalar</h1>
      <p className="prose-text mt-3">
        Shu so&apos;zlar butun kursda bir xil. Darsda yangi atama kerak bo&apos;lsa, avval shu ro&apos;yxatdan qidiring.
      </p>
      <div className="no-print relative mt-6">
        <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-ink-muted" aria-hidden />
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="slope, qiyalik, foiz…"
          aria-label="Atama qidirish"
          className="field h-11 pl-9"
        />
        {query && (
          <button
            type="button"
            onClick={() => setQuery("")}
            className="absolute top-1/2 right-2 inline-flex size-7 -translate-y-1/2 items-center justify-center rounded-md text-ink-muted hover:bg-hover"
            aria-label="Tozalash"
          >
            <X className="size-4" aria-hidden />
          </button>
        )}
      </div>
      <p className="mt-3 text-sm text-ink-muted" aria-live="polite">
        {filtered.length} ta atama
      </p>
      <div className="mt-3 overflow-hidden rounded-xl border border-line">
        <table className="w-full border-collapse text-[0.95rem]">
          <thead>
            <tr className="bg-selected text-left text-on-selected">
              <th className="px-3 py-2 font-semibold">English</th>
              <th className="px-3 py-2 font-semibold">O&apos;zbekcha</th>
              <th className="hidden px-3 py-2 font-semibold sm:table-cell">Eslatma</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => (
              <tr key={row.en} id={`t-${slug(row.en)}`} className="scroll-mt-24 bg-surface odd:bg-surface-2 target:bg-warn-bg">
                <td lang="en" className="border-t border-line px-3 py-2 align-top font-medium">
                  <Highlight text={row.en} needle={needle} />
                  <span className="mt-0.5 block text-sm font-normal text-ink-muted sm:hidden">{row.hint}</span>
                </td>
                <td lang="uz" className="border-t border-line px-3 py-2 align-top text-uz">
                  <Highlight text={row.uz} needle={needle} />
                </td>
                <td className="hidden border-t border-line px-3 py-2 align-top text-ink-muted sm:table-cell">{row.hint}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {filtered.length === 0 && (
        <p className="mt-6 rounded-xl border border-dashed border-line p-4 text-ink-muted">
          Bu so&apos;z lug&apos;atda yo&apos;q. Yozilishini tekshiring yoki inglizcha nomini yozing.
        </p>
      )}
    </article>
  );
}
