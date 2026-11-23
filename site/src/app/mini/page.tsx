import type { Metadata } from "next";
import { MiniView } from "@/components/mini-view";
import { findLesson, guide } from "@/lib/guide";

export const metadata: Metadata = {
  title: "Mini-test",
  description: "20 savollik aralash takrorlash: 35 daqiqa, javoblar serverda tekshiriladi, natija mavzular bo'yicha.",
  alternates: { canonical: "/mini" },
};

/** Which lesson to revisit when a mini-test item goes wrong. */
const REVIEW: Record<number, string> = {
  1: "0.1",
  2: "1.4",
  3: "1.5",
  4: "1.8",
  5: "2.2",
  6: "2.3",
  7: "2.6",
  8: "2.7",
  9: "2.8",
  10: "3.3",
  11: "3.4",
  12: "3.6",
  13: "3.7",
  14: "4.3",
  15: "4.5",
  16: "5.2",
  17: "5.3",
  18: "5.4",
  19: "5.6",
  20: "5.7",
};

export default function MiniPage() {
  const review = Object.fromEntries(
    Object.entries(REVIEW).map(([number, code]) => [number, { code, title: findLesson(code)?.lesson.titleUz ?? "" }]),
  );
  return <MiniView items={guide.mini} review={review} />;
}
