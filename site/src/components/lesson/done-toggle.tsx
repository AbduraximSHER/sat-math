"use client";

import { CheckCircle2, Circle } from "lucide-react";
import { useEffect } from "react";
import { rememberLesson, setLessonDone, useProgress } from "@/lib/progress";

export function DoneToggle({ code }: { code: string }) {
  const progress = useProgress();
  const done = Boolean(progress.done[code]);

  useEffect(() => {
    rememberLesson(code);
  }, [code]);

  return (
    <button
      type="button"
      onClick={() => setLessonDone(code, !done)}
      aria-pressed={done}
      className={`no-print inline-flex h-8 items-center gap-1.5 rounded-full border px-3 text-xs font-semibold transition-colors ${
        done ? "border-good bg-good-bg text-good" : "border-line bg-surface text-ink-muted hover:text-ink"
      }`}
    >
      {done ? <CheckCircle2 className="size-4" aria-hidden /> : <Circle className="size-4" aria-hidden />}
      {done ? "Dars o'tildi" : "O'tildi deb belgilash"}
    </button>
  );
}
