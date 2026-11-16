"""Lesson 0.1 — confirm the four operations, then mixed numbers and signs."""

from guide.model import Example, Lesson, Mistake, Practice, Unit, value

LESSON = Lesson(
    code="0.1",
    title_en="Fraction fluency, mixed numbers, and signs",
    title_uz="Kasr malakasi, aralash kasr va ishora",
    goal_en="Confirm the four fraction operations and extend them to mixed numbers and negative fractions, because every later SAT topic still uses this arithmetic.",
    goal_uz="Kasrning to'rt amalini mustahkamlab, aralash kasr va manfiy kasrga o'tkazish. Keyingi har bir SAT mavzusi shu hisobga tayanadi.",
    prereq_en="Students can add, subtract, multiply, and divide positive fractions with a common denominator or a reciprocal.",
    prereq_uz="O'quvchilar musbat kasrlarni umumiy maxraj yoki teskari kasr yordamida qo'sha, ayira, ko'paytira va bo'la oladi.",
    teacher_en=(
        "Open with 1/2 + 1/3 and no help. Watch who adds the denominators and lands on 2/5. Put 2 1/4 on the board and have the class turn it into ninths-wait, into fourths, before any new rule. Do Example 1 yourself while they copy. Only then show one negative fraction and the sign of a product.",
        "SAY: Avval kasrni bir xil ko'rinishga keltiramiz. Aralash kasr — yashiringan yig'indi. Manfiy ishora qo'shishda ham, ko'paytirishda ham o'z qoidasiga ega. SAT javobni ko'pincha qisqartirilgan kasrda kutadi.",
        "Practice 1–3 is classwork. Practice 4 and 5 go home. Tomorrow, start from whichever of those two came back wrong.",
    ),
    teacher_uz=(
        "Darsni yordamsiz 1/2 + 1/3 dan boshlang. Kim maxrajlarni qo'shib 2/5 chiqarayotganini kuzating. Doskaga 2 1/4 yozing va yangi qoidadan oldin uni to'rtdan birlarga aylantirishni so'rang. 1-misolni o'zingiz yeching, ular ko'chirsin. Shundan keyin bitta manfiy kasr va ko'paytmaning ishorasini ko'rsating.",
        "SAY: Avval kasrni bir xil ko'rinishga keltiramiz. Aralash kasr — yashiringan yig'indi. Manfiy ishora qo'shishda ham, ko'paytirishda ham o'z qoidasiga ega. SAT javobni ko'pincha qisqartirilgan kasrda kutadi.",
        "1–3-mashqlar sinfda. 4 va 5 uyga. Ertaga o'sha ikkisidan qaytib kelgan xatodan boshlang.",
    ),
    explain_en=(
        "A fraction is a division written as a pair. a/b means a ÷ b, and b is never zero. The numerator counts how many parts you have. The denominator names the size of each part. This class already runs the four operations. Today we lock the form of those operations and add the two shapes the SAT hides inside later questions: mixed numbers and negative fractions.",
        "F: a/b + c/d = (ad + bc) / bd",
        "F: a/b − c/d = (ad − bc) / bd",
        "F: a/b × c/d = (a·c) / (b·d)",
        "F: a/b ÷ c/d = a/b × d/c",
        "Any common denominator is legal. The least one keeps the numbers smaller, which matters when a later question already has large denominators. Cancel a common factor before you multiply, while the numbers are still small. Division is not a new operation. Dividing by c/d means multiplying by the reciprocal d/c. The reciprocal of 3/5 is 5/3. Zero still has no reciprocal, so you never flip a fraction whose numerator is zero.",
        "A mixed number is a sum in disguise. 2 1/4 means 2 + 1/4, which is 8/4 + 1/4 = 9/4. Convert to an improper fraction before you multiply or divide. For addition you may add the whole numbers and the fraction parts separately and then carry, but conversion fails less often while speed is still being built. A negative fraction carries one minus sign. Park it on the numerator and write −2/5, not a minus on both floors. The sign rules, which the next lesson will earn properly, are only a tool today: two negatives in a product or a quotient give a positive, one negative gives a negative, and adding a negative moves the result down the number line.",
        "The SAT almost never asks a naked drill such as 'add these two fractions' with nothing around them. The same arithmetic sits inside a percent, a ratio, an equation, or an area formula. If this step is slow, a later question feels hard when the idea was easy. Leave answers in lowest terms. 6/8 is not finished; 3/4 is. An improper fraction such as 29/12 is a fine answer. A mixed number is also fine unless the stem asks for something else. On a student-produced response, 29/12 and 2.416 with a bar, or the decimal 2.4166..., are not all equally convenient: give the fraction.",
    ),
    explain_uz=(
        "Kasr — bo'linishning juft ko'rinishi. a/b degani a ÷ b, va b hech qachon nol bo'lmaydi. Surat qo'lingizdagi bo'laklarni sanaydi. Maxraj har bir bo'lakning o'lchamini aytadi. Bu sinf to'rt amalni bajara oladi. Bugun o'sha amallarning yozuvini qotirib qo'yamiz va SAT keyinroq savol ichiga yashiradigan ikki ko'rinishni qo'shamiz: aralash kasr va manfiy kasr.",
        "F: a/b + c/d = (ad + bc) / bd",
        "F: a/b − c/d = (ad − bc) / bd",
        "F: a/b × c/d = (a·c) / (b·d)",
        "F: a/b ÷ c/d = a/b × d/c",
        "Har qanday umumiy maxraj joiz. Eng kichigi sonlarni mayda saqlaydi. Bu keyingi savolda maxrajlar allaqachon katta bo'lganda muhim. Ko'paytirishdan oldin, sonlar hali kichik ekan, umumiy ko'paytuvchini qisqartiring. Bo'lish yangi amal emas. c/d ga bo'lish — teskari kasr d/c ga ko'paytirish demak. 3/5 ning teskarisi 5/3. Nolning teskarisi yo'q, shuning uchun surati nol bo'lgan kasrni ag'darmang.",
        "Aralash kasr — niqoblangan yig'indi. 2 1/4 degani 2 + 1/4, ya'ni 8/4 + 1/4 = 9/4. Ko'paytirish va bo'lishdan oldin noto'g'ri kasrga o'ting. Qo'shishda butun qismlarni alohida, kasr qismlarni alohida qo'shib, so'ng eltkizish mumkin, lekin tezlik hali qurilayotganda aylantirish kamroq xato beradi. Manfiy kasrda bitta minus bor. Uni suratga qo'ying va −2/5 deb yozing, ikkala qavatga ham minus qo'ymang. Ishora qoidalari keyingi darsda to'liq o'rin oladi, bugun esa qurol sifatida: ko'paytma yoki bo'linmada ikki minus musbat beradi, bitta minus manfiy beradi, manfiyni qo'shish natijani son o'qida pastga suradi.",
        "SAT deyarli hech qachon 'shu ikki kasrni qo'shing' deb yalang'och so'ramaydi. Xuddi shu hisob foizning, nisbatning, tenglamaning yoki yuza formulasining ichida o'tiradi. Bu qadam sekin bo'lsa, keyingi savol g'oyasi oson bo'lsa ham qiyin tuyuladi. Javobni oxirigacha qisqartiring. 6/8 tugagan emas, 3/4 tugagan. 29/12 kabi noto'g'ri kasr yaxshi javob. Aralash son ham yaxshi, agar savol boshqasini so'ramasa. O'quvchi o'zi yozadigan javobda kasr o'nli kasrdan qulayroq: 29/12 ni bering.",
    ),
    examples=(
        Example(
            kind="foundation",
            prompt_en="Compute 2 1/4 + 1/6. Give the answer as a simplified improper fraction.",
            prompt_uz="2 1/4 + 1/6 ni hisoblang. Javobni qisqartirilgan noto'g'ri kasrda yozing.",
            gloss="mixed number — aralash kasr; simplified — qisqartirilgan; improper fraction — noto'g'ri kasr",
            steps=(
                ("Convert the mixed number first: 2 1/4 = 8/4 + 1/4 = 9/4.", "Avval aralash kasrni aylantiring: 2 1/4 = 8/4 + 1/4 = 9/4."),
                ("The denominators are 4 and 6. Their least common multiple is 12.", "Maxrajlar 4 va 6. Eng kichik umumiy karrali 12."),
                ("9/4 = 27/12 and 1/6 = 2/12.", "9/4 = 27/12 va 1/6 = 2/12."),
                ("27/12 + 2/12 = 29/12. 29 and 12 share no common factor greater than 1.", "27/12 + 2/12 = 29/12. 29 va 12 ning 1 dan katta umumiy bo'luvchisi yo'q."),
            ),
            answer="29/12",
            checks=value("(9/4)+(1/6)", "29/12"),
        ),
        Example(
            kind="sat",
            prompt_en="Three fourths of a number is 18. What is one half of the number?",
            prompt_uz="Bir sonning to'rtdan uchi 18 ga teng. Shu sonning yarmi nechaga teng?",
            gloss="of — ning; a number — bir son; one half — yarmi",
            choices=(
                ("A", "6", "6"),
                ("B", "12", "12"),
                ("C", "18", "18"),
                ("D", "24", "24"),
            ),
            steps=(
                ("Translate the first sentence: (3/4) of the number is 18, so (3/4)x = 18.", "Birinchi gapni tarjima qiling: sonning 3/4 qismi 18, demak (3/4)x = 18."),
                ("Dividing by 3/4 means multiplying by 4/3. x = 18 × 4/3 = 24.", "3/4 ga bo'lish — 4/3 ga ko'paytirish. x = 18 × 4/3 = 24."),
                ("The question asks for half of the number, not the number. (1/2) × 24 = 12.", "Savol sonning o'zini emas, yarmini so'raydi. (1/2) × 24 = 12."),
                ("D is the whole number. C is the given piece, 18. A is 18 × 1/3, a third of the given piece, not half of the number.", "D — sonning o'zi. C — berilgan bo'lak, 18. A — 18 × 1/3, berilgan bo'lakning uchdan biri, sonning yarmi emas."),
            ),
            answer="B. 12",
            checks=value("(1/2)*(18*(4/3))", "12"),
        ),
    ),
    mistakes=(
        Mistake(
            en="Adding the denominators: 1/2 + 1/3 is not 2/5. The parts are different sizes. Common denominator first, and 1/2 + 1/3 = 5/6.",
            uz="Maxrajlarni qo'shish: 1/2 + 1/3 bu 2/5 emas. Bo'laklar har xil o'lchamda. Avval umumiy maxraj, va 1/2 + 1/3 = 5/6.",
        ),
        Mistake(
            en="Forgetting to flip when dividing. 7/8 ÷ 1/2 is not 7/16. It is 7/8 × 2/1 = 7/4. The second fraction turns over.",
            uz="Bo'lishda ag'darishni unutish. 7/8 ÷ 1/2 bu 7/16 emas. U 7/8 × 2/1 = 7/4. Ikkinchi kasr ag'dariladi.",
        ),
        Mistake(
            en="Dropping the sign on a mixed number. −2 1/2 means −(2 + 1/2) = −5/2. It is not −2 + 1/2, and it is not −3/2.",
            uz="Aralash kasrning ishorasini tushirib qoldirish. −2 1/2 degani −(2 + 1/2) = −5/2. U −2 + 1/2 emas va −3/2 ham emas.",
        ),
    ),
    practice=(
        Practice(
            prompt_en="Compute 5/6 − 1/4. Give a simplified fraction.",
            prompt_uz="5/6 − 1/4 ni hisoblang. Qisqartirilgan kasr yozing.",
            gloss="subtract — ayirish; simplified fraction — qisqartirilgan kasr",
            answer="7/12",
            solution_en="Common denominator 12: 5/6 = 10/12 and 1/4 = 3/12. 10/12 − 3/12 = 7/12.",
            solution_uz="Umumiy maxraj 12: 5/6 = 10/12 va 1/4 = 3/12. 10/12 − 3/12 = 7/12.",
            checks=value("(5/6)-(1/4)", "7/12"),
        ),
        Practice(
            prompt_en="Compute 2/3 × 9/4. Simplify before you multiply if you can.",
            prompt_uz="2/3 × 9/4 ni hisoblang. Iloji bo'lsa, ko'paytirishdan oldin qisqartiring.",
            answer="3/2",
            solution_en="Cancel a 3: (2/1) × (3/4) = 6/4 = 3/2. Or 2/3 × 9/4 = 18/12 = 3/2.",
            solution_uz="3 ni qisqartiring: (2/1) × (3/4) = 6/4 = 3/2. Yoki 2/3 × 9/4 = 18/12 = 3/2.",
            checks=value("(2/3)*(9/4)", "3/2"),
        ),
        Practice(
            prompt_en="Compute 7/8 ÷ 1/2 and give the answer as a simplified fraction.",
            prompt_uz="7/8 ÷ 1/2 ni hisoblang va javobni qisqartirilgan kasrda yozing.",
            gloss="divide — bo'lish",
            answer="7/4",
            solution_en="Dividing by 1/2 means multiplying by 2/1. So 7/8 × 2/1 = 14/8, which simplifies to 7/4.",
            solution_uz="1/2 ga bo'lish — 2/1 ga ko'paytirish demak. Shuning uchun 7/8 × 2/1 = 14/8, bu 7/4 ga qisqaradi.",
            checks=value("(7/8)/(1/2)", "7/4"),
        ),
        Practice(
            prompt_en="Compute −2/5 + 3/10.",
            prompt_uz="−2/5 + 3/10 ni hisoblang.",
            answer="-1/10",
            solution_en="Rewrite −2/5 with denominator 10: −2/5 = −4/10. Then −4/10 + 3/10 = −1/10. The sign stays negative because 4 tenths is larger than 3 tenths.",
            solution_uz="−2/5 ni maxraji 10 bo'lgan ko'rinishga keltiring: −2/5 = −4/10. So'ng −4/10 + 3/10 = −1/10. 4 o'ndan 3 o'ndan katta bo'lgani uchun ishora manfiy qoladi.",
            checks=value("(-2/5)+(3/10)", "-1/10"),
        ),
        Practice(
            prompt_en="Compute 3 1/2 × 2/5. Give a simplified improper fraction.",
            prompt_uz="3 1/2 × 2/5 ni hisoblang. Qisqartirilgan noto'g'ri kasr yozing.",
            gloss="improper fraction — noto'g'ri kasr",
            answer="7/5",
            solution_en="Convert first: 3 1/2 = 7/2. Then 7/2 × 2/5 = 7/5, because the factor 2 cancels. 7 and 5 share no further common factor.",
            solution_uz="Avval aylantiring: 3 1/2 = 7/2. So'ng 7/2 × 2/5 = 7/5, chunki 2 qisqaradi. 7 va 5 ning boshqa umumiy bo'luvchisi yo'q.",
            checks=value("(7/2)*(2/5)", "7/5"),
        ),
    ),
)

UNIT = Unit(
    code="0",
    title_en="The bridge",
    title_uz="Ko'prik",
    intro_en=(
        "One lesson, on purpose. The class already owns the four operations. This hour confirms the form, adds mixed numbers and a negative sign, and stops. Do not reteach a month of fractions. If the five problems come back clean, start Lesson 1.1 the next day.",
    ),
    intro_uz=(
        "Ataylab bitta dars. Sinf to'rt amalni allaqachon biladi. Bu soat yozuvni tasdiqlaydi, aralash kasr va manfiy ishorani qo'shadi va to'xtaydi. Kasrni bir oy qayta o'qitmang. Besh mashq toza qaytsa, ertaga 1.1-darsdan boshlang.",
    ),
    lessons=(LESSON,),
)
