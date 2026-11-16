import { GlossaryView } from "@/components/glossary-view";
import { guide } from "@/lib/guide";

export const metadata = { title: "Atamalar — SAT Math" };

export default function GlossaryPage() {
  return <GlossaryView rows={guide.glossary} />;
}
