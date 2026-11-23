import { ClipboardCheck, KeyRound, PenLine, Printer, Target } from "lucide-react";
import Link from "next/link";
import { ContinueButton, UnitLink, UnitProgress } from "@/components/home-progress";
import { guide } from "@/lib/guide";

const FACTS = [
  { value: "2", label: "modul" },
  { value: "44", label: "savol" },
  { value: "70", label: "daqiqa" },
  { value: "Desmos", label: "har savolda" },
  { value: "0", label: "noto'g'ri javob jarimasi" },
];

const STEPS = [
  {
    icon: Target,
    title: "Maqsaddan boshlang",
    body: "Darsni o'zbekcha maqsad bilan oching. Til tugmasi (UZ / EN) kerakli tilni qoldiradi.",
  },
  {
    icon: PenLine,
    title: "Misolni qadamma-qadam",
    body: "Foundation misolni doskada yeching. «Qadamma-qadam» tugmasi qadamlarni birma-bir ochadi.",
  },
  {
    icon: KeyRound,
    title: "Kalitni yopiq tuting",
    body: "Ekranni sinfga ko'rsatishdan oldin kalit yopiq bo'lsin: javoblar sahifaga umuman yuklanmaydi.",
  },
  {
    icon: ClipboardCheck,
    title: "O'quvchi o'zi tekshiradi",
    body: "Har darsda 100 ta bank savoli. O'quvchi javob yozadi, sayt to'g'ri-noto'g'rini aytadi, kalitni ochmaydi.",
  },
];

export default function HomePage() {
  const titles = Object.fromEntries(guide.units.flatMap((unit) => unit.lessons.map((lesson) => [lesson.code, lesson.titleUz])));
  const totalLessons = guide.units.reduce((sum, unit) => sum + unit.lessons.length, 0);

  return (
    <div className="reading mx-auto max-w-4xl">
      <section className="relative overflow-hidden rounded-3xl border border-line bg-surface px-6 py-10 sm:px-10 sm:py-14">
        <svg viewBox="0 0 120 120" className="pointer-events-none absolute top-10 right-10 hidden size-36 text-brand opacity-[0.12] md:block" aria-hidden>
          <rect x="10" y="22" width="100" height="18" rx="5" fill="currentColor" />
          <rect x="10" y="51" width="100" height="18" rx="5" fill="currentColor" opacity="0.55" />
          <rect x="10" y="80" width="100" height="18" rx="5" fill="currentColor" />
        </svg>
        <p className="text-sm font-bold tracking-widest text-brand">DIGITAL SAT · SINF UCHUN</p>
        <h1 className="mt-3 font-serif text-5xl leading-[1.05] text-heading sm:text-6xl">SAT Math</h1>
        <p className="mt-2 font-serif text-2xl text-ink-muted">O&apos;qituvchi qo&apos;llanmasi</p>
        <p className="prose-text mt-6 max-w-2xl">
          Kasrlarni qo&apos;shish, ayirish, ko&apos;paytirish va bo&apos;lishni biladigan sinf uchun. {totalLessons} dars raqamli
          SAT Math bo&apos;limining qolganini tartib bilan o&apos;tadi. Har bir dars ikki tilda: chuqur tushuntirish, ikki yechilgan
          misol, beshta sinf mashqi va o&apos;zini o&apos;zi tekshiradigan 100 ta bank savoli.
        </p>
        <div className="mt-7 flex flex-wrap gap-3">
          <ContinueButton titles={titles} />
          <Link href="/mini" className="btn h-11 px-4 text-base">
            <ClipboardCheck className="size-5" aria-hidden /> Mini-test
          </Link>
          <Link href="/varaq" className="btn h-11 px-4 text-base">
            <Printer className="size-5" aria-hidden /> Mashq varag&apos;i
          </Link>
        </div>
      </section>

      <section className="mt-10" aria-labelledby="exam">
        <h2 id="exam" className="font-serif text-2xl text-heading">
          Imtihon
        </h2>
        <dl className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-5">
          {FACTS.map((fact) => (
            <div key={fact.label} className="card px-4 py-3">
              <dt className="sr-only">{fact.label}</dt>
              <dd className="font-serif text-2xl text-heading">{fact.value}</dd>
              <dd className="text-sm leading-snug text-ink-muted">{fact.label}</dd>
            </div>
          ))}
        </dl>
        <p className="mt-4 rounded-xl border border-line-brand bg-say-bg px-4 py-3 text-[0.97rem] leading-relaxed">
          <strong>Nuqta — o&apos;nli kasr belgisi.</strong> 3.5 — uch butun besh o&apos;ndan. 3,500 — uch ming besh yuz. Javob
          maydonida 3,5 yozilsa, sayt buni eslatadi.
        </p>
      </section>

      <section className="mt-10" aria-labelledby="class">
        <h2 id="class" className="font-serif text-2xl text-heading">
          Sinfda
        </h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          {STEPS.map(({ icon: Icon, title, body }, index) => (
            <div key={title} className="card flex gap-4 p-4">
              <span className="inline-flex size-10 shrink-0 items-center justify-center rounded-xl bg-say-bg text-brand">
                <Icon className="size-5" aria-hidden />
              </span>
              <div>
                <p className="font-semibold text-heading">
                  {index + 1}. {title}
                </p>
                <p className="mt-1 text-sm leading-relaxed text-ink">{body}</p>
              </div>
            </div>
          ))}
        </div>
        <p className="mt-3 text-sm text-ink-muted">
          Klaviatura: <kbd className="rounded border border-line px-1">←</kbd> <kbd className="rounded border border-line px-1">→</kbd>{" "}
          darslar orasida, <kbd className="rounded border border-line px-1">K</kbd> kalit,{" "}
          <kbd className="rounded border border-line px-1">F</kbd> ekran rejimi, <kbd className="rounded border border-line px-1">/</kbd> qidirish,{" "}
          <kbd className="rounded border border-line px-1">?</kbd> hammasi.
        </p>
      </section>

      <section className="mt-10" aria-labelledby="units">
        <h2 id="units" className="font-serif text-2xl text-heading">
          Bo&apos;limlar
        </h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          {guide.units.map((unit) => (
            <UnitLink key={unit.code} href={`/dars/${unit.lessons[0].code}`}>
              <p className="text-xs font-bold tracking-wide text-brand">
                {unit.code}-BO&apos;LIM · {unit.lessons.length} DARS
              </p>
              <p className="mt-1 font-serif text-xl text-heading">{unit.titleUz}</p>
              <p lang="en" className="text-sm italic text-ink-muted">
                {unit.titleEn}
              </p>
              <UnitProgress codes={unit.lessons.map((lesson) => lesson.code)} />
            </UnitLink>
          ))}
        </div>
      </section>
    </div>
  );
}
