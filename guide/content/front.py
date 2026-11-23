"""Opening pages and the formula sheet."""

from guide.model import Prose


def front_matter() -> tuple[Prose, ...]:
    return (
        Prose(kind="h1", text="Qanday o'qitiladi  /  How to use this book"),
        Prose(
            kind="pair",
            text=(
                "This is a teacher copy. Every lesson is one class of about 40 to 50 minutes for students who can already add, subtract, multiply, and divide positive fractions. The book then builds the rest of Digital SAT Math in the order a class can actually learn it: number sense, algebra, advanced algebra, data, geometry and trigonometry, then the craft of the test itself."
            ),
            text_uz=(
                "Bu o'qituvchi nusxasi. Har bir dars — musbat kasrlarni qo'shish, ayirish, ko'paytirish va bo'lishni biladigan sinf uchun taxminan 40–50 daqiqa. Kitob SAT Math ning qolganini sinf haqiqatan o'rgana oladigan tartibda quradi: son hissi, algebra, yuqori algebra, ma'lumot, geometriya va trigonometriya, so'ng imtihonning o'zi."
            ),
        ),
        Prose(
            kind="pair",
            text=(
                "In class, read the goal in Uzbek. Work the Foundation example on the board while students copy. Have them try the first two practice problems before you touch the SAT-style example. Translate that stem with the word gloss, solve it, and name the trap answer out loud. Send the rest home. Next period, open with one line from a student's error, not with a new definition."
            ),
            text_uz=(
                "Sinfda maqsadni o'zbekcha o'qing. Foundation misolni doskada o'zingiz yeching, o'quvchilar ko'chirsin. SAT uslubidagi misolga o'tishdan oldin mashqning birinchi ikkitasini ularga bering. Keyin savol matnini so'zlar izohi bilan tarjima qiling, yeching va tuzoq javobni ovoz chiqarib ayting. Qolganini uyga bering. Keyingi dars yangi ta'rifdan emas, o'quvchi xatosining bitta qatoridan boshlang."
            ),
        ),
        Prose(
            kind="pair",
            text=(
                "Practice answers sit in the shaded block at the end of the lesson, and again in the master key. Cover that block before you photocopy a lesson for students. The mixed review at the back is a 35-minute class sitting. It is not a scored practice test and it does not predict a scaled score."
            ),
            text_uz=(
                "Mashq javoblari dars oxiridagi kulrang blokda va kitob oxiridagi qisqa kalitda turadi. Darsni o'quvchiga nusxa qilishdan oldin o'sha blokni yoping. Kitob oxiridagi aralash mini-test 35 daqiqalik sinf ishi. U baholanadigan sinov emas va scaled ballni bashorat qilmaydi."
            ),
        ),
        Prose(kind="h2", text="Raqamli SAT Math qanday tuzilgan"),
        Prose(
            kind="pair",
            text=(
                "The current Digital SAT Math section has two modules. Each module has 22 questions and about 35 minutes. That is 44 questions and 70 minutes. The Desmos calculator is allowed on every question. There is no guessing penalty, so a blank line cannot help and a guess can. Module 2 is adaptive: a stronger first module leads to a harder second module. This book does not invent a raw-to-scaled conversion. About three quarters of the questions are four-choice. The rest ask the student to produce the number. The approximate public mix is Algebra about 35 percent, Advanced Math about 35 percent, Problem-Solving and Data Analysis about 15 percent, and Geometry and Trigonometry about 15 percent."
            ),
            text_uz=(
                "Hozirgi raqamli SAT Math ikki moduldan iborat. Har modulda 22 savol va taxminan 35 daqiqa bor. Jami 44 savol va 70 daqiqa. Desmos kalkulyatori har bir savolda ruxsat etiladi. Noto'g'ri javob uchun alohida jarima yo'q: bo'sh qoldirish yordam bermaydi, taxmin esa ba'zan tegadi. Ikkinchi modul moslashuvchan: birinchi modul qanchalik kuchli bo'lsa, ikkinchisi shunchalik qiyin bo'ladi. Bu kitob raw balldan scaled ballga o'z formulasi yo'q. Savollarning taxminan to'rtdan uchi to'rt variantli. Qolganida o'quvchi sonning o'zini yozadi. E'lon qilingan taxminiy ulush: Algebra taxminan 35 foiz, Advanced Math taxminan 35 foiz, masala va ma'lumot taxminan 15 foiz, geometriya va trigonometriya taxminan 15 foiz."
            ),
        ),
        Prose(kind="h2", text="Nuqta, vergul va inglizcha savol"),
        Prose(
            kind="pair",
            text=(
                "On this test a point is the decimal mark and a comma is not. 3.5 means three and five tenths. 3,500 means three thousand five hundred. Students who write decimals with a comma will misread both. Every SAT-style stem in this book is in English, with Uzbek underneath for you. Early lessons gloss the hard words. Later lessons drop the gloss so the class grows into the stem. The real test will not use local names or local currency symbols as a kindness. Teach the plain voice of the question: of, which of the following, equivalent, in terms of, satisfies, no solution."
            ),
            text_uz=(
                "Shu imtihonda nuqta o'nli kasr belgisi, vergul esa emas. 3.5 degani uch butun besh o'ndan. 3,500 degani uch ming besh yuz. O'nli kasrni vergul bilan yozishga o'rgangan o'quvchi ikkalasini ham adashtiradi. Kitobdagi SAT uslubidagi savol matni inglizcha, tagida siz uchun o'zbekchasi bor. Erta darslarda qiyin so'zlar izohlanadi. Keyinroq izoh kamayadi, sinf savol tiliga o'sadi. Haqiqiy imtihon mahalliy ism yoki mahalliy pul belgisi bilan yengillatmaydi. Savolning oddiy ovozini o'rgating: of, which of the following, equivalent, in terms of, satisfies, no solution."
            ),
        ),
        Prose(kind="h2", text="Dars tartibi"),
        Prose(
            kind="table",
            headers=("Bo'lim", "Darslar", "Nima uchun shu yerda"),
            rows=(
                ("0. Ko'prik", "1", "To'rt amalni tasdiqlash, aralash va manfiy kasr"),
                ("1. Asos", "10", "Imtihon oldindan biladi deb hisoblaydigan son hissi"),
                ("2. Algebra", "8", "Eng katta domen: tenglama, qiyalik, sistema, funksiya"),
                ("3. Advanced Math", "8", "Ko'phad, kvadrat, teng kuchli ifoda, ildiz"),
                ("4. Ma'lumot", "6", "Nisbat, jadval, o'rta qiymat, ehtimollik, da'vo"),
                ("5. Geometriya", "7", "Burchak, uchburchak, trigonometriya, yuza, hajm, aylana"),
                ("6. Imtihon hunari", "4", "Vaqt, inglizcha ibora, Desmos, tuzoq va xato daftari"),
            ),
        ),
        Prose(
            kind="pair",
            text=(
                "A student who finishes a lesson's five problems cleanly can move on. Do not skip the foundations because a topic looks familiar from school. The test mixes the arithmetic with an English stem, and that mix is the new skill. Fractions stay in the room all year: a percent is a fraction out of 100, a slope is a fraction, a probability is a fraction, and a sine is a fraction."
            ),
            text_uz=(
                "Besh mashqni toza yechgan o'quvchi oldinga o'tishi mumkin. Mavzu maktabdan tanish ko'ringani uchun asosni tashlab ketmang. Imtihon hisobni inglizcha savol bilan aralashtiradi, yangi mahorat o'sha aralashmaning o'zida. Kasr yil bo'yi xonada qoladi: foiz — 100 dan olingan kasr, qiyalik — kasr, ehtimollik — kasr, sinus ham kasr."
            ),
        ),
        Prose(kind="h1", text="Mundarija  /  Contents"),
        Prose(kind="contents"),
    )


def formula_sheet() -> tuple[Prose, ...]:
    return (
        Prose(kind="h1", text="Formula varaqasi  /  Formula sheet"),
        Prose(
            kind="pair",
            text=(
                "The test hands students a reference sheet of standard area, volume, circle, and special-triangle facts. This page teaches those facts. It is not a copy of the official sheet. The skill on test day is knowing which fact fits the picture. A student who hunts the sheet for a slope formula will not find one: slope is not on it."
            ),
            text_uz=(
                "Imtihon o'quvchiga yuza, hajm, aylana va maxsus uchburchaklar haqidagi oddiy faktlar yozilgan varaqa beradi. Bu sahifa o'sha faktlarni o'rgatadi. Rasmiy varaqaning nusxasi emas. Imtihon kunidagi mahorat — qaysi fakt rasmga mosligini bilishdir. Qiyalik formulasini varaqadan qidirgan o'quvchi topa olmaydi: qiyalik u yerda yo'q."
            ),
        ),
        Prose(kind="h2", text="Varaqada bor  /  On the sheet"),
        Prose(
            kind="table",
            headers=("Figura", "Fakt"),
            rows=(
                ("Aylana yuzi", "πr²"),
                ("Aylana uzunligi", "2πr"),
                ("To'rtburchak yuzi", "ℓw"),
                ("Uchburchak yuzi", "(1/2)bh"),
                ("Pifagor", "a² + b² = c²"),
                ("45-45-90", "x, x, x√2"),
                ("30-60-90", "x, x√3, 2x"),
                ("To'g'ri burchakli parallelepiped hajmi", "ℓwh"),
                ("Silindr hajmi", "πr²h"),
                ("Shar hajmi", "(4/3)πr³"),
                ("Konus hajmi", "(1/3)πr²h"),
                ("Piramida hajmi", "(1/3)Bh"),
                ("Aylana gradusi", "360"),
                ("Uchburchak burchaklari yig'indisi", "180"),
            ),
        ),
        Prose(kind="h2", text="Yodda turishi kerak  /  Carry these yourself"),
        Prose(
            kind="table",
            headers=("G'oya", "Qoida"),
            rows=(
                ("Foiz o'zgarishi", "(yangi − eski) / eski"),
                ("Qiyalik", "(y₂ − y₁) / (x₂ − x₁)"),
                ("Daraja", "a^m · a^n = a^(m+n), a^m / a^n = a^(m−n), (a^m)^n = a^(mn)"),
                ("Nol daraja va manfiy daraja", "a^0 = 1 (a ≠ 0), a^(−n) = 1/a^n"),
                ("Kvadrat formula", "x = (−b ± √(b² − 4ac)) / (2a)"),
                ("Yo'l", "masofa = tezlik × vaqt"),
                ("O'rta arifmetik", "yig'indi / qiymatlar soni"),
                ("Ehtimollik", "qulay / barcha"),
                ("Sinus, kosinus, tangens", "qarama-qarshi/gipotenuza, yondosh/gipotenuza, qarama-qarshi/yondosh"),
                ("Qo'shni burchaklar", "to'g'ri chiziqda 180°, to'g'ri burchakda 90°"),
                ("Manfiyga ko'paytirish", "tengsizlikning belgisi almashtiriladi"),
            ),
        ),
    )
