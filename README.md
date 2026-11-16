# SAT Math — o'qituvchi qo'llanmasi

Kasrlarni qo'shish, ayirish, ko'paytirish va bo'lishni biladigan sinf uchun raqamli SAT Math kursi. Har bir dars inglizcha va o'zbekcha: maqsad, o'qituvchi yo'li, chuqurlashtirilgan tushuntirish, ikki yechilgan misol, uchta odatiy xato, beshta sinf mashqi va saytda 100 ta tekshirilgan qo'shimcha misol.

Bu College Board nashri emas. Savollar original.

## Fayllar

| Fayl | Nima |
| --- | --- |
| `dist/SAT-Math-Teacher-Guide.docx` | To'liq kitob: 44 dars, formula varaqasi, lug'at, barcha kalitlar, 20 savollik mini-test |
| `dist/01-asos.docx` | Ko'prik va son hissi |
| `dist/02-algebra.docx` | Algebra |
| `dist/03-advanced-math.docx` | Advanced Math |
| `dist/04-malumot-tahlili.docx` | Masala va ma'lumot |
| `dist/05-geometriya.docx` | Geometriya va trigonometriya |
| `dist/06-imtihon-hunari.docx` | Imtihon hunari |

Mashq javoblari har dars oxiridagi kulrang blokda. O'quvchiga varaq berishdan oldin o'sha blokni yoping.

## Sinfda

1. Maqsadni o'zbekcha o'qing.
2. Foundation misolni doskada yeching.
3. Mashqning birinchi ikkitasini sinfda bering.
4. SAT uslubidagi misolni so'zlar izohi bilan tarjima qiling va tuzoqni ayting.
5. Qolgan mashqni uyga bering.

Raqamli SAT Math: 2 modul, 44 savol, 70 daqiqa, Desmos butun bo'limda ruxsat. Kitob scaled ball formulasini bermaydi.

## Sayt

Jonli: [https://sat-math.abenglish.workers.dev](https://sat-math.abenglish.workers.dev)

GitHub: [AbduraximSHER/sat-math](https://github.com/AbduraximSHER/sat-math) — Cloudflare Workers Builds `main` ga push bo‘lganda avtomatik deploy qiladi.

Sinf ekranida ochish uchun sayt `site/` papkasida. Har darsda 100 ta mashq banki (oson / o'rta / SAT) sahifalanadi. Kalit yopiq bo'lsa, mashq va mini-test javoblari brauzerga umuman yuborilmaydi — faqat kalit ochilganda `/api/keys` orqali yuklanadi. Til tugmasi inglizcha, o'zbekcha yoki ikkalasini ko'rsatadi.

```bash
cd site
npm install
npm run dev
```

Brauzerda `http://127.0.0.1:3847`.

## Qayta yig'ish

```bash
python3 -m pip install -r requirements.txt
python3 -m guide.build_guide
```

Tekshiruv har bir javobni SymPy bilan qayta hisoblaydi. Xato bo'lsa, Word fayl yozilmaydi.

## Subagent

Loyihadagi mentor: `.cursor/agents/sat-math-mentor.md`.

Cursor da yangi dars yoki mashq so'rash:

```text
Use the sat-math-mentor subagent to write the next practice set for lesson 2.3.
```
