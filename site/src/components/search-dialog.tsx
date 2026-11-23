"use client";

import { Dialog } from "@base-ui/react/dialog";
import { BookOpen, FileText, Languages, Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState, useSyncExternalStore } from "react";
import { createStore } from "@/lib/local-store";
import { searchEntries, type SearchEntry } from "@/lib/search";

const searchOpen = createStore<boolean>(() => false, () => undefined, false);
export const openSearch = () => searchOpen.set(true);

let indexPromise: Promise<SearchEntry[]> | null = null;
function loadIndex(): Promise<SearchEntry[]> {
  indexPromise ??= fetch("/search-index.json")
    .then((response) => (response.ok ? (response.json() as Promise<SearchEntry[]>) : []))
    .catch(() => {
      indexPromise = null;
      return [];
    });
  return indexPromise;
}

const ICONS = { lesson: BookOpen, term: Languages, page: FileText };
const KIND_LABEL = { lesson: "Dars", term: "Atama", page: "Sahifa" };

export function SearchButton() {
  return (
    <button
      type="button"
      onClick={openSearch}
      title="Qidirish (/ yoki Ctrl K)"
      className="inline-flex h-9 items-center gap-2 rounded-lg border border-line bg-surface px-2.5 text-sm text-ink-muted transition-colors hover:bg-hover md:w-56"
    >
      <Search className="size-4" aria-hidden />
      <span className="hidden md:inline">Dars yoki atama…</span>
      <kbd className="ml-auto hidden rounded border border-line px-1.5 font-sans text-[0.7rem] md:inline">/</kbd>
      <span className="sr-only md:hidden">Qidirish</span>
    </button>
  );
}

export function SearchDialog() {
  const open = useSyncExternalStore(searchOpen.subscribe, searchOpen.get, searchOpen.getServer);
  const [entries, setEntries] = useState<SearchEntry[]>([]);
  const [query, setQuery] = useState("");
  const [active, setActive] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  const list = useRef<HTMLUListElement>(null);
  const router = useRouter();

  useEffect(() => {
    if (open) void loadIndex().then(setEntries);
  }, [open]);

  const results = useMemo(() => searchEntries(entries, query), [entries, query]);

  function go(entry: SearchEntry | undefined) {
    if (!entry) return;
    searchOpen.set(false);
    setQuery("");
    router.push(entry.href);
  }

  function onKeyDown(event: React.KeyboardEvent) {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      const next = (active + (event.key === "ArrowDown" ? 1 : -1) + results.length) % Math.max(1, results.length);
      setActive(next);
      list.current?.querySelector<HTMLElement>(`[data-index="${next}"]`)?.scrollIntoView({ block: "nearest" });
    } else if (event.key === "Enter") {
      event.preventDefault();
      go(results[active]);
    }
  }

  return (
    <Dialog.Root
      open={open}
      onOpenChange={(next) => {
        searchOpen.set(next);
        if (!next) setQuery("");
      }}
    >
      <Dialog.Portal>
        <Dialog.Backdrop className="fixed inset-0 z-50 bg-black/45 backdrop-blur-[2px]" />
        <Dialog.Popup
          initialFocus={input}
          className="fixed top-[8vh] left-1/2 z-50 flex max-h-[80vh] w-[min(94vw,40rem)] -translate-x-1/2 flex-col overflow-hidden rounded-2xl border border-line bg-surface shadow-2xl"
        >
          <Dialog.Title className="sr-only">Qidirish</Dialog.Title>
          <div className="flex items-center gap-3 border-b border-line px-4">
            <Search className="size-5 shrink-0 text-ink-muted" aria-hidden />
            <input
              ref={input}
              value={query}
              onChange={(event) => {
                setQuery(event.target.value);
                setActive(0);
              }}
              onKeyDown={onKeyDown}
              placeholder="qiyalik, slope, 2.6, foiz…"
              className="h-14 w-full bg-transparent text-lg text-ink outline-none placeholder:text-ink-muted/70"
              role="combobox"
              aria-expanded={results.length > 0}
              aria-controls="search-results"
              aria-activedescendant={results[active] ? `search-${active}` : undefined}
            />
            <kbd className="hidden rounded border border-line px-1.5 text-xs text-ink-muted sm:inline">Esc</kbd>
          </div>
          <ul ref={list} id="search-results" role="listbox" className="overflow-y-auto p-2">
            {query && results.length === 0 && (
              <li className="px-3 py-6 text-center text-sm text-ink-muted">
                Hech narsa topilmadi. Inglizcha yoki o&apos;zbekcha nomini sinab ko&apos;ring.
              </li>
            )}
            {!query && (
              <li className="px-3 py-6 text-center text-sm text-ink-muted">
                Dars nomi, raqami (2.6) yoki atama yozing. Har ikki tilda qidiradi.
              </li>
            )}
            {results.map((entry, index) => {
              const Icon = ICONS[entry.kind];
              return (
                <li
                  key={`${entry.kind}-${entry.href}`}
                  id={`search-${index}`}
                  data-index={index}
                  role="option"
                  aria-selected={index === active}
                  onMouseMove={() => setActive(index)}
                  onClick={() => go(entry)}
                  className={`flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2.5 ${
                    index === active ? "bg-hover" : ""
                  }`}
                >
                  <Icon className="size-4 shrink-0 text-brand" aria-hidden />
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium text-ink">
                      {entry.badge && <span className="mr-1.5 font-semibold text-brand">{entry.badge}</span>}
                      {entry.title}
                    </span>
                    <span className="block truncate text-sm text-ink-muted">{entry.subtitle}</span>
                  </span>
                  <span className="chip shrink-0">{KIND_LABEL[entry.kind]}</span>
                </li>
              );
            })}
          </ul>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
