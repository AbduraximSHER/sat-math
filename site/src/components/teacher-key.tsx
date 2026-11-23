"use client";

import { Dialog } from "@base-ui/react/dialog";
import { KeyRound, Lock, LockOpen } from "lucide-react";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { prefsStore, setShowKeys, usePrefs } from "@/components/prefs";
import { createStore } from "@/lib/local-store";

/** Whether the PIN dialog is open. Not persisted. */
const pinStore = createStore<boolean>(() => false, () => undefined, false);
const openPin = () => pinStore.set(true);
const closePin = () => pinStore.set(false);

/** The key was refused (PIN set, cookie missing or old): close it and ask. */
export function lockKeys(): void {
  setShowKeys(false);
  openPin();
}

export async function toggleKeys(): Promise<void> {
  if (prefsStore.get().showKeys) {
    setShowKeys(false);
    return;
  }
  try {
    const response = await fetch("/api/teacher", { cache: "no-store" });
    const status = (await response.json()) as { required: boolean; unlocked: boolean };
    if (status.required && !status.unlocked) {
      openPin();
      return;
    }
  } catch {
    // Offline: try to open; the fetch for keys will report the problem.
  }
  setShowKeys(true);
}

export function KeyToggle({ compact = false }: { compact?: boolean }) {
  const { showKeys } = usePrefs();
  return (
    <button
      type="button"
      onClick={() => void toggleKeys()}
      aria-pressed={showKeys}
      title="Javob kaliti (K)"
      className={`inline-flex h-9 items-center gap-1.5 rounded-lg border px-2.5 text-sm font-semibold transition-colors ${
        showKeys ? "border-gold bg-key-bg text-gold" : "border-line bg-surface text-ink hover:bg-hover"
      }`}
    >
      {showKeys ? <LockOpen className="size-4" aria-hidden /> : <Lock className="size-4" aria-hidden />}
      <span className={compact ? "sr-only" : "hidden md:inline"}>{showKeys ? "Kalit ochiq" : "Kalit yopiq"}</span>
    </button>
  );
}

export function PinDialog() {
  const open = useSyncExternalStore(pinStore.subscribe, pinStore.get, pinStore.getServer);
  const [pin, setPin] = useState("");
  const [state, setState] = useState<"idle" | "busy" | "wrong" | "error">("idle");
  const input = useRef<HTMLInputElement>(null);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setState("busy");
    try {
      const response = await fetch("/api/teacher", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pin }),
      });
      if (response.ok) {
        setPin("");
        setState("idle");
        closePin();
        setShowKeys(true);
        return;
      }
      setState(response.status === 401 ? "wrong" : "error");
    } catch {
      setState("error");
    }
    input.current?.select();
  }

  return (
    <Dialog.Root
      open={open}
      onOpenChange={(next) => {
        if (!next) {
          closePin();
          setPin("");
          setState("idle");
        }
      }}
    >
      <Dialog.Portal>
        <Dialog.Backdrop className="fixed inset-0 z-50 bg-black/45 backdrop-blur-[2px]" />
        <Dialog.Popup
          initialFocus={input}
          className="fixed top-1/2 left-1/2 z-50 w-[min(92vw,24rem)] -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-line bg-surface p-6 shadow-2xl"
        >
          <form onSubmit={submit}>
            <div className="flex items-center gap-2 text-heading">
              <KeyRound className="size-5" aria-hidden />
              <Dialog.Title className="font-serif text-xl">O&apos;qituvchi PIN-kodi</Dialog.Title>
            </div>
            <Dialog.Description className="mt-2 text-sm leading-relaxed text-ink-muted">
              Javob kaliti himoyalangan. PIN-kodni kiriting. Bu qurilma 30 kun eslab qoladi.
            </Dialog.Description>
            <input
              ref={input}
              type="password"
              autoComplete="off"
              value={pin}
              onChange={(event) => {
                setPin(event.target.value);
                if (state !== "busy") setState("idle");
              }}
              className="field mt-4 text-lg tracking-widest"
              aria-label="PIN"
              aria-invalid={state === "wrong"}
            />
            <p role="status" className="mt-2 min-h-5 text-sm text-bad">
              {state === "wrong" && "PIN noto'g'ri. Qayta urinib ko'ring."}
              {state === "error" && "Server bilan bog'lanib bo'lmadi."}
            </p>
            <div className="mt-3 flex justify-end gap-2">
              <Dialog.Close className="btn">Bekor qilish</Dialog.Close>
              <button type="submit" className="btn-primary" disabled={!pin || state === "busy"}>
                {state === "busy" ? "Tekshirilmoqda…" : "Ochish"}
              </button>
            </div>
          </form>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

type KeyState<T> = { data: T | null; state: "off" | "loading" | "ready" | "error" };
type Loaded = { ok: true; data: unknown } | { ok: false; locked: boolean };

/** One request per URL while the key stays open; several sections share it. */
const requests = new Map<string, Promise<Loaded>>();

function load(url: string): Promise<Loaded> {
  let request = requests.get(url);
  if (!request) {
    request = fetch(url, { cache: "no-store" })
      .then(async (response): Promise<Loaded> => {
        if (response.status === 401) return { ok: false, locked: true };
        if (!response.ok) return { ok: false, locked: false };
        return { ok: true, data: await response.json() };
      })
      .catch((): Loaded => ({ ok: false, locked: false }));
    requests.set(url, request);
    void request.then((result) => {
      if (!result.ok) requests.delete(url);
    });
  }
  return request;
}

/** Fetch teacher-only data while the key is open. */
export function useTeacherData<T>(url: string | null): KeyState<T> {
  const { showKeys } = usePrefs();
  const [result, setResult] = useState<{ url: string; data: T | null; failed: boolean } | null>(null);

  useEffect(() => {
    if (!showKeys) {
      requests.clear();
      return;
    }
    if (!url) return;
    let cancelled = false;
    void load(url).then((loaded) => {
      if (cancelled) return;
      if (loaded.ok) setResult({ url, data: loaded.data as T, failed: false });
      else if (loaded.locked) lockKeys();
      else setResult({ url, data: null, failed: true });
    });
    return () => {
      cancelled = true;
    };
  }, [showKeys, url]);

  if (!showKeys || !url) return { data: null, state: "off" };
  if (!result || result.url !== url) return { data: null, state: "loading" };
  return { data: result.data, state: result.failed ? "error" : "ready" };
}
