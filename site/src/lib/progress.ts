"use client";

import { useSyncExternalStore } from "react";
import { createStore, readItem, writeItem } from "@/lib/local-store";

/** What one browser remembers about its own work. Nothing is sent to a server. */
export type Progress = {
  /** Lessons the teacher or student marked as covered. */
  done: Record<string, true>;
  /** Bank results per lesson: "ok" once solved, "no" while only wrong tries. */
  bank: Record<string, Record<string, "ok" | "no">>;
  /** The lesson opened most recently, for "continue". */
  last?: string;
};

const KEY = "sat-progress-v1";
const EMPTY: Progress = { done: {}, bank: {} };

function readProgress(): Progress {
  const raw = readItem(KEY);
  if (!raw) return EMPTY;
  const parsed = JSON.parse(raw) as Partial<Progress>;
  return {
    done: parsed.done && typeof parsed.done === "object" ? parsed.done : {},
    bank: parsed.bank && typeof parsed.bank === "object" ? parsed.bank : {},
    last: typeof parsed.last === "string" ? parsed.last : undefined,
  };
}

export const progressStore = createStore(readProgress, (value) => writeItem(KEY, JSON.stringify(value)), EMPTY);

export function useProgress(): Progress {
  return useSyncExternalStore(progressStore.subscribe, progressStore.get, progressStore.getServer);
}

export function setLessonDone(code: string, done: boolean): void {
  progressStore.set((previous) => {
    const next = { ...previous.done };
    if (done) next[code] = true;
    else delete next[code];
    return { ...previous, done: next };
  });
}

export function recordBankResult(code: string, id: string, correct: boolean): void {
  progressStore.set((previous) => {
    const lesson = { ...(previous.bank[code] ?? {}) };
    if (correct) lesson[id] = "ok";
    else if (lesson[id] !== "ok") lesson[id] = "no";
    return { ...previous, bank: { ...previous.bank, [code]: lesson } };
  });
}

export function rememberLesson(code: string): void {
  if (progressStore.get().last !== code) progressStore.set((previous) => ({ ...previous, last: code }));
}

export function resetBank(code: string): void {
  progressStore.set((previous) => {
    const bank = { ...previous.bank };
    delete bank[code];
    return { ...previous, bank };
  });
}

export function solvedCount(progress: Progress, code: string): number {
  return Object.values(progress.bank[code] ?? {}).filter((status) => status === "ok").length;
}
