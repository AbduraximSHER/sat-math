"""Attach depth paragraphs and practice banks onto lesson objects."""

from __future__ import annotations

from dataclasses import replace

from guide.bank import build_bank
from guide.depth import depth_for
from guide.model import Lesson, Unit


def deepen_lesson(lesson: Lesson) -> Lesson:
    en_extra, uz_extra = depth_for(lesson.code)
    if not en_extra and not uz_extra:
        return lesson
    return replace(
        lesson,
        explain_en=tuple(lesson.explain_en) + tuple(en_extra),
        explain_uz=tuple(lesson.explain_uz) + tuple(uz_extra),
    )


def deepen_units(units: tuple[Unit, ...] | list[Unit]) -> tuple[Unit, ...]:
    out: list[Unit] = []
    for unit in units:
        lessons = tuple(deepen_lesson(lesson) for lesson in unit.lessons)
        out.append(replace(unit, lessons=lessons))
    return tuple(out)


def bank_public_row(row: dict) -> dict:
    return {
        "id": row["id"],
        "level": row["level"],
        "promptEn": row["promptEn"],
        "promptUz": row["promptUz"],
    }


def bank_key_row(row: dict) -> dict:
    return {
        "id": row["id"],
        "answer": row["answer"],
        "solutionEn": row["solutionEn"],
        "solutionUz": row["solutionUz"],
    }


def build_public_and_keys(units: tuple[Unit, ...]):
    """Return (enriched units, public bank map, keys payload)."""
    enriched = deepen_units(units)
    bank = build_bank()
    public_bank = {code: [bank_public_row(row) for row in rows] for code, rows in bank.items()}
    lesson_keys: dict[str, dict] = {}
    for unit in enriched:
        for lesson in unit.lessons:
            lesson_keys[lesson.code] = {
                "practice": [
                    {
                        "answer": item.answer,
                        "solutionEn": item.solution_en,
                        "solutionUz": item.solution_uz,
                    }
                    for item in lesson.practice
                ],
                "bank": [bank_key_row(row) for row in bank.get(lesson.code, [])],
            }
    return enriched, public_bank, lesson_keys
