"""One hundred checked practice items for every lesson.

Each generator writes the student prompt, the displayed answer, a short
solution, and a machine-readable answer spec ("check") that the website uses
to grade a typed answer without ever sending the key to the browser.

Answers are computed here with SymPy. `recheck_bank` then reads every prompt
back the way a student sees it, recomputes the answer independently, and
compares it with the spec. The build stops on any disagreement.
"""

from __future__ import annotations

import math
import re

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

CODES = (
    ["0.1"]
    + [f"1.{i}" for i in range(1, 11)]
    + [f"2.{i}" for i in range(1, 9)]
    + [f"3.{i}" for i in range(1, 9)]
    + [f"4.{i}" for i in range(1, 7)]
    + [f"5.{i}" for i in range(1, 8)]
    + [f"6.{i}" for i in range(1, 5)]
)

MINUS = "−"
X, Y = sp.symbols("x y")
SUPERSCRIPT = {2: "²", 3: "³"}


# --------------------------------------------------------------------------
# Number and expression formatting
# --------------------------------------------------------------------------


def level_of(index: int) -> str:
    """Position in the bank: 40 easy, 40 medium, 20 SAT-style."""
    if index < 40:
        return "oson"
    if index < 80:
        return "orta"
    return "sat"


def fmt(value) -> str:
    """Machine form with an ASCII minus: 3, -3, 7/2."""
    value = sp.nsimplify(value) if isinstance(value, float) else sp.sympify(value)
    value = sp.simplify(value)
    if value.is_integer:
        return str(int(value))
    if value.is_rational:
        return f"{int(value.p)}/{int(value.q)}"
    return str(value)


def num(value) -> str:
    """Display form with a true minus sign: −3, −7/2."""
    return fmt(value).replace("-", MINUS)


def par(value) -> str:
    """A number written after an operator: negatives get parentheses."""
    text = num(value)
    return f"({text})" if text.startswith(MINUS) else text


def poly(expr, var: sp.Symbol = X) -> str:
    """5x² + 11x + 2, x − 4, 10 − x, −3x. No 1x, no + 0, no + (−2)."""
    p = sp.Poly(sp.expand(expr), var)
    terms = [(deg, sp.Rational(c)) for (deg,), c in p.terms() if c != 0]
    if not terms:
        return "0"
    if len(terms) == 2 and terms[0][0] == 1 and terms[0][1] < 0 and terms[1][1] > 0:
        terms = [terms[1], terms[0]]  # 10 − x reads better than −x + 10
    out = ""
    for index, (deg, coef) in enumerate(terms):
        size = abs(coef)
        if deg == 0:
            body = num(size)
        else:
            if size == 1:
                lead = ""
            elif size.q == 1:
                lead = num(size)
            else:
                lead = f"({num(size)})"
            body = f"{lead}{var}{SUPERSCRIPT.get(deg, '' if deg == 1 else f'^{deg}')}"
        if index == 0:
            out = (MINUS if coef < 0 else "") + body
        else:
            out += f" {MINUS if coef < 0 else '+'} {body}"
    return out


def binomial(a: int, b: int) -> str:
    """(ax + b) as a factor, written cleanly: (2x − 3), (x + 4)."""
    return f"({poly(a * X + b)})"


def root_factor(root: int) -> str:
    """The factor that is zero at `root`: x for 0, (x − 3) for 3, (x + 2) for −2."""
    return "x" if root == 0 else binomial(1, -root)


def pi_text(coef) -> str:
    """9π, π, π/3, 3π/2."""
    c = sp.Rational(coef)
    sign = MINUS if c < 0 else ""
    c = abs(c)
    top = "π" if c.p == 1 else f"{c.p}π"
    return sign + (top if c.q == 1 else f"{top}/{c.q}")


def pct(value) -> str:
    """A percent for display: 25%, 12.5%. Non-terminating values are not generated."""
    value = sp.Rational(value)
    if value.q == 1:
        return f"{num(value)}%"
    q = value.q
    while q % 2 == 0:
        q //= 2
    while q % 5 == 0:
        q //= 5
    if q != 1:
        raise AssertionError(f"percent {value} has no finite decimal")
    return format(sp.Float(value, 30), "f").rstrip("0").rstrip(".").replace("-", MINUS) + "%"


def plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


# --------------------------------------------------------------------------
# Answer specs. The website's checker reads these; see site/src/lib/answer-check.ts.
# --------------------------------------------------------------------------


def c_num(value, *, percent: bool = False, simplest: bool = False, form: str = "") -> dict:
    spec: dict = {"kind": "number", "value": fmt(value)}
    if percent:
        spec["percent"] = True
    if simplest:
        spec["simplest"] = True
    if form:
        spec["form"] = form  # "decimal" or "fraction"
    return spec


def c_pi(coef) -> dict:
    return {"kind": "pi", "value": fmt(coef)}


def c_set(*values) -> dict:
    return {"kind": "set", "values": [fmt(v) for v in values]}


def c_pair(x, y) -> dict:
    return {"kind": "pair", "values": [fmt(x), fmt(y)]}


def c_ineq(op: str, bound) -> dict:
    return {"kind": "inequality", "op": op, "value": fmt(bound)}


def c_expr(expr, *, form: str = "simplified", var: str = "x") -> dict:
    return {"kind": "expression", "expr": str(sp.expand(expr)), "form": form, "var": var}


def c_radical(coef: int, rad: int) -> dict:
    return {"kind": "radical", "coef": coef, "rad": rad}


def item(en: str, uz: str, answer: str, sen: str, suz: str, check: dict) -> dict:
    return {
        "promptEn": en,
        "promptUz": uz,
        "answer": answer,
        "solutionEn": sen,
        "solutionUz": suz,
        "check": check,
    }


def take(gen) -> list[dict]:
    rows = []
    seen: set[str] = set()
    k = 0
    while len(rows) < 100:
        row = gen(k)
        k += 1
        if row["promptEn"] in seen:
            if k > 4000:
                raise RuntimeError(f"could not find 100 unique prompts, stuck at {len(rows)}")
            continue
        seen.add(row["promptEn"])
        rows.append(row)
    for index, row in enumerate(rows):
        row["id"] = f"{index + 1:03d}"
        row["level"] = level_of(index)
    return rows


# --------------------------------------------------------------------------
# Generators, one per lesson
# --------------------------------------------------------------------------


def g_fractions(k: int) -> dict:
    op = k % 4
    a, b = 1 + (k % 9), 2 + ((k // 2) % 8)
    c, d = 1 + ((k * 3) % 8), 2 + ((k * 5) % 7)
    left, right = sp.Rational(a, b), sp.Rational(c, d)
    if op == 0:
        value = left + right
        sign, word, suz = "+", "sum", "yig'indisi"
    elif op == 1:
        if left < right:
            left, right = right, left
            a, b, c, d = c, d, a, b
        value = left - right
        sign, word, suz = MINUS, "difference", "ayirmasi"
    elif op == 2:
        value = left * right
        sign, word, suz = "×", "product", "ko'paytmasi"
    else:
        value = left / right
        sign, word, suz = "÷", "quotient", "bo'linmasi"
    answer = num(value)
    return item(
        f"Find the {word} {a}/{b} {sign} {c}/{d} as a simplified fraction.",
        f"{a}/{b} {sign} {c}/{d} ning {suz}ni qisqartirilgan kasrda toping.",
        answer,
        f"Compute {a}/{b} {sign} {c}/{d}. The simplified value is {answer}.",
        f"{a}/{b} {sign} {c}/{d} ni hisoblang. Qisqartirilgan qiymat {answer}.",
        c_num(value, simplest=True, form="fraction"),
    )


def g_abs(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        n = k + 1
        return item(
            f"Evaluate |{MINUS}{n}|.",
            f"|{MINUS}{n}| ning qiymatini toping.",
            str(n),
            f"The distance from {MINUS}{n} to 0 is {n}.",
            f"{MINUS}{n} dan 0 gacha masofa {n}.",
            c_num(n),
        )
    if kind == 1:
        a, b = (k % 12) + 1, ((k * 2) % 9) + 1
        return item(
            f"Evaluate |{a}| + |{MINUS}{b}|.",
            f"|{a}| + |{MINUS}{b}| ifodaning qiymatini toping.",
            str(a + b),
            f"{a} + {b} = {a + b}. Both bars are distances.",
            f"{a} + {b} = {a + b}. Ikkala modul ham masofa.",
            c_num(a + b),
        )
    left, right = -(k % 15), (k % 11) + 1
    dist = abs(right - left)
    return item(
        f"What is the distance on the number line between {num(left)} and {right}?",
        f"Son o'qida {num(left)} va {right} orasidagi masofa necha?",
        str(dist),
        f"|{right} {MINUS} {par(left)}| = {dist}.",
        f"|{right} {MINUS} {par(left)}| = {dist}.",
        c_num(dist),
    )


def g_order(k: int) -> dict:
    a = 2 + (k % 9)
    b = 2 + ((k * 3) % 8)
    c = 1 + (k % 6)
    d = 1 + ((k * 2) % 5)
    kind = k % 4
    if kind == 0:
        value = a + b * c
        expr = f"{a} + {b} × {c}"
    elif kind == 1:
        value = (a + b) * c
        expr = f"({a} + {b}) × {c}"
    elif kind == 2:
        value = a**2 + b**2
        expr = f"{a}² + {b}²"
    else:
        value = a * b - c * (d + 1)
        expr = f"{a} × {b} {MINUS} {c}({d} + 1)"
    return item(
        f"Evaluate {expr}.",
        f"{expr} ifodaning qiymatini toping.",
        num(value),
        f"Follow grouping, then powers, then multiplication. The value is {num(value)}.",
        f"Avval qavs, so'ng daraja, so'ng ko'paytirish. Qiymat {num(value)}.",
        c_num(value),
    )


def g_decimals(k: int) -> dict:
    kind = k % 3
    dens = (2, 4, 5, 8, 10, 16, 20, 25, 40, 50)
    if kind == 0:
        d = dens[k % len(dens)]
        n = 1 + ((k * 3 + k // 10) % (d - 1))
        value = sp.Rational(n, d)
        dec = format(sp.Float(value, 20), "f").rstrip("0").rstrip(".")
        if sp.Rational(dec) != value:
            raise AssertionError(f"{n}/{d} has no short decimal")
        return item(
            f"Write the fraction {n}/{d} as a decimal.",
            f"{n}/{d} kasrini o'nli kasr qilib yozing.",
            dec,
            f"Divide {n} by {d}. The decimal is {dec} (= {fmt(value)}).",
            f"{n} ni {d} ga bo'ling. O'nli kasr {dec} (= {fmt(value)}).",
            c_num(value, form="decimal"),
        )
    if kind == 1:
        hundredths = 1 + (k % 97)
        value = sp.Rational(hundredths, 100)
        text = f"0.{hundredths:02d}"
        return item(
            f"Write the decimal {text} as a simplified fraction.",
            f"{text} o'nli kasrini qisqartirilgan kasr qilib yozing.",
            fmt(value),
            f"{text} means {hundredths}/100, which simplifies to {fmt(value)}.",
            f"{text} degani {hundredths}/100, qisqartirilsa {fmt(value)}.",
            c_num(value, simplest=True, form="fraction"),
        )
    p = 1 + (k % 11)
    q = 2 + ((k * 2) % 9)
    r = 1 + ((k * 3) % 8)
    s = 2 + ((k * 5) % 9)
    value = sp.Rational(p, q) + sp.Rational(r, s)
    return item(
        f"Add {p}/{q} and {r}/{s}. Give a simplified fraction.",
        f"{p}/{q} va {r}/{s} ni qo'shing. Qisqartirilgan kasr yozing.",
        fmt(value),
        f"Use a common denominator. The sum is {fmt(value)}.",
        f"Umumiy maxrajga keltiring. Yig'indi {fmt(value)}.",
        c_num(value, simplest=True, form="fraction"),
    )


def g_percent(k: int) -> dict:
    """Percent of a number, percent of a whole, and conversions (change is lesson 1.5)."""
    kind = k % 10

    if kind == 0:
        p = 5 * (1 + ((k * 3) % 19))
        n = 4 * (5 + ((k * 7) % 45))
        value = sp.Rational(p, 100) * n
        return item(
            f"What is {p}% of {n}?",
            f"{n} ning {p} foizi necha?",
            num(value),
            f"Write {p}% as {p}/100. ({p}/100) × {n} = {num(value)}.",
            f"{p}% ni {p}/100 deb yozing. ({p}/100) × {n} = {num(value)}.",
            c_num(value),
        )

    if kind == 1:
        p = 5 * (1 + ((k * 2) % 18))
        whole = 20 * (1 + ((k * 5) % 20))
        part = int(sp.Rational(p, 100) * whole)
        return item(
            f"{part} is what percent of {whole}?",
            f"{part} soni {whole} ning necha foizi?",
            f"{p}%",
            f"The whole is after 'of': ({part}/{whole}) × 100 = {p}%.",
            f"Butun — 'of' dan keyin: ({part}/{whole}) × 100 = {p}%.",
            c_num(p, percent=True),
        )

    if kind == 2:
        dens = (2, 4, 5, 8, 10, 20, 25, 50)
        d = dens[k % len(dens)]
        n = 1 + ((k // len(dens)) % (d - 1 if d > 1 else 1))
        while sp.gcd(n, d) != 1 and n < d:
            n += 1
        if n >= d:
            n = 1
        value = sp.Rational(n, d) * 100
        return item(
            f"Write {n}/{d} as a percent.",
            f"{n}/{d} ni foizda yozing.",
            pct(value),
            f"A percent is the fraction times 100. ({n}/{d}) × 100 = {pct(value)}.",
            f"Foiz — kasrni 100 ga ko'paytirish. ({n}/{d}) × 100 = {pct(value)}.",
            c_num(value, percent=True),
        )

    if kind == 3:
        p = 5 * (1 + ((k * 4) % 19))
        value = sp.Rational(p, 100)
        return item(
            f"Write {p}% as a simplified fraction.",
            f"{p}% ni qisqartirilgan kasrda yozing.",
            fmt(value),
            f"{p}% = {p}/100 = {fmt(value)} after simplifying.",
            f"{p}% = {p}/100 = {fmt(value)} (qisqartirilgan).",
            c_num(value, simplest=True, form="fraction"),
        )

    if kind == 4:
        p = 5 * (2 + ((k * 3) % 16))
        whole = 10 * (2 + ((k * 11) % 28))
        part = sp.Rational(p, 100) * whole
        return item(
            f"{num(part)} is {p}% of what number?",
            f"{num(part)} qaysi sonning {p} foizi?",
            num(whole),
            f"Part = percent × whole, so whole = {num(part)} ÷ ({p}/100) = {num(whole)}.",
            f"Qism = foiz × butun, demak butun = {num(part)} ÷ ({p}/100) = {num(whole)}.",
            c_num(whole),
        )

    if kind == 5:
        price = 20 * (2 + ((k * 5) % 18))
        p = 5 * (2 + ((k * 2) % 15))
        off = sp.Rational(p, 100) * price
        return item(
            f"A ${price} item is discounted by {p}%. How many dollars are taken off?",
            f"{price} dollarlik mahsulotga {p}% chegirma. Necha dollar ayiriladi?",
            num(off),
            f"The discount is {p}% of {price}: ({p}/100) × {price} = {num(off)}.",
            f"Chegirma — {price} ning {p} foizi: ({p}/100) × {price} = {num(off)}.",
            c_num(off),
        )

    if kind == 6:
        price = 25 * (2 + ((k * 7) % 16))
        p = 5 * (1 + ((k * 5) % 14))
        paid = price * sp.Rational(100 - p, 100)
        return item(
            f"A ${price} jacket is {p}% off. What is the sale price, in dollars?",
            f"{price} dollarlik kurtka {p}% chegirmada. Sotuv narxi necha dollar?",
            num(paid),
            f"You pay {100 - p}% of the original: ({100 - p}/100) × {price} = {num(paid)}.",
            f"To'lanadigan qism {100 - p}%: ({100 - p}/100) × {price} = {num(paid)}.",
            c_num(paid),
        )

    if kind == 7:
        p = 100 + 5 * (1 + ((k * 3) % 20))
        n = 5 * (2 + ((k * 4) % 24))
        value = sp.Rational(p, 100) * n
        return item(
            f"What is {p}% of {n}?",
            f"{n} ning {p} foizi necha?",
            num(value),
            f"{p}% is more than one whole: ({p}/100) × {n} = {num(value)}.",
            f"{p}% birdan katta: ({p}/100) × {n} = {num(value)}.",
            c_num(value),
        )

    if kind == 8:
        p = 5 * (1 + ((k * 3) % 4))
        n = 20 * (2 + ((k * 5) % 18))
        value = sp.Rational(p, 100) * n
        return item(
            f"Sales tax is {p}%. How many dollars of tax are collected on a ${n} purchase?",
            f"Sotuv solig'i {p}%. {n} dollarlik xarid uchun necha dollar soliq olinadi?",
            num(value),
            f"{p}% of {n} is ({p}/100) × {n} = {num(value)}.",
            f"{n} ning {p} foizi ({p}/100) × {n} = {num(value)}.",
            c_num(value),
        )

    total = 20 * (3 + ((k * 3) % 15))
    p = 5 * (2 + ((k * 7) % 12))
    kept = total * sp.Rational(100 - p, 100)
    return item(
        f"A class has {total} students and {p}% are absent. How many students are present?",
        f"{total} o'quvchili sinfda {p}% yo'q. Nechta o'quvchi bor?",
        num(kept),
        f"Present is {100 - p}% of {total}: ({100 - p}/100) × {total} = {num(kept)}.",
        f"Bor o'quvchilar {total} ning {100 - p} foizi: ({100 - p}/100) × {total} = {num(kept)}.",
        c_num(kept),
    )


def g_change(k: int) -> dict:
    if k % 5 == 4:
        start = 20 * (1 + (k % 8))
        first = 10 * (1 + (k % 3))
        second = 10
        final = start * sp.Rational(100 + first, 100) * sp.Rational(100 - second, 100)
        return item(
            f"A price of {start} rises by {first}% and then falls by {second}%. What is the final price?",
            f"{start} narx {first}% ga oshadi, so'ng {second}% ga tushadi. Oxirgi narx necha?",
            num(final),
            f"Multiply by {100 + first}/100 and then by {100 - second}/100. The result is {num(final)}.",
            f"{100 + first}/100 ga, so'ng {100 - second}/100 ga ko'paytiring. Natija {num(final)}.",
            c_num(final),
        )
    old = (20, 25, 40, 50, 80, 100, 125, 160, 200, 250, 400, 500)[k % 12]
    change = 5 * (1 + (k % 7)) * (1 + (k // 12) % 3)
    if k % 2 == 0:
        new = old + change
        word, suz = "increase", "oshdi"
    else:
        if change >= old:
            change = old // 2
        new = old - change
        word, suz = "decrease", "kamaydi"
    value = sp.Rational(change, old) * 100
    return item(
        f"A value goes from {old} to {new}. By what percent did it {word}?",
        f"Qiymat {old} dan {new} ga o'tdi. Necha foizga {suz}?",
        pct(value),
        f"The change is {change} and the original is {old}. ({change}/{old}) × 100 = {pct(value)}.",
        f"O'zgarish {change}, eski son {old}. ({change}/{old}) × 100 = {pct(value)}.",
        c_num(value, percent=True),
    )


def g_ratio(k: int) -> dict:
    a = 1 + (k % 15)
    b = a + 1 + ((k * 3) % 12)
    scale = 2 + ((k * 5) % 14)
    total = (a + b) * scale
    if k % 2 == 0:
        answer, which, qaysi = a * scale, "smaller", "kichik"
    else:
        answer, which, qaysi = b * scale, "larger", "katta"
    return item(
        f"Two parts are in the ratio {a}:{b} and total {total}. What is the {which} part?",
        f"Ikki qism {a}:{b} nisbatda va jami {total}. {qaysi.capitalize()} qism necha?",
        str(answer),
        f"There are {a + b} shares, so one share is {total}/{a + b} = {scale}. The {which} part is {answer}.",
        f"Jami {a + b} ulush, bitta ulush {total}/{a + b} = {scale}. {qaysi.capitalize()} qism {answer}.",
        c_num(answer),
    )


def g_prop(k: int) -> dict:
    if k % 4 == 3:
        workers = 2 + (k % 6)
        days = 4 + (k % 8)
        job = workers * days
        options = [d for d in range(2, job) if job % d == 0 and d != workers] or [job]
        more = options[(k // 4) % len(options)]
        answer = job // more
        return item(
            f"{workers} painters finish a job in {days} days. How many days do {more} painters need?",
            f"{workers} bo'yoqchi ishni {days} kunda tugatadi. {more} bo'yoqchiga necha kun kerak?",
            str(answer),
            f"The job is {workers} × {days} = {job} painter-days. {job}/{more} = {plural(answer, 'day')}.",
            f"Ish {workers} × {days} = {job} bo'yoqchi-kun. {job}/{more} = {answer} kun.",
            c_num(answer),
        )
    a, b = 1 + (k % 8), 2 + (k % 7)
    scale = 2 + (k % 6)
    left = a * scale
    x = b * scale
    return item(
        f"Solve {a}/{b} = {left}/x.",
        f"{a}/{b} = {left}/x tenglamasidan x ni toping.",
        str(x),
        f"The scale from {a} to {left} is {scale}, so x = {b} × {scale} = {x}.",
        f"{a} dan {left} gacha masshtab {scale}, demak x = {b} × {scale} = {x}.",
        c_num(x),
    )


def g_exp(k: int) -> dict:
    base = 2 + (k % 8)
    m = 1 + ((k // 8) % 5)
    n = 1 + ((k // 40) % 5)
    kind = k % 3
    if kind == 0:
        value = base ** (m + n)
        en = f"Evaluate {base}^{m} × {base}^{n}."
        uz = f"{base}^{m} × {base}^{n} ning qiymatini toping."
        sen = f"Same base: add the exponents. {base}^{m + n} = {value}."
        suz = f"Asos bir xil: ko'rsatkichlarni qo'shing. {base}^{m + n} = {value}."
        check = c_num(value)
    elif kind == 1:
        value = base ** (m * n)
        en = f"Evaluate ({base}^{m})^{n}."
        uz = f"({base}^{m})^{n} ning qiymatini toping."
        sen = f"Power of a power: multiply the exponents. {base}^{m * n} = {value}."
        suz = f"Darajaning darajasi: ko'rsatkichlarni ko'paytiring. {base}^{m * n} = {value}."
        check = c_num(value)
    else:
        value = sp.Rational(1, base**m)
        en = f"Write {base}^({MINUS}{m}) as a simplified fraction."
        uz = f"{base}^({MINUS}{m}) ni qisqartirilgan kasr qilib yozing."
        sen = f"A negative exponent means the reciprocal: 1/{base}^{m} = {fmt(value)}."
        suz = f"Manfiy daraja — teskari son: 1/{base}^{m} = {fmt(value)}."
        check = c_num(value, simplest=True, form="fraction")
    return item(en, uz, num(value), sen, suz, check)


SQUAREFREE = (2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, 29, 30)
ROOT_COMPOSITES = sorted({s * s * f for s in range(2, 13) for f in SQUAREFREE if s * s * f <= 720})


def sqrt_parts(n: int) -> tuple[int, int]:
    """n = coef² × rad with rad squarefree."""
    coef, rad = 1, n
    i = 2
    while i * i <= rad:
        while rad % (i * i) == 0:
            rad //= i * i
            coef *= i
        i += 1
    return coef, rad


def radical_text(coef: int, rad: int) -> str:
    if rad == 1:
        return str(coef)
    return f"√{rad}" if coef == 1 else f"{coef}√{rad}"


def g_roots(k: int) -> dict:
    kind = k % 10
    if kind == 8:
        root = 2 + ((k // 10) % 19)
        n = root * root
    elif kind == 9:
        n = SQUAREFREE[(k // 10) % len(SQUAREFREE)]
    else:
        n = ROOT_COMPOSITES[((k // 10) * 8 + kind) % len(ROOT_COMPOSITES)]
    coef, rad = sqrt_parts(n)
    text = radical_text(coef, rad)
    if rad == 1:
        sen = f"{n} is a perfect square: √{n} = {text}."
        suz = f"{n} — to'la kvadrat: √{n} = {text}."
    elif coef == 1:
        sen = f"{n} has no square factor other than 1, so √{n} is already simplest."
        suz = f"{n} ning 1 dan boshqa kvadrat ko'paytuvchisi yo'q, √{n} allaqachon eng sodda."
    else:
        sen = f"{n} = {coef * coef} × {rad}, and √{coef * coef} = {coef}. So √{n} = {text}."
        suz = f"{n} = {coef * coef} × {rad}, √{coef * coef} = {coef}. Demak √{n} = {text}."
    return item(
        f"Simplify √{n}.",
        f"√{n} ni soddalashtiring.",
        text,
        sen,
        suz,
        c_radical(coef, rad),
    )


def g_sci(k: int) -> dict:
    if k % 2 == 0:
        tenths = 10 + ((k // 2) * 7) % 90  # 1.0 to 9.9
        exp = 2 + ((k // 30) % 5)
        coeff = sp.Rational(tenths, 10)
        coeff_text = fmt(coeff) if coeff.q == 1 else f"{tenths // 10}.{tenths % 10}"
        value = coeff * 10**exp
        return item(
            f"Write {coeff_text} × 10^{exp} as an ordinary number.",
            f"{coeff_text} × 10^{exp} ni oddiy son qilib yozing.",
            num(value),
            f"Move the decimal point {exp} places to the right. The number is {num(value)}.",
            f"O'nli nuqtani {exp} o'rin o'ngga suring. Son {num(value)}.",
            c_num(value),
        )
    hours = sp.Rational(1 + ((k // 2) % 40), 2)
    minutes = hours * 60
    hours_text = fmt(hours) if hours.q == 1 else f"{int(hours)}.5"
    return item(
        f"Convert {hours_text} hours to minutes.",
        f"{hours_text} soatni daqiqaga aylantiring.",
        num(minutes),
        f"One hour is 60 minutes. {hours_text} × 60 = {num(minutes)} minutes.",
        f"Bir soat 60 daqiqa. {hours_text} × 60 = {num(minutes)} daqiqa.",
        c_num(minutes),
    )


def g_expr(k: int) -> dict:
    a = 2 + (k % 7)
    b = 1 + ((k * 3) % 9)
    c = (k % 11) - 5
    if c == 0:
        c = 6
    value = sp.expand(a * (X + b) + c * X)
    tail = f"+ {c}x" if c > 0 else f"{MINUS} {abs(c)}x" if c != -1 else f"{MINUS} x"
    if c == 1:
        tail = "+ x"
    expr = f"{a}(x + {b}) {tail}"
    answer = poly(value)
    return item(
        f"Simplify {expr}.",
        f"{expr} ifodasini soddalashtiring.",
        answer,
        f"Distribute: {poly(a * X + a * b)} {tail}. Combine like terms: {answer}.",
        f"Qavsni oching: {poly(a * X + a * b)} {tail}. O'xshash hadlarni birlashtiring: {answer}.",
        c_expr(value),
    )


def g_linear(k: int) -> dict:
    a = 1 + (k % 9)
    x0 = (k % 13) - 4
    b = (k % 11) - 3
    if a == 1 and b == 0:
        b = 5
    right = a * x0 + b
    lhs = poly(a * X + b)
    steps_en, steps_uz = [], []
    if b > 0:
        steps_en.append(f"Subtract {b} from both sides: {poly(a * X)} = {num(right - b)}.")
        steps_uz.append(f"Ikki tomondan {b} ni ayiring: {poly(a * X)} = {num(right - b)}.")
    elif b < 0:
        steps_en.append(f"Add {-b} to both sides: {poly(a * X)} = {num(right - b)}.")
        steps_uz.append(f"Ikki tomonga {-b} ni qo'shing: {poly(a * X)} = {num(right - b)}.")
    if a != 1:
        steps_en.append(f"Divide by {a}: x = {num(x0)}.")
        steps_uz.append(f"{a} ga bo'ling: x = {num(x0)}.")
    return item(
        f"Solve {lhs} = {num(right)}.",
        f"{lhs} = {num(right)} tenglamasini yeching.",
        f"x = {num(x0)}",
        " ".join(steps_en),
        " ".join(steps_uz),
        c_num(x0),
    )


def g_frac_eq(k: int) -> dict:
    p = 1 + (k % 12)
    q = p + 1 + ((k // 12) % 8)
    mult = 1 + ((k // 96) % 8)
    product = p * mult
    x0 = mult * q
    return item(
        f"Solve ({p}/{q})x = {product}.",
        f"({p}/{q})x = {product} tenglamasini yeching.",
        f"x = {x0}",
        f"Multiply both sides by the reciprocal {q}/{p}. x = {product} × {q}/{p} = {x0}.",
        f"Ikki tomonni teskari kasr {q}/{p} ga ko'paytiring. x = {product} × {q}/{p} = {x0}.",
        c_num(x0),
    )


INEQ_SHOW = {"<": "<", ">": ">", "<=": "≤", ">=": "≥"}
INEQ_FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}


def g_ineq(k: int) -> dict:
    kind = k % 5
    step = k // 5
    if kind in (0, 1):
        added = 1 + step % 25
        gap = 1 + (step // 3) % 20 - (8 if kind == 1 else 0)
        limit = added + gap
        op = "<" if kind == 0 else "<="
        en = f"Solve x + {added} {INEQ_SHOW[op]} {num(limit)}."
        sen = f"Subtract {added} from both sides. The sign stays."
        suz = f"Ikki tomondan {added} ni ayiring. Belgi o'zgarmaydi."
        bound = gap
    elif kind == 2:
        taken = 2 + step % 20
        rhs = (step % 13) - 4
        op = ">="
        en = f"Solve x {MINUS} {taken} {INEQ_SHOW[op]} {num(rhs)}."
        sen = f"Add {taken} to both sides. The sign stays."
        suz = f"Ikki tomonga {taken} ni qo'shing. Belgi o'zgarmaydi."
        bound = rhs + taken
    elif kind == 3:
        a = 2 + step % 7
        bound = sp.Rational((step % 15) - 5, 1) if step % 3 else sp.Rational(1 + step % 9, a)
        op = ">"
        en = f"Solve {a}x {INEQ_SHOW[op]} {num(a * bound)}."
        sen = f"Divide by the positive number {a}. The sign stays."
        suz = f"Musbat {a} ga bo'ling. Belgi o'zgarmaydi."
    else:
        a = 2 + step % 6
        bound = sp.Integer(1 + step % 30)
        start = ">" if step % 2 == 0 else "<="
        op = INEQ_FLIP[start]
        en = f"Solve {MINUS}{a}x {INEQ_SHOW[start]} {num(-a * bound)}."
        sen = f"Divide by {MINUS}{a}. Dividing by a negative number flips the sign."
        suz = f"{MINUS}{a} ga bo'ling. Manfiy songa bo'lganda belgi teskari bo'ladi."
        bound = sp.Integer(bound)
    answer = f"x {INEQ_SHOW[op]} {num(bound)}"
    uz = re.sub(r"^Solve (.+)\.$", r"\1 tengsizligini yeching.", en)
    return item(en, uz, answer, f"{sen} {answer}.", f"{suz} {answer}.", c_ineq(op, bound))


def g_words(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        extra = 2 + ((k // 3) % 30)
        total = extra + 3 + ((k // 90) % 25)
        number = total - extra
        return item(
            f"A number increased by {extra} is {total}. What is the number?",
            f"Sonning ustiga {extra} qo'shilsa, {total} chiqadi. Son necha?",
            str(number),
            f"x + {extra} = {total}, so x = {number}.",
            f"x + {extra} = {total}, demak x = {number}.",
            c_num(number),
        )
    if kind == 1:
        fee = 2 + ((k // 3) % 15)
        rate = 2 + ((k // 45) % 10)
        count = 2 + ((k // 450) % 12) + (k // 3) % 7
        total = fee + rate * count
        return item(
            f"Tickets cost ${rate} each plus a ${fee} fee. The total is ${total}. How many tickets were bought?",
            f"Chipta {rate} dollardan, ustiga {fee} dollar xizmat haqi. Jami {total} dollar. Nechta chipta olingan?",
            str(count),
            f"{rate}n + {fee} = {total}, so {rate}n = {total - fee} and n = {count}.",
            f"{rate}n + {fee} = {total}, demak {rate}n = {total - fee} va n = {count}.",
            c_num(count),
        )
    gap = 1 + ((k // 3) % 20)
    number = 3 + ((k // 60) % 20)
    total = 3 * number - gap
    return item(
        f"Three times a number, decreased by {gap}, is {total}. What is the number?",
        f"Sonning uch baravaridan {gap} ayirilsa, {total} chiqadi. Son necha?",
        str(number),
        f"3x {MINUS} {gap} = {total}, so 3x = {total + gap} and x = {number}.",
        f"3x {MINUS} {gap} = {total}, demak 3x = {total + gap} va x = {number}.",
        c_num(number),
    )


def g_slope(k: int) -> dict:
    x1 = (k % 9) - 3
    y1 = (k % 7) - 2
    run = 1 + (k % 6)
    rise = (k % 11) - 5
    if rise == 0 and k % 2 == 0:
        rise = 2
    x2, y2 = x1 + run, y1 + rise
    slope = sp.Rational(rise, run)
    p1, p2 = f"({num(x1)}, {num(y1)})", f"({num(x2)}, {num(y2)})"
    reduced = "" if slope.q == run and abs(slope.p) == abs(rise) else f" = {num(slope)}"
    return item(
        f"What is the slope of the line through {p1} and {p2}?",
        f"{p1} va {p2} nuqtalardan o'tgan to'g'ri chiziqning qiyaligi necha?",
        num(slope),
        f"Rise = {num(y2)} {MINUS} {par(y1)} = {num(rise)}. Run = {num(x2)} {MINUS} {par(x1)} = {run}. Slope = {num(rise)}/{run}{reduced}.",
        f"Ko'tarilish = {num(y2)} {MINUS} {par(y1)} = {num(rise)}. Yugurish = {num(x2)} {MINUS} {par(x1)} = {run}. Qiyalik = {num(rise)}/{run}{reduced}.",
        c_num(slope),
    )


def g_system(k: int) -> dict:
    x0 = (k % 20) - 8
    y0 = ((k // 20) % 15) - 6
    s = x0 + y0
    t = x0 - y0
    answer = f"x = {num(x0)}, y = {num(y0)}"
    return item(
        f"Solve the system x + y = {num(s)} and x {MINUS} y = {num(t)}.",
        f"x + y = {num(s)} va x {MINUS} y = {num(t)} sistemasini yeching.",
        answer,
        f"Add the equations: 2x = {num(s + t)}, so x = {num(x0)}. Then y = {num(s)} {MINUS} {par(x0)} = {num(y0)}.",
        f"Tenglamalarni qo'shing: 2x = {num(s + t)}, demak x = {num(x0)}. So'ng y = {num(s)} {MINUS} {par(x0)} = {num(y0)}.",
        c_pair(x0, y0),
    )


def g_func(k: int) -> dict:
    a = 1 + (k % 8)
    b = (k % 13) - 5
    n = (k % 10) - 2
    value = a * n + b
    rule = poly(a * X + b)
    plug = (num(n) if a == 1 else f"{a} × {par(n)}") + (f" + {b}" if b > 0 else f" {MINUS} {-b}" if b < 0 else "")
    return item(
        f"If f(x) = {rule}, what is f({num(n)})?",
        f"Agar f(x) = {rule} bo'lsa, f({num(n)}) necha?",
        num(value),
        f"Put {num(n)} in for x: {plug} = {num(value)}.",
        f"x o'rniga {num(n)} ni qo'ying: {plug} = {num(value)}.",
        c_num(value),
    )


def g_poly(k: int) -> dict:
    a = 1 + (k % 5)
    b = (k % 9) - 3
    c = 1 + ((k * 2) % 4)
    d = (k % 7) - 2
    if b == 0:
        b = 4
    if d == 0:
        d = -3
    value = sp.expand((a * X + b) * (c * X + d))
    answer = poly(value)
    first, outer, inner, last = a * c, a * d, b * c, b * d
    return item(
        f"Expand {binomial(a, b)}{binomial(c, d)}.",
        f"{binomial(a, b)}{binomial(c, d)} ifodasini qavssiz yozing.",
        answer,
        f"Each term meets each term: {poly(first * X**2)}, {poly(outer * X)}, {poly(inner * X)}, {num(last)}. Combine: {answer}.",
        f"Har bir had har bir had bilan ko'paytiriladi: {poly(first * X**2)}, {poly(outer * X)}, {poly(inner * X)}, {num(last)}. Birlashtiring: {answer}.",
        c_expr(value),
    )


def g_factor(k: int) -> dict:
    kind = k % 3
    r = 1 + ((k // 3) % 12)
    s = r + 1 + ((k // 36) % 8)
    if kind == 0:
        roots = (-r, -s)  # (x + r)(x + s)
    elif kind == 1:
        roots = (r, s)  # (x − r)(x − s)
    else:
        roots = (-s, r)  # (x + s)(x − r)
    value = sp.expand((X - roots[0]) * (X - roots[1]))
    factors = f"{binomial(1, -roots[0])}{binomial(1, -roots[1])}"
    product, total = roots[0] * roots[1], -(roots[0] + roots[1])
    return item(
        f"Factor {poly(value)}.",
        f"{poly(value)} ni ko'paytuvchilarga ajrating.",
        factors,
        f"Find two numbers that multiply to {num(product)} and add to {num(total)}: {num(-roots[0])} and {num(-roots[1])}.",
        f"Ko'paytmasi {num(product)}, yig'indisi {num(total)} bo'lgan ikki son: {num(-roots[0])} va {num(-roots[1])}.",
        c_expr(value, form="factored"),
    )


def g_quad(k: int) -> dict:
    r = (k % 25) - 10
    s = r + 1 + ((k // 25) % 12)
    value = sp.expand((X - r) * (X - s))
    answer = f"x = {num(r)} or x = {num(s)}"
    return item(
        f"Solve {poly(value)} = 0.",
        f"{poly(value)} = 0 tenglamasini yeching.",
        answer,
        f"Factor: {root_factor(r)}{root_factor(s)} = 0. A product is zero when a factor is zero: {answer}.",
        f"Ajrating: {root_factor(r)}{root_factor(s)} = 0. Ko'paytma nol bo'lishi uchun ko'paytuvchi nol bo'ladi: x = {num(r)} yoki x = {num(s)}.",
        c_set(r, s),
    )


def g_vertex(k: int) -> dict:
    h = (k % 11) - 5
    m = 1 + (k % 8)
    sign = 1 if k % 2 == 0 else -1
    top = 3 + (k % 6) + (k // 48)
    name, uz = ("minimum", "eng kichik") if sign == 1 else ("maximum", "eng katta")
    lead = "" if m == 1 else str(m)
    if sign == -1:
        lead = MINUS + lead
    square = "x²" if h == 0 else f"{binomial(1, -h)}²"
    rule = f"{lead}{square} + {top}"
    word, word_uz = ("positive", "musbat") if sign == 1 else ("negative", "manfiy")
    return item(
        f"What is the {name} value of y = {rule}?",
        f"y = {rule} ning {uz} qiymati necha?",
        str(top),
        f"The squared part is 0 at x = {num(h)}. With a {word} leading coefficient that is the {name}, so the value is {top}.",
        f"Kvadrat qism x = {num(h)} da 0 bo'ladi. Yetakchi koeffitsiyent {word_uz}, demak bu {uz} qiymat: {top}.",
        c_num(top),
    )


def g_equiv(k: int) -> dict:
    a = 2 + (k % 6)
    b = 1 + (k % 8)
    c = 1 + ((k // 6) % 5)
    value = sp.expand(a * (X + b) - c * X)
    tail = f"{MINUS} x" if c == 1 else f"{MINUS} {c}x"
    expr = f"{a}(x + {b}) {tail}"
    answer = poly(value)
    return item(
        f"Write an expression equivalent to {expr} with no parentheses.",
        f"{expr} ga teng kuchli ifodani qavssiz yozing.",
        answer,
        f"Distribute and combine like terms: {poly(a * X + a * b)} {tail} = {answer}.",
        f"Qavsni oching va o'xshash hadlarni birlashtiring: {poly(a * X + a * b)} {tail} = {answer}.",
        c_expr(value),
    )


def g_rational(k: int) -> dict:
    p = 2 + (k % 40)
    q = 1 + ((k // 40) % 15)
    if math.gcd(p, q) != 1 and k % 2 == 0:
        q += 1
    x0 = sp.Rational(p, q)
    return item(
        f"Solve {p}/x = {q}.",
        f"{p}/x = {q} tenglamasini yeching.",
        f"x = {num(x0)}",
        f"Multiply both sides by x, then divide by {q}: x = {p}/{q} = {num(x0)}. Zero is excluded and is not the answer.",
        f"Ikki tomonni x ga ko'paytiring, so'ng {q} ga bo'ling: x = {p}/{q} = {num(x0)}. Nol istisno va javob emas.",
        c_num(x0),
    )


def g_radical(k: int) -> dict:
    root = 2 + (k % 25)
    added = (k // 25) % 30
    x0 = root**2 - added
    if x0 < 0:
        added = 0
        x0 = root**2
    inside = "x" if added == 0 else f"(x + {added})"
    square_line = f"x = {root**2}" if added == 0 else f"x + {added} = {root**2}, so x = {x0}"
    square_line_uz = f"x = {root**2}" if added == 0 else f"x + {added} = {root**2}, demak x = {x0}"
    return item(
        f"Solve √{inside} = {root}.",
        f"√{inside} = {root} tenglamasini yeching.",
        f"x = {num(x0)}",
        f"Square both sides: {square_line}. Check: the root is {root}, which is not negative, so it stands.",
        f"Ikki tomonni kvadratga ko'taring: {square_line_uz}. Tekshiruv: ildiz {root}, manfiy emas, javob o'tadi.",
        c_num(x0),
    )


def g_exp_growth(k: int) -> dict:
    start = 4 * (1 + (k % 30))
    times = 1 + ((k // 30) % 6)
    value = start * (2**times)
    how = {1: "once", 2: "twice"}.get(times, f"{times} times")
    return item(
        f"A quantity starts at {start} and doubles {how}. What is the result?",
        f"Miqdor {start} dan boshlanadi va {times} marta ikki baravar bo'ladi. Natija necha?",
        str(value),
        f"Doubling {how} multiplies by 2^{times}: {start} × 2^{times} = {value}.",
        f"{times} marta ikki baravar — 2^{times} ga ko'paytirish: {start} × 2^{times} = {value}.",
        c_num(value),
    )


def g_context_ratio(k: int) -> dict:
    red = 1 + (k % 10)
    blue = 1 + ((k // 10) % 10)
    scale = 1 + ((k // 100) % 8) + (k % 3)
    total = (red + blue) * scale
    answer = red * scale
    return item(
        f"Red and blue paint are mixed in the ratio {red}:{blue}. How many liters of red are in {total} liters of mixture?",
        f"Qizil va ko'k bo'yoq {red}:{blue} nisbatda aralashtiriladi. {total} litr aralashmada necha litr qizil bor?",
        str(answer),
        f"Red is {red}/{red + blue} of the mixture: ({red}/{red + blue}) × {total} = {answer} liters.",
        f"Qizil aralashmaning {red}/{red + blue} qismi: ({red}/{red + blue}) × {total} = {answer} litr.",
        c_num(answer),
    )


def g_table(k: int) -> dict:
    slope = 1 + (k % 7)
    intercept = (k % 10) - 3
    x0 = 3 + (k % 8)
    y0 = slope * x0 + intercept
    rule = poly(slope * X + intercept)
    plug = (str(x0) if slope == 1 else f"{slope} × {x0}") + (f" + {intercept}" if intercept > 0 else f" {MINUS} {-intercept}" if intercept < 0 else "")
    return item(
        f"The rule y = {rule} fits a table of values. What is y when x = {x0}?",
        f"y = {rule} qoidasi qiymatlar jadvaliga mos. x = {x0} bo'lganda y necha?",
        num(y0),
        f"Substitute: {plug} = {num(y0)}.",
        f"O'rniga qo'ying: {plug} = {num(y0)}.",
        c_num(y0),
    )


def g_stats(k: int) -> dict:
    a = 1 + (k % 40)
    b = a + 1 + ((k // 40) % 12)
    c = b + 1 + ((k // 480) % 8) + (k % 5)
    kind = k % 3
    if kind == 0:
        mean = sp.Rational(a + b + c, 3)
        return item(
            f"What is the mean of {a}, {b}, and {c}?",
            f"{a}, {b} va {c} ning o'rta arifmetigi necha?",
            num(mean),
            f"The sum is {a + b + c}. Divide by 3 to get {num(mean)}.",
            f"Yig'indi {a + b + c}. 3 ga bo'ling: {num(mean)}.",
            c_num(mean),
        )
    if kind == 1:
        return item(
            f"What is the median of {c}, {a}, and {b}?",
            f"{c}, {a} va {b} sonlarining medianasi necha?",
            str(b),
            f"Sorted, the list is {a}, {b}, {c}. The middle value is {b}.",
            f"Tartiblanganda {a}, {b}, {c}. O'rtadagi qiymat {b}.",
            c_num(b),
        )
    return item(
        f"What is the range of {a}, {c}, and {b}?",
        f"{a}, {c} va {b} sonlarining qamrovi necha?",
        str(c - a),
        f"Largest minus smallest: {c} {MINUS} {a} = {c - a}.",
        f"Eng katta minus eng kichik: {c} {MINUS} {a} = {c - a}.",
        c_num(c - a),
    )


def g_fit(k: int) -> dict:
    slope = (k % 9) - 3
    if slope == 0:
        slope = 2
    intercept = k % 8
    x0 = 1 + (k % 10)
    pred = slope * x0 + intercept
    actual = pred + ((k % 5) - 2)
    residual = actual - pred
    if k % 2 == 0:
        rule = poly(slope * X + intercept)
        plug = f"{slope} × {x0}".replace("-", MINUS) + (f" + {intercept}" if intercept else "")
        return item(
            f"A line of best fit is y = {rule}. What does it predict at x = {x0}?",
            f"Eng mos chiziq y = {rule}. x = {x0} dagi bashorat necha?",
            num(pred),
            f"Substitute: {plug} = {num(pred)}.",
            f"O'rniga qo'ying: {plug} = {num(pred)}.",
            c_num(pred),
        )
    return item(
        f"A model predicts {num(pred)}, and the actual value is {num(actual)}. What is the residual?",
        f"Model {num(pred)} ni bashorat qiladi, haqiqiy qiymat {num(actual)}. Qoldiq necha?",
        num(residual),
        f"Residual = actual {MINUS} predicted = {num(actual)} {MINUS} {par(pred)} = {num(residual)}.",
        f"Qoldiq = haqiqiy {MINUS} bashorat = {num(actual)} {MINUS} {par(pred)} = {num(residual)}.",
        c_num(residual),
    )


def g_prob(k: int) -> dict:
    red = 1 + (k % 15)
    blue = 1 + ((k // 15) % 12)
    green = 1 + ((k // 180) % 10) + (k % 4)
    total = red + blue + green
    which = k % 3
    count = (red, blue, green)[which]
    name = ("red", "blue", "green")[which]
    uz = ("qizil", "ko'k", "yashil")[which]
    value = sp.Rational(count, total)
    return item(
        f"A bag has {red} red, {blue} blue, and {green} green marbles. One marble is drawn at random. What is the probability that it is {name}?",
        f"Qopda {red} qizil, {blue} ko'k va {green} yashil marmar bor. Tasodifan bitta olinadi. Uning {uz} bo'lish ehtimoli necha?",
        num(value),
        f"{count} favorable outcomes out of {total}. The probability is {count}/{total} = {num(value)}.",
        f"{total} ta holatdan {count} tasi qulay. Ehtimollik {count}/{total} = {num(value)}.",
        c_num(value),
    )


def g_margin(k: int) -> dict:
    estimate = 20 + (k % 60)
    margin = 1 + (k % 8)
    if k % 2 == 0:
        answer, edge, chekka, op = estimate - margin, "lower", "Quyi", MINUS
    else:
        answer, edge, chekka, op = estimate + margin, "upper", "Yuqori", "+"
    return item(
        f"A survey estimate is {estimate}% with a margin of error of {plural(margin, 'percentage point')}. What is the {edge} end of the interval, in percent?",
        f"So'rovnoma bahosi {estimate}%, xato chegarasi {margin} foiz punkti. Oraliqning {chekka.lower()} chegarasi necha foiz?",
        f"{answer}%",
        f"{estimate} {op} {margin} = {answer}. The interval runs from {estimate - margin}% to {estimate + margin}%.",
        f"{estimate} {op} {margin} = {answer}. Oraliq {estimate - margin}% dan {estimate + margin}% gacha.",
        c_num(answer, percent=True),
    )


def g_angles(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        given = 15 + (k % 140)
        other = 180 - given
        return item(
            f"Two adjacent angles form a straight line. One measures {given}°. What is the other, in degrees?",
            f"Ikki qo'shni burchak to'g'ri chiziq hosil qiladi. Biri {given}°. Ikkinchisi necha gradus?",
            f"{other}°",
            f"Angles on a straight line add to 180°: 180 {MINUS} {given} = {other}.",
            f"To'g'ri chiziqdagi burchaklar yig'indisi 180°: 180 {MINUS} {given} = {other}.",
            c_num(other),
        )
    if kind == 1:
        given = 10 + (k % 70)
        other = 90 - given
        return item(
            f"What is the complement of a {given}° angle, in degrees?",
            f"{given}° li burchakning to'ldiruvchisi necha gradus?",
            f"{other}°",
            f"Complementary angles add to 90°: 90 {MINUS} {given} = {other}.",
            f"To'ldiruvchi burchaklar yig'indisi 90°: 90 {MINUS} {given} = {other}.",
            c_num(other),
        )
    a = 20 + (k % 50) + ((k // 50) % 3) * 50
    return item(
        f"Two lines cross and one angle is {a}°. What is the vertical angle, in degrees?",
        f"Ikki chiziq kesishadi va bitta burchak {a}°. Vertikal burchak necha gradus?",
        f"{a}°",
        f"Vertical angles are equal, so the angle is {a}°.",
        f"Vertikal burchaklar teng, demak burchak {a}°.",
        c_num(a),
    )


def g_similar(k: int) -> dict:
    factor = 2 + (k % 12)
    side = 2 + ((k // 12) % 30)
    return item(
        f"Triangle B is similar to triangle A with scale factor {factor}. A side of triangle A is {side}. What is the corresponding side of triangle B?",
        f"B uchburchak A ga o'xshash, masshtab {factor}. A ning bir tomoni {side}. B dagi mos tomon necha?",
        str(side * factor),
        f"Corresponding sides scale by {factor}: {side} × {factor} = {side * factor}.",
        f"Mos tomonlar {factor} marta kattalashadi: {side} × {factor} = {side * factor}.",
        c_num(side * factor),
    )


def g_pythag(k: int) -> dict:
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (7, 24, 25), (8, 15, 17), (9, 12, 15), (9, 40, 41), (20, 21, 29), (12, 16, 20), (12, 35, 37), (11, 60, 61), (28, 45, 53)]
    a, b, c = triples[k % len(triples)]
    scale = 1 + ((k // len(triples)) % 12)
    a, b, c = a * scale, b * scale, c * scale
    if k % 2 == 0:
        return item(
            f"A right triangle has legs {a} and {b}. What is the hypotenuse?",
            f"To'g'ri burchakli uchburchakning katetlari {a} va {b}. Gipotenuza necha?",
            str(c),
            f"{a}² + {b}² = {a * a + b * b} = {c}², so the hypotenuse is {c}.",
            f"{a}² + {b}² = {a * a + b * b} = {c}², demak gipotenuza {c}.",
            c_num(c),
        )
    return item(
        f"A right triangle has hypotenuse {c} and one leg {a}. What is the other leg?",
        f"To'g'ri burchakli uchburchakning gipotenuzasi {c}, bitta kateti {a}. Ikkinchi katet necha?",
        str(b),
        f"Subtract the squares: √({c}² {MINUS} {a}²) = √{c * c - a * a} = {b}.",
        f"Kvadratlarni ayiring: √({c}² {MINUS} {a}²) = √{c * c - a * a} = {b}.",
        c_num(b),
    )


def g_trig(k: int) -> dict:
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41), (20, 21, 29), (12, 35, 37), (9, 12, 15), (28, 45, 53)]
    scale = 1 + ((k // (len(triples) * 3)) % 5)
    a, b, c = triples[k % len(triples)]
    a, b, c = a * scale, b * scale, c * scale
    which = (k // len(triples)) % 3
    if which == 0:
        fn, rule, rule_uz, value = "sin", "opposite/hypotenuse", "qarama-qarshi/gipotenuza", sp.Rational(a, c)
        parts = f"{a}/{c}"
    elif which == 1:
        fn, rule, rule_uz, value = "cos", "adjacent/hypotenuse", "yondosh/gipotenuza", sp.Rational(b, c)
        parts = f"{b}/{c}"
    else:
        fn, rule, rule_uz, value = "tan", "opposite/adjacent", "qarama-qarshi/yondosh", sp.Rational(a, b)
        parts = f"{a}/{b}"
    return item(
        f"In a right triangle, the side opposite angle A is {a}, the side adjacent to angle A is {b}, and the hypotenuse is {c}. What is {fn} A?",
        f"To'g'ri burchakli uchburchakda A burchak qarshisidagi tomon {a}, A ga yondosh tomon {b}, gipotenuza {c}. {fn} A necha?",
        num(value),
        f"{fn} = {rule} = {parts}{'' if parts == num(value) else ' = ' + num(value)}.",
        f"{fn} = {rule_uz} = {parts}{'' if parts == num(value) else ' = ' + num(value)}.",
        c_num(value),
    )


IN_TERMS_OF_PI = ("Give the answer in terms of π.", "Javobni π orqali yozing.")


def g_area(k: int) -> dict:
    kind = k % 4
    if kind == 0:
        base, height = 2 + ((k // 4) % 30), 2 + ((k // 120) % 20) + (k // 4) % 5
        value = sp.Rational(base * height, 2)
        return item(f"A triangle has base {base} and height {height}. What is its area?", f"Uchburchakning asosi {base}, balandligi {height}. Yuzi necha?", num(value), f"(1/2) × {base} × {height} = {num(value)}.", f"(1/2) × {base} × {height} = {num(value)}.", c_num(value))
    if kind == 1:
        length, width = 2 + ((k // 4) % 28), 2 + ((k // 112) % 16) + (k // 4) % 6
        return item(f"A rectangle is {length} by {width}. What is its area?", f"To'g'ri to'rtburchakning tomonlari {length} va {width}. Yuzi necha?", str(length * width), f"{length} × {width} = {length * width}.", f"{length} × {width} = {length * width}.", c_num(length * width))
    if kind == 2:
        r = 1 + ((k // 4) % 24)
        en, uz = IN_TERMS_OF_PI
        return item(f"A circle has radius {r}. What is its area? {en}", f"Doiraning radiusi {r}. Yuzi necha? {uz}", pi_text(r * r), f"Area = πr² = π × {r}² = {pi_text(r * r)}.", f"Yuza = πr² = π × {r}² = {pi_text(r * r)}.", c_pi(r * r))
    b1, b2, h = 2 + ((k // 4) % 16), 4 + ((k // 64) % 18) + (k // 4) % 3, 2 + ((k // 400) % 10) + (k // 8) % 4
    value = sp.Rational(b1 + b2, 2) * h
    return item(f"A trapezoid has bases {b1} and {b2} and height {h}. What is its area?", f"Trapetsiyaning asoslari {b1} va {b2}, balandligi {h}. Yuzi necha?", num(value), f"Average the bases, then multiply by the height: (({b1} + {b2})/2) × {h} = {num(value)}.", f"Asoslarning o'rtachasini balandlikka ko'paytiring: (({b1} + {b2})/2) × {h} = {num(value)}.", c_num(value))


def g_volume(k: int) -> dict:
    kind = k % 4
    en, uz = IN_TERMS_OF_PI
    if kind == 0:
        a, b, c = 2 + ((k // 4) % 12), 2 + ((k // 48) % 10) + (k // 4) % 3, 2 + ((k // 480) % 8) + (k // 8) % 4
        return item(f"A box is {a} by {b} by {c}. What is its volume?", f"Quti o'lchamlari {a}, {b} va {c}. Hajmi necha?", str(a * b * c), f"{a} × {b} × {c} = {a * b * c}.", f"{a} × {b} × {c} = {a * b * c}.", c_num(a * b * c))
    r = 1 + ((k // 4) % 16)
    h = 2 + ((k // 64) % 14) + (k // 4) % 5
    if kind == 1:
        return item(f"A cylinder has radius {r} and height {h}. What is its volume? {en}", f"Silindrning radiusi {r}, balandligi {h}. Hajmi necha? {uz}", pi_text(r * r * h), f"V = πr²h = π × {r}² × {h} = {pi_text(r * r * h)}.", f"V = πr²h = π × {r}² × {h} = {pi_text(r * r * h)}.", c_pi(r * r * h))
    if kind == 2:
        volume = sp.Rational(r * r * h, 3)
        return item(f"A cone has radius {r} and height {h}. What is its volume? {en}", f"Konusning radiusi {r}, balandligi {h}. Hajmi necha? {uz}", pi_text(volume), f"V = (1/3)πr²h = (1/3) × π × {r}² × {h} = {pi_text(volume)}.", f"V = (1/3)πr²h = (1/3) × π × {r}² × {h} = {pi_text(volume)}.", c_pi(volume))
    sphere = sp.Rational(4, 3) * (r**3)
    return item(f"A sphere has radius {r}. What is its volume? {en}", f"Sharning radiusi {r}. Hajmi necha? {uz}", pi_text(sphere), f"V = (4/3)πr³ = (4/3) × π × {r}³ = {pi_text(sphere)}.", f"V = (4/3)πr³ = (4/3) × π × {r}³ = {pi_text(sphere)}.", c_pi(sphere))


def g_circle(k: int) -> dict:
    r = 2 + ((k // 3) % 20)
    angles = [30, 36, 40, 45, 60, 72, 90, 120, 180]
    angle = angles[(k // 3 + k // 60) % len(angles)]
    kind = k % 3
    en, uz = IN_TERMS_OF_PI
    if kind == 0:
        arc = sp.Rational(angle, 360) * 2 * r
        return item(f"A circle has radius {r}. What is the length of a {angle}° arc? {en}", f"Aylananing radiusi {r}. {angle}° li yoyning uzunligi necha? {uz}", pi_text(arc), f"Arc = ({angle}/360) × 2π × {r} = {pi_text(arc)}.", f"Yoy = ({angle}/360) × 2π × {r} = {pi_text(arc)}.", c_pi(arc))
    if kind == 1:
        area = sp.Rational(angle, 360) * (r * r)
        return item(f"A sector has radius {r} and central angle {angle}°. What is its area? {en}", f"Sektorning radiusi {r}, markaziy burchagi {angle}°. Yuzi necha? {uz}", pi_text(area), f"Sector = ({angle}/360) × π × {r}² = {pi_text(area)}.", f"Sektor = ({angle}/360) × π × {r}² = {pi_text(area)}.", c_pi(area))
    radius = 2 + (k // 3) % 13
    h, v = (k % 7) - 3, ((k // 7) % 9) - 4
    equation = f"{'x²' if h == 0 else binomial(1, -h) + '²'} + {'y²' if v == 0 else '(' + poly(Y - v, Y) + ')²'} = {radius * radius}"
    return item(
        f"What is the radius of the circle {equation}?",
        f"{equation} aylananing radiusi necha?",
        str(radius),
        f"The right side is r² = {radius * radius}, so r = {radius}. The center ({num(h)}, {num(v)}) was not asked for.",
        f"O'ng tomon r² = {radius * radius}, demak r = {radius}. Markaz ({num(h)}, {num(v)}) so'ralmagan.",
        c_num(radius),
    )


def g_timing(k: int) -> dict:
    kind = k % 4
    if kind == 0:
        modules = 2
        each = 8 + ((k // 4) % 30)
        return item(f"A test has {modules} modules of {each} questions each. How many questions is that?", f"Sinovda {modules} modul, har birida {each} savol. Jami nechta savol?", str(modules * each), f"{modules} × {each} = {modules * each}.", f"{modules} × {each} = {modules * each}.", c_num(modules * each))
    if kind == 1:
        minutes = 5 + ((k // 4) % 40)
        return item(f"How many seconds are in {minutes} minutes?", f"{minutes} daqiqada necha soniya bor?", str(minutes * 60), f"{minutes} × 60 = {minutes * 60}.", f"{minutes} × 60 = {minutes * 60}.", c_num(minutes * 60))
    if kind == 2:
        left_min = 4 + ((k // 4) % 40)
        left_q = 2 + ((k // 160) % 15) + (k // 8) % 5
        value = sp.Rational(left_min, left_q)
        return item(f"{left_min} minutes remain for {left_q} questions. How many minutes is that per question?", f"{left_q} savolga {left_min} daqiqa qoldi. Bitta savolga necha daqiqa to'g'ri keladi?", num(value), f"{left_min}/{left_q} = {num(value)} minutes per question.", f"{left_min}/{left_q} = {num(value)} daqiqa bir savolga.", c_num(value))
    answered = (k // 4) % 23
    return item(f"A 22-question module has {answered} answers filled in. How many are still blank?", f"22 savollik modulda {answered} ta javob yozilgan. Nechtasi hali bo'sh?", str(22 - answered), f"22 {MINUS} {answered} = {22 - answered}. Every blank is a lost chance: guess before time ends.", f"22 {MINUS} {answered} = {22 - answered}. Har bir bo'sh joy — yo'qotilgan imkoniyat: vaqt tugamasdan taxmin qiling.", c_num(22 - answered))


def g_stems(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        a = 2 + ((k // 3) % 20)
        x0 = 2 + ((k // 60) % 12)
        product = a * x0
        return item(f"If {a}x = {product}, what is the value of x?", f"Agar {a}x = {product} bo'lsa, x ning qiymati necha?", str(x0), f"'The value of x' asks for x itself. Divide by {a}: x = {x0}.", f"'The value of x' — x ning o'zi. {a} ga bo'ling: x = {x0}.", c_num(x0))
    if kind == 1:
        c = 1 + ((k // 3) % 25)
        if (k // 3) % 2 == 0:
            expr = Y - c
            return item(f"If x + {c} = y, what is x in terms of y?", f"Agar x + {c} = y bo'lsa, x ni y orqali ifodalang.", poly(expr, Y), f"'In terms of y' means the answer keeps y. Subtract {c}: x = {poly(expr, Y)}.", f"'In terms of y' — javobda y qoladi. {c} ni ayiring: x = {poly(expr, Y)}.", c_expr(expr, var="y"))
        expr = Y + c
        return item(f"If x {MINUS} {c} = y, what is x in terms of y?", f"Agar x {MINUS} {c} = y bo'lsa, x ni y orqali ifodalang.", poly(expr, Y), f"'In terms of y' means the answer keeps y. Add {c}: x = {poly(expr, Y)}.", f"'In terms of y' — javobda y qoladi. {c} ni qo'shing: x = {poly(expr, Y)}.", c_expr(expr, var="y"))
    add = 1 + ((k // 3) % 25)
    right = add + 1 + ((k // 75) % 20) + (k // 3) % 4
    return item(f"What value of x satisfies x + {add} = {right}?", f"Qaysi x qiymati x + {add} = {right} ni qanoatlantiradi?", str(right - add), f"'Satisfies' means the equation comes out true. x = {right} {MINUS} {add} = {right - add}.", f"'Satisfies' — tenglik rost chiqadi. x = {right} {MINUS} {add} = {right - add}.", c_num(right - add))


def g_hand(k: int) -> dict:
    p = 5 * (1 + ((k // 2) % 18))
    n = 4 * (3 + ((k // 40) % 25) + k % 3)
    value = sp.Rational(p, 100) * n
    return item(
        f"What is {p}% of {n}? Work it as a fraction before you touch a calculator.",
        f"{n} ning {p} foizi necha? Kalkulyatordan oldin kasr bilan hisoblang.",
        num(value),
        f"({p}/100) × {n} = {num(value)}.",
        f"({p}/100) × {n} = {num(value)}.",
        c_num(value),
    )


def g_traps(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        p = 5 * (1 + ((k // 3) % 16))
        n = 10 * (2 + ((k // 48) % 16))
        value = sp.Rational(p, 100) * n
        return item(f"To find {p}% of {n}, a student divides {n} by {p}. What is the correct value of {p}% of {n}?", f"{n} ning {p} foizini topish uchun o'quvchi {n} ni {p} ga bo'ladi. {n} ning {p} foizi aslida necha?", num(value), f"Percent multiplies: ({p}/100) × {n} = {num(value)}.", f"Foiz ko'paytiradi: ({p}/100) × {n} = {num(value)}.", c_num(value))
    if kind == 1:
        old = (20, 25, 40, 50, 80, 100, 125, 160, 200, 250)[(k // 3) % 10]
        new = old + 5 * (1 + ((k // 30) % 12) + (k // 3) % 3)
        value = sp.Rational(new - old, old) * 100
        return item(f"A value goes from {old} to {new}. A student divides the change by {new}. What is the correct percent increase?", f"Qiymat {old} dan {new} ga o'tadi. O'quvchi o'zgarishni {new} ga bo'ladi. To'g'ri o'sish foizi necha?", pct(value), f"Divide by the original {old}: ({new - old}/{old}) × 100 = {pct(value)}.", f"Eski son {old} ga bo'ling: ({new - old}/{old}) × 100 = {pct(value)}.", c_num(value, percent=True))
    r = 2 + ((k // 3) % 30)
    en, uz = IN_TERMS_OF_PI
    return item(f"A circle has radius {r}. A student squares the diameter to find the area. What is the correct area? {en}", f"Aylananing radiusi {r}. O'quvchi yuzani topish uchun diametrni kvadratga oladi. To'g'ri yuza necha? {uz}", pi_text(r * r), f"Area uses the radius, not the diameter: π × {r}² = {pi_text(r * r)}.", f"Yuza diametrni emas, radiusni oladi: π × {r}² = {pi_text(r * r)}.", c_pi(r * r))


BUILDERS = {
    "0.1": g_fractions,
    "1.1": g_abs,
    "1.2": g_order,
    "1.3": g_decimals,
    "1.4": g_percent,
    "1.5": g_change,
    "1.6": g_ratio,
    "1.7": g_prop,
    "1.8": g_exp,
    "1.9": g_roots,
    "1.10": g_sci,
    "2.1": g_expr,
    "2.2": g_linear,
    "2.3": g_frac_eq,
    "2.4": g_ineq,
    "2.5": g_words,
    "2.6": g_slope,
    "2.7": g_system,
    "2.8": g_func,
    "3.1": g_poly,
    "3.2": g_factor,
    "3.3": g_quad,
    "3.4": g_vertex,
    "3.5": g_equiv,
    "3.6": g_rational,
    "3.7": g_radical,
    "3.8": g_exp_growth,
    "4.1": g_context_ratio,
    "4.2": g_table,
    "4.3": g_stats,
    "4.4": g_fit,
    "4.5": g_prob,
    "4.6": g_margin,
    "5.1": g_angles,
    "5.2": g_similar,
    "5.3": g_pythag,
    "5.4": g_trig,
    "5.5": g_area,
    "5.6": g_volume,
    "5.7": g_circle,
    "6.1": g_timing,
    "6.2": g_stems,
    "6.3": g_hand,
    "6.4": g_traps,
}


# --------------------------------------------------------------------------
# Independent recheck: read the prompt as a student would and recompute.
# --------------------------------------------------------------------------

_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


def to_sympy(text: str):
    """Parse the math a student sees: −, ×, ÷, ², ³, ^, √, π, implicit products."""
    t = text.strip().replace(MINUS, "-").replace("×", "*").replace("÷", "/").replace("π", "pi")
    t = t.replace("²", "**2").replace("³", "**3")
    t = re.sub(r"(?<![\w.])(\d+)/(\d+)(?![\w.])", r"(\1/\2)", t)  # 2/3 ÷ 4/5 is (2/3)/(4/5)
    t = re.sub(r"√\(", "sqrt(", t)
    t = re.sub(r"√(\d+|x)", r"sqrt(\1)", t)
    return parse_expr(t, transformations=_TRANSFORMS, local_dict={"x": X, "y": Y, "pi": sp.pi, "sqrt": sp.sqrt})


def spec_value(check: dict):
    """The exact value a numeric spec stands for."""
    kind = check["kind"]
    if kind == "number":
        return sp.Rational(check["value"])
    if kind == "pi":
        return sp.Rational(check["value"]) * sp.pi
    if kind == "radical":
        return check["coef"] * sp.sqrt(check["rad"])
    raise ValueError(kind)


def _solve_set(equation: str) -> set:
    lhs, rhs = equation.split("=")
    return {sp.nsimplify(root) for root in sp.solve(to_sympy(lhs) - to_sympy(rhs), X)}


def _recompute(code: str, prompt: str):
    """Return what the prompt asks for, computed from the prompt text alone, or None."""
    m = re.match(r"^Find the \w+ (.+) as a simplified fraction\.$", prompt)
    if m:
        return to_sympy(m.group(1))
    m = re.match(r"^Evaluate (.+)\.$", prompt)
    if m and code in ("1.1", "1.2", "1.8"):
        return to_sympy(m.group(1).replace("|", "Abs(", 1).replace("|", ")", 1).replace("|", "Abs(", 1).replace("|", ")", 1))
    m = re.match(r"^What is the distance on the number line between (\S+) and (\S+)\?$", prompt)
    if m:
        return abs(to_sympy(m.group(2)) - to_sympy(m.group(1)))
    m = re.match(r"^Write (\S+) as a simplified fraction\.$", prompt)
    if m and code == "1.8":
        return to_sympy(m.group(1))
    m = re.match(r"^Simplify √(\d+)\.$", prompt)
    if m:
        return sp.sqrt(int(m.group(1)))
    m = re.match(r"^Write (\S+) × 10\^(\d+) as an ordinary number\.$", prompt)
    if m:
        return sp.Rational(m.group(1)) * 10 ** int(m.group(2))
    m = re.match(r"^(?:Simplify|Expand|Write an expression equivalent to) (.+?)(?: with no parentheses)?\.$", prompt)
    if m:
        return sp.expand(to_sympy(m.group(1)))
    m = re.match(r"^Factor (.+)\.$", prompt)
    if m:
        return sp.expand(to_sympy(m.group(1)))
    m = re.match(r"^Solve the system x \+ y = (\S+) and x − y = (\S+)\.$", prompt)
    if m:
        sol = sp.solve([X + Y - to_sympy(m.group(1)), X - Y - to_sympy(m.group(2))], [X, Y], dict=True)[0]
        return (sol[X], sol[Y])
    m = re.match(r"^Solve (.+) ([<>≤≥]) (.+)\.$", prompt)
    if m:
        relation = {"<": "<", ">": ">", "≤": "<=", "≥": ">="}[m.group(2)]
        solved = sp.solve_univariate_inequality(sp.Rel(to_sympy(m.group(1)), to_sympy(m.group(3)), relation), X, relational=False)
        return solved
    m = re.match(r"^Solve (.+ = .+)\.$", prompt)
    if m and code in ("2.2", "2.3", "3.3", "3.6", "3.7", "1.7"):
        return _solve_set(m.group(1))
    m = re.match(r"^What is the slope of the line through \((\S+), (\S+)\) and \((\S+), (\S+)\)\?$", prompt)
    if m:
        x1, y1, x2, y2 = (to_sympy(g) for g in m.groups())
        return (y2 - y1) / (x2 - x1)
    m = re.match(r"^If f\(x\) = (.+), what is f\((\S+)\)\?$", prompt)
    if m:
        return to_sympy(m.group(1)).subs(X, to_sympy(m.group(2)))
    m = re.match(r"^What is the (minimum|maximum) value of y = (.+)\?$", prompt)
    if m:
        expr = to_sympy(m.group(2))
        vertex = sp.solve(sp.diff(expr, X), X)[0]
        lead = sp.Poly(expr, X).LC()
        if (lead > 0) != (m.group(1) == "minimum"):
            raise AssertionError(f"{prompt}: the parabola opens the wrong way")
        return expr.subs(X, vertex)
    m = re.match(r"^The rule y = (.+) fits a table of values\. What is y when x = (\S+)\?$", prompt)
    if m:
        return to_sympy(m.group(1)).subs(X, to_sympy(m.group(2)))
    m = re.match(r"^A line of best fit is y = (.+)\. What does it predict at x = (\S+)\?$", prompt)
    if m:
        return to_sympy(m.group(1)).subs(X, to_sympy(m.group(2)))
    m = re.match(r"^In a right triangle, the side opposite angle A is (\d+), the side adjacent to angle A is (\d+), and the hypotenuse is (\d+)\. What is (sin|cos|tan) A\?$", prompt)
    if m:
        a, b, c, fn = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        if a * a + b * b != c * c:
            raise AssertionError(f"{prompt}: not a right triangle")
        return {"sin": sp.Rational(a, c), "cos": sp.Rational(b, c), "tan": sp.Rational(a, b)}[fn]
    m = re.match(r"^What is the radius of the circle (.+) = (\d+)\?$", prompt)
    if m:
        return sp.sqrt(int(m.group(2)))
    m = re.match(r"^A circle has radius (\d+)\. What is its area\?", prompt)
    if m:
        return sp.pi * int(m.group(1)) ** 2
    m = re.match(r"^A cylinder has radius (\d+) and height (\d+)\.", prompt)
    if m:
        return sp.pi * int(m.group(1)) ** 2 * int(m.group(2))
    m = re.match(r"^A cone has radius (\d+) and height (\d+)\.", prompt)
    if m:
        return sp.pi * int(m.group(1)) ** 2 * int(m.group(2)) / 3
    m = re.match(r"^A sphere has radius (\d+)\.", prompt)
    if m:
        return sp.Rational(4, 3) * sp.pi * int(m.group(1)) ** 3
    m = re.match(r"^A circle has radius (\d+)\. What is the length of a (\d+)° arc\?", prompt)
    if m:
        return sp.Rational(int(m.group(2)), 360) * 2 * sp.pi * int(m.group(1))
    m = re.match(r"^A sector has radius (\d+) and central angle (\d+)°\.", prompt)
    if m:
        return sp.Rational(int(m.group(2)), 360) * sp.pi * int(m.group(1)) ** 2
    m = re.match(r"^A circle has radius (\d+)\. A student squares the diameter", prompt)
    if m:
        return sp.pi * int(m.group(1)) ** 2
    m = re.match(r"^What is (\d+)% of (\d+)\?", prompt)
    if m:
        return sp.Rational(int(m.group(1)), 100) * int(m.group(2))
    m = re.match(r"^(\S+) is what percent of (\d+)\?$", prompt)
    if m:
        return to_sympy(m.group(1)) / int(m.group(2)) * 100
    m = re.match(r"^Write (\d+)/(\d+) as a percent\.$", prompt)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2))) * 100
    m = re.match(r"^Write (\d+)% as a simplified fraction\.$", prompt)
    if m:
        return sp.Rational(int(m.group(1)), 100)
    m = re.match(r"^(\S+) is (\d+)% of what number\?$", prompt)
    if m:
        return to_sympy(m.group(1)) * 100 / int(m.group(2))
    m = re.match(r"^Write the fraction (\d+)/(\d+) as a decimal\.$", prompt)
    if m:
        return sp.Rational(int(m.group(1)), int(m.group(2)))
    m = re.match(r"^Write the decimal (\S+) as a simplified fraction\.$", prompt)
    if m:
        return sp.Rational(m.group(1))
    m = re.match(r"^Add (\d+)/(\d+) and (\d+)/(\d+)\. Give a simplified fraction\.$", prompt)
    if m:
        a, b, c, d = (int(g) for g in m.groups())
        return sp.Rational(a, b) + sp.Rational(c, d)
    m = re.match(r"^A value goes from (\d+) to (\d+)\. By what percent did it (?:increase|decrease)\?$", prompt)
    if m:
        old, new = int(m.group(1)), int(m.group(2))
        return sp.Rational(abs(new - old), old) * 100
    m = re.match(r"^A value goes from (\d+) to (\d+)\. A student divides the change by \d+\. What is the correct percent increase\?$", prompt)
    if m:
        old, new = int(m.group(1)), int(m.group(2))
        return sp.Rational(new - old, old) * 100
    m = re.match(r"^To find (\d+)% of (\d+), a student", prompt)
    if m:
        return sp.Rational(int(m.group(1)), 100) * int(m.group(2))
    m = re.match(r"^A price of (\d+) rises by (\d+)% and then falls by (\d+)%\.", prompt)
    if m:
        start, up, down = (int(g) for g in m.groups())
        return start * sp.Rational(100 + up, 100) * sp.Rational(100 - down, 100)
    m = re.match(r"^What is the (mean|median|range) of (\d+), (\d+), and (\d+)\?$", prompt)
    if m:
        values = sorted(int(g) for g in m.groups()[1:])
        return {"mean": sp.Rational(sum(values), 3), "median": values[1], "range": values[2] - values[0]}[m.group(1)]
    m = re.match(r"^A bag has (\d+) red, (\d+) blue, and (\d+) green marbles\. .* that it is (red|blue|green)\?$", prompt)
    if m:
        counts = dict(zip(("red", "blue", "green"), (int(g) for g in m.groups()[:3])))
        return sp.Rational(counts[m.group(4)], sum(counts.values()))
    m = re.match(r"^A survey estimate is (\d+)% with a margin of error of (\d+) percentage points?\. What is the (lower|upper) end", prompt)
    if m:
        estimate, margin = int(m.group(1)), int(m.group(2))
        return estimate - margin if m.group(3) == "lower" else estimate + margin
    m = re.match(r"^Two adjacent angles form a straight line\. One measures (\d+)°", prompt)
    if m:
        return 180 - int(m.group(1))
    m = re.match(r"^What is the complement of a (\d+)° angle", prompt)
    if m:
        return 90 - int(m.group(1))
    m = re.match(r"^A right triangle has legs (\d+) and (\d+)\. What is the hypotenuse\?$", prompt)
    if m:
        return sp.sqrt(int(m.group(1)) ** 2 + int(m.group(2)) ** 2)
    m = re.match(r"^A right triangle has hypotenuse (\d+) and one leg (\d+)\. What is the other leg\?$", prompt)
    if m:
        return sp.sqrt(int(m.group(1)) ** 2 - int(m.group(2)) ** 2)
    m = re.match(r"^Two parts are in the ratio (\d+):(\d+) and total (\d+)\. What is the (smaller|larger) part\?$", prompt)
    if m:
        a, b, total = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return sp.Rational(total * (a if m.group(4) == "smaller" else b), a + b)
    m = re.match(r"^Red and blue paint are mixed in the ratio (\d+):(\d+)\. How many liters of red are in (\d+) liters", prompt)
    if m:
        red, blue, total = (int(g) for g in m.groups())
        return sp.Rational(red * total, red + blue)
    m = re.match(r"^A quantity starts at (\d+) and doubles (once|twice|\d+ times)\.", prompt)
    if m:
        times = {"once": 1, "twice": 2}.get(m.group(2)) or int(m.group(2).split()[0])
        return int(m.group(1)) * 2**times
    m = re.match(r"^If x ([+−]) (\d+) = y, what is x in terms of y\?$", prompt)
    if m:
        c = int(m.group(2))
        return Y - c if m.group(1) == "+" else Y + c
    return None


def _same(got, check: dict) -> bool:
    kind = check["kind"]
    if kind in ("number", "pi", "radical"):
        return sp.simplify(got - spec_value(check)) == 0
    if kind == "expression":
        var = Y if check["var"] == "y" else X
        expected = sp.sympify(check["expr"], locals={check["var"]: var})
        return sp.expand(got - expected) == 0
    if kind == "set":
        return set(got) == {sp.Rational(v) for v in check["values"]}
    if kind == "pair":
        return tuple(got) == tuple(sp.Rational(v) for v in check["values"])
    if kind == "inequality":
        bound = sp.Rational(check["value"])
        expected = {
            "<": sp.Interval.open(-sp.oo, bound),
            "<=": sp.Interval(-sp.oo, bound),
            ">": sp.Interval.open(bound, sp.oo),
            ">=": sp.Interval(bound, sp.oo),
        }[check["op"]]
        return got == expected
    raise ValueError(kind)


def _is_squarefree(n: int) -> bool:
    return all(n % (i * i) for i in range(2, math.isqrt(n) + 1))


def _answer_matches_spec(row: dict) -> str | None:
    """Parse the displayed answer on its own and compare it with the spec.

    This never reuses the formatter that wrote the answer, so a formatting bug
    shows up as a disagreement instead of agreeing with itself.
    """
    check, answer = row["check"], row["answer"]
    kind = check["kind"]
    plain = answer.replace(MINUS, "-")
    if kind == "number":
        value = sp.Rational(check["value"])
        shown = plain.removeprefix("x = ").removesuffix("%").removesuffix("°")
        if sp.Rational(shown) != value:
            return f"answer {answer!r} is not {value}"
        if bool(check.get("percent")) != answer.endswith("%"):
            return f"percent flag and answer {answer!r} disagree"
        if check.get("simplest") and "/" in shown and sp.Rational(shown).q != int(shown.split("/")[1]):
            return f"answer {answer!r} is not in lowest terms"
        if check.get("form") == "decimal" and "/" in shown:
            return f"decimal answer {answer!r} is a fraction"
        if check.get("form") == "fraction" and "." in shown:
            return f"fraction answer {answer!r} is a decimal"
        return None
    if kind == "pi":
        if "π" not in answer or sp.simplify(to_sympy(answer) - spec_value(check)) != 0:
            return f"answer {answer!r} is not {spec_value(check)}"
        return None
    if kind == "radical":
        m = re.fullmatch(r"(\d*)√(\d+)|(\d+)", answer)
        if not m:
            return f"radical answer {answer!r} is not of the form a√b"
        if m.group(3):
            coef, rad = int(m.group(3)), 1
        else:
            coef, rad = int(m.group(1) or 1), int(m.group(2))
        if not _is_squarefree(rad) or (coef, rad) != (check["coef"], check["rad"]):
            return f"answer {answer!r} is not the simplified radical {check}"
        return None
    if kind == "expression":
        var = Y if check["var"] == "y" else X
        expected = sp.sympify(check["expr"], locals={check["var"]: var})
        if sp.expand(to_sympy(answer) - expected) != 0:
            return f"answer {answer!r} is not {expected}"
        if check["form"] == "factored":
            factors = re.findall(r"\(([^()]+)\)", answer)
            if len(factors) != 2 or any(sp.Poly(to_sympy(f), var).degree() != 1 for f in factors):
                return f"factored answer {answer!r} is not two linear factors"
        elif "(" in answer:
            return f"simplified answer {answer!r} still has parentheses"
        return None
    if kind == "set":
        shown = re.fullmatch(r"x = (\S+) or x = (\S+)", answer)
        if not shown or {to_sympy(v) for v in shown.groups()} != {sp.Rational(v) for v in check["values"]}:
            return f"answer {answer!r} does not list {check['values']}"
        return None
    if kind == "pair":
        shown = re.fullmatch(r"x = (\S+), y = (\S+)", answer)
        if not shown or tuple(to_sympy(v) for v in shown.groups()) != tuple(sp.Rational(v) for v in check["values"]):
            return f"answer {answer!r} != pair {check['values']}"
        return None
    if kind == "inequality":
        shown = re.fullmatch(r"x ([<>≤≥]) (\S+)", answer)
        ops = {"<": "<", ">": ">", "≤": "<=", "≥": ">="}
        if not shown or ops[shown.group(1)] != check["op"] or to_sympy(shown.group(2)) != sp.Rational(check["value"]):
            return f"answer {answer!r} != inequality {check}"
        return None
    return f"unknown check kind {kind}"


def recheck_bank(bank: dict[str, list[dict]]) -> list[str]:
    errors: list[str] = []
    recomputed = 0
    for code, rows in bank.items():
        for row in rows:
            where = f"bank {code} #{row['id']}"
            problem = _answer_matches_spec(row)
            if problem:
                errors.append(f"{where}: {problem}")
            try:
                got = _recompute(code, row["promptEn"])
            except Exception as exc:  # noqa: BLE001 — report the prompt that would not parse
                errors.append(f"{where}: could not read the prompt {row['promptEn']!r}: {exc}")
                continue
            if got is None:
                continue
            recomputed += 1
            if row["check"]["kind"] == "number" and isinstance(got, set):
                got = next(iter(got)) if len(got) == 1 else got
            if not _same(got, row["check"]):
                errors.append(f"{where}: prompt {row['promptEn']!r} gives {got}, key says {row['check']}")
    if recomputed < 2000:
        errors.append(f"only {recomputed} bank prompts were recomputed independently")
    return errors


def build_bank() -> dict[str, list[dict]]:
    if set(BUILDERS) != set(CODES):
        raise RuntimeError(f"builder mismatch {set(CODES) ^ set(BUILDERS)}")
    bank = {code: take(builder) for code, builder in BUILDERS.items()}
    errors = recheck_bank(bank)
    if errors:
        raise RuntimeError(f"{len(errors)} bank item(s) failed the recheck:\n" + "\n".join(errors[:40]))
    return bank


if __name__ == "__main__":
    data = build_bank()
    print(len(data), "lessons,", sum(len(rows) for rows in data.values()), "items, all rechecked")
