import { NextResponse } from "next/server";
import { guide } from "@/lib/guide";
import { slug, type SearchEntry } from "@/lib/search";

export const dynamic = "force-static";

/** Built once at build time; the search dialog loads it on first open. */
export function GET() {
  const pages: SearchEntry[] = [
    { kind: "page", href: "/", title: "Kirish", subtitle: "Bosh sahifa", badge: "", text: "home start boshlash" },
    { kind: "page", href: "/formulalar", title: "Formulalar", subtitle: "Formula varaqasi", badge: "", text: "formula reference sheet area volume circle" },
    { kind: "page", href: "/lugat", title: "Atamalar", subtitle: "Inglizcha–o'zbekcha lug'at", badge: "", text: "glossary dictionary terms lugat" },
    { kind: "page", href: "/mini", title: "Mini-test", subtitle: "20 savollik aralash sinov", badge: "", text: "test quiz mixed review sinov" },
    { kind: "page", href: "/varaq", title: "Mashq varag'i", subtitle: "Bankdan chop etiladigan varaq", badge: "", text: "worksheet print chop varaq" },
  ];
  const lessons: SearchEntry[] = guide.units.flatMap((unit) =>
    unit.lessons.map((lesson) => ({
      kind: "lesson" as const,
      href: `/dars/${lesson.code}`,
      title: lesson.titleUz,
      subtitle: lesson.titleEn,
      badge: lesson.code,
      text: `${unit.titleUz} ${unit.titleEn} ${lesson.goalUz} ${lesson.goalEn}`,
    })),
  );
  const terms: SearchEntry[] = guide.glossary.map((row) => ({
    kind: "term" as const,
    href: `/lugat#t-${slug(row.en)}`,
    title: row.en,
    subtitle: row.uz,
    badge: "",
    text: row.hint,
  }));
  return NextResponse.json([...pages, ...lessons, ...terms]);
}
