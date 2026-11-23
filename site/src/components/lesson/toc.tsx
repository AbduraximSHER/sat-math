"use client";

import { useEffect, useState } from "react";

export type TocItem = { id: string; label: string };

/** Sticky "in this lesson" list that follows the reader. */
export function Toc({ items }: { items: TocItem[] }) {
  const [active, setActive] = useState(items[0]?.id);

  useEffect(() => {
    const targets = items
      .map((item) => document.getElementById(item.id))
      .filter((node): node is HTMLElement => node !== null);
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting);
        if (visible.length > 0) {
          visible.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
          setActive(visible[0].target.id);
        }
      },
      { rootMargin: "-80px 0px -65% 0px" },
    );
    targets.forEach((node) => observer.observe(node));
    return () => observer.disconnect();
  }, [items]);

  return (
    <nav aria-label="Bu darsda" className="text-sm">
      <p className="mb-2 text-xs font-bold tracking-widest text-ink-muted">BU DARSDA</p>
      <ul className="space-y-0.5 border-l border-line">
        {items.map((item) => (
          <li key={item.id}>
            <a
              href={`#${item.id}`}
              className={`-ml-px block border-l-2 py-1 pl-3 leading-snug transition-colors ${
                active === item.id ? "border-brand font-semibold text-heading" : "border-transparent text-ink-muted hover:text-ink"
              }`}
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

/** Small screens: the same sections as a row of chips. */
export function TocChips({ items }: { items: TocItem[] }) {
  return (
    <nav aria-label="Bu darsda" className="no-print -mx-1 flex gap-1.5 overflow-x-auto px-1 pb-1 xl:hidden">
      {items.map((item) => (
        <a key={item.id} href={`#${item.id}`} className="chip shrink-0 whitespace-nowrap hover:border-brand hover:text-ink">
          {item.label}
        </a>
      ))}
    </nav>
  );
}
