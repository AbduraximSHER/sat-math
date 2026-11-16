"""Extra teaching depth appended to every lesson explanation.

These blocks sit after the core explain text. They keep the bilingual
rhythm: English first in the EN stream, Uzbek first in the UZ stream.
"""

from __future__ import annotations

# code -> (english paragraphs, uzbek paragraphs)
DEPTH: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "0.1": (
        (
            "When two fractions share a sign change, rewrite both with a common denominator before you decide which is larger. Crossing numerators alone fails when the denominators carry different signs.",
            "SAY: Keep the LCD as a written scaffold until the student no longer needs it. Erase it only after three clean problems in a row.",
            "On the Digital SAT a fraction answer is almost always simplified. Leave an unreduced form only when the stem asks for an equivalent expression, not a value.",
        ),
        (
            "Ikki kasrda ishora o'zgarsa, qaysi kattaroqligini aytishdan oldin ikkalasini umumiy maxrajga keltiring. Maxrajlar turli ishorali bo'lsa, faqat suratlarni solishtirish xato.",
            "SAY: Umumiy maxrajni o'quvchi uchta toza misolgacha yozib tursin. Keyin o'chiring.",
            "Raqamli SAT da kasr javob deyarli har doim qisqartiriladi. Qisqartirilmagan shakl faqat ekvivalent ifoda so'ralganda qoladi, qiymat so'ralganda emas.",
        ),
    ),
    "1.1": (
        (
            "Absolute value is distance, not 'drop the minus.' |a − b| and |b − a| are the same number; the order inside only changes the sign of the expression before the bars swallow it.",
            "On a number-line stem, mark both points first. The length of the segment is the absolute value; the direction is not.",
            "SAY: Ask out loud: distance from what to what? If the student cannot name both endpoints, they are not ready to compute.",
        ),
        (
            "Modul — masofa, 'minusni tashlash' emas. |a − b| va |b − a| bir xil son; ichidagi tartib faqat chiziqlar yutgunga qadar ifodaning ishorasini o'zgartiradi.",
            "Son o'qi savolida avval ikkala nuqtani belgilang. Kesma uzunligi — modul; yo'nalish emas.",
            "SAY: Baland ovozda so'rang: qayerdan qayergacha masofa? O'quvchi ikkala uchini ayta olmasa, hisoblashga hali erta.",
        ),
    ),
    "1.2": (
        (
            "Order of operations is a reading skill before it is a computing skill. Circle every grouping symbol, then every exponent, then decide whether multiplication and division run left to right.",
            "A fraction bar is a grouping symbol for the whole numerator and the whole denominator. Do those stacks completely before you divide.",
            "SAY: Force one rewrite with parentheses inserted where the student claims the order lives. Wrong parentheses reveal the misconception.",
        ),
        (
            "Amallar tartibi avval o'qish mahorati, keyin hisob. Har bir guruhlash belgisini aylana qiling, so'ng darajani, keyin ko'paytirish va bo'lish chapdan o'ngga ketishini tekshiring.",
            "Kasr chizig'i — butun surat va butun maxraj uchun guruhlash. Bo'lishdan oldin ikkala ustunni to'liq hisoblang.",
            "SAY: O'quvchi tartib bor deb o'ylagan joyga qavs qo'yib qayta yozdiring. Noto'g'ri qavs xato g'oyani ochadi.",
        ),
    ),
    "1.3": (
        (
            "Converting a terminating decimal is place-value work: 0.375 is 375/1000, then cancel. A repeating decimal needs the geometric series idea or the 9s / 99s / 999s pattern — only the short patterns appear on the SAT.",
            "When a stem mixes a decimal and a fraction, convert both to the same form before you add. Mixing forms mid-step is how signs and place values drift.",
            "SAY: Have the student say the place name out loud: tenths, hundredths, thousandths. Naming the place prevents 0.4 → 4/100.",
        ),
        (
            "Tugaydigan o'nli kasrni aylantirish — xona qiymati: 0.375 bu 375/1000, so'ng qisqartirish. Takrorlanuvchi o'nli kasr uchun 9 / 99 / 999 qoidasi yetadi — SAT da uzun qatorlar chiqmaydi.",
            "Savolda o'nli kasr va oddiy kasr aralashsa, qo'shishdan oldin ikkalasini bir xil shaklga keltiring. O'rtada aralashtirish ishora va xona qiymatini yo'qotadi.",
            "SAY: O'quvchi xona nomini baland aytisin: o'nlik, yuzlik, minglik. Nomlash 0.4 → 4/100 xatosini to'sadi.",
        ),
    ),
    "1.4": (
        (
            "Percent is a fraction with denominator 100 wearing a percent sign. Translating 'p percent of n' as (p/100)×n is the whole skill; the rest is arithmetic.",
            "F: p% of n = (p/100)·n",
            "When the stem gives a percent and asks for a fraction of a fraction, convert the percent first, then multiply. Do not leave the % symbol inside an algebra step.",
        ),
        (
            "Foiz — maxraji 100 bo'lgan kasr, foiz belgisi bilan. 'n ning p foizi' ni (p/100)×n deb o'qish — butun mahorat; qolgani hisob.",
            "F: n ning p% i = (p/100)·n",
            "Savol foiz bersa va kasrdan kasr so'rasa, avval foizni aylantiring, so'ng ko'paytiring. Algebra qadamida % belgisini qoldirmang.",
        ),
    ),
    "1.5": (
        (
            "Percent change always divides by the original amount, not the new one. Successive percents multiply the growth factors; adding the percents is the trap the test writers love.",
            "F: new = original × (1 ± r/100)",
            "SAY: Write the factor 1.08 or 0.92 before you touch the calculator. The factor is the idea; the decimal is only the clothing.",
        ),
        (
            "Foiz o'zgarishi har doim eski qiymatga bo'linadi, yangisiga emas. Ketma-ket foizlar o'sish koeffitsientlarini ko'paytiradi; foizlarni qo'shish — tuzoq.",
            "F: yangi = eski × (1 ± r/100)",
            "SAY: Kalkulyatorga tegishdan oldin 1.08 yoki 0.92 koeffitsientini yozing. G'oya — koeffitsient; o'nli kasr — faqat kiyim.",
        ),
    ),
    "1.6": (
        (
            "A ratio a:b is the fraction a/b after you confirm the order matches the nouns. Unit rate puts 1 in the denominator of the thing you are pricing or timing.",
            "When units disagree (minutes vs hours, cents vs dollars), convert before you form the ratio. A correct fraction with wrong units is still wrong.",
            "SAY: Underline the two nouns in the stem. The left noun is the numerator until the sentence says otherwise.",
        ),
        (
            "Nisbat a:b — tartib otlarga mosligini tekshirgach a/b kasri. Birlik qiymat — baholayotgan yoki vaqtlayotgan narsaning maxrajida 1 turadi.",
            "Birliklar mos kelmasa (daqiqa–soat, tiyin–so'm), nisbat yasashdan oldin aylantiring. Noto'g'ri birlikdagi to'g'ri kasr ham noto'g'ri.",
            "SAY: Savoldagi ikkita otni chizing. Gap boshqacha demaguncha chap ot — surat.",
        ),
    ),
    "1.7": (
        (
            "A proportion is two equal ratios. Cross-multiplying is legal only after both ratios are set with matching noun order. Inverse proportion multiplies to a constant: xy = k.",
            "F: a/b = c/d  ⇒  ad = bc",
            "On word problems, write the blank as a variable in the same slot both times. Moving the blank mid-proportion flips the answer.",
            "SAY: Before cross-multiplying, read the two ratios aloud with their nouns. If the nouns do not line up, rebuild the proportion instead of forcing the arithmetic.",
        ),
        (
            "Proporsiya — ikkita teng nisbat. Chatishtirib ko'paytirish faqat ikkala nisbatda ot tartibi bir xil bo'lgach qonuniy. Teskari proporsiya ko'paytmasi doimiy: xy = k.",
            "F: a/b = c/d  ⇒  ad = bc",
            "Matnli masalada bo'shliqni har safar bir xil joydagi o'zgaruvchi qilib yozing. Bo'shliqni ko'chirish javobni ag'daradi.",
            "SAY: Chatishtirishdan oldin ikkala nisbatni otlari bilan baland o'qing. Otlar mos kelmasa, hisobni majburlamang — proporsiyani qayta quring.",
        ),
    ),
    "1.8": (
        (
            "Exponent rules rearrange multiplication of the same base. They do not move addition: a² + a³ is not a⁵. When bases differ, factor or rewrite before you combine.",
            "F: aᵐ·aⁿ = aᵐ⁺ⁿ ·  (aᵐ)ⁿ = aᵐⁿ ·  a⁰ = 1 (a ≠ 0)",
            "Negative exponents are reciprocals, not negative numbers. a⁻ⁿ = 1/aⁿ. Students who 'bring the minus down' fail every SAT item that uses them.",
        ),
        (
            "Daraja qoidalari bir xil asosning ko'paytmasini qayta tartiblaydi. Qo'shishni ko'chirmaydi: a² + a³ bu a⁵ emas. Asoslar turlicha bo'lsa, birlashtirishdan oldin ajrating yoki qayta yozing.",
            "F: aᵐ·aⁿ = aᵐ⁺ⁿ ·  (aᵐ)ⁿ = aᵐⁿ ·  a⁰ = 1 (a ≠ 0)",
            "Manfiy daraja — teskari son, manfiy son emas. a⁻ⁿ = 1/aⁿ. Minusni pastga tushiradigan o'quvchi shu mavzudagi har bir SAT savolida yiqiladi.",
        ),
    ),
    "1.9": (
        (
            "A square root asks for the non-negative number whose square is the radicand. √(a²) = |a|, not a, when a might be negative. On the SAT, domain restrictions hide inside radical equations.",
            "Simplifying √(72) = √(36·2) = 6√2 is factoring out perfect squares, not 'dividing by 2 under the root.'",
            "SAY: Before simplifying, ask whether the radicand is a perfect square, a product with a perfect square, or neither.",
        ),
        (
            "Kvadrat ildiz — kvadrati ildiz ostidagi songa teng bo'lgan manfiy bo'lmagan son. a manfiy bo'lishi mumkin bo'lsa √(a²) = |a|, a emas. SAT da soha cheklovi ildizli tenglamalarda yashirinadi.",
            "√(72) = √(36·2) = 6√2 — mukammal kvadratlarni ajratish, 'ildiz ostini 2 ga bo'lish' emas.",
            "SAY: Soddalashtirishdan oldin so'rang: ildiz osti mukammal kvadratmi, mukammal kvadrat ko'paytuvchilimi, yoki yo'qmi?",
        ),
    ),
    "1.10": (
        (
            "Scientific notation is a × 10ᵏ with 1 ≤ |a| < 10. Converting is sliding the decimal and counting the slides as the exponent. Units conversion is the same idea with a conversion factor of 1.",
            "When two scientific numbers multiply, multiply the leading factors and add the exponents, then renormalize if the leading factor leaves the [1, 10) window.",
            "SAY: Write the conversion factor as a fraction equal to 1, with the unwanted unit in the denominator. Cancel units like factors.",
        ),
        (
            "Ilmiy yozuv — a × 10ᵏ, bunda 1 ≤ |a| < 10. Aylantirish — o'nli nuqtani siljitish va siljishlar sonini daraja qilish. Birlik aylantirish — koeffitsienti 1 bo'lgan o'sha g'oya.",
            "Ikki ilmiy son ko'paytirilganda yetakchi omillarni ko'paytiring va darajalarni qo'shing, yetakchi [1, 10) dan chiqsa qayta normallang.",
            "SAY: Aylantirish koeffitsientini 1 ga teng kasr qilib yozing, keraksiz birlik maxrajda. Birliklarni omildek qisqartiring.",
        ),
    ),
    "2.1": (
        (
            "An expression is a noun, not a sentence. Distributing a negative sign flips every term inside the parentheses. Like terms share the exact same variable part, including exponents.",
            "SAY: Expand fully before you combine. Students who combine first invent false like terms.",
            "On the SAT, 'which expression is equivalent' often means distribute and collect, then match a choice. Work the algebra before you glance at the options.",
        ),
        (
            "Ifoda — ot, gap emas. Minus ishorasini tarqatish qavs ichidagi har bir hadning ishorasini o'zgartiradi. O'xshash hadlar o'zgaruvchi qismi, jumladan darajasi, bir xil bo'lgan hadlar.",
            "SAY: Birlashtirishdan oldin to'liq oching. Avval birlashtiradigan o'quvchi soxta o'xshash had yasaydi.",
            "SAT da 'qaysi ifoda teng kuchli' ko'pincha ochish va yig'ish, so'ng variantga moslash demak. Variantlarga qaramasdan avval algebrani qiling.",
        ),
    ),
    "2.2": (
        (
            "A linear equation balances two expressions. Whatever you do to one side, do to the other — including dividing by a negative, which flips an inequality but not an equation.",
            "Clear parentheses first, then collect variable terms on one side and constants on the other. Checking by substitution is mandatory for classroom practice; the SAT will not catch you, but the error log will.",
            "F: ax + b = c  ⇒  x = (c − b)/a  (a ≠ 0)",
        ),
        (
            "Chiziqli tenglama ikki ifodani muvozanatlaydi. Bir tomonga qilganingizni ikkinchisiga ham qiling — manfiyga bo'lish tenglamada ishorani o'zgartirmaydi, tengsizlikda o'zgartiradi.",
            "Avval qavslarni oching, so'ng o'zgaruvchili hadlarni bir tomonga, sonlarni ikkinchisiga yig'ing. Sinash majburiy; SAT ushlamaydi, lekin xato daftari ushlaydi.",
            "F: ax + b = c  ⇒  x = (c − b)/a  (a ≠ 0)",
        ),
    ),
    "2.3": (
        (
            "Fraction equations clear by multiplying through by the LCD of every denominator, including those that hide inside the variable terms. Cancel after multiplying, not before, if a denominator contains the variable.",
            "Always state the excluded value where a denominator would be zero. An algebraic solution that lands on an excluded value is not a solution.",
            "SAY: Write the LCD above the equation before you multiply. Students who skip that line drop a factor.",
        ),
        (
            "Kasrli tenglamalar har bir maxrajning, jumladan o'zgaruvchili maxrajlarning, UM Mini bilan ko'paytirib tozalanadi. Maxrajda o'zgaruvchi bo'lsa, ko'paytirishdan oldin emas, keyin qisqartiring.",
            "Maxraj nol bo'ladigan qiymatni doim yozing. Shu qiymatga tushgan algebra yechimi — yechim emas.",
            "SAY: Ko'paytirishdan oldin UM ni tenglama ustiga yozing. Shu qatorni tashlagan o'quvchi omilni yo'qotadi.",
        ),
    ),
    "2.4": (
        (
            "Inequalities keep the balance idea of equations, with one extra rule: multiplying or dividing by a negative reverses the inequality sign. Graph the solution on a number line when the stem asks for a graph or a compound description.",
            "Compound inequalities 'and' take the intersection; 'or' takes the union. Shade carefully — the endpoint open or closed is part of the answer.",
            "SAY: When you flip the sign, say 'because I divided by a negative' out loud. Ritual prevents silent flips that never happened.",
        ),
        (
            "Tengsizlik tenglama muvozanatini saqlaydi, bitta qo'shimcha qoida bilan: manfiyga ko'paytirish yoki bo'lish belgini ag'daradi. Savol grafik yoki qo'shma tavsif so'rasa, yechimni son o'qida chizing.",
            "Qo'shma tengsizlikda 'va' — kesishma; 'yoki' — birlashma. Uch ochiq yoki yopiqligi javobning qismi.",
            "SAY: Belgini ag'darganda 'chunki manfiyga bo'ldim' deb ayting. Marosim jim ag'darishni to'sadi.",
        ),
    ),
    "2.5": (
        (
            "Translate every English noun into a variable or an expression before you build the equation. 'Is' becomes equals; 'of' often becomes multiplication; 'less than' reverses the order of subtraction.",
            "Read the last noun in the question twice. Many SAT items solve for x correctly and then ask for 2x + 3. The algebra was fine; the target was wrong.",
            "SAY: Underline the quantity the question wants. Circle the quantity you will name x. They are not always the same.",
        ),
        (
            "Tenglama qurishdan oldin har bir inglizcha otni o'zgaruvchi yoki ifodaga aylantiring. 'Is' — tenglik; 'of' ko'pincha ko'paytirish; 'less than' ayirish tartibini ag'daradi.",
            "Savolning oxirgi otini ikki marta o'qing. Ko'p SAT savollari x ni to'g'ri topadi, lekin 2x + 3 ni so'raydi. Algebra yaxshi; nishon noto'g'ri.",
            "SAY: Savol so'rayotgan miqdorni chizing. x deb ataydigan miqdorni aylana qiling. Ular har doim bir xil emas.",
        ),
    ),
    "2.6": (
        (
            "Slope is rise over run between two points on the same line: m = (y₂ − y₁)/(x₂ − x₁). A vertical line has undefined slope; a horizontal line has slope 0. Those two sentences are separate traps.",
            "F: y − y₁ = m(x − x₁) ·  y = mx + b",
            "Parallel lines share slope; perpendicular lines have slopes that multiply to −1 (unless one is vertical). Read the stem for which relationship it wants before you compute.",
        ),
        (
            "Qiyalik — bir chiziqdagi ikki nuqta orasidagi ko'tarilishning yugurishga nisbati: m = (y₂ − y₁)/(x₂ − x₁). Vertikal chiziqda qiyalik aniqlanmagan; gorizontalda 0. Bu ikki gap alohida tuzoq.",
            "F: y − y₁ = m(x − x₁) ·  y = mx + b",
            "Parallel chiziqlar qiyalikni ulashadi; perpendikulyar chiziqlar qiyaliklari −1 ga ko'payadi (biri vertikal bo'lmasa). Hisoblashdan oldin savol qaysi munosabatni so'rashini o'qing.",
        ),
    ),
    "2.7": (
        (
            "A 2×2 linear system is two lines. Elimination and substitution both work; pick the one that cancels a variable with the least fractions. No solution means parallel distinct lines; infinitely many means the same line twice.",
            "On the SAT, a contextual system often asks for one variable only. Solve the system, then answer the noun in the question.",
            "SAY: Before substituting, decide which equation isolates more cleanly. The cleaner isolation prevents fraction storms.",
        ),
        (
            "2×2 chiziqli sistema — ikki chiziq. Eliminatsiya va o'rniga qo'yish ikkalasi ishlaydi; eng kam kasr bilan o'zgaruvchini yo'qotadiganini tanlang. Yechim yo'q — parallel turli chiziqlar; cheksiz — bir chiziq ikki marta.",
            "SAT da kontekstli sistema ko'pincha faqat bitta o'zgaruvchini so'raydi. Sistemani yeching, so'ng savoldagi otga javob bering.",
            "SAY: O'rniga qo'yishdan oldin qaysi tenglama tozaroq ajratishini tanlang. Toza ajratish kasr bo'ronini oldini oladi.",
        ),
    ),
    "2.8": (
        (
            "f(x) is a machine: input x, output the expression. f(3) means replace every x with 3. f(a + 1) means replace every x with the whole bundle a + 1 — use parentheses.",
            "A linear function has constant rate of change. If a table's successive differences in y over differences in x stay constant, the function is linear on that domain.",
            "SAY: Write 'replace x with …' as a spoken step the first week. The notation stops being magic when the replacement is audible.",
        ),
        (
            "f(x) — mashina: kirish x, chiqish ifoda. f(3) har bir x ni 3 bilan almashtirish. f(a + 1) har bir x ni butun a + 1 bog'lami bilan almashtirish — qavs ishlating.",
            "Chiziqli funksiyaning o'zgarish tezligi doimiy. Jadvalda y ning ketma-ket ayirmalari x ayirmalariga bo'linganda doimiy qolsa, shu sohada funksiya chiziqli.",
            "SAY: Birinchi hafta 'x ni … bilan almashtir' ni baland ayting. Almashtirish eshitilganda belgi sehr bo'lishdan toxtaydi.",
        ),
    ),
    "3.1": (
        (
            "A polynomial is a sum of terms aₙxⁿ with non-negative integer powers. Degree is the highest power with a non-zero coefficient. Adding polynomials merges like terms; multiplying uses distribution or a rectangle.",
            "SAY: Degree and leading coefficient are two different labels. Students conflate them when the leading term is not written first.",
            "On the SAT, 'what is the degree of the product' is often answerable without expanding: deg(fg) = deg(f) + deg(g) when both are non-zero.",
        ),
        (
            "Ko'phad — manfiy bo'lmagan butun darajali aₙxⁿ hadlar yig'indisi. Daraja — noli bo'lmagan koeffitsientli eng yuqori kuch. Qo'shish o'xshash hadlarni birlashtiradi; ko'paytirish tarqatish yoki to'rtburchak.",
            "SAY: Daraja va yetakchi koeffitsient — ikki xil yorliq. Yetakchi had birinchi yozilmasa, o'quvchilar ularni aralashtiradi.",
            "SAT da 'ko'paytmaning darajasi nima' ko'pincha ochmasdan javob beriladi: ikkalasi nol emas bo'lsa deg(fg) = deg(f) + deg(g).",
        ),
    ),
    "3.2": (
        (
            "Factoring undoes expanding. Always pull the greatest common factor first. Then look for difference of squares, trinomials, or grouping. Factoring completely means no factor of degree ≥ 1 still factors over the integers.",
            "F: x² − y² = (x − y)(x + y)",
            "SAY: After factoring, multiply back once. The thirty seconds of checking catch the sign errors that cost the point.",
        ),
        (
            "Ajratish — ochishning teskari ishi. Avval eng katta umumiy ko'paytuvchini chiqaring. So'ng kvadratlar ayirmasi, uchhad yoki guruhlashni qidiring. To'liq ajratish — butun sonlar ustida darajasi ≥ 1 bo'lgan omil endi ajralmasligi.",
            "F: x² − y² = (x − y)(x + y)",
            "SAY: Ajratgach, bir marta qayta ko'paytiring. O'ttiz soniyalik tekshiruv ochkoni olib ketadigan ishora xatolarini tutadi.",
        ),
    ),
    "3.3": (
        (
            "A quadratic equation ax² + bx + c = 0 yields zero, one, or two real roots. Factoring, completing the square, and the quadratic formula are three doors to the same room; pick the door the coefficients invite.",
            "F: x = (−b ± √(b² − 4ac))/(2a)",
            "The discriminant b² − 4ac tells the story before you finish: positive two reals, zero one real (double), negative no real roots. On the SAT, 'how many real solutions' is often a discriminant question in disguise.",
        ),
        (
            "Kvadrat tenglama ax² + bx + c = 0 nol, bir yoki ikki haqiqiy ildiz beradi. Ajratish, to'liq kvadrat va kvadrat formula — bir xonaga uch eshik; koeffitsientlar chorlaydiganini tanlang.",
            "F: x = (−b ± √(b² − 4ac))/(2a)",
            "Diskriminant b² − 4ac yakunlashdan oldin hikoyani aytadi: musbat — ikki haqiqiy, nol — bitta (qo'shaloq), manfiy — haqiqiy ildiz yo'q. SAT da 'nechta haqiqiy yechim' ko'pincha yashirin diskriminant savoli.",
        ),
    ),
    "3.4": (
        (
            "A parabola y = ax² + bx + c opens up when a > 0 and down when a < 0. The vertex is the turning point; its x-coordinate is −b/(2a). Axis of symmetry is the vertical line through the vertex.",
            "Vertex form y = a(x − h)² + k makes the vertex (h, k) obvious. Completing the square converts standard form into vertex form.",
            "SAY: Sketch a tiny parabola and mark the vertex before computing. The picture catches sign errors in −b/(2a).",
        ),
        (
            "Parabola y = ax² + bx + c a > 0 da yuqoriga, a < 0 da pastga ochiladi. Uch — burilish nuqtasi; uning x koordinatasi −b/(2a). Simmetriya o'qi — uchdan o'tuvchi vertikal chiziq.",
            "Uch shakli y = a(x − h)² + k uchni (h, k) qilib ko'rsatadi. To'liq kvadrat standart shaklni uch shakliga aylantiradi.",
            "SAY: Hisoblashdan oldin kichik parabola chizib uchni belgilang. Rasm −b/(2a) dagi ishora xatolarini tutadi.",
        ),
    ),
    "3.5": (
        (
            "Equivalent expressions agree for every allowed input. Expanding, factoring, and canceling common factors (with domain notes) are the main moves. An identity that fails at one point is not an identity.",
            "When choices look different, pick a safe test value (not 0, 1, or a root of a denominator) and evaluate. Matching values do not prove equivalence, but mismatching values kill a choice fast.",
            "SAY: State the domain whenever you cancel. The SAT loves choices that match except at the hole you canceled.",
        ),
        (
            "Teng kuchli ifodalar ruxsat etilgan har bir kirishda mos keladi. Ochish, ajratish va umumiy omillarni qisqartirish (soha eslatmasi bilan) asosiy harakatlar. Bitta nuqtada yiqilgan ayniyat — ayniyat emas.",
            "Variantlar turlicha ko'rinsa, xavfsiz sinov qiymati tanlang (0, 1 yoki maxraj ildizi emas) va hisoblang. Mos qiymatlar tenglikni isbotlamaydi, lekin nomoslik variantni tez o'ldiradi.",
            "SAY: Qisqartirganda sohani yozing. SAT siz qisqartirgan teshikdan boshqa joyda mos keladigan variantlarni yaxshi ko'radi.",
        ),
    ),
    "3.6": (
        (
            "A rational expression is a ratio of polynomials. Simplify by factoring and canceling common polynomial factors, never by canceling terms across a plus sign.",
            "A rational equation is cleared by multiplying by the LCD of the factored denominators, then checking every candidate against the excluded values.",
            "SAY: Factor every denominator before you name the LCD. Unfactored denominators hide the common pieces.",
        ),
        (
            "Ratsional ifoda — ko'phadlar nisbati. Soddalashtirish omillarga ajratib umumiy ko'phad omillarini qisqartirish bilan bo'ladi, qo'shimdagi hadlarni o'chirish bilan emas.",
            "Ratsional tenglama ajratilgan maxrajlarning UM si bilan ko'paytirib tozalanadi, so'ng har bir nomzod taqiqlangan qiymatlarga qarshi tekshiriladi.",
            "SAY: UM ni aytishdan oldin har bir maxrajni ajrating. Ajratilmagan maxrajlar umumiy bo'laklarni yashiradi.",
        ),
    ),
    "3.7": (
        (
            "Radical equations isolate the radical, then raise both sides to the matching power. Extraneous roots appear because squaring is not reversible on all reals — check every candidate in the original equation.",
            "Rational exponents rewrite roots: a^(m/n) = (ⁿ√a)^m. The denominator of the exponent is the root index; the numerator is the power.",
            "SAY: After raising both sides, write 'check in original' as its own line. Skipping the check is the most common full-credit miss.",
        ),
        (
            "Ildizli tenglamalar ildizni ajratadi, so'ng ikkala tomonni mos darajaga ko'taradi. Yot ildizlar paydo bo'ladi, chunki kvadratlash barcha haqiqiy sonlarda teskari emas — har bir nomzodni asl tenglamada tekshiring.",
            "Ratsional daraja ildizni qayta yozadi: a^(m/n) = (ⁿ√a)^m. Daraja maxraji — ildiz indeksi; surati — daraja.",
            "SAY: Ikkala tomonni ko'targach, 'aslda tekshir' ni alohida qator qilib yozing. Tekshiruvni tashlash — eng ko'p to'liq ochko yo'qotish.",
        ),
    ),
    "3.8": (
        (
            "Exponential change multiplies by a constant factor each period: A = A₀ · rᵗ. Linear change adds a constant. Reading which one the stem describes is half the item.",
            "A nonlinear system pairing a line and a parabola (or exponential) can have zero, one, or two solutions. Graphing in Desmos is legal and fast; still know the algebra so you can trust the picture.",
            "SAY: Name the growth factor before you plug in t. If the student says 'plus 5%' instead of 'times 1.05', stop and rebuild the model.",
        ),
        (
            "Eksponensial o'zgarish har davrda doimiy koeffitsientga ko'payadi: A = A₀ · rᵗ. Chiziqli o'zgarish doimiy qo'shadi. Savol qaysi birini tasvirlashini o'qish — savolning yarmi.",
            "Chiziq va parabola (yoki eksponensial) juftlashgan nochiziqli sistemada nol, bir yoki ikki yechim bo'lishi mumkin. Desmosda chizish qonuniy va tez; baribir algebrani biling — rasmga ishonish uchun.",
            "SAY: t ni qo'yishdan oldin o'sish koeffitsientini nomlang. O'quvchi '1.05 ga ko'paytirish' o'rniga '5% qo'shish' desa, to'xtating va modelni qayta quring.",
        ),
    ),
    "4.1": (
        (
            "Contextual ratios hide inside recipes, maps, mixtures, and rates. Write the nouns in the fraction before the numbers. A correct computation with swapped nouns is still wrong.",
            "Proportions in context obey the same cross-multiply rule, but units must cancel. Keep unit labels in the fraction until they cancel — they are part of the algebra.",
            "SAY: Cover the numbers and read only the nouns. If the student cannot say the ratio in words, they are not ready for the digits.",
        ),
        (
            "Kontekstdagi nisbatlar retsept, xarita, aralashma va tezlik ichida yashirinadi. Sonlardan oldin kasrga otlarni yozing. Otlar almashtirilgan to'g'ri hisob ham noto'g'ri.",
            "Kontekstdagi proporsiyalar o'sha chatishtirish qoidasiga bo'ysinadi, lekin birliklar qisqarishi kerak. Birlik yorliqlarini qisqarguncha kasrda saqlang — ular algebraning qismi.",
            "SAY: Sonlarni yoping va faqat otlarni o'qing. O'quvchi nisbatni so'zda ayta olmasa, raqamlarga hali erta.",
        ),
    ),
    "4.2": (
        (
            "Tables and graphs are compressed stories. Read the axis labels and the units before you read any number. A slope taken from a graph is rise/run in those units.",
            "When two rows of a table give a rate, use those two rows — do not invent a third. Extrapolation past the table needs an explicit model the stem must justify.",
            "SAY: Point with a finger to the exact cell or tick mark you will use. Vague pointing produces vague arithmetic.",
        ),
        (
            "Jadval va grafik — qisqargan hikoyalar. Har qanday songa qaraguncha o'q yorliqlari va birliklarni o'qing. Grafikdan olingan qiyalik — shu birliklardagi ko'tarilish/yugurish.",
            "Jadvalning ikki qatori tezlik bersa, o'sha ikkisini ishlating — uchinchisini o'ylab topmang. Jadvaldan tashqariga ekstrapolyatsiya uchun savol asoslagan aniq model kerak.",
            "SAY: Ishlatadigan katak yoki belgini barmoq bilan ko'rsating. Noaniq ko'rsatish noaniq hisob beradi.",
        ),
    ),
    "4.3": (
        (
            "Mean is the balance point (sum divided by count). Median is the middle after sorting. Mode is the most frequent value. Range is max minus min. Outliers pull the mean harder than the median.",
            "When a stem asks which measure changes, rebuild only that measure. Students who recompute everything waste time and introduce new errors.",
            "SAY: Sort the list on paper even when it 'looks sorted.' The median error is almost always an unsorted list.",
        ),
        (
            "O'rta arifmetik — muvozanat nuqtasi (yig'indi / soni). Mediana — tartiblangandan keyingi o'rta. Moda — eng ko'p uchraydigan. Qamrov — max minus min. Ajralib turuvchilar o'rtani medianaga qaraganda kuchliroq tortadi.",
            "Savol qaysi o'lchov o'zgarishini so'rasa, faqat shuni qayta hisoblang. Hammasini qayta qiladigan o'quvchi vaqt yo'qotadi va yangi xato kiritadi.",
            "SAY: Ro'yxat 'tartibli' ko'rinsa ham qog'ozda tartiblang. Mediana xatosi deyarli har doim tartiblanmagan ro'yxat.",
        ),
    ),
    "4.4": (
        (
            "A scatterplot shows association, not automatic causation. A line of best fit summarizes a linear trend; residual is actual y minus predicted y. Positive association rises together; negative falls as the other rises.",
            "Extrapolation beyond the cloud of points is weaker than interpolation inside it. The SAT often asks which claim the scatterplot supports — stay inside what the points show.",
            "SAY: Trace the cloud with a finger before you draw a fit line. The shape tells you whether a line is honest.",
        ),
        (
            "Sochilma diagramma bog'liqlikni ko'rsatadi, avtomatik sababni emas. Eng mos chiziq chiziqli tendentsiyani qisqacha ifodalaydi; qoldiq — haqiqiy y minus bashorat y. Musbat bog'liqlik birga o'sadi; manfiy biri o'sganda ikkinchisi kamayadi.",
            "Nuqtalar bulutidan tashqariga ekstrapolyatsiya ichidagi interpolatsiyadan zaifroq. SAT ko'pincha sochilma qaysi da'voni qo'llab-quvvatlashini so'raydi — nuqtalar ko'rsatganidan chiqmang.",
            "SAY: Mos chiziq chizishdan oldin bulutni barmoq bilan kuzating. Shakl chiziq rostgo'ymi yoki yo'qmi aytadi.",
        ),
    ),
    "4.5": (
        (
            "Probability of an event is favorable outcomes over total equally likely outcomes, when that model applies. Independent events multiply; mutually exclusive events add (and cannot both happen).",
            "F: P(A or B) = P(A) + P(B) − P(A and B)",
            "Conditional language ('given that') restricts the denominator to the given group. Re-read the table headers before you divide.",
        ),
        (
            "Hodisa ehtimolligi — model mos kelganda qulay natijalarning barcha teng ehtimolli natijalarga nisbati. Mustaqil hodisalar ko'payadi; bir-birini istisno qiluvchilar qo'shiladi (va ikkalasi birga bo'lmaydi).",
            "F: P(A yoki B) = P(A) + P(B) − P(A va B)",
            "Shartli til ('agar ... berilgan') maxrajni berilgan guruhga qisqartiradi. Bo'lishdan oldin jadval sarlavhalarini qayta o'qing.",
        ),
    ),
    "4.6": (
        (
            "A sample estimates a population; a margin of error sketches a plausible range around that estimate. Claims that leap from sample to 'every' or 'proves' go beyond what the data support.",
            "Larger random samples tend to shrink margin of error; biased samples do not become honest by growing. The SAT tests whether you notice the bias, not whether you compute a fancy interval.",
            "SAY: Rewrite the claim in one cautious sentence before judging it. Caution is the skill being scored.",
        ),
        (
            "Tanlanma populyatsiyani baholaydi; xato chegarasi shu baho atrofida ehtimoliy oralik chizadi. Tanlanmadan 'har bir' yoki 'isbotlaydi' ga sakragan da'volar ma'lumot ko'tara oladiganidan oshadi.",
            "Kattaroq tasodifiy tanlanmalar xato chegarasini kichraytirishga moyil; tarafkash tanlanma kattalashib rostgo'y bo'lmaydi. SAT tarafkashlikni sezishingizni sinaydi, murakkab interval hisoblashingizni emas.",
            "SAY: Da'voni baholashdan oldin ehtiyotkor bitta gap bilan qayta yozing. Ehtiyot — baholanayotgan mahorat.",
        ),
    ),
    "5.1": (
        (
            "Vertical angles are equal; adjacent angles on a straight line sum to 180°. When a transversal crosses parallel lines, corresponding and alternate interior angles match; consecutive interior angles are supplementary.",
            "SAY: Mark the parallel arrows on the diagram before you chase angles. Unmarked parallels are not parallels.",
            "On the SAT, a missing angle is often one equation away once you label every angle you know. Write the relation before you solve for the number.",
        ),
        (
            "Vertikal burchaklar teng; to'g'ri chiziqdagi qo'shni burchaklar yig'indisi 180°. Kesuvchi parallel chiziqlarni kesganda mos va almashinuvchi ichki burchaklar teng; ketma-ket ichki burchaklar qo'shimcha.",
            "SAY: Burchak quvguncha diagrammada parallel strelkalarni belgilang. Belgilanmagan parallellar — parallel emas.",
            "SAT da yetishmayotgan burchak ko'pincha bilgan burchaklaringizni yozgach bitta tenglama uzoqlikda. Sonni topishdan oldin munosabatni yozing.",
        ),
    ),
    "5.2": (
        (
            "Similar triangles have equal corresponding angles and proportional corresponding sides. AA is enough to prove similarity. The scale factor multiplies lengths; its square multiplies areas.",
            "Write the correspondence of vertices in order: △ABC ~ △DEF means A↔D, B↔E, C↔F. A wrong correspondence silently swaps sides.",
            "SAY: Trace the two triangles with different colors or hatch marks. Correspondence becomes visible when the shapes are marked.",
        ),
        (
            "O'xshash uchburchaklarning mos burchaklari teng, mos tomonlari proporsional. AA o'xshashlikni isbotlashga yetadi. Masshtab koeffitsienti uzunliklarni ko'paytiradi; uning kvadrati yuzalarni ko'paytiradi.",
            "Uchlar muvofiqligini tartibda yozing: △ABC ~ △DEF demak A↔D, B↔E, C↔F. Noto'g'ri muvofiqlik tomonlarni jim almashtiradi.",
            "SAY: Ikki uchburchakni turli rang yoki chiziqlar bilan belgilang. Shakllar belgilanganda muvofiqlik ko'rinadi.",
        ),
    ),
    "5.3": (
        (
            "In a right triangle, a² + b² = c² with c the hypotenuse. The 45-45-90 and 30-60-90 patterns are on the reference sheet — memorize the shape of the ratios so you recognize them without re-deriving.",
            "F: 45-45-90 → x : x : x√2 ·  30-60-90 → x : x√3 : 2x",
            "SAY: Identify the right angle first, then the hypotenuse. Students who square the wrong side invent a false Pythagorean triple.",
        ),
        (
            "To'g'ri burchakli uchburchakda a² + b² = c², c gipotenuza. 45-45-90 va 30-60-90 qoliplari varaqada — nisbatlar shaklini yodlang, qayta chiqarmasdan taniysiz.",
            "F: 45-45-90 → x : x : x√2 ·  30-60-90 → x : x√3 : 2x",
            "SAY: Avval to'g'ri burchakni, so'ng gipotenuzani toping. Noto'g'ri tomonni kvadratga olgan o'quvchi soxta Pifagor uchligini yasaydi.",
        ),
    ),
    "5.4": (
        (
            "In a right triangle, sine is opposite/hypotenuse, cosine adjacent/hypotenuse, tangent opposite/adjacent. SOH-CAH-TOA is a memory hook, not a substitute for labeling the sides relative to the angle in play.",
            "The angle matters: switching which acute angle you stand at swaps opposite and adjacent. Complementary angles swap sine and cosine.",
            "SAY: Draw a tiny altitude mark on the opposite side before writing the ratio. The picture locks the definition.",
        ),
        (
            "To'g'ri burchakli uchburchakda sinus — qarama-qarshi/gipotenuza, kosinus — yondosh/gipotenuza, tangens — qarama-qarshi/yondosh. SOH-CAH-TOA — yodlash ilgagi, ishlatilayotgan burchakka nisbatan tomonlarni belgilashning o'rnini bosmaydi.",
            "Burchak muhim: qaysi o'tmas burchakda turishingizni almashtirish qarama-qarshi va yondoshni almashtiradi. Komplementar burchaklar sinus va kosinusni almashtiradi.",
            "SAY: Nisbat yozishdan oldin qarama-qarshi tomonga kichik balandlik belgisini qo'ying. Rasm ta'rifni mahkamlaydi.",
        ),
    ),
    "5.5": (
        (
            "Area formulas live on the reference sheet, but the diagram decides which length is the base and which is the height. Height is perpendicular to the base you chose — not just 'the tall side.'",
            "Composite shapes split into rectangles, triangles, and circles you already know. Draw the split lines; do not invent a new formula for an L-shape.",
            "SAY: Write the name of the formula you will use before the numbers. Naming the tool prevents grabbing the wrong one.",
        ),
        (
            "Yuza formulalari varaqada, lekin diagramma qaysi uzunlik asos va qaysi balandlik ekanini hal qiladi. Balandlik tanlagan asosga perpendikulyar — shunchaki 'uzun tomon' emas.",
            "Murakkab shakllar allaqachon bilgan to'rtburchak, uchburchak va aylanalarga bo'linadi. Bo'lish chiziqlarini chizing; L-shakl uchun yangi formula o'ylab topmang.",
            "SAY: Sonlardan oldin ishlatadigan formula nomini yozing. Asbobni nomlash noto'g'risini olishni to'sadi.",
        ),
    ),
    "5.6": (
        (
            "Volume formulas also sit on the sheet. Prisms and cylinders are base area times height; pyramids and cones take one-third of that. Spheres use (4/3)πr³ — radius, not diameter, unless you convert.",
            "Units of volume are cubed. A stem that mixes cm and m needs a conversion before you cube a length.",
            "SAY: Circle whether the solid is prism-like or pyramid-like before you reach for 1/3. That binary choice is most of the item.",
        ),
        (
            "Hajm formulalari ham varaqada. Prisma va silindr — asos yuzasi × balandlik; piramida va konus — shuning uchdan biri. Sfera — (4/3)πr³; diametr emas, radius (aylantirmasangiz).",
            "Hajm birliklari kubda. sm va m aralashgan savolda uzunlikni kubga olishdan oldin aylantirish kerak.",
            "SAY: 1/3 ga qo'l uzatishdan oldin jism prisma tipimi yoki piramida tipimi aylana qiling. Shu ikkilik tanlov — savolning ko'p qismi.",
        ),
    ),
    "5.7": (
        (
            "Circle equations (x − h)² + (y − k)² = r² center at (h, k) with radius r. Arc length and sector area are fractions of the full circle given by the central angle over 360° (or 2π radians).",
            "F: arc = (θ/360)·2πr ·  sector = (θ/360)·πr²",
            "SAY: Convert the angle to a fraction of the circle before multiplying. Students who multiply by the angle in degrees invent nonsense units.",
            "When the stem gives a diameter, halve it before any area or arc formula. Using the diameter as if it were r doubles lengths and quadruples areas.",
        ),
        (
            "Aylana tenglamasi (x − h)² + (y − k)² = r² markaz (h, k), radius r. Yoy uzunligi va sektor yuzasi to'liq aylananing markaziy burchak / 360° (yoki 2π radian) kasridir.",
            "F: yoy = (θ/360)·2πr ·  sektor = (θ/360)·πr²",
            "SAY: Ko'paytirishdan oldin burchakni aylana kasriga aylantiring. Gradusdagi burchakka to'g'ridan-to'g'ri ko'paytirgan o'quvchi bema'ni birlik yasaydi.",
            "Savol diametr bersa, yuza yoki yoy formulasidan oldin uni ikkiga bo'ling. Diametrni r o'rniga ishlatish uzunlikni ikki, yuzani to'rt baravar qiladi.",
        ),
    ),
    "6.1": (
        (
            "The Digital SAT Math section is two equal modules with a short break structure built into the adaptive design. Timing is a resource: easy points first, marked skips second, stubborn algebra last inside a module.",
            "Desmos is available; it does not replace reading. A perfect graph of the wrong equation scores zero. Use the grid to check, not to avoid thinking.",
            "SAY: After a practice module, ask only one timing question: where did the clock actually hurt? Fix that slice next, not 'everything.'",
        ),
        (
            "Raqamli SAT Math bo'limi — adaptive tuzilmadagi ikki teng modul. Vaqt — resurs: avval oson ochkolar, keyin belgilangan o'tkazishlar, modul ichida qaysar algebra oxirida.",
            "Desmos bor; u o'qishning o'rnini bosmaydi. Noto'g'ri tenglamarning mukammal grafigi nol beradi. To'rni tekshirish uchun ishlating, o'ylashdan qochish uchun emas.",
            "SAY: Mashq modulidan keyin faqat bitta vaqt savolini bering: soat qayerda haqiqatan og'ritdi? Keyin 'hammasini' emas, o'sha bo'lakni tuzating.",
        ),
    ),
    "6.2": (
        (
            "SAT English hides the math target in ordinary nouns: 'how many more,' 'in terms of,' 'which could be,' 'closest to.' Translate the phrase before you touch algebra.",
            "Build a two-column habit: left side the English chunk, right side the math chunk. When the columns disagree, the student guessed.",
            "SAY: Make the student point to the exact words that become the equation. If they point at empty air, the stem was never read.",
        ),
        (
            "SAT inglizchasi matematik nishonni oddiy otlarda yashiradi: 'how many more,' 'in terms of,' 'which could be,' 'closest to.' Algebraga tegishdan oldin iborani tarjima qiling.",
            "Ikki ustun odati: chapda inglizcha bo'lak, o'ngda matematik bo'lak. Ustunlar mos kelmasa, o'quvchi taxmin qilgan.",
            "SAY: O'quvchi tenglamaga aylanadigan aniq so'zlarni ko'rsatsin. Bo'sh havoga ko'rsatasa, savol umuman o'qilmagan.",
        ),
    ),
    "6.3": (
        (
            "Hand work builds the model; Desmos checks or solves the graph you already named. Entering a cloud of points without an equation is not a strategy — it is hope.",
            "Good Desmos habits: one equation per line, zoom until the feature you care about fills the view, use a table when the stem gives discrete inputs.",
            "SAY: Require a handwritten equation before the laptop opens. The hand commits; the screen verifies.",
        ),
        (
            "Qo'l ishi modelni quradi; Desmos siz allaqachon nomlagan grafikni tekshiradi yoki yechadi. Tenglamasiz nuqtalar bulutini kiritish — strategiya emas, umid.",
            "Yaxshi Desmos odati: har qatorda bitta tenglama, sizni qiziqtirgan qism ekranni to'ldirguncha zum qiling, savol diskret kirish bersa jadval ishlating.",
            "SAY: Noutbuk ochilishidan oldin qo'lda yozilgan tenglamani talab qiling. Qo'l majburlaydi; ekran tasdiqlaydi.",
        ),
    ),
    "6.4": (
        (
            "Traps are reusable: wrong noun, unsimplified fraction, sign flip on inequality, canceled terms instead of factors, percent of the new instead of the old. The error log turns a trap into a named enemy.",
            "Each log row needs a date, a topic, what you did, the right idea, and a retest date. Without the retest date, the log is a diary, not a tool.",
            "SAY: Start the next lesson with one log row, not a new lecture. Repair beats coverage when the exam is near.",
        ),
        (
            "Tuzoqlar qayta ishlatiladi: noto'g'ri ot, qisqartirilmagan kasr, tengsizlikda ishora ag'darilishi, omil o'rniga hadlarni o'chirish, eski o'rniga yangining foizi. Xato daftari tuzoqni nomli dushmanga aylantiradi.",
            "Har bir qatorda sana, mavzu, nima qilganingiz, to'g'ri g'oya va qayta sinov sanasi bo'lishi kerak. Qayta sinov sanasisiz daftar — kundalik, asbob emas.",
            "SAY: Keyingi darsni yangi ma'ruza bilan emas, bitta daftar qatori bilan boshlang. Imtihon yaqinida tuzatish qamrovdan ustun.",
        ),
    ),
}


def depth_for(code: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    return DEPTH.get(code, ((), ()))
