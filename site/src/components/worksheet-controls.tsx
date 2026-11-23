"use client";

import { Printer, Shuffle } from "lucide-react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { M } from "@/components/text";
import { useTeacherData } from "@/components/teacher-key";
import type { BankKey } from "@/lib/keys";

type Option = { code: string; label: string; unit: string };

export function WorksheetControls({ lessons }: { lessons: Option[] }) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();

  function set(changes: Record<string, string | null>) {
    const next = new URLSearchParams(params.toString());
    for (const [name, value] of Object.entries(changes)) {
      if (value === null || value === "") next.delete(name);
      else next.set(name, value);
    }
    router.replace(`${pathname}?${next.toString()}`, { scroll: false });
  }

  const units = Array.from(new Set(lessons.map((lesson) => lesson.unit)));
  const field = "h-9 rounded-lg border border-line bg-surface px-2 text-sm text-ink";

  return (
    <div className="no-print card mb-8 grid gap-3 p-4 sm:grid-cols-2 lg:grid-cols-4">
      <label className="text-xs font-semibold text-ink-muted sm:col-span-2">
        Dars
        <select className={`${field} mt-1 w-full`} value={params.get("dars") ?? "0.1"} onChange={(event) => set({ dars: event.target.value })}>
          {units.map((unit) => (
            <optgroup key={unit} label={unit}>
              {lessons
                .filter((lesson) => lesson.unit === unit)
                .map((lesson) => (
                  <option key={lesson.code} value={lesson.code}>
                    {lesson.code}. {lesson.label}
                  </option>
                ))}
            </optgroup>
          ))}
        </select>
      </label>
      <label className="text-xs font-semibold text-ink-muted">
        Daraja
        <select className={`${field} mt-1 w-full`} value={params.get("daraja") ?? "all"} onChange={(event) => set({ daraja: event.target.value === "all" ? null : event.target.value })}>
          <option value="all">Hammasi</option>
          <option value="oson">Oson</option>
          <option value="orta">O&apos;rta</option>
          <option value="sat">SAT</option>
        </select>
      </label>
      <label className="text-xs font-semibold text-ink-muted">
        Savollar soni
        <select className={`${field} mt-1 w-full`} value={params.get("soni") ?? "10"} onChange={(event) => set({ soni: event.target.value })}>
          {["5", "10", "15", "20", "30"].map((count) => (
            <option key={count} value={count}>
              {count} ta
            </option>
          ))}
        </select>
      </label>
      <label className="text-xs font-semibold text-ink-muted">
        Ish joyi
        <select className={`${field} mt-1 w-full`} value={params.get("joy") ?? "keng"} onChange={(event) => set({ joy: event.target.value })}>
          <option value="keng">Keng</option>
          <option value="ixcham">Ixcham</option>
        </select>
      </label>
      <div className="flex items-end gap-2 sm:col-span-2 lg:col-span-3">
        <button type="button" className="btn h-9" onClick={() => set({ variant: String(Math.floor(Math.random() * 9000) + 1000) })}>
          <Shuffle className="size-4" aria-hidden /> Yangi variant
        </button>
        {params.get("variant") && (
          <button type="button" className="btn h-9" onClick={() => set({ variant: null })}>
            Bank tartibi
          </button>
        )}
        <button type="button" className="btn-primary ml-auto h-9" onClick={() => window.print()}>
          <Printer className="size-4" aria-hidden /> Chop etish
        </button>
      </div>
    </div>
  );
}

/** The answer page, printed after the questions, only while the teacher key is open. */
export function WorksheetKey({ code, ids }: { code: string; ids: string[] }) {
  const keys = useTeacherData<{ bank: BankKey[] }>(`/api/keys?code=${encodeURIComponent(code)}`);
  if (keys.state === "off") {
    return (
      <p className="no-print mt-8 rounded-lg border border-dashed border-line p-4 text-sm text-ink-muted">
        Javoblar sahifasi kerak bo&apos;lsa, yuqoridagi <strong>Kalit</strong> tugmasini oching. U chop etishda alohida
        varaqqa tushadi.
      </p>
    );
  }
  if (!keys.data) return <p className="no-print mt-8 text-sm text-ink-muted">Kalit yuklanmoqda…</p>;
  const byId = new Map(keys.data.bank.map((row) => [row.id, row]));
  return (
    <section className="print-break mt-12 border-t border-line pt-6">
      <h2 className="font-serif text-xl text-heading">Javoblar · O&apos;qituvchi uchun</h2>
      <ol className="mt-4 grid gap-x-8 gap-y-2 text-sm sm:grid-cols-2">
        {ids.map((id, index) => {
          const row = byId.get(id);
          return (
            <li key={id} className="avoid-break">
              <span className="font-semibold text-heading">{index + 1}.</span> <M>{row?.answer ?? "—"}</M>
              <span className="ml-1 text-xs text-ink-muted">#{id}</span>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
