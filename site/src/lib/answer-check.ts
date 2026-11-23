/**
 * Grade a typed answer against an answer spec from keys.json.
 *
 * Runs on the server only. The spec never reaches the browser: the client gets
 * back "correct", "incorrect", or a format hint, never the answer itself.
 *
 * Specs are written by guide/bank.py (c_num, c_pi, c_radical, c_expr, c_set,
 * c_pair, c_ineq) and guide/export_site.py (mini-test).
 */

export type CheckSpec =
  | { kind: "number"; value: string; percent?: boolean; simplest?: boolean; form?: "decimal" | "fraction" }
  | { kind: "pi"; value: string }
  | { kind: "radical"; coef: number; rad: number }
  | { kind: "expression"; expr: string; form: "simplified" | "factored"; var: string }
  | { kind: "set"; values: string[] }
  | { kind: "pair"; values: string[] }
  | { kind: "inequality"; op: "<" | ">" | "<=" | ">="; value: string };

/** Why a right-looking answer was not accepted, or why it could not be read. */
export type Hint =
  | "empty"
  | "unreadable"
  | "mixed-number"
  | "decimal-comma"
  | "simplify"
  | "more-digits"
  | "use-decimal"
  | "use-fraction"
  | "use-percent"
  | "no-percent"
  | "single-number"
  | "combine"
  | "factor"
  | "radical"
  | "use-pi"
  | "both-values"
  | "inequality";

export type Verdict = { result: "correct" } | { result: "incorrect" } | { result: "format"; hint: Hint };

const CORRECT: Verdict = { result: "correct" };
const INCORRECT: Verdict = { result: "incorrect" };
const format = (hint: Hint): Verdict => ({ result: "format", hint });

export const MAX_ANSWER_LENGTH = 80;

// ---------------------------------------------------------------------------
// Exact rationals
// ---------------------------------------------------------------------------

export type Rat = { n: bigint; d: bigint };

function gcd(a: bigint, b: bigint): bigint {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a;
}

function rat(n: bigint, d: bigint = 1n): Rat {
  if (d === 0n) throw new Error("division by zero");
  if (d < 0n) {
    n = -n;
    d = -d;
  }
  const g = gcd(n, d) || 1n;
  return { n: n / g, d: d / g };
}

const sameRat = (a: Rat, b: Rat) => a.n === b.n && a.d === b.d;
const ratValue = (r: Rat) => Number(r.n) / Number(r.d);

/** "7", "-7/2", "0.375", ".5", "3." */
export function parseRat(text: string): Rat | null {
  const t = text.trim();
  let m = /^([+-]?)(\d+)\/(\d+)$/.exec(t);
  if (m) {
    if (BigInt(m[3]) === 0n) return null;
    return rat(BigInt(m[1] + m[2]), BigInt(m[3]));
  }
  m = /^([+-]?)(\d*)\.(\d*)$/.exec(t);
  if (m && (m[2] || m[3])) {
    const digits = m[3] ?? "";
    return rat(BigInt(m[1] + (m[2] || "0") + digits), 10n ** BigInt(digits.length));
  }
  m = /^([+-]?\d+)$/.exec(t);
  return m ? rat(BigInt(m[1])) : null;
}

function isTerminating(r: Rat): boolean {
  let d = r.d;
  while (d % 2n === 0n) d /= 2n;
  while (d % 5n === 0n) d /= 5n;
  return d === 1n;
}

/** Truncate or round |r| to `places` decimals, as a rational. */
function cut(r: Rat, places: number, mode: "trunc" | "round"): Rat {
  const scale = 10n ** BigInt(places);
  const sign = r.n < 0n ? -1n : 1n;
  const abs = r.n < 0n ? -r.n : r.n;
  let q = (abs * scale) / r.d;
  if (mode === "round" && ((abs * scale) % r.d) * 2n >= r.d) q += 1n;
  return rat(sign * q, scale);
}

// ---------------------------------------------------------------------------
// Normalizing what a student types
// ---------------------------------------------------------------------------

export function normalize(raw: string): string {
  return raw
    .replace(/[−‐‑‒–—﹣－]/g, "-")
    .replace(/[×·∙⋅]/g, "*")
    .replace(/÷/g, "/")
    .replace(/\*\*/g, "^")
    .replace(/≤|⩽|=</g, "<=")
    .replace(/≥|⩾|=>/g, ">=")
    .replace(/(?<![a-z])sqrt(?![a-z])/gi, "√")
    .replace(/(?<![a-z])pi(?![a-z])/gi, "π")
    .replace(/[ \s]+/g, " ")
    .trim()
    .toLowerCase();
}

/** Drop "x =", "y =" or "f(3) =" in front of a single value. */
function stripLabel(text: string): string {
  return text.replace(/^(?:[a-z]|f\s*\([^)]*\))\s*=\s*/, "");
}

// ---------------------------------------------------------------------------
// A small expression parser: + - * / ^ ² ³, implicit products, √, π, x, y
// ---------------------------------------------------------------------------

type Node =
  | { t: "num"; v: Rat }
  | { t: "var"; name: string }
  | { t: "pi" }
  | { t: "neg"; a: Node }
  | { t: "add"; a: Node; b: Node }
  | { t: "sub"; a: Node; b: Node }
  | { t: "mul"; a: Node; b: Node }
  | { t: "div"; a: Node; b: Node }
  | { t: "pow"; a: Node; b: Node }
  | { t: "sqrt"; a: Node }
  | { t: "group"; a: Node };

type Token = { k: "num"; v: string } | { k: "var"; v: string } | { k: "op"; v: string };

function tokenize(text: string): Token[] | null {
  const tokens: Token[] = [];
  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    if (ch === " ") {
      i += 1;
      continue;
    }
    const num = /^(\d+\.?\d*|\.\d+)/.exec(text.slice(i));
    if (num) {
      tokens.push({ k: "num", v: num[1] });
      i += num[1].length;
      continue;
    }
    if (ch === "x" || ch === "y") {
      tokens.push({ k: "var", v: ch });
    } else if ("+-*/^()√π²³".includes(ch)) {
      tokens.push({ k: "op", v: ch });
    } else {
      return null;
    }
    i += 1;
  }
  return tokens;
}

export function parseExpression(text: string): Node | null {
  const found = tokenize(text);
  if (!found || found.length === 0) return null;
  const tokens: Token[] = found;
  let pos = 0;
  const peek = () => tokens[pos];
  const isOp = (v: string) => peek()?.k === "op" && peek()?.v === v;
  const startsAtom = () => {
    const tok = peek();
    if (!tok) return false;
    return tok.k !== "op" || tok.v === "(" || tok.v === "√" || tok.v === "π";
  };

  function expr(): Node {
    let node = term();
    while (isOp("+") || isOp("-")) {
      const op = tokens[pos++].v;
      const right = term();
      node = op === "+" ? { t: "add", a: node, b: right } : { t: "sub", a: node, b: right };
    }
    return node;
  }

  function term(): Node {
    let node = unary();
    for (;;) {
      if (isOp("*")) {
        pos += 1;
        node = { t: "mul", a: node, b: unary() };
      } else if (isOp("/")) {
        pos += 1;
        node = { t: "div", a: node, b: unary() };
      } else if (startsAtom()) {
        node = { t: "mul", a: node, b: power() };
      } else {
        return node;
      }
    }
  }

  function unary(): Node {
    if (isOp("-")) {
      pos += 1;
      return { t: "neg", a: unary() };
    }
    if (isOp("+")) {
      pos += 1;
      return unary();
    }
    return power();
  }

  function power(): Node {
    let node = atom();
    for (;;) {
      if (isOp("^")) {
        pos += 1;
        node = { t: "pow", a: node, b: unary() };
      } else if (isOp("²") || isOp("³")) {
        const exponent = tokens[pos++].v === "²" ? 2n : 3n;
        node = { t: "pow", a: node, b: { t: "num", v: rat(exponent) } };
      } else {
        return node;
      }
    }
  }

  function atom(): Node {
    const tok = tokens[pos++];
    if (!tok) throw new Error("unexpected end");
    if (tok.k === "num") {
      const value = parseRat(tok.v);
      if (!value) throw new Error("bad number");
      return { t: "num", v: value };
    }
    if (tok.k === "var") return { t: "var", name: tok.v };
    if (tok.v === "π") return { t: "pi" };
    if (tok.v === "√") return { t: "sqrt", a: power() };
    if (tok.v === "(") {
      const inner = expr();
      if (!isOp(")")) throw new Error("missing )");
      pos += 1;
      return { t: "group", a: inner };
    }
    throw new Error(`unexpected ${tok.v}`);
  }

  try {
    const node = expr();
    return pos === tokens.length ? node : null;
  } catch {
    return null;
  }
}

function evaluate(node: Node, env: Record<string, number>): number {
  switch (node.t) {
    case "num":
      return ratValue(node.v);
    case "var":
      return env[node.name] ?? NaN;
    case "pi":
      return Math.PI;
    case "neg":
      return -evaluate(node.a, env);
    case "add":
      return evaluate(node.a, env) + evaluate(node.b, env);
    case "sub":
      return evaluate(node.a, env) - evaluate(node.b, env);
    case "mul":
      return evaluate(node.a, env) * evaluate(node.b, env);
    case "div":
      return evaluate(node.a, env) / evaluate(node.b, env);
    case "pow":
      return Math.pow(evaluate(node.a, env), evaluate(node.b, env));
    case "sqrt":
      return Math.sqrt(evaluate(node.a, env));
    case "group":
      return evaluate(node.a, env);
  }
}

function mentions(node: Node, test: (n: Node) => boolean): boolean {
  if (test(node)) return true;
  switch (node.t) {
    case "neg":
    case "sqrt":
    case "group":
      return mentions(node.a, test);
    case "add":
    case "sub":
    case "mul":
    case "div":
    case "pow":
      return mentions(node.a, test) || mentions(node.b, test);
    default:
      return false;
  }
}

const hasVar = (node: Node) => mentions(node, (n) => n.t === "var");
const hasPi = (node: Node) => mentions(node, (n) => n.t === "pi");
const hasGroupWithVar = (node: Node) => mentions(node, (n) => n.t === "group" && hasVar(n.a));

const SAMPLES = [-3.7, -1.3, 0.6, 2.2, 5.1];

function sameFunction(a: Node, b: Node, variable: string): boolean {
  return SAMPLES.every((point) => {
    const left = evaluate(a, { [variable]: point });
    const right = evaluate(b, { [variable]: point });
    return Number.isFinite(left) && Math.abs(left - right) <= 1e-9 * Math.max(1, Math.abs(right));
  });
}

/** Split a sum into signed terms. */
function terms(node: Node, sign = 1, out: { sign: number; node: Node }[] = []) {
  if (node.t === "add") {
    terms(node.a, sign, out);
    terms(node.b, sign, out);
  } else if (node.t === "sub") {
    terms(node.a, sign, out);
    terms(node.b, -sign, out);
  } else if (node.t === "neg") {
    terms(node.a, -sign, out);
  } else {
    out.push({ sign, node });
  }
  return out;
}

/** Degree of a monomial like 5x², −x, 12, (1/2)x. Null for anything else. */
function monomialDegree(node: Node): number | null {
  switch (node.t) {
    case "num":
    case "pi":
      return 0;
    case "var":
      return 1;
    case "neg":
      return monomialDegree(node.a);
    case "group":
      return hasVar(node.a) ? null : 0;
    case "mul": {
      const a = monomialDegree(node.a);
      const b = monomialDegree(node.b);
      return a === null || b === null ? null : a + b;
    }
    case "div":
      return hasVar(node.b) ? null : monomialDegree(node.a);
    case "pow": {
      if (hasVar(node.b)) return null;
      const base = monomialDegree(node.a);
      const exponent = evaluate(node.b, {});
      return base === null || !Number.isInteger(exponent) || exponent < 0 ? null : base * exponent;
    }
    default:
      return null;
  }
}

/** Non-constant factors of a product: (x + 1)(x − 2) has two. */
function factorCount(node: Node): number {
  if (node.t === "neg" || (node.t === "group" && node.a.t === "mul")) return factorCount(node.a);
  if (node.t === "mul") return factorCount(node.a) + factorCount(node.b);
  if (node.t === "pow" && !hasVar(node.b)) {
    const exponent = evaluate(node.b, {});
    return Number.isInteger(exponent) && exponent > 0 ? exponent * factorCount(node.a) : 0;
  }
  return hasVar(node) ? 1 : 0;
}

// ---------------------------------------------------------------------------
// Numbers
// ---------------------------------------------------------------------------

type NumberReading =
  | { ok: true; value: Rat; shape: "integer" | "decimal" | "fraction"; text: string }
  | { ok: false; verdict?: Verdict; mixed?: Rat; comma?: Rat };

/** Read one plain number: thousands commas allowed, mixed numbers and decimal commas flagged. */
function readNumber(text: string): NumberReading {
  let t = text.replace(/^\$\s*/, "").replace(/\s*°$/, "").trim();
  if (/^[+-]?\d{1,3}(,\d{3})+(\.\d+)?$/.test(t)) t = t.replace(/,/g, "");
  const mixed = /^([+-]?)(\d+) (\d+)\/(\d+)$/.exec(t);
  if (mixed && BigInt(mixed[4]) !== 0n) {
    const whole = BigInt(mixed[2]);
    const part = rat(BigInt(mixed[3]), BigInt(mixed[4]));
    const value = rat(whole * part.d + part.n, part.d);
    return { ok: false, mixed: mixed[1] === "-" ? rat(-value.n, value.d) : value };
  }
  const comma = /^([+-]?\d+),(\d+)$/.exec(t);
  if (comma) return { ok: false, comma: parseRat(`${comma[1]}.${comma[2]}`) ?? undefined };
  const value = parseRat(t);
  if (!value) return { ok: false };
  const shape = t.includes("/") ? "fraction" : t.includes(".") ? "decimal" : "integer";
  return { ok: true, value, shape, text: t };
}

/** SAT rule for a decimal that does not end: fill the space, truncated or rounded. */
function acceptsLongDecimal(expected: Rat, text: string, value: Rat): Verdict {
  const unsigned = text.replace(/^[+-]/, "");
  const [whole, places = ""] = unsigned.split(".");
  // Five characters fit: .6667 needs four decimals, 0.667 or 8.333 three, 33.33 two.
  const needed = Math.max(1, 4 - whole.length);
  const close = [cut(expected, places.length, "trunc"), cut(expected, places.length, "round")];
  if (!close.some((option) => sameRat(option, value))) return INCORRECT;
  return places.length >= needed ? CORRECT : format("more-digits");
}

function checkNumber(spec: Extract<CheckSpec, { kind: "number" }>, input: string): Verdict {
  const expected = parseRat(spec.value);
  if (!expected) throw new Error(`bad spec value ${spec.value}`);
  let text = stripLabel(input);
  const hasPercent = text.endsWith("%");
  if (hasPercent) text = text.slice(0, -1).trim();

  const reading = readNumber(text);
  if (!reading.ok) {
    if (reading.mixed) return sameRat(reading.mixed, expected) ? format("mixed-number") : INCORRECT;
    if (reading.comma) return sameRat(reading.comma, expected) ? format("decimal-comma") : INCORRECT;
    const node = parseExpression(text);
    if (node && !hasVar(node)) {
      const value = evaluate(node, {});
      return Math.abs(value - ratValue(expected)) < 1e-9 ? format("single-number") : INCORRECT;
    }
    return format("unreadable");
  }

  const { value, shape } = reading;
  if (hasPercent && !spec.percent) return sameRat(value, expected) ? format("no-percent") : INCORRECT;
  if (!sameRat(value, expected)) {
    if (spec.percent && !hasPercent && sameRat(rat(value.n * 100n, value.d), expected)) return format("use-percent");
    if (shape === "decimal" && !isTerminating(expected)) return acceptsLongDecimal(expected, reading.text, value);
    return INCORRECT;
  }
  if (spec.form === "decimal" && shape === "fraction") return format("use-decimal");
  if (spec.form === "fraction" && shape === "decimal") return format("use-fraction");
  if (spec.simplest && shape === "fraction") {
    const [, top, bottom] = /^[+-]?(\d+)\/(\d+)$/.exec(reading.text) ?? [];
    if (bottom && (BigInt(bottom) !== value.d || BigInt(top) !== (value.n < 0n ? -value.n : value.n))) {
      return format("simplify");
    }
  }
  return CORRECT;
}

// ---------------------------------------------------------------------------
// The other spec kinds
// ---------------------------------------------------------------------------

function checkPi(spec: Extract<CheckSpec, { kind: "pi" }>, input: string): Verdict {
  const coefficient = parseRat(spec.value);
  if (!coefficient) throw new Error(`bad spec value ${spec.value}`);
  const node = parseExpression(stripLabel(input));
  if (!node || hasVar(node)) return format("unreadable");
  const want = ratValue(coefficient) * Math.PI;
  const got = evaluate(node, {});
  if (!Number.isFinite(got)) return format("unreadable");
  if (hasPi(node)) return Math.abs(got - want) <= 1e-9 * Math.max(1, Math.abs(want)) ? CORRECT : INCORRECT;
  // A decimal approximation of the π answer is fine if it is close: 28.27 for 9π.
  if (Math.abs(got - want) <= 0.002 * Math.abs(want)) return CORRECT;
  return Math.abs(got - ratValue(coefficient)) < 1e-9 ? format("use-pi") : INCORRECT;
}

function checkRadical(spec: Extract<CheckSpec, { kind: "radical" }>, input: string): Verdict {
  const text = stripLabel(input).replace(/\s+/g, "");
  const node = parseExpression(text);
  if (!node || hasVar(node)) return format("unreadable");
  const want = spec.coef * Math.sqrt(spec.rad);
  const got = evaluate(node, {});
  if (Math.abs(got - want) > 1e-9 * Math.max(1, want)) {
    // 2.828 for 2√2 is the right size in the wrong form.
    const decimal = /^\d*\.\d+$/.test(text) && Math.abs(got - want) <= 0.005 * want;
    return decimal ? format("radical") : INCORRECT;
  }
  const integer = /^\d+$/.exec(text);
  if (integer) return spec.rad === 1 ? CORRECT : format("radical");
  const shape = /^(\d*)\*?√\(?(\d+)\)?$/.exec(text);
  if (!shape) return format("radical");
  const radicand = Number(shape[2]);
  for (let i = 2; i * i <= radicand; i += 1) if (radicand % (i * i) === 0) return format("radical");
  return CORRECT;
}

function checkExpression(spec: Extract<CheckSpec, { kind: "expression" }>, input: string): Verdict {
  const expected = parseExpression(normalize(spec.expr));
  if (!expected) throw new Error(`bad spec expr ${spec.expr}`);
  const text = input.replace(new RegExp(`^${spec.var === "y" ? "x" : "[a-z]"}\\s*=\\s*`), "");
  const node = parseExpression(text);
  if (!node) return format("unreadable");
  if (!sameFunction(node, expected, spec.var)) return INCORRECT;
  if (spec.form === "factored") return factorCount(node) >= 2 ? CORRECT : format("factor");
  if (hasGroupWithVar(node)) return format("combine");
  const degrees = terms(node).map(({ node: part }) => monomialDegree(part));
  if (degrees.some((degree) => degree === null) || new Set(degrees).size !== degrees.length) return format("combine");
  return CORRECT;
}

const NUMBER_PATTERN = /[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:\/\d+)?/g;

function numbersIn(text: string): Rat[] | null {
  const found = text.match(NUMBER_PATTERN) ?? [];
  const values = found.map((part) => parseRat(part));
  return values.every((value): value is Rat => value !== null) ? values : null;
}

function checkSet(spec: Extract<CheckSpec, { kind: "set" }>, input: string): Verdict {
  const expected = spec.values.map((value) => parseRat(value)!);
  const values = numbersIn(input.replace(/[a-z]\s*=/g, " "));
  if (!values || values.length === 0) return format("unreadable");
  const unique = values.filter((value, index) => values.findIndex((other) => sameRat(other, value)) === index);
  if (!unique.every((value) => expected.some((want) => sameRat(want, value)))) return INCORRECT;
  return unique.length === expected.length ? CORRECT : format("both-values");
}

function checkPair(spec: Extract<CheckSpec, { kind: "pair" }>, input: string): Verdict {
  const [wantX, wantY] = spec.values.map((value) => parseRat(value)!);
  const labelled = (name: string) => {
    const m = new RegExp(`${name}\\s*=\\s*(${NUMBER_PATTERN.source})`).exec(input);
    return m ? parseRat(m[1]) : null;
  };
  let x = labelled("x");
  let y = labelled("y");
  if (!x || !y) {
    const values = numbersIn(input);
    if (!values) return format("unreadable");
    if (values.length < 2) return values.length === 1 ? format("both-values") : format("unreadable");
    [x, y] = values;
  }
  return sameRat(x, wantX) && sameRat(y, wantY) ? CORRECT : INCORRECT;
}

const FLIP = { "<": ">", ">": "<", "<=": ">=", ">=": "<=" } as const;

function checkInequality(spec: Extract<CheckSpec, { kind: "inequality" }>, input: string): Verdict {
  const want = parseRat(spec.value);
  if (!want) throw new Error(`bad spec value ${spec.value}`);
  const text = input.replace(/\s+/g, "");
  let m = /^x(<=|>=|<|>)(.+)$/.exec(text);
  let op: keyof typeof FLIP | undefined;
  let side: string | undefined;
  if (m) {
    op = m[1] as keyof typeof FLIP;
    side = m[2];
  } else if ((m = /^(.+?)(<=|>=|<|>)x$/.exec(text))) {
    op = FLIP[m[2] as keyof typeof FLIP];
    side = m[1];
  }
  if (!op || !side) {
    const lone = readNumber(stripLabel(input));
    return lone.ok && sameRat(lone.value, want) ? format("inequality") : format("unreadable");
  }
  const reading = readNumber(side);
  if (!reading.ok) return format("unreadable");
  return op === spec.op && sameRat(reading.value, want) ? CORRECT : INCORRECT;
}

// ---------------------------------------------------------------------------

export function checkAnswer(spec: CheckSpec, raw: string): Verdict {
  const input = normalize(raw ?? "");
  if (!input) return format("empty");
  if (input.length > MAX_ANSWER_LENGTH) return format("unreadable");
  switch (spec.kind) {
    case "number":
      return checkNumber(spec, input);
    case "pi":
      return checkPi(spec, input);
    case "radical":
      return checkRadical(spec, input);
    case "expression":
      return checkExpression(spec, input);
    case "set":
      return checkSet(spec, input);
    case "pair":
      return checkPair(spec, input);
    case "inequality":
      return checkInequality(spec, input);
  }
}
