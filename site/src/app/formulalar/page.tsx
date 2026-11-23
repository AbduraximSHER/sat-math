import type { Metadata } from "next";
import { M } from "@/components/text";
import { guide } from "@/lib/guide";

export const metadata: Metadata = {
  title: "Formulalar",
  description: "Imtihon beradigan formulalar va yodda turishi kerak bo'lganlari: yuza, hajm, aylana, qiyalik, foiz o'zgarishi.",
  alternates: { canonical: "/formulalar" },
};

export default function FormulasPage() {
  const [onSheet, memorize] = guide.formulaTables;
  return (
    <article className="reading mx-auto max-w-3xl">
      <p className="text-sm font-bold tracking-wide text-brand">MA&apos;LUMOTNOMA</p>
      <h1 className="mt-1 font-serif text-[2.3rem] leading-tight text-heading">Formula varaqasi</h1>
      <p className="prose-text mt-3">
        Imtihon yuza, hajm, aylana va maxsus uchburchaklar faktlarini beradi. Qiyalik, foiz o&apos;zgarishi va funksiya
        yozuvi varaqada yo&apos;q. Ular yodda turadi.
      </p>
      <FormulaTable title="Varaqada bor" note="Imtihonda ekranda ochiladi." table={onSheet} />
      <FormulaTable title="Yodda turishi kerak" note="Varaqda yo'q — sinfda yodlatiladi." table={memorize} />
    </article>
  );
}

function FormulaTable({ title, note, table }: { title: string; note: string; table: { headers: string[]; rows: string[][] } }) {
  return (
    <section className="avoid-break mt-10">
      <h2 className="font-serif text-2xl text-heading">{title}</h2>
      <p className="mt-1 text-sm text-ink-muted">{note}</p>
      <div className="mt-3 overflow-x-auto rounded-xl border border-line">
        <table className="w-full border-collapse text-[0.95rem]">
          <thead>
            <tr className="bg-selected text-left text-on-selected">
              {table.headers.map((header) => (
                <th key={header} className="px-3 py-2 font-semibold">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.rows.map((row) => (
              <tr key={row.join("|")} className="bg-surface odd:bg-surface-2">
                {row.map((cell, index) => (
                  <td key={index} className={`border-t border-line px-3 py-2 align-top ${index === 1 ? "font-serif text-heading" : ""}`}>
                    <M>{cell}</M>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
