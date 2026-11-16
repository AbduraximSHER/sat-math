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
