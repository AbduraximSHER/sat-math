"use client";

import { useMemo, useState } from "react";

export function GlossaryView({ rows }: { rows: { en: string; uz: string; hint: string }[] }) {
  const [query, setQuery] = useState("");
  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) return rows;
    return rows.filter((row) =>
      `${row.en} ${row.uz} ${row.hint}`.toLowerCase().includes(needle),
    );
  }, [query, rows]);

  return (
    <article>
      <h1 className="font-serif text-4xl text-[var(--navy)]">Atamalar</h1>
      <p className="mt-3 text-[16.5px] leading-relaxed">
        Shu so&apos;zlar butun kursda bir xil. Darsda yangi atama kerak bo&apos;lsa, avval shu ro&apos;yxatdan qidiring.
      </p>
      <label className="mt-5 block text-sm font-medium text-[var(--navy)]">
        Qidirish
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="slope, qiyalik, foiz..."
          className="mt-1 w-full rounded-lg border border-[#e4ddd0] bg-white px-3 py-2 text-base"
        />
      </label>
      <p className="mt-3 text-sm text-[#5c6b73]">{filtered.length} ta atama</p>
      <div className="mt-4 overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="bg-[var(--navy)] text-left text-[#f7f4ec]">
              <th className="px-3 py-2">English</th>
              <th className="px-3 py-2">O&apos;zbekcha</th>
              <th className="px-3 py-2">Eslatma</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => (
              <tr key={row.en} className="odd:bg-white even:bg-[#f7f4ec]">
                <td className="border-t border-[#e4ddd0] px-3 py-2">{row.en}</td>
                <td className="border-t border-[#e4ddd0] px-3 py-2 text-[var(--teal)]">{row.uz}</td>
                <td className="border-t border-[#e4ddd0] px-3 py-2 text-[#5c6b73]">{row.hint}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {filtered.length === 0 && (
        <p className="mt-6 rounded-lg border border-dashed border-[#e4ddd0] p-4">
          Bu so&apos;z lug&apos;atda yo&apos;q. Yozilishini tekshiring yoki inglizcha nomini yozing.
        </p>
      )}
    </article>
  );
}
