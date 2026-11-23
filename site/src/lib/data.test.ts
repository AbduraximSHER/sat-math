import { describe, expect, it } from "vitest";
import { allLessons, guide } from "@/lib/guide";
import { loadKeys } from "@/lib/keys";

const SECRET_FIELDS = ["answer", "solutionEn", "solutionUz", "analysisEn", "analysisUz", "check"];

describe("exported site data", () => {
  const keys = loadKeys();
  const lessons = allLessons().map(({ lesson }) => lesson);

  it("has the 44 lessons in teaching order", () => {
    expect(lessons).toHaveLength(44);
    expect(new Set(lessons.map((lesson) => lesson.code)).size).toBe(44);
    expect(lessons[0].code).toBe("0.1");
    expect(lessons.at(-1)?.code).toBe("6.4");
  });

  it("keeps answers out of the public guide", () => {
    for (const lesson of lessons) {
      for (const item of [...lesson.practice, ...lesson.bank]) {
        for (const field of SECRET_FIELDS) expect(item).not.toHaveProperty(field);
      }
    }
    for (const item of guide.mini) {
      for (const field of SECRET_FIELDS) expect(item).not.toHaveProperty(field);
    }
  });

  it("has a key for every practice item and bank item", () => {
    for (const lesson of lessons) {
      const lessonKeys = keys.lessons[lesson.code];
      expect(lessonKeys, lesson.code).toBeDefined();
      expect(lessonKeys.practice).toHaveLength(lesson.practice.length);
      expect(lesson.bank).toHaveLength(100);
      expect(lessonKeys.bank.map((row) => row.id)).toEqual(lesson.bank.map((row) => row.id));
    }
    expect(keys.mini.map((row) => row.number)).toEqual(guide.mini.map((row) => row.number));
  });

  it("names a figure file only when it has both captions", () => {
    for (const lesson of lessons) {
      if (!lesson.figure) continue;
      expect(lesson.figureCaptionEn.length, lesson.code).toBeGreaterThan(0);
      expect(lesson.figureCaptionUz.length, lesson.code).toBeGreaterThan(0);
    }
  });
});
