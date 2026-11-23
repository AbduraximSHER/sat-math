import { ArrowLeft, ArrowRight, Clock, Printer } from "lucide-react";
import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { BankSection } from "@/components/lesson/bank-section";
import { DoneToggle } from "@/components/lesson/done-toggle";
import { ExampleCard } from "@/components/lesson/example-card";
import { PracticeSection } from "@/components/lesson/practice-section";
import { Toc, TocChips, type TocItem } from "@/components/lesson/toc";
import { M, Pair } from "@/components/text";
import { allLessons, findLesson, neighbors, type Lesson } from "@/lib/guide";

export function generateStaticParams() {
  return allLessons().map(({ lesson }) => ({ code: lesson.code }));
}

export const dynamicParams = false;

export async function generateMetadata({ params }: { params: Promise<{ code: string }> }): Promise<Metadata> {
  const { code } = await params;
  const found = findLesson(decodeURIComponent(code));
  if (!found) return { title: "Dars topilmadi" };
  const { lesson } = found;
  return {
    title: `${lesson.code}. ${lesson.titleUz}`,
    description: lesson.goalUz,
    alternates: { canonical: `/dars/${lesson.code}` },
    openGraph: { title: `Dars ${lesson.code}. ${lesson.titleUz}`, description: lesson.goalUz },
  };
}

function sectionsFor(lesson: Lesson): TocItem[] {
  const items: TocItem[] = [
    { id: "maqsad", label: "Maqsad" },
    { id: "oldin", label: "Oldindan bilishi kerak" },
    { id: "yol", label: "O'qituvchi yo'li" },
    { id: "tushuntirish", label: "Tushuntirish" },
  ];
  if (lesson.figure) items.push({ id: "rasm", label: "Rasm" });
  if (lesson.extras.includes("error_log")) items.push({ id: "xato-daftari", label: "Xato daftari" });
  lesson.examples.forEach((example, index) =>
    items.push({ id: `misol-${index + 1}`, label: `Misol ${index + 1} · ${example.kind === "sat" ? "SAT" : "Foundation"}` }),
  );
  items.push({ id: "xatolar", label: "Tez-tez xatolar" }, { id: "mashq", label: "Sinf mashqi" }, { id: "bank", label: "100 mashq banki" });
  return items;
}

function Section({ id, title, children }: { id: string; title: string; children: React.ReactNode }) {
  return (
    <section id={id} className="mt-10 scroll-mt-20">
      <h2 className="mb-3 font-serif text-2xl text-heading">{title}</h2>
      {children}
    </section>
  );
}

export default async function LessonPage({ params }: { params: Promise<{ code: string }> }) {
  const { code } = await params;
  const found = findLesson(decodeURIComponent(code));
  if (!found) notFound();
  const { unit, lesson } = found;
  const near = neighbors(lesson.code);
  const toc = sectionsFor(lesson);
  const showIntro = unit.lessons[0].code === lesson.code;

  return (
    <div className="xl:grid xl:grid-cols-[minmax(0,1fr)_13.5rem] xl:gap-12">
      <article className="reading mx-auto w-full max-w-3xl xl:mx-0">
        <p className="text-sm text-ink-muted">
          <Link href={`/dars/${unit.lessons[0].code}`} className="hover:text-ink hover:underline">
            {unit.code}-bo&apos;lim · {unit.titleUz}
          </Link>
        </p>
        <header className="mt-2">
          <p className="text-sm font-bold tracking-wide text-brand">DARS {lesson.code}</p>
          <h1 className="mt-1 font-serif text-[2.1rem] leading-tight text-heading sm:text-[2.5rem]">{lesson.titleUz}</h1>
          <p lang="en" className="lang-en mt-1.5 text-lg italic text-ink-muted">
            {lesson.titleEn}
          </p>
          <div className="mt-4 flex flex-wrap items-center gap-2">
            <span className="chip">
              <Clock className="size-3.5" aria-hidden /> 40–50 daqiqa
            </span>
            <span className="chip">2 misol · 5 mashq · 100 bank</span>
            <DoneToggle code={lesson.code} />
            <Link href={`/varaq?dars=${encodeURIComponent(lesson.code)}`} className="no-print chip h-8 px-3 hover:text-ink">
              <Printer className="size-3.5" aria-hidden /> Varaq
            </Link>
          </div>
        </header>

        <div className="mt-6">
          <TocChips items={toc} />
        </div>

        {showIntro && (
          <details open className="card group mt-8 p-5">
            <summary className="cursor-pointer list-none">
              <span className="font-serif text-xl text-heading">
                {unit.code}-bo&apos;lim. {unit.titleUz}
              </span>
              <span lang="en" className="lang-en ml-2 text-sm italic text-brand">
                {unit.titleEn}
              </span>
              <span className="no-print float-right text-xs text-ink-muted group-open:hidden">ochish</span>
            </summary>
            <div className="mt-4">
              <Pair enBlocks={unit.introEn} uzBlocks={unit.introUz} />
            </div>
          </details>
        )}

        <Section id="maqsad" title="Maqsad">
          <Pair en={lesson.goalEn} uz={lesson.goalUz} />
        </Section>
        <Section id="oldin" title="Oldindan bilishi kerak">
          <Pair en={lesson.prereqEn} uz={lesson.prereqUz} />
        </Section>
        <Section id="yol" title="O'qituvchi yo'li">
          <Pair enBlocks={lesson.teacherEn} uzBlocks={lesson.teacherUz} />
        </Section>
        <Section id="tushuntirish" title="Tushuntirish">
          <Pair enBlocks={lesson.explainEn} uzBlocks={lesson.explainUz} />
        </Section>

        {lesson.figure && (
          <figure id="rasm" className="avoid-break my-10 scroll-mt-20">
            <Image
              src={`/figures/${lesson.figure}.svg`}
              alt={lesson.figureCaptionEn}
              width={1200}
              height={720}
              unoptimized
              className="mx-auto h-auto w-full rounded-xl border border-line bg-white p-2"
            />
            <figcaption className="mt-2 space-y-1 text-center text-sm text-ink-muted">
              <p lang="en" className="lang-en">
                <M>{lesson.figureCaptionEn}</M>
              </p>
              <p lang="uz" className="lang-uz text-uz">
                <M>{lesson.figureCaptionUz}</M>
              </p>
            </figcaption>
          </figure>
        )}

        {lesson.extras.includes("error_log") && (
          <Section id="xato-daftari" title="Xato daftari">
            <p className="prose-text mb-3">
              Shu jadvalni nusxa qiling. Har bir xato uchun bitta qator. Keyingi dars shu daftarning bir qatoridan
              boshlanadi.
            </p>
            <div className="overflow-x-auto rounded-xl border border-line">
              <table className="w-full border-collapse text-sm">
                <thead>
                  <tr className="bg-selected text-left text-on-selected">
                    {["Sana", "Mavzu", "Men nima qildim", "To'g'ri g'oya", "Qayta sana"].map((cell) => (
                      <th key={cell} className="px-3 py-2 font-semibold">
                        {cell}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {Array.from({ length: 6 }, (_, row) => (
                    <tr key={row}>
                      {Array.from({ length: 5 }, (_, col) => (
                        <td key={col} className="h-10 border-t border-l border-line bg-surface first:border-l-0" />
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
        )}

        {lesson.examples.map((example, index) => (
          <ExampleCard key={index} example={example} index={index} id={`misol-${index + 1}`} />
        ))}

        <Section id="xatolar" title="Tez-tez uchraydigan xatolar">
          <ol className="space-y-3">
            {lesson.mistakes.map((mistake, index) => (
              <li key={index} className="avoid-break card flex gap-3 p-4">
                <span className="mt-0.5 inline-flex size-7 shrink-0 items-center justify-center rounded-full bg-bad-bg text-sm font-bold text-bad">
                  {index + 1}
                </span>
                <div className="min-w-0">
                  <p lang="en" className="lang-en leading-relaxed">
                    <M>{mistake.en}</M>
                  </p>
                  <p lang="uz" className="lang-uz mt-1 leading-relaxed text-uz">
                    <M>{mistake.uz}</M>
                  </p>
                </div>
              </li>
            ))}
          </ol>
        </Section>

        <Section id="mashq" title="Sinf mashqi (5 ta)">
          <PracticeSection code={lesson.code} items={lesson.practice} />
        </Section>

        <Section id="bank" title="100 mashq banki">
          <BankSection code={lesson.code} items={lesson.bank} />
        </Section>

        <nav className="no-print mt-12 grid gap-3 sm:grid-cols-2" aria-label="Darslar orasida">
          {near.prev ? (
            <Link href={`/dars/${near.prev.code}`} className="card group p-4 hover:border-brand">
              <span className="flex items-center gap-1 text-xs font-semibold text-ink-muted">
                <ArrowLeft className="size-3.5 transition-transform group-hover:-translate-x-0.5" aria-hidden /> Oldingi dars
              </span>
              <span className="mt-1 block font-medium text-heading">
                {near.prev.code}. {near.prev.titleUz}
              </span>
            </Link>
          ) : (
            <span className="hidden sm:block" />
          )}
          {near.next && (
            <Link href={`/dars/${near.next.code}`} className="card group p-4 text-right hover:border-brand">
              <span className="flex items-center justify-end gap-1 text-xs font-semibold text-ink-muted">
                Keyingi dars <ArrowRight className="size-3.5 transition-transform group-hover:translate-x-0.5" aria-hidden />
              </span>
              <span className="mt-1 block font-medium text-heading">
                {near.next.code}. {near.next.titleUz}
              </span>
            </Link>
          )}
        </nav>
      </article>

      <aside className="no-print hidden xl:block">
        <div className="sticky top-20 max-h-[calc(100dvh-6rem)] overflow-y-auto">
          <Toc items={toc} />
        </div>
      </aside>
    </div>
  );
}
