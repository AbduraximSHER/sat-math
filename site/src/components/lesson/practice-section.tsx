"use client";

import { M, Prompt } from "@/components/text";
import { useTeacherData } from "@/components/teacher-key";
import type { Practice } from "@/lib/guide";
import type { BankKey, PracticeKey } from "@/lib/keys";

export type LessonKeyData = { practice: PracticeKey[]; bank: BankKey[] };

export function KeyPanel({ answer, en, uz }: { answer: string; en: string; uz: string }) {
  return (
    <div className="mt-3 rounded-lg border border-gold/30 bg-key-bg p-3">
      <p className="font-semibold text-heading">
        <span className="mr-1.5 text-xs font-bold tracking-widest text-gold">KALIT</span>
        <M>{answer}</M>
      </p>
      <p lang="en" className="lang-en mt-1 text-[0.95rem] leading-relaxed">
        <M>{en}</M>
      </p>
      <p lang="uz" className="lang-uz mt-1 text-[0.95rem] leading-relaxed text-uz">
        <M>{uz}</M>
      </p>
    </div>
  );
}

export function KeyStatus({ state }: { state: "off" | "loading" | "ready" | "error" }) {
  if (state === "loading") return <p className="no-print mt-3 text-sm text-ink-muted">Kalit yuklanmoqda…</p>;
  if (state === "error")
    return <p className="no-print mt-3 text-sm text-bad">Kalitni yuklab bo&apos;lmadi. Internetni tekshirib, qayta oching.</p>;
  return null;
}

export function PracticeSection({ code, items }: { code: string; items: Practice[] }) {
  const keys = useTeacherData<LessonKeyData>(`/api/keys?code=${encodeURIComponent(code)}`);
  return (
    <>
      <p className="mb-4 text-sm text-ink-muted">
        Darsning yakuniy beshtasi: birinchi ikkitasi sinfda, qolgani uyga. Javoblar faqat kalit ochiq bo&apos;lganda
        yuklanadi.
      </p>
      <ol className="space-y-3">
        {items.map((item, index) => {
          const key = keys.data?.practice[index];
          return (
            <li key={index} className="avoid-break card flex gap-3 p-4">
              <span className="mt-0.5 inline-flex size-7 shrink-0 items-center justify-center rounded-full bg-surface-2 text-sm font-bold text-heading">
                {index + 1}
              </span>
              <div className="min-w-0 flex-1">
                <Prompt en={item.promptEn} uz={item.promptUz} />
                {item.gloss && (
                  <p className="mt-1.5 text-sm italic text-ink-muted">
                    So&apos;zlar: <M>{item.gloss}</M>
                  </p>
                )}
                {key && <KeyPanel answer={key.answer} en={key.solutionEn} uz={key.solutionUz} />}
              </div>
            </li>
          );
        })}
      </ol>
      <KeyStatus state={keys.state} />
    </>
  );
}
