"use client";

import type { Block } from "@/lib/guide";
import { usePrefs, type Lang } from "@/components/prefs";

export function showLang(lang: Lang, which: "en" | "uz"): boolean {
  return lang === "both" || lang === which;
}

export function Blocks({ items }: { items: Block[] }) {
  return (
    <div className="space-y-3">
      {items.map((block, index) => {
        if (block.type === "formula") {
          return (
            <p key={index} className="text-center font-serif text-lg text-[var(--navy)]">
              {block.text}
            </p>
          );
        }
        if (block.type === "say") {
          return (
            <blockquote
              key={index}
              className="border-l-4 border-[var(--teal)] bg-[#f3faf9] px-4 py-3 text-[15px] leading-relaxed"
            >
              {block.text}
            </blockquote>
          );
        }
        return (
          <p key={index} className="text-[16.5px] leading-[1.65] text-[var(--ink)]">
            {block.text}
          </p>
        );
      })}
    </div>
  );
}

export function Pair({
  en,
  uz,
  enBlocks,
  uzBlocks,
}: {
  en?: string;
  uz?: string;
  enBlocks?: Block[];
  uzBlocks?: Block[];
}) {
  const { lang } = usePrefs();
  return (
    <div className="space-y-4">
      {showLang(lang, "en") && (
        <div>
          {lang === "both" && <p className="mb-1 text-xs font-semibold tracking-wide text-[var(--navy)]">ENGLISH</p>}
          {enBlocks ? <Blocks items={enBlocks} /> : <p className="text-[16.5px] leading-[1.65]">{en}</p>}
        </div>
      )}
      {showLang(lang, "uz") && (
        <div>
          {lang === "both" && <p className="mb-1 text-xs font-semibold tracking-wide text-[var(--teal)]">O&apos;ZBEKCHA</p>}
          {uzBlocks ? <Blocks items={uzBlocks} /> : <p className="text-[16.5px] leading-[1.65] text-[#245c59]">{uz}</p>}
        </div>
      )}
    </div>
  );
}
