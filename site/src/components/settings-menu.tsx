"use client";

import { Dialog } from "@base-ui/react/dialog";
import { Popover } from "@base-ui/react/popover";
import { Keyboard, Minus, Monitor, Moon, Plus, Settings2, Sun } from "lucide-react";
import { useSyncExternalStore } from "react";
import {
  setAnswerMode,
  setFocus,
  setTheme,
  stepFont,
  usePrefs,
  type Theme,
} from "@/components/prefs";
import { createStore } from "@/lib/local-store";

const shortcutsOpen = createStore<boolean>(() => false, () => undefined, false);
export const openShortcuts = () => shortcutsOpen.set(true);

const THEMES: { id: Theme; label: string; icon: typeof Sun }[] = [
  { id: "system", label: "Tizim", icon: Monitor },
  { id: "light", label: "Yorug'", icon: Sun },
  { id: "dark", label: "Qorong'i", icon: Moon },
];

function Switch({ checked, onChange, label, hint }: { checked: boolean; onChange: (value: boolean) => void; label: string; hint: string }) {
  return (
    <label className="flex cursor-pointer items-start justify-between gap-3 py-2">
      <span>
        <span className="block text-sm font-medium text-ink">{label}</span>
        <span className="block text-xs leading-snug text-ink-muted">{hint}</span>
      </span>
      <input
        type="checkbox"
        role="switch"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
        className="peer sr-only"
      />
      <span
        aria-hidden
        className={`relative mt-0.5 h-5 w-9 shrink-0 rounded-full transition-colors peer-focus-visible:outline-2 peer-focus-visible:outline-brand ${
          checked ? "bg-brand" : "bg-line"
        }`}
      >
        <span
          className={`absolute top-0.5 size-4 rounded-full bg-surface shadow transition-transform ${
            checked ? "translate-x-4.5" : "translate-x-0.5"
          }`}
        />
      </span>
    </label>
  );
}

export function SettingsMenu() {
  const prefs = usePrefs();
  return (
    <Popover.Root>
      <Popover.Trigger
        title="Sozlamalar"
        className="inline-flex size-9 items-center justify-center rounded-lg border border-line bg-surface text-ink transition-colors hover:bg-hover"
      >
        <Settings2 className="size-4" aria-hidden />
        <span className="sr-only">Sozlamalar</span>
      </Popover.Trigger>
      <Popover.Portal>
        <Popover.Positioner side="bottom" align="end" sideOffset={8} className="z-50">
          <Popover.Popup className="w-[min(92vw,19rem)] rounded-xl border border-line bg-surface p-4 shadow-xl outline-none">
            <Popover.Title className="text-xs font-bold tracking-widest text-ink-muted">KO&apos;RINISH</Popover.Title>
            <div className="mt-2 grid grid-cols-3 gap-1 rounded-lg border border-line bg-surface-2 p-1" role="radiogroup" aria-label="Mavzu">
              {THEMES.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  type="button"
                  role="radio"
                  aria-checked={prefs.theme === id}
                  onClick={() => setTheme(id)}
                  className={`inline-flex items-center justify-center gap-1 rounded-md px-2 py-1.5 text-xs font-medium ${
                    prefs.theme === id ? "bg-selected text-on-selected" : "text-ink hover:bg-hover"
                  }`}
                >
                  <Icon className="size-3.5" aria-hidden />
                  {label}
                </button>
              ))}
            </div>

            <p className="mt-4 text-xs font-bold tracking-widest text-ink-muted">SHRIFT HAJMI</p>
            <div className="mt-2 flex items-center gap-2">
              <button type="button" className="btn size-9 px-0" onClick={() => stepFont(-1)} aria-label="Kichikroq">
                <Minus className="size-4" aria-hidden />
              </button>
              <button
                type="button"
                className="flex-1 rounded-lg border border-line py-1.5 text-center text-sm font-semibold text-ink hover:bg-hover"
                onClick={() => stepFont(0)}
                title="Asl hajm"
              >
                {Math.round(prefs.fontScale * 100)}%
              </button>
              <button type="button" className="btn size-9 px-0" onClick={() => stepFont(1)} aria-label="Kattaroq">
                <Plus className="size-4" aria-hidden />
              </button>
            </div>

            <div className="mt-3 divide-y divide-line border-t border-line">
              <Switch
                checked={prefs.focus}
                onChange={setFocus}
                label="Ekran rejimi"
                hint="Yon panelni yashiradi, matnni kengaytiradi. Proyektor uchun."
              />
              <Switch
                checked={prefs.answerMode}
                onChange={setAnswerMode}
                label="Javob yozish maydoni"
                hint="Bank savollari ostida javobni tekshirish qatori."
              />
            </div>
            <button type="button" onClick={openShortcuts} className="btn mt-3 w-full">
              <Keyboard className="size-4" aria-hidden />
              Tezkor tugmalar
            </button>
          </Popover.Popup>
        </Popover.Positioner>
      </Popover.Portal>
    </Popover.Root>
  );
}

const SHORTCUTS: [string, string][] = [
  ["/  yoki  Ctrl K", "Qidirish"],
  ["←  →", "Oldingi / keyingi dars"],
  ["K", "Javob kalitini ochish / yopish"],
  ["L", "Til: ikkalasi → o'zbekcha → inglizcha"],
  ["F", "Ekran rejimi"],
  ["+  −  0", "Shriftni kattalashtirish, kichraytirish, asl holi"],
  ["T", "Yorug' / qorong'i mavzu"],
  ["?", "Shu ro'yxat"],
];

export function ShortcutsDialog() {
  const open = useSyncExternalStore(shortcutsOpen.subscribe, shortcutsOpen.get, shortcutsOpen.getServer);
  return (
    <Dialog.Root open={open} onOpenChange={(next) => shortcutsOpen.set(next)}>
      <Dialog.Portal>
        <Dialog.Backdrop className="fixed inset-0 z-50 bg-black/45 backdrop-blur-[2px]" />
        <Dialog.Popup className="fixed top-1/2 left-1/2 z-50 w-[min(92vw,26rem)] -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-line bg-surface p-6 shadow-2xl">
          <Dialog.Title className="font-serif text-xl text-heading">Tezkor tugmalar</Dialog.Title>
          <dl className="mt-4 space-y-2">
            {SHORTCUTS.map(([keys, action]) => (
              <div key={keys} className="flex items-center justify-between gap-4 text-sm">
                <dt>
                  <kbd className="rounded-md border border-line bg-surface-2 px-2 py-0.5 font-sans text-xs font-semibold text-ink">
                    {keys}
                  </kbd>
                </dt>
                <dd className="text-right text-ink-muted">{action}</dd>
              </div>
            ))}
          </dl>
          <Dialog.Close className="btn mt-5 w-full">Yopish</Dialog.Close>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
