"use client";

import { Check, CircleAlert, Minus, RotateCcw, Send, Timer, X } from "lucide-react";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { HINTS } from "@/components/lesson/bank-section";
import { KeyPanel, KeyStatus } from "@/components/lesson/practice-section";
import { M, Pair, Prompt } from "@/components/text";
import { useTeacherData } from "@/components/teacher-key";
import type { Verdict } from "@/lib/answer-check";
import type { MiniItem } from "@/lib/guide";
import type { MiniKey } from "@/lib/keys";
import { readItem, writeItem } from "@/lib/local-store";

type Result = Verdict | { result: "blank" };
type Saved = { answers: Record<string, string>; results?: Record<string, Result>; startedAt?: number };

const STORAGE = "sat-mini-v1";
const MINUTES = 35;

function load(): Saved {
  try {
    const parsed = JSON.parse(readItem(STORAGE) ?? "{}") as Saved;
    return { answers: parsed.answers ?? {}, results: parsed.results, startedAt: parsed.startedAt };
  } catch {
    return { answers: {} };
  }
}

function clock(ms: number): string {
  const total = Math.max(0, Math.round(ms / 1000));
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

export function MiniView({ items, review }: { items: MiniItem[]; review: Record<number, { code: string; title: string }> }) {
  const [saved, setSaved] = useState<Saved>({ answers: {} });
  const [now, setNow] = useState(() => Date.now());
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const keys = useTeacherData<{ mini: MiniKey[] }>("/api/keys?mini=1");
  const keyByNumber = useMemo(() => new Map((keys.data?.mini ?? []).map((row) => [row.number, row])), [keys.data]);

  useEffect(() => {
    setSaved(load());
  }, []);

  useEffect(() => {
    if (!saved.startedAt || saved.results) return;
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [saved.startedAt, saved.results]);

  function update(next: Saved) {
    setSaved(next);
    writeItem(STORAGE, JSON.stringify(next));
  }

  const answered = items.filter((item) => saved.answers[item.number]?.trim()).length;
  const remaining = saved.startedAt ? saved.startedAt + MINUTES * 60_000 - now : MINUTES * 60_000;
  const results = saved.results;
  const score = results ? items.filter((item) => results[item.number]?.result === "correct").length : 0;

  async function submit() {
    setBusy(true);
    setError(false);
    try {
      const response = await fetch("/api/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mini: true, answers: saved.answers }),
      });
      if (!response.ok) throw new Error(String(response.status));
      const data = (await response.json()) as { results: Record<string, Result> };
      update({ ...saved, results: data.results });
      window.scrollTo({ top: 0 });
    } catch {
      setError(true);
    } finally {
      setBusy(false);
    }
  }

  const weak = results
    ? items.filter((item) => results[item.number]?.result !== "correct").map((item) => ({ item, lesson: review[item.number] }))
    : [];

  return (
    <article className="reading mx-auto max-w-3xl">
      <p className="text-sm font-bold tracking-wide text-brand">ARALASH TAKRORLASH</p>
      <h1 className="mt-1 font-serif text-[2.3rem] leading-tight text-heading">Mini-test</h1>
      <div className="mt-4">
        <Pair
          en="Twenty original questions, 35 minutes. This is not a scored practice test and it does not predict a scaled score. It shows which topic still wobbles. Type each answer; the site checks them all when you submit."
          uz="Yigirma original savol, 35 daqiqa. Bu baholanadigan sinov emas va scaled ballni bashorat qilmaydi. Qaysi mavzu hali qaltisligini ko'rsatadi. Har bir javobni yozing; topshirganda sayt hammasini tekshiradi."
        />
      </div>

      {results && (
        <section className="card mt-8 overflow-hidden" aria-live="polite">
          <div className="flex flex-wrap items-center gap-5 border-b border-line bg-surface-2 p-5">
            <div className="flex size-20 items-center justify-center rounded-full border-4 border-brand bg-surface">
              <span className="font-serif text-2xl text-heading">
                {score}
                <span className="text-base text-ink-muted">/20</span>
              </span>
            </div>
            <div className="min-w-0 flex-1">
              <h2 className="font-serif text-2xl text-heading">Natija</h2>
              <p className="text-sm text-ink-muted">
                {score === 20
                  ? "Hammasi to'g'ri. Keyingi qadam — SAT uslubidagi bank savollari."
                  : "Noto'g'ri javoblar qaysi darsni takrorlash kerakligini ko'rsatadi."}
              </p>
            </div>
            <button
              type="button"
              className="btn"
              onClick={() => {
                if (window.confirm("Javoblarni o'chirib, testni qaytadan boshlaysizmi?")) update({ answers: {} });
              }}
            >
              <RotateCcw className="size-4" aria-hidden /> Qaytadan
            </button>
          </div>
          {weak.length > 0 && (
            <div className="p-5">
              <p className="text-xs font-bold tracking-widest text-ink-muted">TAKRORLASH UCHUN</p>
              <ul className="mt-2 grid gap-2 sm:grid-cols-2">
                {weak.map(({ item, lesson }) => (
                  <li key={item.number}>
                    <Link href={lesson ? `/dars/${lesson.code}` : "/"} className="flex items-center gap-2 rounded-lg border border-line px-3 py-2 text-sm hover:border-brand">
                      <span className="font-semibold text-bad">{item.number}.</span>
                      <span className="min-w-0 flex-1 truncate">{item.domain}</span>
                      {lesson && <span className="shrink-0 text-xs font-semibold text-brand">Dars {lesson.code} →</span>}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}

      {!results && !saved.startedAt && (
        <div className="card mt-8 flex flex-wrap items-center gap-4 p-5">
          <Timer className="size-8 text-brand" aria-hidden />
          <div className="min-w-0 flex-1">
            <p className="font-semibold text-heading">Tayyormisiz?</p>
            <p className="text-sm text-ink-muted">Vaqt 35 daqiqa. Javoblar shu brauzerda saqlanib boradi.</p>
          </div>
          <button type="button" className="btn-primary" onClick={() => update({ ...saved, startedAt: Date.now() })}>
            Boshlash
          </button>
        </div>
      )}

      <ol className="mt-8 space-y-4">
        {items.map((item) => {
          const result = results?.[item.number];
          const key = keyByNumber.get(item.number);
          return (
            <li key={item.number} className="avoid-break card p-4 sm:p-5">
              <div className="mb-2 flex items-center gap-2 text-xs font-semibold tracking-wide">
                <span className="inline-flex size-7 items-center justify-center rounded-full bg-surface-2 text-sm font-bold text-heading">
                  {item.number}
                </span>
                <span className="chip">{item.domain}</span>
                {result?.result === "correct" && (
                  <span className="ml-auto inline-flex items-center gap-1 text-good">
                    <Check className="size-4" aria-hidden /> To&apos;g&apos;ri
                  </span>
                )}
                {result?.result === "incorrect" && (
                  <span className="ml-auto inline-flex items-center gap-1 text-bad">
                    <X className="size-4" aria-hidden /> Noto&apos;g&apos;ri
                  </span>
                )}
                {result?.result === "blank" && (
                  <span className="ml-auto inline-flex items-center gap-1 text-ink-muted">
                    <Minus className="size-4" aria-hidden /> Javobsiz
                  </span>
                )}
                {result?.result === "format" && (
                  <span className="ml-auto inline-flex items-center gap-1 text-warn">
                    <CircleAlert className="size-4" aria-hidden /> Shakl
                  </span>
                )}
              </div>
              <Prompt en={item.promptEn} uz={item.promptUz} />
              {item.choices.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {item.choices.map((choice) => (
                    <li key={choice.letter}>
                      <span className="font-semibold">{choice.letter}.</span>{" "}
                      <span lang="en" className="lang-en">
                        <M>{choice.en}</M>
                      </span>
                      <span className="lang-both text-ink-muted"> / </span>
                      <span lang="uz" className="lang-uz text-uz">
                        <M>{choice.uz}</M>
                      </span>
                    </li>
                  ))}
                </ul>
              )}
              <input
                value={saved.answers[item.number] ?? ""}
                onChange={(event) => {
                  const answers = { ...saved.answers, [item.number]: event.target.value };
                  update({ ...saved, answers, results: undefined, startedAt: saved.startedAt ?? Date.now() });
                }}
                disabled={Boolean(results)}
                placeholder="Javob"
                aria-label={`${item.number}-savol javobi`}
                autoComplete="off"
                autoCapitalize="off"
                spellCheck={false}
                maxLength={80}
                className="no-print field mt-3 h-10 py-1.5 disabled:opacity-80"
              />
              {result?.result === "format" && (
                <p className="mt-2 text-sm text-warn">
                  {HINTS[result.hint][0]} <span className="text-ink-muted">{HINTS[result.hint][1]}</span>
                </p>
              )}
              {key && <KeyPanel answer={key.answer} en={key.analysisEn} uz={key.analysisUz} />}
            </li>
          );
        })}
      </ol>
      <KeyStatus state={keys.state} />

      {!results && (
        <div className="no-print sticky bottom-3 z-20 mt-6">
          <div className="card flex flex-wrap items-center gap-3 p-3 shadow-lg">
            <span className="text-sm font-semibold text-ink tabular-nums">{answered}/20 javob</span>
            {saved.startedAt && (
              <span className={`inline-flex items-center gap-1 text-sm tabular-nums ${remaining <= 0 ? "font-semibold text-bad" : "text-ink-muted"}`}>
                <Timer className="size-4" aria-hidden />
                {remaining > 0 ? clock(remaining) : "Vaqt tugadi"}
              </span>
            )}
            {error && <span className="text-sm text-bad">Yuborib bo&apos;lmadi. Qayta urining.</span>}
            <button type="button" className="btn-primary ml-auto" disabled={busy || answered === 0} onClick={submit}>
              <Send className="size-4" aria-hidden />
              {busy ? "Tekshirilmoqda…" : "Topshirish"}
            </button>
          </div>
        </div>
      )}
    </article>
  );
}
