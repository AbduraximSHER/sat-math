"""Extra teaching depth appended to every lesson explanation.

These blocks sit after the core explain text. They keep the bilingual
rhythm: English first in the EN stream, Uzbek first in the UZ stream.
"""

from __future__ import annotations

# code -> (english paragraphs, uzbek paragraphs)
DEPTH: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "1.6": (
        (
            "After the parts are named, write the whole as a sum before any multiplication. The board should show 2 + 3 = 5, then 2/5 × total — never jump straight to 2/3 × total.",
            "Map and recipe stems are the same scale factor in different clothes. Distance on map / map unit = real distance / real unit; cups / batch size stays constant.",
            "SAY: Underline the two nouns in the stem. Ask aloud: part-to-part, or part of the whole? The answer decides whether you divide by b or by a + b.",
        ),
        (
            "Ulushlar nomlangach, ko'paytirishdan oldin butunni yig'indi qilib yozing. Doskada 2 + 3 = 5, so'ng 2/5 × jami ko'rinsin — to'g'ridan-to'g'ri 2/3 × jami ga sakramang.",
            "Xarita va retsept savollari — turli kiyimdagi bir xil masshtab. Xaritadagi masofa / xarita birligi = haqiqiy masofa / haqiqiy birlik; stakan / partiya o'lchami doimiy.",
            "SAY: Savoldagi ikkita otni chizing. Baland so'rang: qism-qismmi, yoki butunning ulushimi? Javob b ga bo'lishni yoki a + b ga bo'lishni belgilaydi.",
        ),
    ),
}


def depth_for(code: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    return DEPTH.get(code, ((), ()))
