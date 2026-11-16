import { notFound } from "next/navigation";
import { LessonView } from "@/components/lesson-view";
import { allLessons, findLesson, neighbors } from "@/lib/guide";

export function generateStaticParams() {
  return allLessons().map(({ lesson }) => ({ code: lesson.code }));
}

export async function generateMetadata({ params }: { params: Promise<{ code: string }> }) {
  const { code } = await params;
  const found = findLesson(code);
  if (!found) return { title: "Dars topilmadi" };
  return { title: `Dars ${found.lesson.code}. ${found.lesson.titleUz}` };
}

export default async function LessonPage({ params }: { params: Promise<{ code: string }> }) {
  const { code } = await params;
  const found = findLesson(decodeURIComponent(code));
  if (!found) notFound();
  const near = neighbors(found.lesson.code);
  return (
    <LessonView
      unit={found.unit}
      lesson={found.lesson}
      showIntro={found.unit.lessons[0].code === found.lesson.code}
      prev={near.prev ? { code: near.prev.code, titleUz: near.prev.titleUz } : undefined}
      next={near.next ? { code: near.next.code, titleUz: near.next.titleUz } : undefined}
    />
  );
}
