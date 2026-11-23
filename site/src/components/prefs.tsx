"use client";

import { useEffect, useSyncExternalStore } from "react";
import { createStore, readItem, writeItem } from "@/lib/local-store";

export type Lang = "both" | "en" | "uz";
export type Theme = "system" | "light" | "dark";

export type Prefs = {
  lang: Lang;
  showKeys: boolean;
  theme: Theme;
  fontScale: number;
  focus: boolean;
  answerMode: boolean;
};

export const FONT_STEPS = [0.9, 1, 1.12, 1.25, 1.4, 1.6] as const;

const DEFAULTS: Prefs = {
  lang: "both",
  showKeys: false,
  theme: "system",
  fontScale: 1,
  focus: false,
  answerMode: true,
};

function readPrefs(): Prefs {
  const lang = readItem("sat-lang");
  const theme = readItem("sat-theme");
  const font = Number(readItem("sat-font"));
  return {
    lang: lang === "en" || lang === "uz" || lang === "both" ? lang : DEFAULTS.lang,
    showKeys: readItem("sat-keys") === "show",
    theme: theme === "light" || theme === "dark" || theme === "system" ? theme : DEFAULTS.theme,
    fontScale: (FONT_STEPS as readonly number[]).includes(font) ? font : DEFAULTS.fontScale,
    focus: readItem("sat-focus") === "on",
    answerMode: readItem("sat-answer") !== "off",
  };
}

function writePrefs(prefs: Prefs): void {
  writeItem("sat-lang", prefs.lang);
  writeItem("sat-keys", prefs.showKeys ? "show" : "hide");
  writeItem("sat-theme", prefs.theme);
  writeItem("sat-font", String(prefs.fontScale));
  writeItem("sat-focus", prefs.focus ? "on" : "off");
  writeItem("sat-answer", prefs.answerMode ? "on" : "off");
}

export const prefsStore = createStore(readPrefs, writePrefs, DEFAULTS);

const update = (patch: Partial<Prefs>) => prefsStore.set((previous) => ({ ...previous, ...patch }));

export const setLang = (lang: Lang) => update({ lang });
export const setShowKeys = (showKeys: boolean) => update({ showKeys });
export const setTheme = (theme: Theme) => update({ theme });
export const setFocus = (focus: boolean) => update({ focus });
export const setAnswerMode = (answerMode: boolean) => update({ answerMode });

export function stepFont(direction: 1 | -1 | 0): void {
  prefsStore.set((previous) => {
    if (direction === 0) return { ...previous, fontScale: 1 };
    const index = FONT_STEPS.indexOf(previous.fontScale as (typeof FONT_STEPS)[number]);
    const next = FONT_STEPS[Math.min(FONT_STEPS.length - 1, Math.max(0, (index < 0 ? 1 : index) + direction))];
    return { ...previous, fontScale: next };
  });
}

export function cycleLang(): void {
  const order: Lang[] = ["both", "uz", "en"];
  const current = prefsStore.get().lang;
  setLang(order[(order.indexOf(current) + 1) % order.length]);
}

export function usePrefs(): Prefs {
  return useSyncExternalStore(prefsStore.subscribe, prefsStore.get, prefsStore.getServer);
}

function isDark(theme: Theme): boolean {
  return theme === "dark" || (theme === "system" && window.matchMedia("(prefers-color-scheme: dark)").matches);
}

/** Mirror the stored prefs onto <html>; CSS does the rest. */
function applyToDocument(): void {
  const prefs = prefsStore.get();
  const root = document.documentElement;
  const dark = isDark(prefs.theme);
  root.classList.toggle("dark", dark);
  root.style.colorScheme = dark ? "dark" : "light";
  root.dataset.lang = prefs.lang;
  root.dataset.focus = prefs.focus ? "on" : "off";
  root.style.setProperty("--font-scale", String(prefs.fontScale));
  document.querySelector('meta[name="theme-color"]')?.setAttribute("content", dark ? "#0f1518" : "#1b3a4b");
}

export function PrefsEffects() {
  const prefs = usePrefs();
  useEffect(() => {
    applyToDocument();
  }, [prefs]);
  useEffect(() => {
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => applyToDocument();
    media.addEventListener("change", onChange);
    return () => media.removeEventListener("change", onChange);
  }, []);
  return null;
}

/** Runs before first paint so the stored theme, language and size never flash. */
export const PREFS_SCRIPT = `(function(){try{var d=document.documentElement,s=window.localStorage;var t=s.getItem("sat-theme")||"system";var k=t==="dark"||(t==="system"&&window.matchMedia("(prefers-color-scheme: dark)").matches);d.classList.toggle("dark",k);d.style.colorScheme=k?"dark":"light";var l=s.getItem("sat-lang");if(l==="en"||l==="uz"||l==="both")d.dataset.lang=l;d.dataset.focus=s.getItem("sat-focus")==="on"?"on":"off";var f=Number(s.getItem("sat-font"));if(f>=0.8&&f<=1.7)d.style.setProperty("--font-scale",String(f));}catch(e){}})();`;
