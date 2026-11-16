import raw from "../../data/guide.json";

export type Block = { type: "p" | "formula" | "say"; text: string };
export type Choice = { letter: string; en: string; uz: string };

export type Example = {
  kind: "foundation" | "sat" | string;
  promptEn: string;
  promptUz: string;
  gloss: string;
  choices: Choice[];
  steps: { en: string; uz: string }[];
  answer: string;
};

export type Practice = {
  promptEn: string;
  promptUz: string;
  gloss: string;
};

export type BankItem = {
  id: string;
  level: "oson" | "orta" | "sat" | string;
  promptEn: string;
  promptUz: string;
};

export type Lesson = {
  code: string;
  titleEn: string;
  titleUz: string;
  goalEn: string;
  goalUz: string;
  prereqEn: string;
  prereqUz: string;
  teacherEn: Block[];
  teacherUz: Block[];
  explainEn: Block[];
  explainUz: Block[];
  examples: Example[];
  mistakes: { en: string; uz: string }[];
  practice: Practice[];
  bank: BankItem[];
  figure: string;
  figureCaptionEn: string;
  figureCaptionUz: string;
  extras: string[];
};

export type Unit = {
  code: string;
  titleEn: string;
  titleUz: string;
  introEn: Block[];
  introUz: Block[];
  lessons: Lesson[];
};

export type MiniItem = {
  number: number;
  domain: string;
  promptEn: string;
  promptUz: string;
  choices: Choice[];
};

export type Guide = {
  units: Unit[];
  glossary: { en: string; uz: string; hint: string }[];
  formulaTables: { headers: string[]; rows: string[][] }[];
  mini: MiniItem[];
};

export const guide = raw as Guide;

export function allLessons(): { unit: Unit; lesson: Lesson }[] {
  return guide.units.flatMap((unit) => unit.lessons.map((lesson) => ({ unit, lesson })));
}

export function findLesson(code: string): { unit: Unit; lesson: Lesson } | undefined {
  return allLessons().find((item) => item.lesson.code === code);
}

export function neighbors(code: string): {
  prev?: Lesson;
  next?: Lesson;
} {
  const list = allLessons();
  const index = list.findIndex((item) => item.lesson.code === code);
  return {
    prev: index > 0 ? list[index - 1].lesson : undefined,
    next: index >= 0 && index < list.length - 1 ? list[index + 1].lesson : undefined,
  };
}
