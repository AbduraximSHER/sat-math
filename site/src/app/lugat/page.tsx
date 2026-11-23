import type { Metadata } from "next";
import { GlossaryView } from "@/components/glossary-view";
import { guide } from "@/lib/guide";

export const metadata: Metadata = {
  title: "Atamalar",
  description: "SAT Math atamalari inglizcha va o'zbekcha: kurs bo'yi bir xil ishlatiladigan lug'at.",
  alternates: { canonical: "/lugat" },
};

export default function GlossaryPage() {
  return <GlossaryView rows={guide.glossary} />;
}
