import "server-only";
import raw from "../../data/keys.json";
import type { CheckSpec } from "@/lib/answer-check";

export type PracticeKey = {
  answer: string;
  solutionEn: string;
  solutionUz: string;
};

/** What the browser may see once the teacher key is open. */
export type BankKey = {
  id: string;
  answer: string;
  solutionEn: string;
  solutionUz: string;
};

/** Server-only: the grading spec stays here. */
export type BankKeyWithCheck = BankKey & { check: CheckSpec };

export type LessonKeys = {
  practice: PracticeKey[];
  bank: BankKeyWithCheck[];
};

export type MiniKey = {
  number: number;
  answer: string;
  analysisEn: string;
  analysisUz: string;
};

export type MiniKeyWithCheck = MiniKey & { check: CheckSpec };

export type KeysFile = {
  lessons: Record<string, LessonKeys>;
  mini: MiniKeyWithCheck[];
};

export function loadKeys(): KeysFile {
  return raw as KeysFile;
}

/** Strip grading specs before keys leave the server. */
export function publicLessonKeys(lesson: LessonKeys): { practice: PracticeKey[]; bank: BankKey[] } {
  return {
    practice: lesson.practice,
    bank: lesson.bank.map(({ id, answer, solutionEn, solutionUz }) => ({ id, answer, solutionEn, solutionUz })),
  };
}

export function publicMiniKeys(rows: MiniKeyWithCheck[]): MiniKey[] {
  return rows.map(({ number, answer, analysisEn, analysisUz }) => ({ number, answer, analysisEn, analysisUz }));
}
