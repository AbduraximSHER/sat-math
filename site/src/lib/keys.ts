import raw from "../../data/keys.json";

export type PracticeKey = {
  answer: string;
  solutionEn: string;
  solutionUz: string;
};

export type BankKey = {
  id: string;
  answer: string;
  solutionEn: string;
  solutionUz: string;
};

export type LessonKeys = {
  practice: PracticeKey[];
  bank: BankKey[];
};

export type MiniKey = {
  number: number;
  answer: string;
  analysisEn: string;
  analysisUz: string;
};

export type KeysFile = {
  lessons: Record<string, LessonKeys>;
  mini: MiniKey[];
};

export function loadKeys(): KeysFile {
  return raw as KeysFile;
}
