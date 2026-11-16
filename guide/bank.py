"""One hundred checked practice items for every lesson.

Answers are computed here, then checked again before they are exported.
"""

from __future__ import annotations

import math

import sympy as sp

CODES = (
    ["0.1"]
    + [f"1.{i}" for i in range(1, 11)]
    + [f"2.{i}" for i in range(1, 9)]
    + [f"3.{i}" for i in range(1, 9)]
    + [f"4.{i}" for i in range(1, 7)]
    + [f"5.{i}" for i in range(1, 8)]
    + [f"6.{i}" for i in range(1, 5)]
)


def level_of(i: int) -> str:
    if i < 40:
        return "oson"
    if i < 80:
        return "orta"
    return "sat"


def fmt(value) -> str:
    value = sp.simplify(value)
    if value.is_integer:
        return str(int(value))
    if value.is_rational:
        return f"{int(value.p)}/{int(value.q)}"
    return str(value)


def frac(n: int, d: int) -> str:
    return fmt(sp.Rational(n, d))


def item(i: int, en: str, uz: str, answer: str, sen: str, suz: str, expr: str | None = None) -> dict:
    return {
        "level": level_of(i),
        "promptEn": en,
        "promptUz": uz,
        "answer": answer,
        "solutionEn": sen,
        "solutionUz": suz,
        "expr": expr or "",
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
    for index, row in enumerate(rows, start=1):
        row["id"] = f"{index:03d}"
    return rows


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
        sign, word, suz = "−", "difference", "ayirmasi"
    elif op == 2:
        value = left * right
        sign, word, suz = "×", "product", "ko'paytmasi"
    else:
        value = left / right
        sign, word, suz = "÷", "quotient", "bo'linmasi"
    answer = fmt(value)
    en = f"Find the {word} {a}/{b} {sign} {c}/{d} as a simplified fraction."
    uz = f"{a}/{b} {sign} {c}/{d} ning {suz}ni qisqartirilgan kasrda toping."
    sen = f"Compute {a}/{b} {sign} {c}/{d}. The simplified value is {answer}."
    suz_s = f"{a}/{b} {sign} {c}/{d} ni hisoblang. Qisqartirilgan qiymat {answer}."
    return item(k, en, uz, answer, sen, suz_s, expr=str(value))


def g_abs(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        n = k + 1
        answer = str(n)
        return item(
            k,
            f"Evaluate |−{n}|.",
            f"|−{n}| ning qiymatini toping.",
            answer,
            f"The distance from −{n} to 0 is {n}.",
            f"−{n} dan 0 gacha masofa {n}.",
            expr=str(n),
        )
    if kind == 1:
        a, b = (k % 12) + 1, ((k * 2) % 9) + 1
        answer = str(a + b)
        return item(
            k,
            f"Evaluate |{a}| + |−{b}|.",
            f"|{a}| + |−{b}| ifodaning qiymatini toping.",
            answer,
            f"{a} + {b} = {answer}. Both bars are distances.",
            f"{a} + {b} = {answer}. Ikkala modul ham masofa.",
            expr=str(a + b),
        )
    left, right = -(k % 15), (k % 11) + 1
    dist = abs(right - left)
    return item(
        k,
        f"What is the distance on the number line between {left} and {right}?",
        f"Son o'qida {left} va {right} orasidagi masofa necha?",
        str(dist),
        f"|{right} − ({left})| = {dist}.",
        f"|{right} − ({left})| = {dist}.",
        expr=str(dist),
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
        expr = f"{a} × {b} − {c}({d} + 1)"
    return item(
        k,
        f"Evaluate {expr}.",
        f"{expr} ifodaning qiymatini toping.",
        str(value),
        f"Follow grouping, then powers, then multiplication. The value is {value}.",
        f"Avval qavs, so'ng daraja, so'ng ko'paytirish. Qiymat {value}.",
        expr=str(value),
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
            dec = fmt(value)
        return item(
            k,
            f"Write the fraction {n}/{d} as a decimal.",
            f"{n}/{d} kasrini o'nli kasr qilib yozing.",
            f"{dec} ({fmt(value)})",
            f"Divide {n} by {d}. The decimal is {dec}.",
            f"{n} ni {d} ga bo'ling. O'nli kasr {dec}.",
            expr=str(value),
        )
    if kind == 1:
        hundredths = 1 + (k % 97)
        value = sp.Rational(hundredths, 100)
        text = f"0.{hundredths:02d}"
        return item(
            k,
            f"Write the decimal {text} as a simplified fraction.",
            f"{text} o'nli kasrini qisqartirilgan kasr qilib yozing.",
            fmt(value),
            f"{text} means {hundredths}/100, which simplifies to {fmt(value)}.",
            f"{text} degani {hundredths}/100, qisqartirilsa {fmt(value)}.",
            expr=str(value),
        )
    p = 1 + (k % 11)
    q = 2 + ((k * 2) % 9)
    r = 1 + ((k * 3) % 8)
    s = 2 + ((k * 5) % 9)
    value = sp.Rational(p, q) + sp.Rational(r, s)
    return item(
        k,
        f"Add {p}/{q} and {r}/{s}. Give a simplified fraction.",
        f"{p}/{q} va {r}/{s} ni qo'shing. Qisqartirilgan kasr yozing.",
        fmt(value),
        f"The sum is {fmt(value)}.",
        f"Yig'indi {fmt(value)}.",
        expr=str(value),
    )


def g_percent(k: int) -> dict:
    """One hundred percent items for lesson 1.4 (not percent change — that is 1.5)."""
    kind = k % 10

    if kind == 0:
        # p% of n
        p = 5 * (1 + ((k * 3) % 19))
        n = 4 * (5 + ((k * 7) % 45))
        value = sp.Rational(p, 100) * n
        return item(
            k,
            f"What is {p}% of {n}?",
            f"{n} ning {p} foizi necha?",
            fmt(value),
            f"Write {p}% as {p}/100. ({p}/100) × {n} = {fmt(value)}.",
            f"{p}% ni {p}/100 deb yozing. ({p}/100) × {n} = {fmt(value)}.",
            expr=str(value),
        )

    if kind == 1:
        # part is what percent of whole — force a clean integer percent
        p = 5 * (1 + ((k * 2) % 18))
        whole = 20 * (1 + ((k * 5) % 20))
        part = int(sp.Rational(p, 100) * whole)
        return item(
            k,
            f"{part} is what percent of {whole}?",
            f"{part} soni {whole} ning necha foizi?",
            f"{p}%",
            f"The whole is after 'of': ({part}/{whole}) × 100 = {p}%.",
            f"Butun — 'of' dan keyin: ({part}/{whole}) × 100 = {p}%.",
            expr=str(p),
        )

    if kind == 2:
        # fraction → percent
        dens = (2, 4, 5, 8, 10, 20, 25, 50)
        d = dens[k % len(dens)]
        n = 1 + ((k // len(dens)) % (d - 1 if d > 1 else 1))
        while sp.gcd(n, d) != 1 and n < d:
            n += 1
        if n >= d:
            n = 1
        value = sp.Rational(n, d) * 100
        return item(
            k,
            f"Write {n}/{d} as a percent.",
            f"{n}/{d} ni foizda yozing.",
            f"{fmt(value)}%",
            f"A percent is the fraction times 100. ({n}/{d}) × 100 = {fmt(value)}%.",
            f"Foiz — kasrni 100 ga ko'paytirish. ({n}/{d}) × 100 = {fmt(value)}%.",
            expr=str(value),
        )

    if kind == 3:
        # percent → simplified fraction
        p = 5 * (1 + ((k * 4) % 19))
        value = sp.Rational(p, 100)
        return item(
            k,
            f"Write {p}% as a simplified fraction.",
            f"{p}% ni qisqartirilgan kasrda yozing.",
            fmt(value),
            f"{p}% = {p}/100 = {fmt(value)} after simplifying.",
            f"{p}% = {p}/100 = {fmt(value)} (qisqartirilgan).",
            expr=str(value),
        )

    if kind == 4:
        # find the whole: p% of ? = part
        p = 5 * (2 + ((k * 3) % 16))
        whole = 10 * (2 + ((k * 11) % 28))
        part = sp.Rational(p, 100) * whole
        return item(
            k,
            f"{fmt(part)} is {p}% of what number?",
            f"{fmt(part)} qaysi sonning {p} foizi?",
            fmt(whole),
            f"Part = percent × whole, so whole = part ÷ (p/100) = {fmt(part)} ÷ ({p}/100) = {fmt(whole)}.",
            f"Qism = foiz × butun, demak butun = qism ÷ (p/100) = {fmt(part)} ÷ ({p}/100) = {fmt(whole)}.",
            expr=str(whole),
        )

    if kind == 5:
        # discount: amount removed
        price = 20 * (2 + ((k * 5) % 18))
        p = 5 * (2 + ((k * 2) % 15))
        off = sp.Rational(p, 100) * price
        return item(
            k,
            f"A ${price} item is discounted by {p}%. How many dollars are taken off?",
            f"{price}$ li mahsulotga {p}% chegirma. Necha dollar ayiriladi?",
            fmt(off),
            f"The discount is {p}% of {price}: ({p}/100) × {price} = {fmt(off)}.",
            f"Chegirma — {price} ning {p} foizi: ({p}/100) × {price} = {fmt(off)}.",
            expr=str(off),
        )

    if kind == 6:
        # discount: price paid (remainder)
        price = 25 * (2 + ((k * 7) % 16))
        p = 5 * (1 + ((k * 5) % 14))
        paid = price * sp.Rational(100 - p, 100)
        return item(
            k,
            f"A ${price} jacket is {p}% off. What is the sale price?",
            f"{price}$ kurtka {p}% chegirmada. Sotuv narxi necha?",
            fmt(paid),
            f"You pay {100 - p}% of the original: ({100 - p}/100) × {price} = {fmt(paid)}.",
            f"To'lanadigan qism {100 - p}%: ({100 - p}/100) × {price} = {fmt(paid)}.",
            expr=str(paid),
        )

    if kind == 7:
        # over 100%
        p = 100 + 5 * (1 + ((k * 3) % 20))
        n = 5 * (2 + ((k * 4) % 24))
        value = sp.Rational(p, 100) * n
        return item(
            k,
            f"What is {p}% of {n}?",
            f"{n} ning {p} foizi necha?",
            fmt(value),
            f"{p}% is more than one whole: ({p}/100) × {n} = {fmt(value)}.",
            f"{p}% birdan katta: ({p}/100) × {n} = {fmt(value)}.",
            expr=str(value),
        )

    if kind == 8:
        # sales tax with an integer dollar answer
        p = 5 * (1 + ((k * 3) % 4))  # 5,10,15,20
        n = 20 * (2 + ((k * 5) % 18))
        value = sp.Rational(p, 100) * n
        return item(
            k,
            f"Sales tax is {p}%. How much tax is collected on a ${n} purchase?",
            f"Sotuv solig'i {p}%. {n}$ xarid uchun soliq necha?",
            fmt(value),
            f"{p}% of {n} is ({p}/100)×{n} = {fmt(value)}.",
            f"{n} ning {p} foizi ({p}/100)×{n} = {fmt(value)}.",
            expr=str(value),
        )

    # kind == 9: remaining / complement word problem
    total = 20 * (3 + ((k * 3) % 15))
    p = 5 * (2 + ((k * 7) % 12))
    kept = total * sp.Rational(100 - p, 100)
    return item(
        k,
        f"A class of {total} students: {p}% are absent. How many students are present?",
        f"{total} o'quvchili sinfda {p}% yo'q. Nechta o'quvchi bor?",
        fmt(kept),
        f"Present is {100 - p}% of {total}: ({100 - p}/100) × {total} = {fmt(kept)}.",
        f"Borligi {total} ning {100 - p} foizi: ({100 - p}/100) × {total} = {fmt(kept)}.",
        expr=str(kept),
    )


def g_change(k: int) -> dict:
    if k % 5 == 4:
        start = 20 * (1 + (k % 8))
        first = 10 * (1 + (k % 3))
        second = 10
        factor = (sp.Rational(100 + first, 100)) * (sp.Rational(100 - second, 100))
        final = start * factor
        return item(
            k,
            f"A price of {start} rises by {first}% and then falls by {second}%. What is the final price?",
            f"{start} narx {first}% ga oshadi, so'ng {second}% ga tushadi. Oxirgi narx necha?",
            fmt(final),
            f"Multiply by {100 + first}/100 and then by {100 - second}/100. The result is {fmt(final)}.",
            f"{100 + first}/100 ga, so'ng {100 - second}/100 ga ko'paytiring. Natija {fmt(final)}.",
            expr=str(final),
        )
    old = 10 * (2 + (k % 20))
    change = 5 * (1 + (k % 7))
    if k % 2 == 0:
        new = old + change
        word, suz = "increase", "oshdi"
        value = sp.Rational(change, old) * 100
    else:
        if change >= old:
            change = old // 2
        new = old - change
        word, suz = "decrease", "kamaydi"
        value = sp.Rational(change, old) * 100
    return item(
        k,
        f"A value goes from {old} to {new}. By what percent did it {word}?",
        f"Qiymat {old} dan {new} ga o'tdi. Necha foizga {s