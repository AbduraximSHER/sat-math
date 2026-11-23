"use client";

import { Dialog } from "@base-ui/react/dialog";
import { BookA, CheckCircle2, ClipboardCheck, Home, Menu, Printer, Sigma, X } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { cycleLang, prefsStore, PrefsEffects, setFocus, setLang, setTheme, stepFont, usePrefs, type Lang } from "@/components/prefs";
import { openSearch, SearchButton, SearchDialog } from "@/components/search-dialog";
import { openShortcuts, SettingsMenu, ShortcutsDialog } from "@/components/settings-menu";
import { KeyToggle, PinDialog, toggleKeys } from "@/components/teacher-key";
import { useProgress } from "@/lib/progress";

export type IndexUnit = {
  code: string;
  titleEn: string;
  titleUz: string;
  lessons: { code: string; titleEn: string; titleUz: string }[];
};

const LANGS: { id: Lang; label: string; title: string }[] = [
  { id: "both", label: "UZ+EN", title: "Ikkala til" },
  { id: "uz", label: "UZ", title: "Faqat o'zbekcha" },
  { id: "en", label: "EN", title: "Faqat inglizcha" },
];

const LINKS = [
  { href: "/", label: "Kirish", icon: Home },
  { href: "/formulalar", label: "Formulalar", icon: Sigma },
  { href: "/lugat", label: "Atamalar", icon: BookA },
  { href: "/mini", label: "Mini-test", icon: ClipboardCheck },
  { href: "/varaq", label: "Mashq varag'i", icon: Printer },
];

export function LogoMark({ className = "size-7" }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden>
      <rect width="32" height="32" rx="8" fill="#1b3a4b" />
      <rect x="7" y="8.5" width="18" height="4" rx="1" fill="#f7f4ec" />
      <rect x="7" y="14" width="18" height="4" rx="1" fill="#2e9c97" />
      <rect x="7" y="19.5" width="18" height="4" rx="1" fill="#f7f4ec" />
    </svg>
  );
}

function LangSwitch() {
  const { lang } = usePrefs();
  return (
    <div className="flex h-9 rounded-lg border border-line bg-surface p-0.5" role="group" aria-label="Til">
      {LANGS.map((item) => (
        <button
          key={item.id}
          type="button"
          onClick={() => setLang(item.id)}
          title={item.title}
          aria-pressed={lang === item.id}
          className={`rounded-md px-2 text-xs font-bold tracking-wide sm:px-2.5 ${
            lang === item.id ? "bg-selected text-on-selected" : "text-ink-muted hover:text-ink"
          }`}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}

function useShortcuts(units: IndexUnit[]) {
  const pathname = usePathname();
  const router = useRouter();
  useEffect(() => {
    const order = units.flatMap((unit) => unit.lessons.map((lesson) => lesson.code));
    function onKey(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        openSearch();
        return;
      }
      const target = event.target as HTMLElement | null;
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      if (target?.closest("input, textarea, select, [contenteditable='true']")) return;
      if (document.querySelector("[role='dialog']")) return;
      const current = pathname.startsWith("/dars/") ? decodeURIComponent(pathname.slice(6)) : null;
      const index = current ? order.indexOf(current) : -1;
      switch (event.key) {
        case "/":
          event.preventDefault();
          openSearch();
          break;
        case "ArrowLeft":
          if (index > 0) router.push(`/dars/${order[index - 1]}`);
          break;
        case "ArrowRight":
          if (index >= 0 && index < order.length - 1) router.push(`/dars/${order[index + 1]}`);
          break;
        case "k":
        case "K":
          void toggleKeys();
          break;
        case "l":
        case "L":
          cycleLang();
          break;
        case "f":
        case "F":
          setFocus(!prefsStore.get().focus);
          break;
        case "+":
        case "=":
          stepFont(1);
          break;
        case "-":
          stepFont(-1);
          break;
        case "0":
          stepFont(0);
          break;
        case "t":
        case "T":
          setTheme(document.documentElement.classList.contains("dark") ? "light" : "dark");
          break;
        case "?":
          openShortcuts();
          break;
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [pathname, router, units]);
}

function useServiceWorker() {
  useEffect(() => {
    if (process.env.NODE_ENV !== "production" || !("serviceWorker" in navigator)) return;
    const register = () => navigator.serviceWorker.register("/sw.js").catch(() => undefined);
    if (document.readyState === "complete") register();
    else window.addEventListener("load", register, { once: true });
  }, []);
}

export function Shell({ units, children }: { units: IndexUnit[]; children: React.ReactNode }) {
  const pathname = usePathname();
  const [drawer, setDrawer] = useState(false);
  useShortcuts(units);
  useServiceWorker();

  return (
    <div className="min-h-dvh bg-paper text-ink">
      <a
        href="#main"
        className="sr-only z-50 rounded-lg bg-selected px-4 py-2 text-on-selected focus:not-sr-only focus:fixed focus:top-2 focus:left-2"
      >
        Asosiy matnga o&apos;tish
      </a>
      <header className="no-print sticky top-0 z-30 border-b border-line bg-raised/90 backdrop-blur supports-[backdrop-filter]:bg-raised/80">
        <div className="flex h-14 items-center gap-2 px-3 sm:gap-3 lg:px-5">
          <button
            type="button"
            onClick={() => setDrawer(true)}
            className="menu-button inline-flex size-9 items-center justify-center rounded-lg border border-line bg-surface text-ink hover:bg-hover lg:hidden"
            aria-label="Darslar ro'yxati"
          >
            <Menu className="size-5" aria-hidden />
          </button>
          <Link href="/" className="flex items-center gap-2.5" aria-label="SAT Math, bosh sahifa">
            <LogoMark />
            <span className="hidden font-serif text-xl leading-none text-heading sm:inline">SAT Math</span>
          </Link>
          <span className="hidden text-sm text-ink-muted xl:inline">O&apos;qituvchi qo&apos;llanmasi</span>
          <div className="ml-auto flex items-center gap-1.5 sm:gap-2">
            <SearchButton />
            <LangSwitch />
            <KeyToggle />
            <SettingsMenu />
          </div>
        </div>
      </header>

      <div className="app-grid lg:grid lg:grid-cols-[17.5rem_minmax(0,1fr)]">
        <aside className="focus-hide no-print sticky top-14 hidden h-[calc(100dvh-3.5rem)] overflow-y-auto border-r border-line bg-raised px-3 py-4 lg:block">
          <Nav units={units} pathname={pathname} />
        </aside>
        <main id="main" className="app-main mx-auto w-full max-w-[70rem] px-4 pt-8 pb-16 sm:px-6 lg:px-10">
          {children}
          <footer className="no-print mt-16 border-t border-line pt-6 text-sm leading-relaxed text-ink-muted">
            Original darslar va savollar. College Board bilan bog&apos;liq emas. Har bir kalit javob SymPy bilan qayta
            hisoblangan.
          </footer>
        </main>
      </div>

      <Dialog.Root open={drawer} onOpenChange={setDrawer}>
        <Dialog.Portal>
          <Dialog.Backdrop className="fixed inset-0 z-40 bg-black/45" />
          <Dialog.Popup className="fixed inset-y-0 left-0 z-50 w-[min(88vw,20rem)] overflow-y-auto bg-raised p-4 shadow-2xl outline-none">
            <div className="mb-3 flex items-center justify-between">
              <Dialog.Title className="font-serif text-lg text-heading">Darslar</Dialog.Title>
              <Dialog.Close className="inline-flex size-9 items-center justify-center rounded-lg border border-line bg-surface hover:bg-hover">
                <X className="size-4" aria-hidden />
                <span className="sr-only">Yopish</span>
              </Dialog.Close>
            </div>
            <Nav units={units} pathname={pathname} onNavigate={() => setDrawer(false)} />
          </Dialog.Popup>
        </Dialog.Portal>
      </Dialog.Root>

      <SearchDialog />
      <PinDialog />
      <ShortcutsDialog />
      <PrefsEffects />
    </div>
  );
}

function Nav({ units, pathname, onNavigate }: { units: IndexUnit[]; pathname: string; onNavigate?: () => void }) {
  const progress = useProgress();
  const box = useRef<HTMLElement>(null);
  const total = units.reduce((sum, unit) => sum + unit.lessons.length, 0);
  const doneCount = units.reduce(
    (sum, unit) => sum + unit.lessons.filter((lesson) => progress.done[lesson.code]).length,
    0,
  );

  useEffect(() => {
    // Center the open lesson in the list, without scrolling the page itself.
    const list = box.current;
    const active = list?.querySelector<HTMLElement>("ul ul [aria-current='page'], div > ul [aria-current='page']");
    const scroller = list?.parentElement;
    if (!list || !active || !scroller) return;
    const top = active.getBoundingClientRect().top - scroller.getBoundingClientRect().top + scroller.scrollTop;
    scroller.scrollTop = Math.max(0, top - scroller.clientHeight / 2 + active.offsetHeight / 2);
  }, [pathname]);

  return (
    <nav ref={box} className="space-y-5 text-sm" aria-label="Sayt bo'limlari">
      <ul className="space-y-0.5">
        {LINKS.map(({ href, label, icon: Icon }) => {
          const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <li key={href}>
              <Link
                href={href}
                onClick={onNavigate}
                aria-current={active ? "page" : undefined}
                className={`flex items-center gap-2.5 rounded-md px-2 py-1.5 ${
                  active ? "bg-selected text-on-selected" : "text-ink hover:bg-hover"
                }`}
              >
                <Icon className="size-4 opacity-80" aria-hidden />
                {label}
              </Link>
            </li>
          );
        })}
      </ul>

      <div className="rounded-lg border border-line bg-surface px-3 py-2.5">
        <div className="flex items-baseline justify-between text-xs">
          <span className="font-semibold text-ink">O&apos;tilgan darslar</span>
          <span className="text-ink-muted">
            {doneCount}/{total}
          </span>
        </div>
        <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-hover">
          <div className="h-full rounded-full bg-brand transition-[width]" style={{ width: `${(doneCount / total) * 100}%` }} />
        </div>
      </div>

      {units.map((unit) => {
        const unitDone = unit.lessons.filter((lesson) => progress.done[lesson.code]).length;
        return (
          <div key={unit.code}>
            <p className="flex items-baseline justify-between gap-2 px-2 text-xs font-semibold tracking-wide text-brand">
              <span>
                {unit.code}-bo&apos;lim. {unit.titleUz}
              </span>
              {unitDone > 0 && (
                <span className="shrink-0 font-normal text-ink-muted">
                  {unitDone}/{unit.lessons.length}
                </span>
              )}
            </p>
            <ul className="mt-1 space-y-0.5">
              {unit.lessons.map((lesson) => {
                const href = `/dars/${lesson.code}`;
                const active = pathname === href;
                const done = Boolean(progress.done[lesson.code]);
                return (
                  <li key={lesson.code}>
                    <Link
                      href={href}
                      onClick={onNavigate}
                      aria-current={active ? "page" : undefined}
                      className={`flex items-start gap-2 rounded-md px-2 py-1.5 leading-snug ${
                        active ? "bg-selected text-on-selected" : "text-ink hover:bg-hover"
                      }`}
                    >
                      <span className={`w-8 shrink-0 font-semibold tabular-nums ${active ? "" : "text-ink-muted"}`}>
                        {lesson.code}
                      </span>
                      <span className="min-w-0 flex-1">{lesson.titleUz}</span>
                      {done && (
                        <CheckCircle2
                          className={`mt-0.5 size-4 shrink-0 ${active ? "" : "text-good"}`}
                          aria-label="o'tilgan"
                        />
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        );
      })}
    </nav>
  );
}
