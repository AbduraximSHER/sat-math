"""Foundations 1.1–1.5: integers, operations, decimals, percent."""

from guide.model import Example, Lesson, Mistake, Practice, eq, order, value

L11 = Lesson(
    code="1.1",
    title_en="Integers, the number line, and absolute value",
    title_uz="Butun sonlar, son o'qi va modul",
    goal_en="Place integers, name an opposite, and read absolute value as distance from zero so later signed work has a picture.",
    goal_uz="Butun sonlarni joylashtirish, qarama-qarshi sonni aytish va modulni noldan uzoqlik sifatida o'qish. Keyingi ishorali ishlarning rasmi shu.",
    prereq_en="Students can compute with positive fractions. Negative fractions appeared once in the bridge lesson.",
    prereq_uz="O'quvchilar musbat kasrlar bilan hisoblay oladi. Manfiy kasr ko'prik darsida bir marta ko'rilgan.",
    teacher_en=(
        "Draw a number line from −5 to 5 before any definition. Ask where −3 lives, and which direction is negative. Then cover the absolute-value bars with your hand and ask what changed: the bars ask for a distance, and a distance has no sign.",
        "SAY: Modul — noldan qancha uzoqda ekaning. Uzoqlik manfiy bo'lmaydi. Qarama-qarshi son esa ishorani almashtiradi, masofani emas.",
        "Do the distance from −4 to 3 on the figure together. That is the SAT example. Practice 1–3 in class, 4 and 5 at home.",
    ),
    teacher_uz=(
        "Ta'rifdan oldin −5 dan 5 gacha son o'qini chizing. −3 qayerda turishini va manfiy tomon qaysi ekanini so'rang. So'ng modul chiziqlarini qo'lingiz bilan yoping va nima o'zgarganini so'rang: chiziqlar masofani so'raydi, masofaning ishorasi yo'q.",
        "SAY: Modul — noldan qancha uzoqda ekaning. Uzoqlik manfiy bo'lmaydi. Qarama-qarshi son esa ishorani almashtiradi, masofani emas.",
        "−4 dan 3 gacha masofani rasmda birga toping. Bu SAT misoli. 1–3 sinfda, 4 va 5 uyda.",
    ),
    explain_en=(
        "The integers are the whole numbers and their opposites, with zero between them: …, −3, −2, −1, 0, 1, 2, 3, …. On a number line the positives sit to the right of zero and the negatives sit to the left. Moving right means adding a positive. Moving left means adding a negative, which is subtraction.",
        "The opposite of a number is the same distance from zero on the other side. The opposite of −8 is 8. The opposite of 8 is −8. Zero is its own opposite. Taking the opposite flips the sign and leaves the size alone.",
        "F: |a| = distance from a to 0",
        "Absolute value is that distance, so it is never negative. |−3| = 3 and |3| = 3 and |0| = 0. The bars do not mean 'make it positive by deleting a minus you do not like.' They mean 'how far from zero.' Distance between two numbers is the absolute value of their difference, and the order inside does not matter: |3 − (−4)| and |(−4) − 3| are the same 7.",
        "A fraction still lives on this line. −1/2 is halfway between −1 and 0. The class already added a negative fraction; the new picture is why −4/10 + 3/10 landed at −1/10, closer to zero but still on the left. The SAT uses this in two quiet ways: a distance on a number line, and an expression such as |x − 2| that measures how far x is from 2. If a choice is negative and the question asked for a distance or an absolute value, that choice is finished before you compute.",
    ),
    explain_uz=(
        "Butun sonlar — natural sonlar, ularning qarama-qarshilari va o'rtadagi nol: …, −3, −2, −1, 0, 1, 2, 3, …. Son o'qida musbatlar nolning o'ngida, manfiylar chapida turadi. O'ngga yurish musbatni qo'shish. Chapga yurish manfiyni qo'shish, ya'ni ayirish.",
        "Qarama-qarshi son — noldan xuddi shu uzoqlikda, lekin narigi tomonda. −8 ning qarama-qarshisi 8. 8 ning qarama-qarshisi −8. Nol o'zining qarama-qarshisi. Qarama-qarshi olish ishorani almashtiradi, o'lchamni emas.",
        "F: |a| = a dan 0 gacha bo'lgan masofa",
        "Modul o'sha masofa, shuning uchun u manfiy bo'lmaydi. |−3| = 3, |3| = 3 va |0| = 0. Chiziqlar 'yoqmagan minusni o'chir' degani emas. Ular 'noldan qanchalik uzoq' degani. Ikki son orasidagi masofa ular ayirmasining moduli, ichidagi tartib esa muhim emas: |3 − (−4)| va |(−4) − 3| ikkalasi ham 7.",
        "Kasr ham shu o'qda yashaydi. −1/2 soni −1 va 0 ning o'rtasida. Sinf manfiy kasrni qo'shgan; yangi rasm — nima uchun −4/10 + 3/10 javobi −1/10 chiqqanini, nolga yaqinroq, lekin hali chapda. SAT buni ikki tinch joyda ishlatadi: son o'qidagi masofa va |x − 2| kabi ifoda, ya'ni x 2 dan qanchalik uzoq. Agar savol masofa yoki modul so'rasa va variant manfiy bo'lsa, u variant hisobdan oldin yiqiladi.",
    ),
    figure="number_line",
    figure_caption_en="A is at −4 and B is at 3. The distance is |3 − (−4)| = 7.",
    figure_caption_uz="A nuqta −4 da, B nuqta 3 da. Masofa |3 − (−4)| = 7.",
    examples=(
        Example(
            kind="foundation",
            prompt_en="Evaluate |−3| + |2| − |−1|.",
            prompt_uz="|-3| + |2| - |-1| ifodaning qiymatini toping.",
            gloss="evaluate — qiymatini toping; absolute value — modul",
            steps=(
                ("Each bar is a distance from zero: |−3| = 3, |2| = 2, and |−1| = 1.", "Har bir modul noldan uzoqlik: |-3| = 3, |2| = 2 va |-1| = 1."),
                ("The expression is now ordinary arithmetic: 3 + 2 − 1.", "Ifoda endi oddiy hisob: 3 + 2 - 1."),
                ("3 + 2 − 1 = 4. The distances were positive before any subtracting happened.", "3 + 2 - 1 = 4. Ayirishdan oldin masofalar musbat edi."),
            ),
            answer="4",
            checks=value("Abs(-3)+Abs(2)-Abs(-1)", "4"),
        ),
        Example(
            kind="sat",
            prompt_en="On a number line, point A is at −4 and point B is at 3. What is the distance between A and B?",
            prompt_uz="Son o'qida A nuqta −4 da, B nuqta 3 da. A va B orasidagi masofa nechaga teng?",
            gloss="distance — masofa; between — orasida; point — nuqta",
            choices=(
                ("A", "1", "1"),
                ("B", "7", "7"),
                ("C", "−7", "−7"),
                ("D", "12", "12"),
            ),
            steps=(
                ("Distance is the absolute value of the difference: |3 − (−4)|.", "Masofa — ayirmaning moduli: |3 - (-4)|."),
                ("Subtracting a negative is adding: 3 − (−4) = 3 + 4 = 7, and |7| = 7.", "Manfiyni ayirish — qo'shish: 3 - (-4) = 3 + 4 = 7, va |7| = 7."),
                ("A is what you get from 4 − 3 if the signs are ignored. D is the product 4 × 3. C is a distance with a sign, which a distance does not have.", "A — ishoralarni tashlab 4 - 3 qilinsa chiqadi. D — 