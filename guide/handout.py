"""One Word file per lesson: a one-page summary, then the full bilingual lesson.

    python3 -m guide.handout 1.7

writes dist/Dars-1.7.docx. Add a SUMMARIES entry to support another lesson.
"""

from __future__ import annotations

import sys
from pathlib import Path

from guide import build_guide as bg
from guide.content import UNITS
from guide.enrich import deepen_units
from guide.figures import make_figures

# Per lesson: ideas (name, rule), three quick examples (question, worked answer), traps.
SUMMARIES: dict[str, dict] = {
    "1.6": {
        "ideas": [
            ("Nisbat (ratio) a:b", "Ikki miqdorni ulushlar bilan solishtiradi. Tartib so'zlarga bo'ysunadi: 'mushuklarning itlarga nisbati 3:4' — mushuk/it = 3/4."),
            ("Butun va qism", "2:3 da jami 2 + 3 = 5 ulush. Birinchi guruh butunning 2/5 qismi, 2/3 emas. 2/3 — guruhni guruh bilan solishtirish."),
            ("Bitta ulush", "Avval bitta ulushni toping: berilgan miqdorni u qamragan ulushlar soniga bo'ling. Jami berilsa — barcha ulushlarga, farq berilsa — farqdagi ulushlarga."),
            ("Teng nisbatlar", "Ikkala sonni bir xil songa ko'paytirish yoki bo'lish nisbatni o'zgartirmaydi: 12:18 = 2:3. Avval birliklarni bir xil qiling: 30 daqiqa : 2 soat = 30:120 = 1:4."),
            ("Tezlik va birlik qiymat (rate, unit rate)", "Ikki xil birlik nisbati. Birlik qiymat — bitta birlikka to'g'ri keladigan miqdor. 'Per' (-ga, boshiga) maxrajdagi birlikni aytadi."),
            ("Masofa, tezlik, vaqt", "miqdor = tezlik × vaqt; vaqt = miqdor ÷ tezlik."),
            ("Birlikni almashtirish", "1 ga teng kasrga ko'paytiring: 60 km/soat × (1000 m / 1 km) × (1 soat / 60 daqiqa) = daqiqasiga 1000 m."),
        ],
        "examples": [
            ("30 o'quvchi, o'g'il : qiz = 2:3. O'g'il bolalar nechta?", "5 ulush. (2/5) × 30 = 12."),
            ("Qizil : ko'k = 5:2, qizil ko'kdan 15 ta ko'p. Ko'k nechta?", "Farq 3 ulush = 15, bitta ulush 5. Ko'k 2 × 5 = 10."),
            ("2.5 soatda 150 mil. Tezlik soatiga necha mil?", "150 ÷ 2.5 = 60."),
        ],
        "traps": [
            "2:3 ni butunning 2/3 qismi deb olish. To'g'risi: 2/5.",
            "'Soatiga mil' so'ralganda soatni milga bo'lish. 'Per' maxrajni aytadi: mil/soat.",
            "Turli birlikdan nisbat tuzish (30 daqiqa : 2 soat ≠ 30:2).",
            "Javobni noto'g'ri birlikda qoldirish: savol soat so'rasa, daqiqani soatga aylantiring.",
        ],
    },
    "1.7": {
        "ideas": [
            ("Proporsiya", "Ikki nisbat teng: a/b = c/d. Bir xil munosabat ikki o'lchamda."),
            ("Yechish", "Noma'lumni ajratish uchun ko'paytiring (3/4 = x/20 → x = 20 × 3/4 = 15) yoki diagonali bo'yicha ko'paytiring: ad = bc."),
            ("Tuzish tartibi", "Ikki tomonda birliklar bir xil joyda: stakan/kishi = stakan/kishi. Kichik jadval: ustun — birlik, qator — vaziyat."),
            ("Proporsiyami?", "Diagonal ko'paytmalar teng bo'lsa — ha: 6/9 va 8/12 → 72 = 72. 6/9 va 8/10 → 60 ≠ 72, yo'q."),
            ("To'g'ri proporsiya", "y = kx, y/x o'zgarmaydi. Biri ikki baravar oshsa, ikkinchisi ham. Grafik — (0, 0) dan o'tadigan to'g'ri chiziq."),
            ("Teskari proporsiya", "xy = k, ko'paytma o'zgarmaydi. Biri ikki baravar oshsa, ikkinchisi yarmiga tushadi: ko'proq ishchi — kamroq kun, tezroq — kamroq vaqt."),
            ("Qavs", "Surat yig'indi bo'lsa, qavsda saqlang: (x + 1)/4 = 6/8 → 8(x + 1) = 24 → x = 2."),
        ],
        "examples": [
            ("3/4 = x/20. x = ?", "x = 20 × 3/4 = 15."),
            ("4 bo'yoqchi ishni 10 kunda tugatadi. 5 bo'yoqchiga necha kun?", "Ish 4 × 10 = 40 bo'yoqchi-kun. 40 ÷ 5 = 8 kun."),
            ("y x ga teskari proporsional; x = 4 da y = 6. x = 8 da y = ?", "k = 4 × 6 = 24. y = 24 ÷ 8 = 3."),
        ],
        "traps": [
            "Diagonali bo'yicha noto'g'ri ko'paytirish: 3/4 = x/20 dan 3x = 80 emas, 4x = 60.",
            "Bo'lib bajariladigan ishga to'g'ri proporsiya qo'llash: ko'proq ishchiga kamroq kun kerak.",
            "Suratning faqat bir qismini ko'paytirish: 8(x + 1), 8x + 1 emas.",
            "Javob noto'g'ri tomonga o'zgarsa, proporsiya ag'darilgan yoki turi noto'g'ri.",
        ],
    },
}


def build(code: str) -> Path:
    if code not in SUMMARIES:
        raise SystemExit(f"No summary for lesson {code}. Add one to SUMMARIES in guide/handout.py.")
    lesson = next((l for unit in deepen_units(UNITS) for l in unit.lessons if l.code == code), None)
    if lesson is None:
        raise SystemExit(f"No lesson {code}.")
    summary = SUMMARIES[code]
    make_figures()

    doc = bg._new_doc()
    bg._title_page(
        doc,
        kicker=f"DARS {code}",
        title=lesson.title_uz,
        subtitle_en=lesson.title_en,
        subtitle_uz="Qisqa konspekt va batafsil dars",
        foot="1-qism: bir sahifalik qisqa konspekt\n2-qism: batafsil dars, misollar, xatolar va mashq (javoblar oxirida)",
    )

    doc.add_page_break()
    bg._heading(doc, "1-qism. Qisqacha", 2)
    intro = doc.add_paragraph()
    bg._add_text(intro, "Darsning asosiy g'oyalari bir sahifada. Doskaga yozish yoki uyga berish uchun.", italic=True, color=bg.MUTED)
    bg._table(doc, ("G'oya", "Qoida"), tuple(summary["ideas"]))

    bg._heading(doc, "Uch qisqa misol", 3)
    for question, answer in summary["examples"]:
        line = doc.add_paragraph()
        bg._add_text(line, question, bold=True, space_after=1)
        worked = doc.add_paragraph()
        worked.paragraph_format.left_indent = bg.Cm(0.5)
        bg._add_text(worked, "→ " + answer, color=bg.TEAL, space_after=5)

    traps = [f"{index}. {text}" for index, text in enumerate(summary["traps"], start=1)]
    bg._box(doc, traps, fill="FBF7EF", border="E4D3A8", left="C4A35A", label="TUZOQLAR", label_color=bg.GOLD)

    bg._render_lesson(doc, lesson)
    out = bg.DIST / f"Dars-{code}.docx"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    return out


if __name__ == "__main__":
    for code in sys.argv[1:] or sorted(SUMMARIES):
        print(f"Wrote {build(code)}")
