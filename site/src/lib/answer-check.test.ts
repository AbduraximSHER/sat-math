import { describe, expect, it } from "vitest";
import { checkAnswer, parseExpression, parseRat, type CheckSpec } from "@/lib/answer-check";
import { loadKeys } from "@/lib/keys";

const ok = { result: "correct" };
const no = { result: "incorrect" };
const hint = (name: string) => ({ result: "format", hint: name });

function expectAll(spec: CheckSpec, cases: Record<string, unknown>) {
  for (const [input, verdict] of Object.entries(cases)) {
    expect(checkAnswer(spec, input), `${JSON.stringify(spec)} ← ${JSON.stringify(input)}`).toEqual(verdict);
  }
}

describe("parsing", () => {
  it("reads rationals exactly", () => {
    expect(parseRat("-7/2")).toEqual({ n: -7n, d: 2n });
    expect(parseRat("0.375")).toEqual({ n: 3n, d: 8n });
    expect(parseRat(".5")).toEqual({ n: 1n, d: 2n });
    expect(parseRat("4/0")).toBeNull();
    expect(parseRat("abc")).toBeNull();
  });

  it("parses implicit products, powers and roots", () => {
    for (const text of ["5x^2 + 11x + 2", "(x + 1)(x - 2)", "2√2", "3π/2", "x²-4x", "-(x+1)"]) {
      expect(parseExpression(text), text).not.toBeNull();
    }
    for (const text of ["5x +", "(x + 1", "2 ** ", "javob", "x = 3"]) {
      expect(parseExpression(text), text).toBeNull();
    }
  });
});

describe("number answers", () => {
  it("accepts equivalent forms and labels", () => {
    expectAll({ kind: "number", value: "-4" }, {
      "-4": ok,
      "−4": ok,
      "x = -4": ok,
      "x=−4": ok,
      "-4.0": ok,
      "4": no,
      "-8/2": ok,
      "": hint("empty"),
      "hello": hint("unreadable"),
      "-2-2": hint("single-number"),
    });
  });

  it("flags SAT entry mistakes", () => {
    const spec: CheckSpec = { kind: "number", value: "7/2" };
    expectAll(spec, { "7/2": ok, "3.5": ok, "3 1/2": hint("mixed-number"), "3,5": hint("decimal-comma"), "3 1/3": no });
    expectAll({ kind: "number", value: "1250" }, { "1,250": ok, "1250": ok, "$1,250": ok, "1.250": no });
  });

  it("applies the SAT rule for decimals that do not end", () => {
    expectAll({ kind: "number", value: "2/3" }, {
      "2/3": ok,
      ".6666": ok,
      ".6667": ok,
      "0.666": ok,
      "0.667": ok,
      "0.6666667": ok,
      "0.67": hint("more-digits"),
      ".66": hint("more-digits"),
      "0.668": no,
    });
    expectAll({ kind: "number", value: "100/3" }, { "33.33": ok, "33.3": hint("more-digits"), "33.34": no });
  });

  it("checks the requested form", () => {
    expectAll({ kind: "number", value: "3/8", form: "decimal" }, { "0.375": ok, ".375": ok, "3/8": hint("use-decimal") });
    expectAll({ kind: "number", value: "3/4", simplest: true, form: "fraction" }, {
      "3/4": ok,
      "6/8": hint("simplify"),
      "0.75": hint("use-fraction"),
    });
  });

  it("handles percents both ways", () => {
    expectAll({ kind: "number", value: "25", percent: true }, { "25": ok, "25%": ok, "0.25": hint("use-percent"), "75": no });
    expectAll({ kind: "number", value: "0", percent: true }, { "0": ok, "0%": ok });
    expectAll({ kind: "number", value: "12" }, { "12": ok, "12%": hint("no-percent"), "13%": no });
  });

  it("strips degree signs", () => {
    expectAll({ kind: "number", value: "165" }, { "165°": ok, "165": ok });
  });
});

describe("π answers", () => {
  it("accepts π forms and close decimals", () => {
    expectAll({ kind: "pi", value: "9" }, { "9π": ok, "9pi": ok, "9*π": ok, "28.27": ok, "28.274": ok, "28": no, "9": hint("use-pi"), "18π": no });
    expectAll({ kind: "pi", value: "1/3" }, { "π/3": ok, "(1/3)π": ok, "1/3π": ok, "pi/3": ok, "π/6": no });
    expectAll({ kind: "pi", value: "100/9" }, { "100π/9": ok, "(100/9)π": ok });
  });
});

describe("radicals", () => {
  it("wants the simplified radical", () => {
    expectAll({ kind: "radical", coef: 2, rad: 2 }, { "2√2": ok, "2sqrt(2)": ok, "2 √2": ok, "√8": hint("radical"), "2.828": hint("radical"), "4√2": no });
    expectAll({ kind: "radical", coef: 12, rad: 1 }, { "12": ok, "√144": hint("radical"), "13": no });
    expectAll({ kind: "radical", coef: 1, rad: 15 }, { "√15": ok, "sqrt15": ok, "√16": no });
  });
});

describe("expressions", () => {
  it("accepts any simplified equivalent form", () => {
    expectAll({ kind: "expression", expr: "5*x**2 + 11*x + 2", form: "simplified", var: "x" }, {
      "5x² + 11x + 2": ok,
      "5x^2+11x+2": ok,
      "2 + 11x + 5x^2": ok,
      "5x^2 + 10x + x + 2": hint("combine"),
      "(5x + 1)(x + 2)": hint("combine"),
      "5x^2 + 11x - 2": no,
    });
    expectAll({ kind: "expression", expr: "10 - x", form: "simplified", var: "x" }, { "10 − x": ok, "-x + 10": ok, "x - 10": no });
  });

  it("wants a product for factoring", () => {
    expectAll({ kind: "expression", expr: "x**2 + 2*x - 8", form: "factored", var: "x" }, {
      "(x + 4)(x − 2)": ok,
      "(x-2)(x+4)": ok,
      "x² + 2x − 8": hint("factor"),
      "(x + 2)(x − 4)": no,
    });
    expectAll({ kind: "expression", expr: "x**2 - 4*x", form: "factored", var: "x" }, { "x(x − 4)": ok, "(x - 4)x": ok });
  });

  it("works in terms of y", () => {
    expectAll({ kind: "expression", expr: "y - 4", form: "simplified", var: "y" }, { "y − 4": ok, "x = y - 4": ok, "y + 4": no, "x - 4": no });
  });
});

describe("sets, pairs and inequalities", () => {
  it("needs every root, in any order", () => {
    expectAll({ kind: "set", values: ["-10", "-9"] }, {
      "x = −10 or x = −9": ok,
      "-9, -10": ok,
      "-10 va -9": ok,
      "-10": hint("both-values"),
      "-10, 9": no,
      "or": hint("unreadable"),
    });
  });

  it("reads labelled and unlabelled pairs", () => {
    expectAll({ kind: "pair", values: ["-8", "-6"] }, {
      "x = −8, y = −6": ok,
      "(-8, -6)": ok,
      "y = -6, x = -8": ok,
      "(-6, -8)": no,
      "-8": hint("both-values"),
    });
  });

  it("checks the direction of the sign", () => {
    expectAll({ kind: "inequality", op: "<", value: "-4" }, {
      "x < −4": ok,
      "x<-4": ok,
      "-4 > x": ok,
      "x > -4": no,
      "x <= -4": no,
      "-4": hint("inequality"),
    });
    expectAll({ kind: "inequality", op: ">=", value: "3/4" }, { "x ≥ 3/4": ok, "x >= 0.75": ok, "x => 3/4": ok });
  });
});

describe("every key in the bank", () => {
  const keys = loadKeys();

  it("accepts the displayed answer of all 4,400 bank items and all 20 mini-test items", () => {
    let checked = 0;
    for (const [code, lesson] of Object.entries(keys.lessons)) {
      for (const row of lesson.bank) {
        expect(checkAnswer(row.check, row.answer), `${code} #${row.id}: ${row.answer}`).toEqual(ok);
        checked += 1;
      }
    }
    for (const row of keys.mini) {
      expect(checkAnswer(row.check, row.answer), `mini ${row.number}: ${row.answer}`).toEqual(ok);
    }
    expect(checked).toBe(4400);
  });

  it("rejects an answer that is off by one for every numeric bank item", () => {
    for (const [code, lesson] of Object.entries(keys.lessons)) {
      for (const row of lesson.bank) {
        if (row.check.kind !== "number") continue;
        const wrong = parseRat(row.check.value)!;
        const text = `${(wrong.n + wrong.d).toString()}/${wrong.d.toString()}`;
        expect(checkAnswer(row.check, text).result, `${code} #${row.id}: ${text}`).not.toBe("correct");
      }
    }
  });
});
