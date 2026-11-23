import type { Metadata } from "next";
import { Suspense } from "react";
import { M } from "@/components/text";
import { WorksheetControls, WorksheetKey } from "@/components/worksheet-controls";
import { allLessons, findLesson } from "@/lib/guide";

export const metadata: Metadata = {
  title: "Mashq varag'i",
  description: "Har darsning 100 ta bank savolidan chop etiladigan mashq varag'i: daraja, son va variant tanlanadi.",
  alternates: { canonical: "/varaq" },
};

type Search = Promise<Record<string, string | string[] | undefined>>;

/** Same seed, same order: a printed variant can be reproduced from its URL. */
function shuffle<T>(items: T[], seed: number): T[] {
  let state = seed >>> 0;
  const random = () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const out = [...items];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

const LEVEL_LABEL: Record<string, string> = { oson: "Oson", orta: "O'rta", sat: "SAT" };

export default async function WorksheetPage({ searchParams }: { searchParams: Search }) {
  const params = await searchParams;
  const one = (name: string) => (Array.isArray(params[name]) ? params[name]?.[0] : params[name]) as string | undefined;
  const found = findLesson(one("dars") ?? "0.1") ?? findLesson("0.1")!;
  const { lesson, unit } = found;
  const level = ["oson", "orta", "sat"].includes(one("daraja") ?? "") ? one("daraja")! : "all";
  const count = Math.min(30, Math.max(5, Number(one("soni")) || 10));
  const variant = Number(one("variant")) || 0;
  const compact = one("joy") === "ixcham";

  const pool = lesson.bank.filter((item) => level === "all" || item.level === level);
  const items = (variant ? shuffle(pool, variant) : pool).slice(0, count);
  const options = allLessons().map(({ unit: u, lesson: l }) => ({
    code: l.code,
    label: l.titleUz,
    unit: `${u.code}-bo'lim. ${u.titleUz}`,
  }));

  return (
    <article className="reading mx-auto max-w-3xl">
      <div className="no-print">
        <p className="text-sm font-bold tracking-wide text-brand">CHOP ETISH UCHUN</p>
        <h1 className="mt-1 font-serif text-[2.3rem] leading-tight text-heading">Mashq varag&apos;i</h1>
        <p className="prose-text mt-3 text-ink-muted">
          Darsning 100 ta bank savolidan varaq tuzing. «Yangi variant» savollarni aralashtiradi; havola shu variantni
          eslab qoladi, shuning uchun ikki guruhga ikki xil varaq berish oson. Til tugmasi varaqdagi tilni ham
          belgilaydi.
        </p>
      </div>

      <Suspense>
        <WorksheetControls lessons={options} />
      </Suspense>

      <header className="border-b-2 border-heading pb-3">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <p className="text-xs font-bold tracking-widest text-ink-muted">SAT MATH · MASHQ VARAG&apos;I</p>
          <p className="text-xs text-ink-muted">
            {unit.code}-bo&apos;lim · {level === "all" ? "aralash daraja" : LEVEL_LABEL[level]} · {items.length} savol
            {variant ? ` · variant ${variant}` : ""}
          </p>
        </div>
        <h2 className="mt-1 font-serif text-2xl text-heading">
          Dars {lesson.code}. {lesson.titleUz}
        </h2>
        <p lang="en" className="lang-en text-sm italic text-ink-muted">
          {lesson.titleEn}
        </p>
        <div className="mt-4 grid grid-cols-2 gap-6 text-sm">
          <p className="border-b border-ink-muted pb-1">Ism:</p>
          <p className="border-b border-ink-muted pb-1">Sana:</p>
        </div>
      </header>

      <ol className={compact ? "mt-5 grid gap-x-8 gap-y-4 sm:grid-cols-2 print:grid-cols-2" : "mt-6 space-y-5"}>
        {items.map((item, index) => (
          <li key={item.id} className="avoid-break flex gap-3">
            <span className="w-6 shrink-0 text-right font-bold text-heading">{index + 1}.</span>
            <div className="min-w-0 flex-1">
              <p lang="en" className="lang-en leading-relaxed">
                <M>{item.promptEn}</M>
              </p>
              <p lang="uz" className="lang-uz leading-relaxed text-uz">
                <M>{item.promptUz}</M>
              </p>
              {!compact && <div className="h-16" aria-hidden />}
              <p className="mt-2 text-sm text-ink-muted">
                Javob: <span className="inline-block w-40 border-b border-ink-muted" />
              </p>
            </div>
          </li>
        ))}
      </ol>

      <WorksheetKey code={lesson.code} ids={items.map((item) => item.id)} />
    </article>
  );
}
