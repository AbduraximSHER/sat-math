"use client";

import { ArrowRight, PlayCircle } from "lucide-react";
import Link from "next/link";
import { solvedCount, useProgress } from "@/lib/progress";

export function ContinueButton({ titles }: { titles: Record<string, string> }) {
  const { last } = useProgress();
  const code = last && titles[last] ? last : "0.1";
  return (
    <Link href={`/dars/${code}`} className="btn-primary h-11 px-5 text-base">
      <PlayCircle className="size-5" aria-hidden />
      {last && titles[last] ? `Davom etish: ${code}` : "Birinchi darsdan boshlash"}
    </Link>
  );
}

export function UnitProgress({ codes }: { codes: string[] }) {
  const progress = useProgress();
  const done = codes.filter((code) => progress.done[code]).length;
  const solved = codes.reduce((sum, code) => sum + solvedCount(progress, code), 0);
  return (
    <div className="mt-3">
      <div className="h-1.5 overflow-hidden rounded-full bg-hover" aria-hidden>
        <div className="h-full rounded-full bg-brand" style={{ width: `${(done / codes.length) * 100}%` }} />
      </div>
      <p className="mt-1.5 flex justify-between text-xs text-ink-muted">
        <span>
          {done}/{codes.length} dars o&apos;tildi
        </span>
        {solved > 0 && <span>{solved} bank savoli yechildi</span>}
      </p>
    </div>
  );
}

export function UnitLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link href={href} className="card group block p-5 transition-colors hover:border-brand">
      {children}
      <span className="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-brand">
        Ochish <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" aria-hidden />
      </span>
    </Link>
  );
}
