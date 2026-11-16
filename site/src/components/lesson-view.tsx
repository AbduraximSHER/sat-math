"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { Pair, showLang } from "@/components/text";
import { usePrefs } from "@/components/prefs";
import type { BankItem, Lesson, Unit } from "@/lib/guide";
import type { BankKey, PracticeKey } from "@/lib/keys";

const PAGE_SIZE = 10;
type LevelFilter = "all" | "oson" | "orta" | "sat";

const LEVEL_LABEL: Record<string, string> = {
  oson: "Oson",
  orta: "O'rta",
  sat: "SAT",
};

export function LessonView({
  unit,
  lesson,
  showIntro,
  prev,
  next,
}: {
  unit: Unit;
  lesson: Lesson;
  showIntro: boolean;
  prev?: { code: string; titleUz: string };
  next?: { code: string; titleUz: string };
}) {
  const { lang, showKeys } = usePrefs();
  const [level, setLevel] = useState<LevelFilter>("all");
  const [page, setPage] = useState(0);
  const [practiceKeys, setPracticeKeys] = useState<PracticeKey[] | null>(null);
  const [bankKeys, setBankKeys] = useState<Record<string, BankKey> | null>(null);
  const [keysError, setKeysError] = useState(false);

  const filtered = useMemo(() => {
    const bank = lesson.bank ?? [];
    if (level === "all") return bank;
    return bank.filter((item) => item.level === level);
  }, [lesson.bank, level]);

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const pageItems = filtered.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);

  useEffect(() => {
    setPage(0);
  }, [level, lesson.code]);

  useEffect(() => {
    if (!showKeys) {
      setPracticeKeys(null);
      setBankKeys(null);
      setKeysError(false);
      return;
    }
    let cancelled = false;
    setKeysError(false);
    fetch(`/api/keys?code=${encodeURIComponent(lesson.code)}`)
      .then(async (response) => {
        if (!response.ok) throw new Error("keys");
        return response.json();
      })
      .then((data: { practice: PracticeKey[]; bank: BankKey[] }) => {
        if (cancelled) return;
        setPracticeKeys(data.practice ?? []);
        const map: Record<string, BankKey> = {};
        for (const row of data.bank ?? []) map[row.id] = row;
        setBankKeys(map);
      })
      .catch(() => {
        if (!cancelled) setKeysError(true);
      });
    return () => {
      cancelled = true;
    };
  }, [showKeys, lesson.code]);

  return (
    <article>
      {showIntro && (
        <section className="mb-8 rounded-xl border border-[#e4ddd0] bg-white p-5">
          <p className="font-serif text-2xl text-[var(--navy)]">
            {unit.code}-bo&apos;lim. {unit.titleUz}
          </p>
          <p className="mt-1 text-sm italic text-[var(--teal)]">{unit.titleEn}</p>
          <div className="mt-4">
            <Pair enBlocks={unit.introEn} uzBlocks={unit.introUz} />
          </div>
        </section>
      )}

      <p className="text-sm font-semibold text-[var(--teal)]">Dars {lesson.code}</p>
      <h1 className="mt-1 font-serif text-4xl leading-tight text-[var(--navy)]">{lesson.titleUz}</h1>
      <p className="mt-2 text-lg italic text-[#5c6b73]">{lesson.titleEn}</p>

      <Section title="Maqsad">
        <Pair en={lesson.goalEn} uz={lesson.goalUz} />
      </Section>
      <Section title="Oldindan bilishi kerak">
        <Pair en={lesson.prereqEn} uz={lesson.prereqUz} />
      </Section>
      <Section title="O'qituvchi yo'li">
        <Pair enBlocks={lesson.teacherEn} uzBlocks={lesson.teacherUz} />
      </Section>
      <Section title="Tushuntirish">
        <Pair enBlocks={lesson.explainEn} uzBlocks={lesson.explainUz} />
      </Section>

      {lesson.figure && (
        <figure className="my-8">
          <Image
            src={`/figures/${lesson.figure}.png`}
            alt={lesson.figureCaptionEn}
            width={1200}
            height={720}
            className="mx-auto h-auto w-full rounded-lg border border-[#e4ddd0] bg-white"
          />
          <figcaption className="mt-2 space-y-1 text-center text-sm text-[#5c6b73]">
            {showLang(lang, "en") && <p>{lesson.figureCaptionEn}</p>}
            {showLang(lang, "uz") && <p className="text-[var(--teal)]">{lesson.figureCaptionUz}</p>}
          </figcaption>
        </figure>
      )}

      {lesson.extras.includes("error_log") && (
        <Section title="Xato daftari">
          <p className="mb-3 text-[16.5px] leading-relaxed">
            Shu jadvalni nusxa qiling. Har bir xato uchun bitta qator. Keyingi dars shu daftarning bir qatoridan boshlanadi.
          </p>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="bg-[var(--navy)] text-left text-[#f7f4ec]">
                  {["Sana", "Mavzu", "Men nima qildim", "To'g'ri g'oya", "Qayta sana"].map((cell) => (
                    <th key={cell} className="border border-[#1b3a4b] px-2 py-2 font-medium">
                      {cell}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Array.from({ length: 6 }, (_, row) => (
                  <tr key={row}>
                    {Array.from({ length: 5 }, (_, col) => (
                      <td key={col} className="h-10 border border-[#e4ddd0] bg-white" />
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {lesson.examples.map((example, index) => (
        <section
          key={index}
          className={`my-8 rounded-xl border p-5 ${
            example.kind === "sat" ? "border-[#e4d3a8] bg-[#fbf7ef]" : "border-[#d5e4e3] bg-[#f4f8f8]"
          }`}
        >
          <h2 className="font-serif text-2xl text-[var(--navy)]">
            Misol {index + 1} — {example.kind === "sat" ? "SAT uslubi" : "Foundation"}
          </h2>
          <div className="mt-3">
            <Pair en={example.promptEn} uz={example.promptUz} />
          </div>
          {example.gloss && <p className="mt-2 text-sm italic text-[#5c6b73]">So&apos;zlar: {example.gloss}</p>}
          {example.choices.length > 0 && (
            <ul className="mt-3 space-y-1">
              {example.choices.map((choice) => (
                <li key={choice.letter} className="text-[16px]">
                  <span className="font-semibold">{choice.letter}.</span>{" "}
                  {showLang(lang, "en") && choice.en}
                  {lang === "both" && "  /  "}
                  {showLang(lang, "uz") && <span className="text-[#245c59]">{choice.uz}</span>}
                </li>
              ))}
            </ul>
          )}
          <ol className="mt-4 space-y-3">
            {example.steps.map((step, stepIndex) => (
              <li key={stepIndex} className="text-[16px] leading-relaxed">
                <span className="font-semibold text-[var(--navy)]">{stepIndex + 1}. </span>
                {showLang(lang, "en") && step.en}
                {lang === "both" && <span className="mt-1 block pl-5 text-[#245c59]">{step.uz}</span>}
                {lang === "uz" && <span className="text-[#245c59]">{step.uz}</span>}
              </li>
            ))}
          </ol>
          <p className="mt-4 font-semibold text-[var(--navy)]">Javob: {example.answer}</p>
        </section>
      ))}

      <Section title="Tez-tez uchraydigan xatolar">
        <ol className="space-y-4">
          {lesson.mistakes.map((mistake, index) => (
            <li key={index}>
              <Pair en={`${index + 1}. ${mistake.en}`} uz={mistake.uz} />
            </li>
          ))}
        </ol>
      </Section>

      <Section title="Sinf mashqi (5 ta)">
        <p className="mb-4 text-sm italic text-[#5c6b73]">
          Qisqa to&apos;plam. Javoblar faqat kalit ochiq bo&apos;lganda yuklanadi.
        </p>
        <ol className="space-y-4">
          {lesson.practice.map((item, index) => (
            <li key={index}>
              <p className="font-medium">
                {index + 1}. {showLang(lang, "en") && item.promptEn}
              </p>
              {showLang(lang, "uz") && <p className="mt-1 text-[#245c59]">{item.promptUz}</p>}
              {item.gloss && <p className="mt-1 text-sm italic text-[#5c6b73]">So&apos;zlar: {item.gloss}</p>}
              {showKeys && practiceKeys?.[index] && (
                <div className="mt-2 rounded-lg bg-[#f3efe6] p-3">
                  <p className="font-semibold text-[var(--navy)]">{practiceKeys[index].answer}</p>
                  {showLang(lang, "en") && (
                    <p className="mt-1 text-[15px] leading-relaxed">{practiceKeys[index].solutionEn}</p>
                  )}
                  {showLang(lang, "uz") && (
                    <p className="mt-1 text-[15px] leading-relaxed text-[#245c59]">
                      {practiceKeys[index].solutionUz}
                    </p>
                  )}
                </div>
              )}
            </li>
          ))}
        </ol>
      </Section>

      <BankSection
        items={pageItems}
        total={filtered.length}
        level={level}
        setLevel={setLevel}
        page={page}
        pageCount={pageCount}
        setPage={setPage}
        showKeys={showKeys}
        bankKeys={bankKeys}
        keysError={keysError}
        lang={lang}
      />

      <nav className="mt-10 flex flex-col gap-3 border-t border-[#e4ddd0] pt-6 sm:flex-row sm:justify-between">
        {prev ? (
          <Link href={`/dars/${prev.code}`} className="text-[var(--teal)] hover:underline">
            ← {prev.code}. {prev.titleUz}
          </Link>
        ) : (
          <span />
        )}
        {next && (
          <Link href={`/dars/${next.code}`} className="text-[var(--teal)] hover:underline sm:text-right">
            {next.code}. {next.titleUz} →
          </Link>
        )}
      </nav>
    </article>
  );
}

function BankSection({
  items,
  total,
  level,
  setLevel,
  page,
  pageCount,
  setPage,
  showKeys,
  bankKeys,
  keysError,
  lang,
}: {
  items: BankItem[];
  total: number;
  level: LevelFilter;
  setLevel: (level: LevelFilter) => void;
  page: number;
  pageCount: number;
  setPage: (page: number | ((prev: number) => number)) => void;
  showKeys: boolean;
  bankKeys: Record<string, BankKey> | null;
  keysError: boolean;
  lang: "both" | "en" | "uz";
}) {
  return (
    <Section title={`100 mashq banki (${total} ta)`}>
      <p className="mb-4 text-sm italic text-[#5c6b73]">
        Har bir mavzuda 100 ta tekshirilgan misol. Daraja bo&apos;yicha filtrlash va sahifalash mumkin. Javoblar kalit ochilganda
        serverdan keladi.
      </p>
      <div className="mb-4 flex flex-wrap gap-2">
        {(["all", "oson", "orta", "sat"] as LevelFilter[]).map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => setLevel(option)}
            className={`rounded-md border px-3 py-1.5 text-sm ${
              level === option
                ? "border-[var(--navy)] bg-[var(--navy)] text-[#f7f4ec]"
                : "border-[#d5e4e3] bg-white text-[var(--navy)]"
            }`}
          >
            {option === "all" ? "Hammasi" : LEVEL_LABEL[option]}
          </button>
        ))}
      </div>
      <ol className="space-y-4" start={page * PAGE_SIZE + 1}>
        {items.map((item) => {
          const key = bankKeys?.[item.id];
          return (
            <li key={item.id} className="rounded-lg border border-[#e4ddd0] bg-white p-3">
              <p className="text-xs font-semibold tracking-wide text-[var(--teal)]">
                #{item.id} · {LEVEL_LABEL[item.level] ?? item.level}
              </p>
              {showLang(lang, "en") && <p className="mt-1 font-medium">{item.promptEn}</p>}
              {showLang(lang, "uz") && <p className="mt-1 text-[#245c59]">{item.promptUz}</p>}
              {showKeys && key && (
                <div className="mt-2 rounded-md bg-[#f3efe6] p-2.5">
                  <p className="font-semibold text-[var(--navy)]">{key.answer}</p>
                  {showLang(lang, "en") && <p className="mt-1 text-sm leading-relaxed">{key.solutionEn}</p>}
                  {showLang(lang, "uz") && (
                    <p className="mt-1 text-sm leading-relaxed text-[#245c59]">{key.solutionUz}</p>
                  )}
                </div>
              )}
            </li>
          );
        })}
      </ol>
      {showKeys && keysError && (
        <p className="mt-3 text-sm text-[#8c2f2f]">Kalitni yuklab bo&apos;lmadi. Sahifani yangilang.</p>
      )}
      {showKeys && !keysError && !bankKeys && (
        <p className="mt-3 text-sm text-[#5c6b73]">Kalit yuklanmoqda…</p>
      )}
      <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
        <button
          type="button"
          disabled={page <= 0}
          onClick={() => setPage((p) => Math.max(0, p - 1))}
          className="rounded-md border border-[#d5e4e3] bg-white px-3 py-1.5 text-sm disabled:opacity-40"
        >
          ← Oldingi
        </button>
        <p className="text-sm text-[#5c6b73]">
          Sahifa {page + 1} / {pageCount}
        </p>
        <button
          type="button"
          disabled={page >= pageCount - 1}
          onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))}
          className="rounded-md border border-[#d5e4e3] bg-white px-3 py-1.5 text-sm disabled:opacity-40"
        >
          Keyingi →
        </button>
      </div>
    </Section>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-8">
      <h2 className="font-serif text-2xl text-[var(--navy)]">{title}</h2>
      <div className="mt-3">{children}</div>
    </section>
  );
}
