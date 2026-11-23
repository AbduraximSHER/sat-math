"use client";

import { Eye, ListOrdered, StepForward } from "lucide-react";
import { useState } from "react";
import { M, Prompt } from "@/components/text";
import type { Example } from "@/lib/guide";

/** A worked example. In step mode the class sees one step at a time, then the answer. */
export function ExampleCard({ example, index, id }: { example: Example; index: number; id: string }) {
  const sat = example.kind === "sat";
  const total = example.steps.length;
  const [stepMode, setStepMode] = useState(false);
  const [shown, setShown] = useState(1);
  const visible = stepMode ? shown : total;

  return (
    <section
      id={id}
      className={`avoid-break my-8 scroll-mt-20 rounded-2xl border p-5 sm:p-6 ${
        sat ? "border-sat-line bg-sat-bg" : "border-found-line bg-found-bg"
      }`}
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="font-serif text-2xl text-heading">
          Misol {index + 1}
          <span className="ml-2 align-middle text-sm font-sans font-bold tracking-wide text-ink-muted">
            {sat ? "SAT USLUBI" : "FOUNDATION"}
          </span>
        </h2>
        <button
          type="button"
          onClick={() => {
            setStepMode(!stepMode);
            setShown(1);
          }}
          aria-pressed={stepMode}
          className="no-print btn h-8 text-xs"
          title="Sinfda qadamlarni birma-bir ochish"
        >
          <ListOrdered className="size-3.5" aria-hidden />
          {stepMode ? "Hammasini ko'rsatish" : "Qadamma-qadam"}
        </button>
      </div>

      <div className="mt-4 rounded-xl border border-line bg-surface p-4">
        <Prompt en={example.promptEn} uz={example.promptUz} />
        {example.gloss && (
          <p className="mt-2 text-sm italic text-ink-muted">
            So&apos;zlar: <M>{example.gloss}</M>
          </p>
        )}
        {example.choices.length > 0 && (
          <ul className="mt-3 grid gap-1.5 sm:grid-cols-2">
            {example.choices.map((choice) => (
              <li key={choice.letter} className="flex gap-2 rounded-lg border border-line bg-surface-2 px-3 py-1.5">
                <span className="font-bold text-heading">{choice.letter}</span>
                <span>
                  <span lang="en" className="lang-en">
                    <M>{choice.en}</M>
                  </span>
                  <span className="lang-both text-ink-muted"> / </span>
                  <span lang="uz" className="lang-uz text-uz">
                    <M>{choice.uz}</M>
                  </span>
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <ol className="mt-5 space-y-3">
        {example.steps.slice(0, visible).map((step, stepIndex) => (
          <li key={stepIndex} className="flex gap-3 leading-relaxed">
            <span className="mt-0.5 inline-flex size-6 shrink-0 items-center justify-center rounded-full bg-surface text-xs font-bold text-heading ring-1 ring-line">
              {stepIndex + 1}
            </span>
            <span className="min-w-0">
              <span lang="en" className="lang-en block">
                <M>{step.en}</M>
              </span>
              <span lang="uz" className="lang-uz block text-uz">
                <M>{step.uz}</M>
              </span>
            </span>
          </li>
        ))}
      </ol>

      {stepMode && shown < total && (
        <div className="no-print mt-4 flex flex-wrap gap-2">
          <button type="button" className="btn-primary" onClick={() => setShown(shown + 1)}>
            <StepForward className="size-4" aria-hidden />
            Keyingi qadam ({shown + 1}/{total})
          </button>
          <button type="button" className="btn" onClick={() => setShown(total)}>
            <Eye className="size-4" aria-hidden />
            Javobgacha ochish
          </button>
        </div>
      )}

      {visible === total && (
        <p className="mt-5 rounded-lg bg-surface px-4 py-2.5 font-semibold text-heading ring-1 ring-line">
          Javob: <M>{example.answer}</M>
        </p>
      )}
    </section>
  );
}
