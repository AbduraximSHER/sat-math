import { Fragment, type ReactNode } from "react";
import type { Block } from "@/lib/guide";

type Part = string | { sup: string };

/** Split "2^(3+2) = 2^5" into text and exponents. Balanced parentheses only. */
export function mathParts(text: string): Part[] {
  if (!text.includes("^")) return [text];
  const parts: Part[] = [];
  let buffer = "";
  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    if (ch === "^" && i > 0) {
      const rest = text.slice(i + 1);
      let exponent: string | null = null;
      let length = 0;
      if (rest.startsWith("(")) {
        let depth = 0;
        for (let j = 0; j < rest.length; j += 1) {
          if (rest[j] === "(") depth += 1;
          if (rest[j] === ")") depth -= 1;
          if (depth === 0) {
            exponent = rest.slice(1, j);
            length = j + 1;
            break;
          }
        }
      } else {
        const match = /^[−-]?\d+(?:\.\d+)?|^[a-zA-Z]/.exec(rest);
        if (match) {
          exponent = match[0];
          length = match[0].length;
        }
      }
      if (exponent !== null && exponent.length > 0) {
        if (buffer) parts.push(buffer);
        parts.push({ sup: exponent });
        buffer = "";
        i += 1 + length;
        continue;
      }
    }
    buffer += ch;
    i += 1;
  }
  if (buffer) parts.push(buffer);
  return parts;
}

/** Math-aware text: exponents written with ^ become real superscripts. */
export function M({ children }: { children: string | undefined | null }): ReactNode {
  if (!children) return null;
  const parts = mathParts(children);
  if (parts.length === 1 && typeof parts[0] === "string") return parts[0];
  return parts.map((part, index) =>
    typeof part === "string" ? (
      <Fragment key={index}>{part}</Fragment>
    ) : (
      <sup key={index}>
        <M>{part.sup}</M>
      </sup>
    ),
  );
}

export function Blocks({ items, uz = false }: { items: Block[]; uz?: boolean }) {
  return (
    <div className="space-y-3">
      {items.map((block, index) => {
        if (block.type === "formula") {
          return (
            <p
              key={index}
              className="rounded-lg bg-surface-2 px-4 py-2.5 text-center font-serif text-[1.15rem] text-heading"
            >
              <M>{block.text}</M>
            </p>
          );
        }
        if (block.type === "say") {
          return (
            <blockquote
              key={index}
              className="rounded-r-lg border-l-4 border-brand bg-say-bg px-4 py-3 text-[0.97rem] leading-relaxed"
            >
              <span className="mb-1 block text-[0.7rem] font-bold tracking-widest text-brand">AYTING · SAY</span>
              <M>{block.text}</M>
            </blockquote>
          );
        }
        return (
          <p key={index} className={`prose-text ${uz ? "text-uz" : "text-ink"}`}>
            <M>{block.text}</M>
          </p>
        );
      })}
    </div>
  );
}

/** English and Uzbek side by side; the language switch hides one with CSS. */
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
  return (
    <div className="space-y-4">
      <div lang="en" className="lang-en">
        <p className="lang-both mb-1 text-[0.7rem] font-bold tracking-widest text-heading">ENGLISH</p>
        {enBlocks ? (
          <Blocks items={enBlocks} />
        ) : (
          <p className="prose-text">
            <M>{en}</M>
          </p>
        )}
      </div>
      <div lang="uz" className="lang-uz">
        <p className="lang-both mb-1 text-[0.7rem] font-bold tracking-widest text-brand">O&apos;ZBEKCHA</p>
        {uzBlocks ? (
          <Blocks items={uzBlocks} uz />
        ) : (
          <p className="prose-text text-uz">
            <M>{uz}</M>
          </p>
        )}
      </div>
    </div>
  );
}

/** A short prompt in both languages, stacked tightly. */
export function Prompt({ en, uz, className = "" }: { en: string; uz: string; className?: string }) {
  return (
    <div className={className}>
      <p lang="en" className="lang-en font-medium leading-relaxed text-ink">
        <M>{en}</M>
      </p>
      <p lang="uz" className="lang-uz mt-0.5 leading-relaxed text-uz">
        <M>{uz}</M>
      </p>
    </div>
  );
}
