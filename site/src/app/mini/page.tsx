import { MiniView } from "@/components/mini-view";
import { guide } from "@/lib/guide";

export const metadata = { title: "Mini-test — SAT Math" };

export default function MiniPage() {
  return <MiniView items={guide.mini} />;
}
