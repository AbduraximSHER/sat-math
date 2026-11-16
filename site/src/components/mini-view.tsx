"use client";

import { useEffect, useState } from "react";
import { Pair, showLang } from "@/components/text";
import { usePrefs } from "@/components/prefs";
import type { MiniItem } from "@/lib/guide";
import type { MiniKey } from "@/lib/keys";

export function MiniView({ items }: { items: MiniItem[] }) {
  const { lang, showKeys } = usePrefs();
  const [keys, setKeys] = useState<Record<number, MiniKey> | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!showKeys) {
      setKeys(null);
      setError(false);
      return;
    }
    let cancelled = false;
    fetch("/api/keys?mini=1")
      .then(async (response) => {
        if (!response.ok) throw new Error("keys");
        return response.json();
      })
      .then((data: { mini: MiniKey[] }) => {
        if (cancelled) return;
        const map: Record<number, MiniKey> = {};
        for (const row of data.mini ?? []) map[row.number] = row;
        setKeys(map);
      })
      .catch(() => {
        if (!cancelled) setError(true);
      });
    return () => {
      cancelled = true;
    };
  }, [showKeys]);

  return (
    <article>
      <h1 className="font-serif text-4xl text-[var(--navy)]">Aralash mini-test</h1>
      <div className="mt-4">
        <Pair
          en="Twenty original questions. Give the class 35 minutes. This is not a scored practice test and it does not predict a scaled score. It shows which domain still wobbles. Turn the key off before you project the questions."
          uz="Yigirma original savol. Sinfga 35 daqiqa bering. Bu baholanadigan sinov emas va scaled ballni bashorat qilmaydi. Qaysi domen hali qaltisligini ko'rsatadi. Savollarni ekranga chiqarishdan oldin kalitni yoping."
        />
      </div>
      <ol className="mt-8 space-y-6">
        {items.map((item) => {
          const key = keys?.[item.number];
          return (
            <li key={item.number} className="rounded-xl border border-[#e4ddd0] bg-white p-4">
              <p className="text-xs font-semibold tracking-wide text-[var(--teal)]">
                {item.number}. {item.domain}
              </p>
              {showLang(lang, "en") && <p className="mt-2 text-[16.5px] leading-relaxed">{item.promptEn}</p>}
              {showLang(lang, "uz") && (
                <p className="mt-1 text-[16.5px] leading-relaxed text-[#245c59]">{item.promptUz}</p>
              )}
              {item.choices.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {item.choices.map((choice) => (
                    <li key={choice.letter}>
                      {choice.letter}. {showLang(lang, "en") && choice.en}
                      {lang === "both" && " / "}
                      {showLang(lang, "uz") && choice.uz}
                    </li>
                  ))}
                </ul>
              )}
              {showKeys && key && (
                <div className="mt-3 rounded-lg bg-[#f3efe6] p-3">
                  <p className="font-semibold text-[var(--navy)]">{key.answer}</p>
                  {showLang(lang, "en") && <p className="mt-1 text-sm leading-relaxed">{key.analysisEn}</p>}
                  {showLang(lang, "uz") && (
                    <p className="mt-1 text-sm leading-relaxed text-[#245c59]">{key.analysisUz}</p>
                  )}
                </div>
              )}
            </li>
          );
        })}
      </ol>
      {showKeys && error && (
        <p className="mt-4 text-sm text-[#8c2f2f]">Kalitni yuklab bo&apos;lmadi. Sahifani yangilang.</p>
      )}
    </article>
  );
}
