"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { usePrefs, type Lang } from "@/components/prefs";

type IndexUnit = {
  code: string;
  titleEn: string;
  titleUz: string;
  lessons: { code: string; titleEn: string; titleUz: string }[];
};

const LANGS: { id: Lang; label: string }[] = [
  { id: "both", label: "Ikkalasi" },
  { id: "en", label: "English" },
  { id: "uz", label: "O'zbekcha" },
];

export function Shell({
  units,
  children,
}: {
  units: IndexUnit[];
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { lang, setLang, showKeys, setShowKeys } = usePrefs();
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)]">
      <header className="sticky top-0 z-30 border-b border-[#e4ddd0] bg-[#f7f4ec]/95 backdrop-blur">
        <div className="flex flex-wrap items-center gap-3 px-4 py-3 lg:px-6">
          <Button variant="outline" className="lg:hidden" onClick={() => setOpen(true)}>
            Darslar
          </Button>
          <Link href="/" className="font-serif text-xl text-[var(--navy)]">
            SAT Math
          </Link>
          <p className="hidden text-sm text-[var(--muted-ink)] sm:block">O&apos;qituvchi qo&apos;llanmasi</p>
          <div className="ml-auto flex flex-wrap items-center gap-2">
            <div className="flex rounded-lg border border-[#e4ddd0] bg-white p-0.5">
              {LANGS.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setLang(item.id)}
                  className={`rounded-md px-2.5 py-1 text-sm ${
                    lang === item.id ? "bg-[var(--navy)] text-[#f7f4ec]" : "text-[var(--ink)]"
                  }`}
                  aria-pressed={lang === item.id}
                >
                  {item.label}
                </button>
              ))}
            </div>
            <button
              type="button"
              onClick={() => setShowKeys(!showKeys)}
              aria-pressed={showKeys}
              className={`rounded-lg border px-2.5 py-1.5 text-sm font-medium ${
                showKeys
                  ? "border-[var(--navy)] bg-[var(--navy)] text-[#f7f4ec]"
                  : "border-[#e4ddd0] bg-white text-[var(--ink)] hover:bg-[#efeae0]"
              }`}
            >
              {showKeys ? "Kalit ochiq" : "Kalit yopiq"}
            </button>
          </div>
        </div>
      </header>

      <div className="lg:grid lg:grid-cols-[280px_minmax(0,1fr)]">
        <aside className="sticky top-[65px] hidden h-[calc(100vh-65px)] overflow-y-auto border-r border-[#e4ddd0] bg-[#fbf8f2] px-3 py-4 lg:block">
          <Nav units={units} pathname={pathname} onNavigate={() => undefined} />
        </aside>
        <main className="mx-auto w-full max-w-3xl px-4 py-8 lg:px-10">{children}</main>
      </div>

      {open && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <button className="absolute inset-0 bg-black/40" aria-label="Yopish" onClick={() => setOpen(false)} />
          <div className="absolute inset-y-0 left-0 w-[min(100%,320px)] overflow-y-auto bg-[#fbf8f2] p-4 shadow-xl">
            <div className="mb-3 flex items-center justify-between">
              <p className="font-serif text-lg text-[var(--navy)]">Darslar</p>
              <Button variant="outline" onClick={() => setOpen(false)}>
                Yopish
              </Button>
            </div>
            <Nav units={units} pathname={pathname} onNavigate={() => setOpen(false)} />
          </div>
        </div>
      )}
    </div>
  );
}

function Nav({
  units,
  pathname,
  onNavigate,
}: {
  units: IndexUnit[];
  pathname: string;
  onNavigate: () => void;
}) {
  const links = [
    { href: "/", label: "Kirish" },
    { href: "/formulalar", label: "Formulalar" },
    { href: "/lugat", label: "Atamalar" },
    { href: "/mini", label: "Mini-test" },
  ];
  return (
    <nav className="space-y-5 text-sm">
      <ul className="space-y-1">
        {links.map((link) => (
          <li key={link.href}>
            <Link
              href={link.href}
              onClick={onNavigate}
              className={`block rounded-md px-2 py-1.5 ${
                pathname === link.href ? "bg-[var(--navy)] text-[#f7f4ec]" : "hover:bg-[#efeae0]"
              }`}
            >
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
      {units.map((unit) => (
        <div key={unit.code}>
          <p className="px-2 text-xs font-semibold tracking-wide text-[var(--teal)]">
            {unit.code}-bo&apos;lim. {unit.titleUz}
          </p>
          <ul className="mt-1 space-y-0.5">
            {unit.lessons.map((lesson) => {
              const href = `/dars/${lesson.code}`;
              const active = pathname === href;
              return (
                <li key={lesson.code}>
                  <Link
                    href={href}
                    onClick={onNavigate}
                    className={`block rounded-md px-2 py-1.5 leading-snug ${
                      active ? "bg-[var(--navy)] text-[#f7f4ec]" : "hover:bg-[#efeae0]"
                    }`}
                  >
                    <span className="font-medium">{lesson.code}</span> {lesson.titleUz}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </nav>
  );
}

