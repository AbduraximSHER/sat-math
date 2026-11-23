import type { MetadataRoute } from "next";
import { allLessons } from "@/lib/guide";
import { SITE_URL } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  const pages = ["", "/formulalar", "/lugat", "/mini", "/varaq"].map((path) => ({
    url: `${SITE_URL}${path}`,
    changeFrequency: "monthly" as const,
    priority: path === "" ? 1 : 0.6,
  }));
  const lessons = allLessons().map(({ lesson }) => ({
    url: `${SITE_URL}/dars/${lesson.code}`,
    changeFrequency: "monthly" as const,
    priority: 0.8,
  }));
  return [...pages, ...lessons];
}
