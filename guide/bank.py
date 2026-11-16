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
        f"Qiymat {old} dan {new} ga o'tdi. Necha foizga {suz}?",
        f"{fmt(value)}%",
        f"The change is {change} and the original is {old}. {change}/{old} = {fmt(value)}%.",
        f"O'zgarish {change}, eski son {old}. {change}/{old} = {fmt(value)}%.",
        expr=str(value),
    )


def g_ratio(k: int) -> dict:
    a = 1 + (k % 15)
    b = a + 1 + ((k * 3) % 12)
    parts = a + b
    scale = 2 + ((k * 5) % 14)
    total = parts * scale
    if k % 2 == 0:
        answer = a * scale
        which, qaysi = "smaller", "kichik"
    else:
        answer = b * scale
        which, qaysi = "larger", "katta"
    return item(
        k,
        f"Two parts are in the ratio {a}:{b} and total {total}. What is the {which} part?",
        f"Ikki qism {a}:{b} nisbatda va jami {total}. {qaysi.capitalize()} qism necha?",
        str(answer),
        f"One share is {scale}. The {which} part is {answer}.",
        f"Bitta ulush {scale}. {qaysi.capitalize()} qism {answer}.",
        expr=str(answer),
    )


def g_prop(k: int) -> dict:
    if k % 4 == 3:
        workers = 2 + (k % 6)
        days = 4 + (k % 8)
        more = workers + 1 + (k % 4)
        job = workers * days
        if job % more != 0:
            more = math.gcd(job, more) or 1
            if more == 0:
                more = 1
        answer = job // more
        return item(
            k,
            f"{workers} painters finish a job in {days} days. How many days do {more} painters need?",
            f"{workers} bo'yoqchi ishni {days} kunda tugatadi. {more} bo'yoqchiga necha kun kerak?",
            str(answer),
            f"The job is {job} painter-days. {job}/{more} = {answer} days.",
            f"Ish {job} bo'yoqchi-kun. {job}/{more} = {answer} kun.",
            expr=str(answer),
        )
    a, b = 1 + (k % 8), 2 + (k % 7)
    scale = 2 + (k % 6)
    left = a * scale
    right = b * scale
    x = right
    return item(
        k,
        f"Solve {a}/{b} = {left}/x.",
        f"{a}/{b} = {left}/x tenglamasidan x ni toping.",
        str(x),
        f"The scale from {a} to {left} is {scale}, so x = {b} × {scale} = {x}.",
        f"{a} dan {left} gacha masshtab {scale}, demak x = {b} × {scale} = {x}.",
        expr=str(x),
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
    elif kind == 1:
        value = base ** (m * n)
        en = f"Evaluate ({base}^{m})^{n}."
        uz = f"({base}^{m})^{n} ning qiymatini toping."
    else:
        value = sp.Rational(1, base**m)
        en = f"Write {base}^(−{m}) as a simplified fraction."
        uz = f"{base}^(−{m}) ni qisqartirilgan kasr qilib yozing."
    return item(
        k,
        en,
        uz,
        fmt(value),
        f"Use the exponent rule. The value is {fmt(value)}.",
        f"Daraja qoidasini qo'llang. Qiymat {fmt(value)}.",
        expr=str(sp.simplify(value)),
    )


def sqrt_form(n: int) -> tuple[str, sp.Expr]:
    a = 1
    b = n
    i = 2
    while i * i <= b:
        while b % (i * i) == 0:
            b //= i * i
            a *= i
        i += 1
    expr = a * sp.sqrt(b)
    if b == 1:
        text = str(a)
    elif a == 1:
        text = f"√{b}"
    else:
        text = f"{a}√{b}"
    return text, expr


def g_roots(k: int) -> dict:
    n = 2 + (k % 180)
    text, expression = sqrt_form(n)
    if sp.simplify(expression - sp.sqrt(n)) != 0:
        raise AssertionError(n)
    return item(
        k,
        f"Simplify √{n}.",
        f"√{n} ni soddalashtiring.",
        text,
        f"Pull out square factors. √{n} = {text}.",
        f"Kvadrat ko'paytuvchilarni chiqaring. √{n} = {text}.",
        expr="",
    )


def g_sci(k: int) -> dict:
    coeff = 1 + ((k // 2) % 30)
    exp = 1 + ((k // 60) % 6)
    if k % 2 == 0:
        value = coeff * 10**exp
        return item(
            k,
            f"Write {coeff} × 10^{exp} as an ordinary number.",
            f"{coeff} × 10^{exp} ni oddiy son qilib yozing.",
            str(value),
            f"Move the point {exp} places right. The number is {value}.",
            f"Nuqtani {exp} o'rin o'ngga suring. Son {value}.",
            expr=str(value),
        )
    hours = sp.Rational(1 + ((k // 2) % 40), 2)
    minutes = hours * 60
    return item(
        k,
        f"Convert {fmt(hours)} hours to minutes.",
        f"{fmt(hours)} soatni daqiqaga aylantiring.",
        fmt(minutes),
        f"Multiply by 60. The result is {fmt(minutes)} minutes.",
        f"60 ga ko'paytiring. Natija {fmt(minutes)} daqiqa.",
        expr=str(minutes),
    )


def g_expr(k: int) -> dict:
    a = 1 + (k % 8)
    b = 1 + ((k * 3) % 9)
    c = (k % 7) - 2
    x = sp.symbols("x")
    value = sp.expand(a * (x + b) + c * x)
    answer = str(value).replace("**", "^").replace("*", "")
    return item(
        k,
        f"Simplify {a}(x + {b}) + ({c})x.",
        f"{a}(x + {b}) + ({c})x ifodasini soddalashtiring.",
        answer,
        f"Distribute, then combine like terms. The result is {answer}.",
        f"Qavsni oching, so'ng o'xshash hadlarni birlashtiring. Natija {answer}.",
        expr=str(sp.simplify(value - sp.expand(value))),
    )


def g_linear(k: int) -> dict:
    a = 1 + (k % 9)
    x0 = (k % 13) - 4
    b = (k % 11) - 3
    right = a * x0 + b
    return item(
        k,
        f"Solve {a}x + ({b}) = {right}.",
        f"{a}x + ({b}) = {right} tenglamasini yeching.",
        str(x0),
        f"Undo the addition, then divide by {a}. x = {x0}.",
        f"Qo'shishni qaytaring, so'ng {a} ga bo'ling. x = {x0}.",
        expr=str(x0),
    )


def g_frac_eq(k: int) -> dict:
    p = 1 + (k % 12)
    q = p + 1 + ((k // 12) % 8)
    mult = 1 + ((k // 96) % 8)
    product = p * mult
    x0 = mult * q
    return item(
        k,
        f"Solve ({p}/{q})x = {product}.",
        f"({p}/{q})x = {product} tenglamasini yeching.",
        str(x0),
        f"Multiply by the reciprocal {q}/{p}. x = {x0}.",
        f"Teskari kasr {q}/{p} ga ko'paytiring. x = {x0}.",
        expr=str(x0),
    )


def g_ineq(k: int) -> dict:
    if k % 5 == 4:
        bound = 1 + ((k // 5) % 40)
        # -2x > 2*bound => x < -bound
        answer = f"x < -{bound}"
        return item(
            k,
            f"Solve −2x > {2 * bound}.",
            f"−2x > {2 * bound} tengsizligini yeching.",
            answer,
            f"Divide by −2 and flip the sign. {answer}.",
            f"−2 ga bo'ling va belgini almashtiring. {answer}.",
            expr=str(-bound),
        )
    added = (k // 5) % 25
    gap = 1 + ((k // 125) % 20)
    limit = added + gap
    answer = f"x < {gap}"
    return item(
        k,
        f"Solve x + {added} < {limit}.",
        f"x + {added} < {limit} tengsizligini yeching.",
        answer,
        f"Subtract {added}. {answer}.",
        f"{added} ni ayiring. {answer}.",
        expr=str(gap),
    )


def g_words(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        extra = 2 + ((k // 3) % 30)
        total = extra + 3 + ((k // 90) % 25)
        number = total - extra
        return item(
            k,
            f"A number increased by {extra} is {total}. What is the number?",
            f"Sonning ustiga {extra} qo'shilsa, {total} chiqadi. Son necha?",
            str(number),
            f"x + {extra} = {total}, so x = {number}.",
            f"x + {extra} = {total}, demak x = {number}.",
            expr=str(number),
        )
    if kind == 1:
        fee = 2 + ((k // 3) % 15)
        rate = 2 + ((k // 45) % 10)
        count = 2 + ((k // 450) % 12)
        total = fee + rate * count
        return item(
            k,
            f"Tickets cost ${rate} each plus a ${fee} fee. The total is ${total}. How many tickets?",
            f"Chipta {rate} dollardan, ustiga {fee} dollar haq. Jami {total} dollar. Nechta chipta?",
            str(count),
            f"{rate}n + {fee} = {total}, so n = {count}.",
            f"{rate}n + {fee} = {total}, demak n = {count}.",
            expr=str(count),
        )
    twice_gap = 1 + ((k // 3) % 20)
    number = 3 + ((k // 60) % 20)
    total = 3 * number - twice_gap
    return item(
        k,
        f"Three times a number, decreased by {twice_gap}, is {total}. What is the number?",
        f"Sonning uch baravari, {twice_gap} ga kamaytirilsa, {total}. Son necha?",
        str(number),
        f"3x − {twice_gap} = {total}, so x = {number}.",
        f"3x − {twice_gap} = {total}, demak x = {number}.",
        expr=str(number),
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
    return item(
        k,
        f"What is the slope of the line through ({x1}, {y1}) and ({x2}, {y2})?",
        f"({x1}, {y1}) va ({x2}, {y2}) nuqtalardan o'tgan chiziqning qiyaligi necha?",
        fmt(slope),
        f"Rise {rise}, run {run}. Slope = {fmt(slope)}.",
        f"Ko'tarilish {rise}, yugurish {run}. Qiyalik = {fmt(slope)}.",
        expr=str(slope),
    )


def g_system(k: int) -> dict:
    x0 = (k % 20) - 8
    y0 = ((k // 20) % 15) - 6
    s = x0 + y0
    t = x0 - y0
    return item(
        k,
        f"Solve the system x + y = {s} and x − y = {t}.",
        f"x + y = {s} va x − y = {t} sistemasini yeching.",
        f"x = {x0}, y = {y0}",
        f"Add the equations to get x, then subtract to get y. x = {x0}, y = {y0}.",
        f"Tenglamalarni qo'shib x ni, ayirib y ni toping. x = {x0}, y = {y0}.",
        expr=f"{x0},{y0}",
    )


def g_func(k: int) -> dict:
    a = 1 + (k % 8)
    b = (k % 13) - 5
    n = (k % 10) - 2
    value = a * n + b
    return item(
        k,
        f"If f(x) = {a}x + ({b}), what is f({n})?",
        f"Agar f(x) = {a}x + ({b}) bo'lsa, f({n}) necha?",
        str(value),
        f"Substitute {n}: {a}×{n} + ({b}) = {value}.",
        f"{n} ni qo'ying: {a}×{n} + ({b}) = {value}.",
        expr=str(value),
    )


def g_poly(k: int) -> dict:
    a = 1 + (k % 5)
    b = (k % 9) - 3
    c = 1 + ((k * 2) % 4)
    d = (k % 7) - 2
    x = sp.symbols("x")
    value = sp.expand((a * x + b) * (c * x + d))
    answer = str(value).replace("**", "^").replace("*", "")
    return item(
        k,
        f"Expand ({a}x + ({b}))({c}x + ({d})).",
        f"({a}x + ({b}))({c}x + ({d})) ifodasini yoying.",
        answer,
        f"Each term meets each term. The product is {answer}.",
        f"Har bir had har bir had bilan uchrashadi. Ko'paytma {answer}.",
        expr="0",
    )


def g_factor(k: int) -> dict:
    r = 1 + (k % 30)
    s = r + 1 + ((k // 30) % 8)
    b = r + s
    c = r * s
    return item(
        k,
        f"Factor x² + {b}x + {c}.",
        f"x² + {b}x + {c} ni ko'paytuvchilarga ajrating.",
        f"(x + {r})(x + {s})",
        f"{r} and {s} multiply to {c} and add to {b}.",
        f"{r} va {s} ning ko'paytmasi {c}, yig'indisi {b}.",
        expr="0",
    )


def g_quad(k: int) -> dict:
    r = (k % 25) - 10
    s = r + 1 + ((k // 25) % 12)
    b = -(r + s)
    c = r * s
    bsign = f"+ {b}" if b >= 0 else f"− {abs(b)}"
    csign = f"+ {c}" if c >= 0 else f"− {abs(c)}"
    return item(
        k,
        f"Solve x² {bsign}x {csign} = 0.",
        f"x² {bsign}x {csign} = 0 tenglamasini yeching.",
        f"x = {r} or x = {s}",
        f"The roots are {r} and {s}, because those values make a factor zero.",
        f"Ildizlar {r} va {s}, chunki o'sha qiymatlar ko'paytuvchini nol qiladi.",
        expr=f"{r},{s}",
    )


def g_vertex(k: int) -> dict:
    h = (k % 11) - 5
    m = 1 + (k % 8)
    sign = 1 if k % 2 == 0 else -1
    name = "minimum" if sign == 1 else "maximum"
    uz = "minimum" if sign == 1 else "maksimum"
    inside = f"x − ({h})" if h >= 0 else f"x + {abs(h)}"
    coef = "" if sign == 1 else "−"
    if m != 1:
        coef = f"{sign * m}"
    return item(
        k,
        f"What is the {name} value of y = {coef}({inside})² + ({m if sign == 1 else -m})?" if False else f"What is the {name} value of y = {sign * m}({inside})² + {3 + (k % 6)}?",
        f"y = {sign * m}({inside})² + {3 + (k % 6)} ning {uz} qiymati necha?",
        str(3 + (k % 6)) if sign == 1 else str(3 + (k % 6)),
        f"The squared term cannot go past the vertex value {3 + (k % 6)} when the leading coefficient is {'positive' if sign == 1 else 'negative'}.",
        f"Yetakchi koeffitsiyent {'musbat' if sign == 1 else 'manfiy'} bo'lgani uchun uchdagi qiymat {3 + (k % 6)}.",
        expr=str(3 + (k % 6)),
    )


def g_equiv(k: int) -> dict:
    a = 2 + (k % 6)
    b = 1 + (k % 8)
    c = 1 + (k % 5)
    x = sp.symbols("x")
    value = sp.expand(a * (x + b) - c * x)
    answer = str(value).replace("**", "^").replace("*", "")
    return item(
        k,
        f"Write an expression equivalent to {a}(x + {b}) − {c}x.",
        f"{a}(x + {b}) − {c}x ga teng kuchli ifoda yozing.",
        answer,
        f"Distribute and combine. The equivalent expression is {answer}.",
        f"Qavsni oching va birlashtiring. Teng kuchli ifoda {answer}.",
        expr="0",
    )


def g_rational(k: int) -> dict:
    p = 2 + (k % 40)
    q = 1 + ((k // 40) % 15)
    if math.gcd(p, q) != 1 and k % 2 == 0:
        q += 1
    x0 = sp.Rational(p, q)
    return item(
        k,
        f"Solve {p}/x = {q}.",
        f"{p}/x = {q} tenglamasini yeching.",
        fmt(x0),
        f"x = {p}/{q} = {fmt(x0)}. Zero is excluded.",
        f"x = {p}/{q} = {fmt(x0)}. Nol istisno.",
        expr=str(x0),
    )


def g_radical(k: int) -> dict:
    root = 2 + (k % 25)
    added = (k // 25) % 30
    x0 = root**2 - added
    if x0 < 0:
        added = 0
        x0 = root**2
    return item(
        k,
        f"Solve √(x + {added}) = {root}.",
        f"√(x + {added}) = {root} tenglamasini yeching.",
        str(x0),
        f"Square: x + {added} = {root**2}, so x = {x0}. The check passes because the root is nonnegative.",
        f"Kvadrat: x + {added} = {root**2}, demak x = {x0}. Ildiz manfiy emas, tekshiruv o'tadi.",
        expr=str(x0),
    )


def g_exp_growth(k: int) -> dict:
    start = 4 * (1 + (k % 30))
    times = 1 + ((k // 30) % 6)
    value = start * (2**times)
    return item(
        k,
        f"A quantity starts at {start} and doubles {times} time{'s' if times != 1 else ''}. What is the result?",
        f"Miqdor {start} dan boshlanadi va {times} marta ikki baravar bo'ladi. Natija necha?",
        str(value),
        f"{start} × 2^{times} = {value}.",
        f"{start} × 2^{times} = {value}.",
        expr=str(value),
    )


def g_context_ratio(k: int) -> dict:
    red = 1 + (k % 10)
    blue = 1 + ((k // 10) % 10)
    scale = 1 + ((k // 100) % 8)
    total = (red + blue) * scale
    answer = red * scale
    return item(
        k,
        f"Red and blue paint are mixed {red}:{blue}. How many liters of red are in {total} liters of mixture?",
        f"Qizil va ko'k bo'yoq {red}:{blue} aralashadi. {total} litr aralashmada necha litr qizil bor?",
        str(answer),
        f"Red is {red}/{red + blue} of the mixture, which is {answer} liters.",
        f"Qizil aralashmaning {red}/{red + blue} qismi, ya'ni {answer} litr.",
        expr=str(answer),
    )


def g_table(k: int) -> dict:
    slope = 1 + (k % 7)
    intercept = k % 10
    x0 = 3 + (k % 8)
    y0 = slope * x0 + intercept
    return item(
        k,
        f"The rule y = {slope}x + {intercept} fits a table. What is y when x = {x0}?",
        f"y = {slope}x + {intercept} qoidasi jadvalga mos. x = {x0} bo'lganda y necha?",
        str(y0),
        f"Substitute: {slope}×{x0} + {intercept} = {y0}.",
        f"Qo'ying: {slope}×{x0} + {intercept} = {y0}.",
        expr=str(y0),
    )


def g_stats(k: int) -> dict:
    a = 1 + (k % 40)
    b = a + 1 + ((k // 40) % 12)
    c = b + 1 + ((k // 480) % 8)
    kind = k % 3
    if kind == 0:
        mean = sp.Rational(a + b + c, 3)
        return item(
            k,
            f"What is the mean of {a}, {b}, and {c}?",
            f"{a}, {b} va {c} ning o'rta arifmetigi necha?",
            fmt(mean),
            f"The sum is {a + b + c}. Divide by 3 to get {fmt(mean)}.",
            f"Yig'indi {a + b + c}. 3 ga bo'ling: {fmt(mean)}.",
            expr=str(mean),
        )
    if kind == 1:
        return item(
            k,
            f"What is the median of {c}, {a}, {b}?",
            f"{c}, {a}, {b} sonlarining medianasi necha?",
            str(b),
            f"Sorted, the list is {a}, {b}, {c}. The middle is {b}.",
            f"Tartiblanganda {a}, {b}, {c}. O'rtasi {b}.",
            expr=str(b),
        )
    return item(
        k,
        f"What is the range of {a}, {c}, {b}?",
        f"{a}, {c}, {b} sonlarining qamrovi necha?",
        str(c - a),
        f"Largest minus smallest is {c} − {a} = {c - a}.",
        f"Eng katta minus eng kichik: {c} − {a} = {c - a}.",
        expr=str(c - a),
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
        return item(
            k,
            f"A line of fit is y = {slope}x + {intercept}. What does it predict at x = {x0}?",
            f"Mos chiziq y = {slope}x + {intercept}. x = {x0} dagi bashorat necha?",
            str(pred),
            f"{slope}×{x0} + {intercept} = {pred}.",
            f"{slope}×{x0} + {intercept} = {pred}.",
            expr=str(pred),
        )
    return item(
        k,
        f"The prediction is {pred} and the actual value is {actual}. What is the residual?",
        f"Bashorat {pred}, haqiqiy qiymat {actual}. Qoldiq necha?",
        str(residual),
        f"Residual = actual − predicted = {actual} − {pred} = {residual}.",
        f"Qoldiq = haqiqiy − bashorat = {actual} − {pred} = {residual}.",
        expr=str(residual),
    )


def g_prob(k: int) -> dict:
    red = 1 + (k % 15)
    blue = 1 + ((k // 15) % 12)
    green = 1 + ((k // 180) % 10)
    total = red + blue + green
    which = k % 3
    count = (red, blue, green)[which]
    name = ("red", "blue", "green")[which]
    uz = ("qizil", "ko'k", "yashil")[which]
    value = sp.Rational(count, total)
    return item(
        k,
        f"A bag has {red} red, {blue} blue, and {green} green marbles. What is the probability of {name}?",
        f"Qopda {red} qizil, {blue} ko'k va {green} yashil marmar bor. {uz.capitalize()} ehtimoli necha?",
        fmt(value),
        f"{count} favorable out of {total}. The probability is {fmt(value)}.",
        f"{total} tadan {count} qulay. Ehtimollik {fmt(value)}.",
        expr=str(value),
    )


def g_margin(k: int) -> dict:
    estimate = 20 + (k % 60)
    margin = 1 + (k % 8)
    if k % 2 == 0:
        answer = estimate - margin
        edge, chekka = "lower", "past"
    else:
        answer = estimate + margin
        edge, chekka = "upper", "yuqori"
    return item(
        k,
        f"An estimate is {estimate}% with a margin of error of {margin} percentage points. What is the {edge} end?",
        f"Taxmin {estimate}%, xato chegarasi {margin} foiz punkti. {chekka.capitalize()} chekka necha?",
        str(answer),
        f"{estimate} {'−' if edge == 'lower' else '+'} {margin} = {answer}.",
        f"{estimate} {'−' if edge == 'lower' else '+'} {margin} = {answer}.",
        expr=str(answer),
    )


def g_angles(k: int) -> dict:
    kind = k % 3
    if kind == 0:
        given = 15 + (k % 140)
        other = 180 - given
        return item(
            k,
            f"An angle of {given}° sits on a straight line. What is the adjacent angle?",
            f"{given}° li burchak to'g'ri chiziqda turadi. Qo'shni burchak necha gradus?",
            str(other),
            f"180 − {given} = {other}.",
            f"180 − {given} = {other}.",
            expr=str(other),
        )
    if kind == 1:
        given = 10 + (k % 70)
        other = 90 - given
        return item(
            k,
            f"What is the complement of a {given}° angle?",
            f"{given}° li burchakning to'ldiruvchisi necha gradus?",
            str(other),
            f"90 − {given} = {other}.",
            f"90 − {given} = {other}.",
            expr=str(other),
        )
    a = 20 + (k % 50)
    return item(
        k,
        f"Two lines cross and one angle is {a}°. What is the vertical angle?",
        f"Ikki chiziq kesishadi va bitta burchak {a}°. Vertikal burchak necha?",
        str(a),
        f"Vertical angles are equal, so the angle is {a}°.",
        f"Vertikal burchaklar teng, demak burchak {a}°.",
        expr=str(a),
    )


def g_similar(k: int) -> dict:
    factor = 2 + (k % 12)
    side = 2 + ((k // 12) % 30)
    return item(
        k,
        f"Similar triangles have scale factor {factor}. A side of {side} corresponds to what length?",
        f"O'xshash uchburchaklarning masshtabi {factor}. {side} tomonga qanday uzunlik mos?",
        str(side * factor),
        f"{side} × {factor} = {side * factor}.",
        f"{side} × {factor} = {side * factor}.",
        expr=str(side * factor),
    )


def g_pythag(k: int) -> dict:
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (7, 24, 25), (8, 15, 17), (9, 12, 15), (9, 40, 41), (20, 21, 29), (12, 16, 20), (12, 35, 37), (11, 60, 61), (28, 45, 53)]
    a, b, c = triples[k % len(triples)]
    scale = 1 + ((k // len(triples)) % 12)
    a, b, c = a * scale, b * scale, c * scale
    if k % 2 == 0:
        return item(
            k,
            f"A right triangle has legs {a} and {b}. What is the hypotenuse?",
            f"To'g'ri burchakli uchburchakning katetlari {a} va {b}. Gipotenuza necha?",
            str(c),
            f"{a}² + {b}² = {c}², so the hypotenuse is {c}.",
            f"{a}² + {b}² = {c}², demak gipotenuza {c}.",
            expr=str(c),
        )
    return item(
        k,
        f"A right triangle has hypotenuse {c} and one leg {a}. What is the other leg?",
        f"Gipotenuza {c} va bitta katet {a}. Ikkinchi katet necha?",
        str(b),
        f"√({c}² − {a}²) = {b}.",
        f"√({c}² − {a}²) = {b}.",
        expr=str(b),
    )


def g_trig(k: int) -> dict:
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41), (20, 21, 29), (12, 35, 37), (9, 12, 15), (28, 45, 53)]
    scale = 1 + ((k // (len(triples) * 3)) % 5)
    a, b, c = triples[k % len(triples)]
    a, b, c = a * scale, b * scale, c * scale
    which = (k // len(triples)) % 3
    if which == 0:
        name, uz, value = "sine", "sinusi", sp.Rational(a, c)
    elif which == 1:
        name, uz, value = "cosine", "kosinusi", sp.Rational(b, c)
    else:
        name, uz, value = "tangent", "tangensi", sp.Rational(a, b)
    return item(
        k,
        f"In a right triangle with opposite {a}, adjacent {b}, and hypotenuse {c}, what is the {name}?",
        f"Qarama-qarshi {a}, yondosh {b}, gipotenuza {c} bo'lgan to'g'ri burchakli uchburchakda {uz} necha?",
        fmt(value),
        f"The {name} is {fmt(value)}.",
        f"{uz.capitalize()} {fmt(value)}.",
        expr=str(value),
    )


def g_area(k: int) -> dict:
    kind = k % 4
    if kind == 0:
        base, height = 2 + ((k // 4) % 30), 2 + ((k // 120) % 20)
        value = sp.Rational(base * height, 2)
        return item(k, f"A triangle has base {base} and height {height}. What is its area?", f"Uchburchakning asosi {base}, balandligi {height}. Yuzi necha?", fmt(value), f"(1/2)×{base}×{height} = {fmt(value)}.", f"(1/2)×{base}×{height} = {fmt(value)}.", str(value))
    if kind == 1:
        length, width = 2 + ((k // 4) % 28), 2 + ((k // 112) % 16)
        return item(k, f"A rectangle is {length} by {width}. What is its area?", f"To'g'ri to'rtburchak {length} ga {width}. Yuzi necha?", str(length * width), f"{length}×{width} = {length * width}.", f"{length}×{width} = {length * width}.", str(length * width))
    if kind == 2:
        r = 1 + ((k // 4) % 24)
        return item(k, f"A circle has radius {r}. What is its area?", f"Aylananing radiusi {r}. Yuzi necha?", f"{r * r}π", f"π×{r}² = {r * r}π.", f"π×{r}² = {r * r}π.", str(r * r))
    b1, b2, h = 2 + ((k // 4) % 16), 4 + ((k // 64) % 18), 2 + ((k // 400) % 10)
    value = sp.Rational(b1 + b2, 2) * h
    return item(k, f"A trapezoid has bases {b1} and {b2} and height {h}. What is its area?", f"Trapetsiyaning asoslari {b1} va {b2}, balandligi {h}. Yuzi necha?", fmt(value), f"Average the bases, then multiply by {h}. The