"use client";

import { createContext, useContext, useEffect, useState } from "react";

export type Lang = "both" | "en" | "uz";

type Prefs = {
  lang: Lang;
  setLang: (lang: Lang) => void;
  showKeys: boolean;
  setShowKeys: (show: boolean) => void;
};

const PrefsContext = createContext<Prefs | null>(null);

export function PrefsProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLangState] = useState<Lang>("both");
  const [showKeys, setShowKeysState] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const storedLang = window.localStorage.getItem("sat-lang");
    const storedKeys = window.localStorage.getItem("sat-keys");
    if (storedLang === "both" || storedLang === "en" || storedLang === "uz") {
      setLangState(storedLang);
    }
    if (storedKeys === "show") setShowKeysState(true);
    setReady(true);
  }, []);

  useEffect(() => {
    if (!ready) return;
    window.localStorage.setItem("sat-lang", lang);
    window.localStorage.setItem("sat-keys", showKeys ? "show" : "hide");
  }, [lang, showKeys, ready]);

  return (
    <PrefsContext.Provider
      value={{
        lang,
        setLang: setLangState,
        showKeys,
        setShowKeys: setShowKeysState,
      }}
    >
      {children}
    </PrefsContext.Provider>
  );
}

export function usePrefs(): Prefs {
  const value = useContext(PrefsContext);
  if (!value) throw new Error("PrefsProvider is missing");
  return value;
}
