"""The full teacher book, in teaching order."""

from guide.content.mini import MINI
from guide.content.u0_bridge import UNIT as UNIT0
from guide.content.u1a import LESSONS as FOUNDATIONS_A
from guide.content.u1b import LESSONS as FOUNDATIONS_B
from guide.content.u2_algebra import LESSONS as ALGEBRA
from guide.content.u3a import LESSONS as ADVANCED_A
from guide.content.u3b import LESSONS as ADVANCED_B
from guide.content.u4_data import LESSONS as DATA
from guide.content.u5_geometry import LESSONS as GEOMETRY
from guide.content.u6_craft import LESSONS as CRAFT
from guide.content.front import formula_sheet, front_matter
from guide.model import Unit

UNIT1 = Unit(
    code="1",
    title_en="Foundations: number sense",
    title_uz="Asos: son hissi",
    intro_en=(
        "Ten lessons on the arithmetic the SAT assumes and never reteaches: the number line, the order of operations, decimals, percent, ratio, proportion, exponents, roots, and scientific notation. A student who can compute these cleanly will recognize them later wearing algebra's clothes.",
        "Do not skip a lesson because it looks like school review. The English stem and the decimal point are part of the skill. If the five problems come back clean, move on the next day.",
    ),
    intro_uz=(
        "O'n dars, SAT biladi deb hisoblab, qayta o'qitmaydigan hisob: son o'qi, amallar tartibi, o'nli kasr, foiz, nisbat, proporsiya, daraja, ildiz va ilmiy yozuv. Bularni toza hisoblay olgan o'quvchi keyin ularni algebra kiyimida taniydi.",
        "Maktab takrori ko'ringani uchun darsni tashlab ketmang. Inglizcha savol va o'nli nuqta mahoratning qismi. Besh mashq toza qaytsa, ertaga oldinga o'ting.",
    ),
    lessons=FOUNDATIONS_A + FOUNDATIONS_B,
)

UNIT2 = Unit(
    code="2",
    title_en="Algebra",
    title_uz="Algebra",
    intro_en=(
        "Eight lessons for the largest domain: expressions, equations, fraction equations, inequalities, sentences, slope, systems, and f(x). The equations are short. The translation and the last noun are where points are lost.",
    ),
    intro_uz=(
        "Eng katta domen uchun sakkiz dars: ifoda, tenglama, kasrli tenglama, tengsizlik, gap, qiyalik, sistema va f(x). Tenglamalar qisqa. Ochko tarjima va oxirgi otda yo'qoladi.",
    ),
    lessons=ALGEBRA,
)

UNIT3 = Unit(
    code="3",
    title_en="Advanced Math",
    title_uz="Yuqori matematika",
    intro_en=(
        "Eight lessons on polynomials, factoring, quadratics, parabolas, equivalent expressions, rational expressions, radicals, and exponential change. Equivalent expressions are the heart of this domain. A rewrite that keeps the exceptions is the skill.",
    ),
    intro_uz=(
        "Sakkiz dars: ko'phad, ajratish, kvadrat, parabola, teng kuchli ifoda, ratsional ifoda, radikal va eksponensial o'zgarish. Teng kuchli ifodalar shu domenning yuragi. Istisnolarni saqlagan qayta yozish — mahorat.",
    ),
    lessons=ADVANCED_A + ADVANCED_B,
)

UNIT4 = Unit(
    code="4",
    title_en="Problem-Solving and Data Analysis",
    title_uz="Masala yechish va ma'lumot tahlili",
    intro_en=(
        "Six lessons on ratios in a story, tables, the four summaries, scatterplots, probability, and what a sample with a margin of error can actually support. The arithmetic is the percent and fraction work from the foundations. The new skill is reading the situation.",
    ),
    intro_uz=(
        "Olti dars: hikoyadagi nisbat, jadval, to'rt xulosa, sochilma diagramma, ehtimollik va xato chegarali tanlanma haqiqatan nimani ko'tara olishi. Hisob — asosdagi foiz va kasr. Yangi mahorat — vaziyatni o'qish.",
    ),
    lessons=DATA,
)

UNIT5 = Unit(
    code="5",
    title_en="Geometry and Trigonometry",
    title_uz="Geometriya va trigonometriya",
    intro_en=(
        "Seven lessons on angles, similar triangles, right triangles, sine cosine and tangent, area, volume, and circles. Several formulas are on the reference sheet. The lesson is knowing which length is the height, the radius, or the opposite side.",
    ),
    intro_uz=(
        "Yetti dars: burchak, o'xshash uchburchak, to'g'ri burchakli uchburchak, sinus kosinus va tangens, yuza, hajm va aylana. Bir necha formula varaqada. Dars — qaysi uzunlik balandlik, radius yoki qarama-qarshi tomon ekanini bilish.",
    ),
    lessons=GEOMETRY,
)

UNIT6 = Unit(
    code="6",
    title_en="Test craft",
    title_uz="Imtihon hunari",
    intro_en=(
        "Four lessons on the shape of the section, the English of the stems, when the hand is the right tool and when Desmos is, and the error log. These lessons assume the content is underway. They do not replace it.",
    ),
    intro_uz=(
        "To'rt dars: bo'limning shakli, savol iboralarining inglizchasi, qo'l qachon to'g'ri qurol va Desmos qachon, hamda xato daftari. Bu darslar mazmun ketayotganini taxmin qiladi. Ular mazmunning o'rnini bosmaydi.",
    ),
    lessons=CRAFT,
)

UNITS = (UNIT0, UNIT1, UNIT2, UNIT3, UNIT4, UNIT5, UNIT6)

__all__ = ["MINI", "UNITS", "formula_sheet", "front_matter"]
