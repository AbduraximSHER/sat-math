/** Search over lessons, glossary terms and pages. Shared by the index route and the dialog. */

export type SearchEntry = {
  kind: "lesson" | "term" | "page";
  href: string;
  title: string;
  subtitle: string;
  badge: string;
  text: string;
};

/** Lowercase, unify apostrophes (o' oʻ o’), drop accents. */
export function fold(text: string): string {
  return text
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[ʻʼ’‘`´]/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

export function slug(text: string): string {
  return fold(text)
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export function searchEntries(entries: SearchEntry[], query: string, limit = 24): SearchEntry[] {
  const words = fold(query).split(" ").filter(Boolean);
  if (words.length === 0) return [];
  const scored: { entry: SearchEntry; score: number }[] = [];
  for (const entry of entries) {
    const title = fold(entry.title);
    const haystack = fold(`${entry.badge} ${entry.title} ${entry.subtitle} ${entry.text}`);
    if (!words.every((word) => haystack.includes(word))) continue;
    let score = 0;
    const whole = words.join(" ");
    if (fold(entry.badge) === whole) score += 100;
    if (title.startsWith(whole)) score += 40;
    if (title.includes(whole)) score += 20;
    score += words.filter((word) => title.includes(word)).length * 5;
    if (entry.kind === "lesson") score += 3;
    if (entry.kind === "page") score += 2;
    scored.push({ entry, score });
  }
  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((item) => item.entry);
}
