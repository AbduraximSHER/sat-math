import { guide } from "@/lib/guide";

export const metadata = { title: "Formulalar — SAT Math" };

export default function FormulasPage() {
  const [onSheet, memorize] = guide.formulaTables;
  return (
    <article>
      <h1 className="font-serif text-4xl text-[var(--navy)]">Formula varaqasi</h1>
      <p className="mt-3 text-[16.5px] leading-relaxed">
        Imtihon yuza, hajm, aylana va maxsus uchburchaklar faktlarini beradi. Qiyalik, foiz o&apos;zgarishi va
        funksiya yozuvi varaqada yo&apos;q. Ular yodda turadi.
      </p>
      <FormulaTable title="Varaqada bor" table={onSheet} />
      <FormulaTable title="Yodda turishi kerak" table={memorize} />
    </article>
  );
}

function FormulaTable({
  title,
  table,
}: {
  title: string;
  table: { headers: string[]; rows: string[][] };
}) {
  return (
    <section className="mt-8">
      <h2 className="font-serif text-2xl text-[var(--navy)]">{title}</h2>
      <div className="mt-3 overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="bg-[var(--navy)] text-left text-[#f7f4ec]">
              {table.headers.map((header) => (
                <th key={header} className="px-3 py-2 font-medium">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.rows.map((row) => (
              <tr key={row.join("|")} className="odd:bg-white even:bg-[#f7f4ec]">
                {row.map((cell) => (
                  <td key={cell} className="border-t border-[#e4ddd0] px-3 py-2">
                    {cell}
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
