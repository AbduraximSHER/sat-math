"use client";

import { Check, ChevronLeft, ChevronRight, CircleAlert, Printer, RotateCcw, X } from "lucide-react";
import Link from "next/link";
import { useMemo, useState } from "react";
import { KeyPanel, KeyStatus, type LessonKeyData } from "@/components/lesson/practice-section";
import { usePrefs } from "@/components/prefs";
import { Prompt } from "@/components/text";
import { useTeacherData } from "@/components/teacher-key";
import type { Hint, Verdict } from "@/lib/answer-check";
import type { BankItem } from "@/lib/guide";
import { recordBankResult, resetBank, solvedCount, useProgress } from "@/lib/progress";

const PAGE_SIZE = 10;
type Level = "all" | "oson" | "orta" | "sat";
type Status = "all" | "open" | "solved";
const NO_RESULTS: Record<string, "ok" | "no"> = {};

export const LEVEL_LABEL: Record<string, string> = { oson: "Oson", orta: "O'rta", sat: "SAT" };

/** What to say when an answer is close but not in the accepted form. Uzbek first, English second. */
export const HINTS: Record<Hint, [string, string]> = {
  empty: ["Avval javob yozing.", "Type an answer first."],
  unreadable: ["Javobni o'qib bo'lmadi. Son yoki ifoda yozing: 3/4, −2, 2x + 1.", "Could not read that. Type a number or expression: 3/4, −2, 2x + 1."],
  "mixed-number": ["SAT aralash sonni qabul qilmaydi: 3 1/2 emas, 7/2 yoki 3.5 yozing.", "The SAT does not take mixed numbers: write 7/2 or 3.5, not 3 1/2."],
  "decimal-comma": ["SAT'da o'nli kasr nuqta bilan yoziladi: 3,5 emas, 3.5.", "The SAT uses a decimal point: 3.5, not 3,5."],
  simplify: ["Qiymat to'g'ri. Endi kasrni qisqartiring.", "Right value. Now simplify the fraction."],
  "more-digits": ["Juda qisqa yaxlitlangan. Kasr yozing yoki joyni to'ldiring: .6667.", "Rounded too short. Give the fraction or fill the space: .6667."],
  "use-decimal": ["Savol o'nli kasr so'rayapti.", "The question asks for a decimal."],
  "use-fraction": ["Savol kasr so'rayapti.", "The question asks for a fraction."],
  "use-percent": ["Bu birning ulushi. Foizda yozing: 0.25 emas, 25.", "That is a share of 1. Give the percent: 25, not 0.25."],
  "no-percent": ["Bu javob oddiy son, foiz emas.", "This answer is a number, not a percent."],
  "single-number": ["Hisobni oxirigacha yetkazing: bitta son yozing.", "Finish the arithmetic: give one number."],
  combine: ["Qavsni oching va o'xshash hadlarni birlashtiring.", "Expand and combine like terms."],
  factor: ["Ko'paytuvchilarga ajratib yozing: (x + 1)(x + 2) kabi.", "Write it factored, like (x + 1)(x + 2)."],
  radical: ["Ildizni soddalashtiring: √8 emas, 2√2.", "Simplify the radical: 2√2, not √8."],
  "use-pi": ["Javobda π bor: masalan 9π.", "The answer includes π, like 9π."],
  "both-values": ["Ikkala qiymatni ham yozing.", "Give both values."],
  inequality: ["Tengsizlik ko'rinishida yozing: x < 4 kabi.", "Write the inequality, like x < 4."],
};

type Feedback = Verdict | { result: "error" };

function FeedbackLine({ feedback }: { feedback: Feedback }) {
  if (feedback.result === "correct") {
    return (
      <p role="status" className="flex items-center gap-1.5 text-sm font-semibold text-good">
        <Check className="size-4" aria-hidden /> To&apos;g&apos;ri! <span className="font-normal text-ink-muted">Correct.</span>
      </p>
    );
  }
  if (feedback.result === "incorrect") {
    return (
      <p role="status" className="flex items-center gap-1.5 text-sm font-semibold text-bad">
        <X className="size-4" aria-hidden /> Hali emas. Yana urinib ko&apos;ring.
        <span className="font-normal text-ink-muted">Not yet.</span>
      </p>
    );
  }
  if (feedback.result === "error") {
    return (
      <p role="status" className="text-sm text-bad">
        Tekshirib bo&apos;lmadi. Internet aloqasini tekshiring.
      </p>
    );
  }
  const [uz, en] = HINTS[feedback.hint];
  return (
    <p role="status" className="flex items-start gap-1.5 text-sm text-warn">
      <CircleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
      <span>
        <span className="font-semibold">{uz}</span> <span className="text-ink-muted">{en}</span>
      </span>
    </p>
  );
}

function AnswerForm({ code, id, solved }: { code: string; id: string; solved: boolean }) {
  const [value, setValue] = useState("");
  const [busy, setBusy] = useState(false);
  const [feedback, setFeedback] = useState<Feedback | null>(null);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!value.trim()) {
      setFeedback({ result: "format", hint: "empty" });
      return;
    }
    setBusy(true);
    try {
      const response = await fetch("/api/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, id, answer: value }),
      });
      if (!response.ok) throw new Error(String(response.status));
      const verdict = (await response.json()) as Verdict;
      setFeedback(verdict);
      if (verdict.result !== "format") recordBankResult(code, id, verdict.result === "correct");
    } catch {
      setFeedback({ result: "error" });
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="no-print mt-3 space-y-2">
      <div className="flex gap-2">
        <input
          value={value}
          onChange={(event) => {
            setValue(event.target.value);
            setFeedback(null);
          }}
          placeholder={solved ? "Yechilgan — yana sinash mumkin" : "Javobingiz"}
          aria-label={`#${id} javobi`}
          autoComplete="off"
          autoCapitalize="off"
          spellCheck={false}
          maxLength={80}
          className={`field h-10 py-1.5 ${
            feedback?.result === "correct" ? "border-good" : feedback?.result === "incorrect" ? "border-bad" : ""
          }`}
        />
        <button type="submit" className="btn-primary h-10 shrink-0 px-4" disabled={busy}>
          {busy ? "…" : "Tekshirish"}
        </button>
      </div>
      {feedback && <FeedbackLine feedback={feedback} />}
    </form>
  );
}

export function BankSection({ code, items }: { code: string; items: BankItem[] }) {
  const { answerMode } = usePrefs();
  const progress = useProgress();
  const results = progress.bank[code] ?? NO_RESULTS;
  const solved = solvedCount(progress, code);
  const [level, setLevel] = useState<Level>("all");
  const [status, setStatus] = useState<Status>("all");
  const [page, setPage] = useState(0);
  const keys = useTeacherData<LessonKeyData>(`/api/keys?code=${encodeURIComponent(code)}`);
  const keyById = useMemo(() => new Map((keys.data?.bank ?? []).map((row) => [row.id, row])), [keys.data]);

  const counts = useMemo(() => {
    const out: Record<Level, number> = { all: items.length, oson: 0, orta: 0, sat: 0 };
    for (const item of items) if (item.level in out) out[item.level as Level] += 1;
    return out;
  }, [items]);

  const filtered = useMemo(
    () =>
      items.filter(
        (item) =>
          (level === "all" || item.level === level) &&
          (status === "all" || (status === "solved") === (results[item.id] === "ok")),
      ),
    [items, level, status, results],
  );
  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const current = Math.min(page, pageCount - 1);
  const pageItems = filtered.slice(current * PAGE_SIZE, current * PAGE_SIZE + PAGE_SIZE);

  function goTo(next: number) {
    setPage(next);
    document.getElementById("bank")?.scrollIntoView({ block: "start" });
  }

  return (
    <>
      <p className="mb-4 text-sm leading-relaxed text-ink-muted">
        Har bir savolning javobi SymPy bilan tekshirilgan. Javobni yozing va <strong>Tekshirish</strong> ni bosing: sayt
        to&apos;g&apos;ri yoki noto&apos;g&apos;ri ekanini aytadi, kalitni esa ochmaydi. Natijalar shu brauzerda saqlanadi.
      </p>

      <div className="no-print card mb-4 space-y-3 p-3">
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex flex-wrap gap-1" role="group" aria-label="Daraja">
            {(["all", "oson", "orta", "sat"] as Level[]).map((option) => (
              <button
                key={option}
                type="button"
                onClick={() => {
                  setLevel(option);
                  setPage(0);
                }}
                aria-pressed={level === option}
                className={`rounded-md border px-2.5 py-1 text-sm ${
                  level === option ? "border-selected bg-selected text-on-selected" : "border-line bg-surface text-ink hover:bg-hover"
                }`}
              >
                {option === "all" ? "Hammasi" : LEVEL_LABEL[option]}
                <span className="ml-1 opacity-70">{counts[option]}</span>
              </button>
            ))}
          </div>
          <select
            value={status}
            onChange={(event) => {
              setStatus(event.target.value as Status);
              setPage(0);
            }}
            aria-label="Holat"
            className="h-8 rounded-md border border-line bg-surface px-2 text-sm text-ink"
          >
            <option value="all">Barcha savollar</option>
            <option value="open">Yechilmaganlar</option>
            <option value="solved">Yechilganlar</option>
          </select>
          <Link href={`/varaq?dars=${encodeURIComponent(code)}${level === "all" ? "" : `&daraja=${level}`}`} className="btn ml-auto h-8 text-xs">
            <Printer className="size-3.5" aria-hidden />
            Varaq qilish
          </Link>
        </div>
        <div className="flex items-center gap-3">
          <div className="h-2 flex-1 overflow-hidden rounded-full bg-hover" aria-hidden>
            <div className="h-full rounded-full bg-good transition-[width]" style={{ width: `${solved}%` }} />
          </div>
          <span className="text-sm font-semibold text-ink tabular-nums">{solved}/100 yechildi</span>
          {solved > 0 && (
            <button
              type="button"
              onClick={() => {
                if (window.confirm("Shu darsdagi bank natijalarini o'chirasizmi?")) resetBank(code);
              }}
              className="inline-flex items-center gap-1 text-xs text-ink-muted hover:text-ink"
              title="Natijalarni tozalash"
            >
              <RotateCcw className="size-3.5" aria-hidden />
              <span className="sr-only sm:not-sr-only">Tozalash</span>
            </button>
          )}
        </div>
      </div>

      {filtered.length === 0 ? (
        <p className="card p-6 text-center text-ink-muted">Bu tanlovda savol qolmadi.</p>
      ) : (
        <ol className="space-y-3">
          {pageItems.map((item) => {
            const key = keyById.get(item.id);
            const state = results[item.id];
            return (
              <li key={item.id} className="avoid-break card p-4">
                <div className="mb-1.5 flex items-center gap-2 text-xs font-semibold tracking-wide">
                  <span className="text-brand">#{item.id}</span>
                  <span className="chip py-0">{LEVEL_LABEL[item.level] ?? item.level}</span>
                  {state === "ok" && (
                    <span className="ml-auto inline-flex items-center gap-1 text-good">
                      <Check className="size-3.5" aria-hidden /> yechilgan
                    </span>
                  )}
                  {state === "no" && <span className="ml-auto text-bad">urinib ko&apos;rilgan</span>}
                </div>
                <Prompt en={item.promptEn} uz={item.promptUz} />
                {answerMode && <AnswerForm code={code} id={item.id} solved={state === "ok"} />}
                {key && <KeyPanel answer={key.answer} en={key.solutionEn} uz={key.solutionUz} />}
              </li>
            );
          })}
        </ol>
      )}
      <KeyStatus state={keys.state} />

      {pageCount > 1 && (
        <nav className="no-print mt-5 flex flex-wrap items-center justify-center gap-1.5" aria-label="Sahifalar">
          <button type="button" className="btn size-9 px-0" disabled={current === 0} onClick={() => goTo(current - 1)} aria-label="Oldingi sahifa">
            <ChevronLeft className="size-4" aria-hidden />
          </button>
          {Array.from({ length: pageCount }, (_, index) => (
            <button
              key={index}
              type="button"
              onClick={() => goTo(index)}
              aria-current={index === current ? "page" : undefined}
              className={`size-9 rounded-lg border text-sm font-semibold ${
                index === current ? "border-selected bg-selected text-on-selected" : "border-line bg-surface text-ink hover:bg-hover"
              }`}
            >
              {index + 1}
            </button>
          ))}
          <button
            type="button"
            className="btn size-9 px-0"
            disabled={current >= pageCount - 1}
            onClick={() => goTo(current + 1)}
            aria-label="Keyingi sahifa"
          >
            <ChevronRight className="size-4" aria-hidden />
          </button>
        </nav>
      )}
    </>
  );
}
