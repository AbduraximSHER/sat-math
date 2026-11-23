"""Write the website's guide.json (no keys) and keys.json (server-only)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import sympy as sp

from guide.bank import c_num, c_pair, c_pi
from guide.content import MINI, UNITS
from guide.content.front import formula_sheet
from guide.content.glossary import GLOSSARY
from guide.enrich import build_public_and_keys
from guide.figures import ASSET_DIR, make_figures
from guide.model import Example, Lesson, MiniItem, Practice, Unit

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "site" / "data" / "guide.json"
KEYS_PATH = ROOT / "site" / "data" / "keys.json"
PUBLIC_FIGURES = ROOT / "site" / "public" / "figures"


def blocks(parts: tuple[str, ...] | str) -> list[dict[str, str]]:
    if isinstance(parts, str):
        chunks = [parts]
    else:
        chunks = list(parts)
    out: list[dict[str, str]] = []
    for part in chunks:
        text = part.strip()
        if not text:
            continue
        if text.startswith("F: "):
            out.append({"type": "formula", "text": text[3:].strip()})
        elif text.startswith("SAY: "):
            out.append({"type": "say", "text": text[5:].strip()})
        else:
            out.append({"type": "p", "text": text})
    return out


def example_json(example: Example) -> dict:
    return {
        "kind": example.kind,
        "promptEn": example.prompt_en,
        "promptUz": example.prompt_uz,
        "gloss": example.gloss,
        "choices": [
            {"letter": letter, "en": en, "uz": uz} for letter, en, uz in example.choices
        ],
        "steps": [{"en": en, "uz": uz} for en, uz in example.steps],
        "answer": example.answer,
    }


def practice_public(item: Practice) -> dict:
    return {
        "promptEn": item.prompt_en,
        "promptUz": item.prompt_uz,
        "gloss": item.gloss,
    }


def lesson_json(lesson: Lesson, bank_rows: list[dict]) -> dict:
    return {
        "code": lesson.code,
        "titleEn": lesson.title_en,
        "titleUz": lesson.title_uz,
        "goalEn": lesson.goal_en,
        "goalUz": lesson.goal_uz,
        "prereqEn": lesson.prereq_en,
        "prereqUz": lesson.prereq_uz,
        "teacherEn": blocks(lesson.teacher_en),
        "teacherUz": blocks(lesson.teacher_uz),
        "explainEn": blocks(lesson.explain_en),
        "explainUz": blocks(lesson.explain_uz),
        "examples": [example_json(example) for example in lesson.examples],
        "mistakes": [{"en": mistake.en, "uz": mistake.uz} for mistake in lesson.mistakes],
        "practice": [practice_public(item) for item in lesson.practice],
        "bank": bank_rows,
        "figure": lesson.figure,
        "figureCaptionEn": lesson.figure_caption_en,
        "figureCaptionUz": lesson.figure_caption_uz,
        "extras": list(lesson.extras),
    }


def unit_json(unit: Unit, public_bank: dict[str, list[dict]]) -> dict:
    return {
        "code": unit.code,
        "titleEn": unit.title_en,
        "titleUz": unit.title_uz,
        "introEn": blocks(unit.intro_en),
        "introUz": blocks(unit.intro_uz),
        "lessons": [
            lesson_json(lesson, public_bank.get(lesson.code, [])) for lesson in unit.lessons
        ],
    }


def mini_public(item: MiniItem) -> dict:
    return {
        "number": item.number,
        "domain": item.domain,
        "promptEn": item.prompt_en,
        "promptUz": item.prompt_uz,
        "choices": [
            {"letter": letter, "en": en, "uz": uz} for letter, en, uz in item.choices
        ],
    }


def mini_check(item: MiniItem) -> dict:
    """The answer spec the site's checker grades a typed mini-test answer against."""
    check = item.checks[0]
    if check.kind == "system2":
        return c_pair(check.x, check.y)
    if check.kind == "eq" and "π" in item.answer:
        return c_pi(sp.simplify(sp.sympify(check.right) / sp.pi))
    if check.kind in ("value", "solve"):
        return c_num(check.expected, percent=item.answer.endswith("%"))
    raise ValueError(f"mini {item.number}: no answer spec for check kind {check.kind}")


def formula_tables() -> list[dict]:
    tables = []
    for block in formula_sheet():
        if block.kind == "table":
            tables.append(
                {
                    "headers": list(block.headers),
                    "rows": [list(row) for row in block.rows],
                }
            )
    return tables


def export_site(*, render_figures: bool = True) -> tuple[Path, Path]:
    if render_figures:
        make_figures()
    enriched, public_bank, lesson_keys = build_public_and_keys(UNITS)
    payload = {
        "units": [unit_json(unit, public_bank) for unit in enriched],
        "glossary": [{"en": en, "uz": uz, "hint": hint} for en, uz, hint in GLOSSARY],
        "formulaTables": formula_tables(),
        "mini": [mini_public(item) for item in MINI],
    }
    keys_payload = {
        "lessons": lesson_keys,
        "mini": [
            {
                "number": item.number,
                "answer": item.answer,
                "analysisEn": item.analysis_en,
                "analysisUz": item.analysis_uz,
                "check": mini_check(item),
            }
            for item in MINI
        ],
    }
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    KEYS_PATH.write_text(json.dumps(keys_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # The site shows vector figures. PNGs stay in guide/assets for the Word book.
    PUBLIC_FIGURES.mkdir(parents=True, exist_ok=True)
    for stale in PUBLIC_FIGURES.glob("*.png"):
        stale.unlink()
    for image in sorted(ASSET_DIR.glob("*.svg")):
        shutil.copyfile(image, PUBLIC_FIGURES / image.name)
    return DATA_PATH, KEYS_PATH


if __name__ == "__main__":
    guide_path, keys_path = export_site()
    print(f"Wrote {guide_path}")
    print(f"Wrote {keys_path}")
