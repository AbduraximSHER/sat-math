"""Build the teacher Word book and the six printable unit files."""

from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

from guide.figures import make_figures
from guide.model import Lesson, MiniItem, Prose, Unit
from guide.verify import self_test_matcher, verify_book

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ASSETS = ROOT / "guide" / "assets"

NAVY = RGBColor(0x1B, 0x3A, 0x4B)
TEAL = RGBColor(0x0F, 0x6E, 0x6B)
GOLD = RGBColor(0x8C, 0x6A, 0x2F)
INK = RGBColor(0x1F, 0x29, 0x33)
MUTED = RGBColor(0x5C, 0x6B, 0x73)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

PAGE_WIDTH = 17.6  # cm of text on A4 with 1.7 cm margins


def _rgb(hex_color: str) -> str:
    return hex_color


def _shade(cell, hex_color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shade = OxmlElement("w:shd")
    shade.set(qn("w:val"), "clear")
    shade.set(qn("w:fill"), hex_color)
    tc_pr.append(shade)


def _borders(cell, color: str, sz: str = "4", left_sz: str | None = None, left_color: str | None = None) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), left_sz if edge == "left" and left_sz else sz)
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), left_color if edge == "left" and left_color else color)
        borders.append(node)
    tc_pr.append(borders)


def _cell_margins(cell, dxa: int = 120) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    margins = OxmlElement("w:tcMar")
    for edge in ("top", "left", "bottom", "right"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:w"), str(dxa if edge in ("left", "right") else 80))
        node.set(qn("w:type"), "dxa")
        margins.append(node)
    tc_pr.append(margins)


def _set_run_font(run, name: str = "Calibri") -> None:
    run.font.name = name
    r_pr = run._element.get_or_add_rPr()
    fonts = r_pr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        r_pr.append(fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), name)


def _add_text(paragraph, text: str, *, size=11.5, bold=False, italic=False, color=INK, space_after=8):
    paragraph.paragraph_format.space_after = Pt(space_after)
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.12
    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.color.rgb = color
    _set_run_font(run)
    return run


def _label(container, text: str, color) -> None:
    paragraph = container.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(10)
    paragraph.paragraph_format.space_after = Pt(2)
    _add_text(paragraph, text, size=10.5, bold=True, color=color, space_after=2)


def _body_chunks(container, chunks: tuple[str, ...] | str) -> None:
    if isinstance(chunks, str):
        parts = [part.strip() for part in chunks.split("\n\n") if part.strip()]
    else:
        parts = [part.strip() for part in chunks if part.strip()]
    for part in parts:
        if part.startswith("F: "):
            paragraph = container.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.space_before = Pt(4)
            paragraph.paragraph_format.space_after = Pt(4)
            _add_text(paragraph, part[3:].strip(), size=13, italic=False, color=NAVY, space_after=4)
            continue
        if part.startswith("SAY: "):
            _box(container, [part[5:].strip()], fill="F3FAF9", border="0F6E6B", left="0F6E6B", left_sz="16")
            continue
        paragraph = container.add_paragraph()
        _add_text(paragraph, part)


def _bilingual(container, en: tuple[str, ...] | str, uz: tuple[str, ...] | str) -> None:
    _label(container, "ENGLISH", NAVY)
    _body_chunks(container, en)
    _label(container, "O'ZBEKCHA", TEAL)
    _body_chunks(container, uz)


def _box(container, paragraphs: list[str], *, fill: str, border: str, left: str, left_sz: str = "16", label: str = "", label_color=NAVY) -> None:
    table = container.add_table(rows=1, cols=1)
    table.autofit = False
    _fixed(table, PAGE_WIDTH)
    cell = table.cell(0, 0)
    _shade(cell, fill)
    _borders(cell, border, sz="4", left_sz=left_sz, left_color=left)
    _cell_margins(cell, 140)
    cell.text = ""
    first = True
    if label:
        paragraph = cell.paragraphs[0]
        first = False
        _add_text(paragraph, label, size=10.5, bold=True, color=label_color, space_after=4)
    for text in paragraphs:
        paragraph = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        if text.startswith("F: "):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            _add_text(paragraph, text[3:], size=12, color=NAVY, space_after=4)
        else:
            _add_text(paragraph, text, size=11, space_after=4)
    container.add_paragraph().paragraph_format.space_after = Pt(4)


def _fixed(table, width_cm: float) -> None:
    tbl_pr = table._tbl.tblPr
    width = OxmlElement("w:tblW")
    width.set(qn("w:w"), str(int(width_cm / 2.54 * 1440)))
    width.set(qn("w:type"), "dxa")
    tbl_pr.append(width)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)


def _bottom_rule(paragraph, color: str = "C4A35A", size: str = "12") -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    p_pr.append(borders)


def _page_number(paragraph) -> None:
    run = paragraph.add_run()
    _set_run_font(run)
    run.font.size = Pt(9)
    run.font.color.rgb = MUTED

    def _field(kind: str) -> OxmlElement:
        node = OxmlElement("w:fldChar")
        node.set(qn("w:fldCharType"), kind)
        return node

    run._r.append(_field("begin"))
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    run._r.append(instr)
    run._r.append(_field("end"))


def _apply_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11.5)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.12
    for style_name, size, color, before, after in (
        ("Heading 1", 22, NAVY, 0, 8),
        ("Heading 2", 16, TEAL, 0, 6),
        ("Heading 3", 13, NAVY, 12, 4),
    ):
        style = doc.styles[style_name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.color.rgb = color
        style.font.bold = True
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)


def _new_doc() -> Document:
    doc = Document()
    _apply_styles(doc)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.7)
    section.right_margin = Cm(1.7)
    section.top_margin = Cm(1.8)
    section.bottom_margin = Cm(1.7)
    section.header_distance = Cm(0.55)
    section.footer_distance = Cm(0.45)
    section.different_first_page_header_footer = True

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _add_text(header, "SAT Math   ·   O'qituvchi qo'llanmasi", size=9, color=NAVY, space_after=2)
    _bottom_rule(header, "C4A35A", "8")

    footer = section.footer.paragraphs[0]
    footer.paragraph_format.tab_stops.add_tab_stop(Cm(PAGE_WIDTH), WD_TAB_ALIGNMENT.RIGHT)
    _add_text(footer, "O'qituvchi nusxasi\t", size=9, color=MUTED, space_after=0)
    _page_number(footer)

    core = doc.core_properties
    core.title = "SAT Math — O'qituvchi qo'llanmasi"
    core.subject = "Digital SAT Math teacher guide in English and Uzbek"
    core.category = "Teacher guide"
    core.comments = (
        "Original classroom lessons from fraction operations through Digital SAT Math. "
        "Not a College Board publication."
    )
    return doc


def _heading(doc: Document, text: str, level: int):
    paragraph = doc.add_heading(text, level=level)
    for run in paragraph.runs:
        _set_run_font(run)
        run.font.color.rgb = NAVY if level != 2 else TEAL
    if level == 2:
        _bottom_rule(paragraph, "D7E6E4", "10")
    return paragraph


def _title_page(doc: Document, *, kicker: str, title: str, subtitle_en: str, subtitle_uz: str, foot: str) -> None:
    for _ in range(2):
        doc.add_paragraph()
    kicker_p = doc.add_paragraph()
    kicker_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _add_text(kicker_p, kicker, size=12, bold=True, color=TEAL, space_after=8)
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _add_text(title_p, title, size=36, bold=True, color=NAVY, space_after=4)
    rule = doc.add_paragraph()
    rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _add_text(rule, " ", size=6, space_after=2)
    _bottom_rule(rule, "C4A35A", "18")
    for text, size, color in (
        (subtitle_en, 16, INK),
        (subtitle_uz, 16, TEAL),
    ):
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _add_text(paragraph, text, size=size, color=color, space_after=4)
    doc.add_paragraph()
    for line in foot.split("\n"):
        foot_p = doc.add_paragraph()
        foot_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _add_text(foot_p, line if line else " ", size=11, color=MUTED, space_after=2)
    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _add_text(
        note,
        "Original lessons. Not affiliated with the College Board.",
        size=10,
        italic=True,
        color=MUTED,
        space_after=2,
    )


def _render_prose(doc: Document, blocks: tuple[Prose, ...]) -> None:
    for block in blocks:
        if block.kind == "h1":
            _heading(doc, block.text, 1)
        elif block.kind == "h2":
            _heading(doc, block.text, 2)
        elif block.kind == "pair":
            _bilingual(doc, (block.text,), (block.text_uz,))
        elif block.kind == "en":
            _body_chunks(doc, (block.text,))
        elif block.kind == "table":
            _table(doc, block.headers, block.rows)
        elif block.kind == "contents":
            _contents_from_units(doc)
        else:
            raise ValueError(block.kind)


def _table(doc: Document, headers: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> None:
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.autofit = False
    _fixed(table, PAGE_WIDTH)
    width = PAGE_WIDTH / len(headers)
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        _shade(cell, "1B3A4B")
        _cell_margins(cell, 80)
        cell.text = ""
        _add_text(cell.paragraphs[0], header, size=10, bold=True, color=WHITE, space_after=2)
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = table.rows[r + 1].cells[c]
            if r % 2 == 1:
                _shade(cell, "F7F4EC")
            _cell_margins(cell, 80)
            _borders(cell, "E4DDD0", sz="4")
            cell.text = ""
            _add_text(cell.paragraphs[0], value, size=10, color=INK, space_after=2)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def _contents_from_units(doc: Document) -> None:
    from guide.content import UNITS

    for unit in UNITS:
        paragraph = doc.add_paragraph()
        _add_text(paragraph, f"{unit.code}-bo'lim.  {unit.title_uz}", size=12, bold=True, color=NAVY, space_after=2)
        sub = doc.add_paragraph()
        _add_text(sub, unit.title_en, size=11, italic=True, color=TEAL, space_after=2)
        for lesson in unit.lessons:
            line = doc.add_paragraph()
            line.paragraph_format.left_indent = Cm(0.6)
            _add_text(
                line,
                f"Dars {lesson.code}    {lesson.title_uz}  /  {lesson.title_en}",
                size=11,
                space_after=2,
            )


def _render_lesson(doc: Document, lesson: Lesson) -> None:
    doc.add_page_break()
    _heading(doc, f"Dars {lesson.code}.  {lesson.title_uz}", 2)
    en_title = doc.add_paragraph()
    _add_text(en_title, lesson.title_en, size=12, italic=True, color=MUTED, space_after=8)

    _heading(doc, "Maqsad  /  Goal", 3)
    _bilingual(doc, (lesson.goal_en,), (lesson.goal_uz,))

    _heading(doc, "Oldindan bilishi kerak  /  Already in place", 3)
    _bilingual(doc, (lesson.prereq_en,), (lesson.prereq_uz,))

    _heading(doc, "O'qituvchi yo'li  /  Teacher path", 3)
    _bilingual(doc, lesson.teacher_en, lesson.teacher_uz)

    _heading(doc, "Tushuntirish  /  Explanation", 3)
    _bilingual(doc, lesson.explain_en, lesson.explain_uz)

    if lesson.figure:
        path = ASSETS / f"{lesson.figure}.png"
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run()
        run.add_picture(str(path), width=Cm(lesson.figure_width_cm))
        caption = doc.add_paragraph()
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _add_text(caption, lesson.figure_caption_en, size=10, italic=True, color=MUTED, space_after=1)
        caption_uz = doc.add_paragraph()
        caption_uz.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _add_text(caption_uz, lesson.figure_caption_uz, size=10, italic=True, color=TEAL, space_after=8)

    if "error_log" in lesson.extras:
        _error_log(doc)

    for index, example in enumerate(lesson.examples, start=1):
        kind = "Foundation" if example.kind == "foundation" else "SAT uslubi  /  SAT-style"
        _heading(doc, f"Misol {index}  —  {kind}", 3)
        paragraphs = [example.prompt_en, example.prompt_uz]
        if example.gloss:
            paragraphs.append("So'zlar  /  Words:  " + example.gloss)
        if example.choices:
            for letter, en, uz in example.choices:
                paragraphs.append(f"{letter}.  {en}    /    {uz}")
        if example.kind == "sat":
            _box(doc, paragraphs, fill="FBF7EF", border="E4D3A8", left="C4A35A", label="SAVOL  /  QUESTION", label_color=GOLD)
        else:
            _box(doc, paragraphs, fill="F4F8F8", border="D5E4E3", left="0F6E6B", label="SAVOL  /  QUESTION", label_color=TEAL)
        for step_index, (step_en, step_uz) in enumerate(example.steps, start=1):
            paragraph = doc.add_paragraph()
            _add_text(paragraph, f"{step_index}.  {step_en}", size=11.5, space_after=1)
            uz = doc.add_paragraph()
            uz.paragraph_format.left_indent = Cm(0.5)
            _add_text(uz, step_uz, size=11.5, color=TEAL, space_after=4)
        answer = doc.add_paragraph()
        _add_text(answer, "Javob  /  Answer:  " + example.answer, size=12, bold=True, color=NAVY, space_after=6)

    _heading(doc, "Tez-tez uchraydigan xatolar  /  Mistakes that come back", 3)
    for index, mistake in enumerate(lesson.mistakes, start=1):
        paragraph = doc.add_paragraph()
        _add_text(paragraph, f"{index}.  {mistake.en}", space_after=1)
        uz = doc.add_paragraph()
        uz.paragraph_format.left_indent = Cm(0.5)
        _add_text(uz, mistake.uz, color=TEAL, space_after=4)

    _heading(doc, "Mashq  /  Practice", 3)
    note = doc.add_paragraph()
    _add_text(
        note,
        "Javoblar shu darsning oxiridagi kulrang blokda. O'quvchiga berishdan oldin o'sha blokni yopib qo'ying.",
        size=10.5,
        italic=True,
        color=MUTED,
        space_after=6,
    )
    for index, item in enumerate(lesson.practice, start=1):
        paragraph = doc.add_paragraph()
        _add_text(paragraph, f"{index}.  {item.prompt_en}", space_after=1)
        uz = doc.add_paragraph()
        uz.paragraph_format.left_indent = Cm(0.45)
        _add_text(uz, item.prompt_uz, color=TEAL, space_after=1)
        if item.gloss:
            gloss = doc.add_paragraph()
            gloss.paragraph_format.left_indent = Cm(0.45)
            _add_text(gloss, "So'zlar:  " + item.gloss, size=10, italic=True, color=MUTED, space_after=4)

    bank_note = doc.add_paragraph()
    _add_text(
        bank_note,
        "Qo'shimcha 100 ta tekshirilgan mashq (oson / o'rta / SAT) hamroh saytda shu dars sahifasida. Chop etilgan kitobdagi beshta mashq — sinf uchun qisqa to'plam.",
        size=10.5,
        italic=True,
        color=MUTED,
        space_after=2,
    )
    bank_note_en = doc.add_paragraph()
    _add_text(
        bank_note_en,
        "Another 100 checked items (easy / medium / SAT) live on the companion site for this lesson. The five above are the short classroom set.",
        size=10.5,
        italic=True,
        color=MUTED,
        space_after=6,
    )

    key_lines = ["O'qituvchi kaliti  /  Teacher key", "Misollar yuqorida to'liq yechilgan. Bu yerda faqat mashq."]
    for index, item in enumerate(lesson.practice, start=1):
        key_lines.append(f"{index}.  {item.answer}")
        key_lines.append(item.solution_en)
        key_lines.append(item.solution_uz)
    _box(doc, key_lines, fill="F3EFE6", border="E4D9C4", left="8C6A2F", label_color=GOLD)


def _error_log(doc: Document) -> None:
    _heading(doc, "Xato daftari  /  Error log", 3)
    intro = doc.add_paragraph()
    _add_text(
        intro,
        "Shu jadvalni nusxa qiling. Har bir xato uchun bitta qator. Ertangi dars shu daftarning bir qatoridan boshlanadi.",
        space_after=4,
    )
    headers = ("Sana", "Mavzu", "Men nima qildim", "To'g'ri g'oya", "Qayta sana")
    blanks = tuple((" ", " ", " ", " ", " ") for _ in range(6))
    _table(doc, headers, blanks)


def _render_unit(doc: Document, unit: Unit, *, break_first: bool) -> None:
    if break_first:
        doc.add_page_break()
    _heading(doc, f"{unit.code}-bo'lim.  {unit.title_uz}", 1)
    sub = doc.add_paragraph()
    _add_text(sub, unit.title_en, size=13, italic=True, color=TEAL, space_after=8)
    _bilingual(doc, unit.intro_en, unit.intro_uz)
    for lesson in unit.lessons:
        _render_lesson(doc, lesson)


def _master_key(doc: Document, units: tuple[Unit, ...] | None = None) -> None:
    from guide.content import UNITS
    from guide.enrich import deepen_units

    book = units if units is not None else deepen_units(UNITS)

    doc.add_page_break()
    _heading(doc, "Barcha kalitlar  /  Master key", 1)
    paragraph = doc.add_paragraph()
    _add_text(
        paragraph,
        "Qisqa ko'z yugurtirish uchun. To'liq yechim o'sha darsning kulrang blokida.",
        space_after=8,
    )
    for unit in book:
        for lesson in unit.lessons:
            heading = doc.add_paragraph()
            _add_text(heading, f"Dars {lesson.code}.  {lesson.title_uz}", size=12, bold=True, color=NAVY, space_after=2)
            for index, example in enumerate(lesson.examples, start=1):
                line = doc.add_paragraph()
                _add_text(line, f"Misol {index}:  {example.answer}", size=11, space_after=1)
            for index, item in enumerate(lesson.practice, start=1):
                line = doc.add_paragraph()
                _add_text(line, f"{index}.  {item.answer}", size=11, space_after=1)


def _mini(doc: Document, items: tuple[MiniItem, ...]) -> None:
    doc.add_page_break()
    _heading(doc, "Yakuniy aralash mini-test  /  Mixed review", 1)
    _bilingual(
        doc,
        (
            "Twenty original questions, one sitting, no calculator required though a calculator is allowed. Give the class 35 minutes. The questions are in English on purpose. Photocopy from here through the last question, and stop before the analysis.",
            "This is not a scored practice test and it does not predict a scaled score. It tells you which domain still wobbles.",
        ),
        (
            "Yigirma original savol. Bir o'tirish, 35 daqiqa. Kalkulyator shart emas, lekin ruxsat etiladi. Savollar ataylab inglizcha. Shu yerdan oxirgi savolgacha nusxa oling va tahlil sahifasidan oldin to'xtang.",
            "Bu baholanadigan sinov emas va scaled ballni bashorat qilmaydi. Qaysi domen hali qaltisligini ko'rsatadi.",
        ),
    )
    for item in items:
        paragraph = doc.add_paragraph()
        _add_text(paragraph, f"{item.number}.  [{item.domain}]  {item.prompt_en}", space_after=1)
        uz = doc.add_paragraph()
        uz.paragraph_format.left_indent = Cm(0.45)
        _add_text(uz, item.prompt_uz, color=TEAL, space_after=2)
        for letter, en, uz_choice in item.choices:
            choice = doc.add_paragraph()
            choice.paragraph_format.left_indent = Cm(0.8)
            _add_text(choice, f"{letter}.  {en}    /    {uz_choice}", size=11, space_after=1)

    doc.add_page_break()
    _heading(doc, "Mini-test tahlili  /  Mini-test analysis", 1)
    for item in items:
        _box(
            doc,
            [
                f"{item.number}.  {item.answer}",
                item.analysis_en,
                item.analysis_uz,
            ],
            fill="F3EFE6",
            border="E4D9C4",
            left="8C6A2F",
        )


def _glossary(doc: Document) -> None:
    from guide.content.glossary import GLOSSARY

    doc.add_page_break()
    _heading(doc, "Atamalar  /  Glossary", 1)
    paragraph = doc.add_paragraph()
    _add_text(
        paragraph,
        "Shu so'zlar butun kitobda bir xil. Yangi dars yozsangiz, yangi atama o'ylab topmang — avval shu ro'yxatga qarang.",
        space_after=8,
    )
    rows = tuple((en, uz, hint) for en, uz, hint in GLOSSARY)
    _table(doc, ("English", "O'zbekcha", "Eslatma"), rows)


def build_full(path: Path, units: tuple[Unit, ...] | None = None) -> None:
    from guide.content import MINI, UNITS, front_matter, formula_sheet
    from guide.enrich import deepen_units

    book = units if units is not None else deepen_units(UNITS)
    doc = _new_doc()
    _title_page(
        doc,
        kicker="DIGITAL SAT   ·   CLASSROOM GUIDE",
        title="SAT MATH",
        subtitle_en="Teacher guide",
        subtitle_uz="O'qituvchi qo'llanmasi",
        foot="Kasr amallaridan raqamli SAT Math bo'limigacha\nFrom fraction operations to the full math section\n\n44 lessons  ·  100 practice items each on the site  ·  English and Uzbek",
    )
    _render_prose(doc, front_matter())
    for unit in book:
        _render_unit(doc, unit, break_first=True)
    _render_prose(doc, formula_sheet())
    _glossary(doc)
    _master_key(doc, book)
    _mini(doc, MINI)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)


def build_unit_file(unit: Unit, path: Path) -> None:
    doc = _new_doc()
    _title_page(
        doc,
        kicker=f"{unit.code}-BO'LIM",
        title=unit.title_uz,
        subtitle_en=unit.title_en,
        subtitle_uz="O'qituvchi nusxasi  ·  javoblar dars oxirida",
        foot="To'liq kitob: SAT-Math-Teacher-Guide.docx",
    )
    _render_unit(doc, unit, break_first=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)


UNIT_FILES = {
    "0": "01-asos.docx",
    "1": "01-asos.docx",
    "2": "02-algebra.docx",
    "3": "03-advanced-math.docx",
    "4": "04-malumot-tahlili.docx",
    "5": "05-geometriya.docx",
    "6": "06-imtihon-hunari.docx",
}


def build_sections(units: tuple[Unit, ...] | None = None) -> None:
    from guide.content import UNITS
    from guide.enrich import deepen_units

    book = units if units is not None else deepen_units(UNITS)
    grouped: dict[str, list[Unit]] = {}
    for unit in book:
        grouped.setdefault(UNIT_FILES[unit.code], []).append(unit)
    for filename, units in grouped.items():
        if len(units) == 1:
            build_unit_file(units[0], DIST / filename)
            continue
        doc = _new_doc()
        _title_page(
            doc,
            kicker="01-BO'LIM",
            title="Asos",
            subtitle_en="The bridge and number sense",
            subtitle_uz="Ko'prik va son hissi",
            foot="Kasr tasdig'i shu faylning birinchi darsi. To'liq kitob: SAT-Math-Teacher-Guide.docx",
        )
        for index, unit in enumerate(units):
            _render_unit(doc, unit, break_first=True)
        doc.save(DIST / filename)


def main() -> int:
    from guide.content import MINI, UNITS
    from guide.enrich import deepen_units

    book = deepen_units(UNITS)
    self_test_matcher()
    errors = verify_book(book, MINI)
    if errors:
        print(f"{len(errors)} check(s) failed:", file=sys.stderr)
        for error in errors:
            print(" -", error, file=sys.stderr)
        return 1
    # The practice bank is generated and rechecked before anything is written.
    from guide.bank import build_bank

    try:
        bank = build_bank()
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    figures = make_figures()
    missing = [
        lesson.figure
        for unit in book
        for lesson in unit.lessons
        if lesson.figure and lesson.figure not in figures
    ]
    if missing:
        print("missing figures:", missing, file=sys.stderr)
        return 1
    build_full(DIST / "SAT-Math-Teacher-Guide.docx", book)
    build_sections(book)
    from guide.export_site import export_site

    export_site(render_figures=False, bank=bank)
    print(f"Wrote {DIST / 'SAT-Math-Teacher-Guide.docx'}")
    for name in dict.fromkeys(UNIT_FILES.values()):
        print(f"Wrote {DIST / name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
