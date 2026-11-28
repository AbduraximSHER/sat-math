# SAT Math — o'qituvchi qo'llanmasi

Kasrlarni qo'shish, ayirish, ko'paytirish va bo'lishni biladigan sinf uchun raqamli SAT Math kursi. Har bir dars inglizcha va o'zbekcha: maqsad, o'qituvchi yo'li, chuqurlashtirilgan tushuntirish, ikki yechilgan misol, uchta odatiy xato, beshta sinf mashqi va saytda o'quvchi o'zi tekshiradigan 100 ta qo'shimcha misol.

Bu College Board nashri emas. Savollar original.

## Fayllar

Word kitoblar `python3 -m guide.build_guide` bilan `dist/` papkasiga yoziladi. Ular repoda saqlanmaydi: GitHub Actions har tekshiruvda ularni **word-books** artefakti sifatida yig'adi (Actions → oxirgi CI → Artifacts).

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
2. Foundation misolni doskada yeching. Saytdagi «Qadamma-qadam» tugmasi qadamlarni birma-bir ochadi.
3. Mashqning birinchi ikkitasini sinfda bering.
4. SAT uslubidagi misolni so'zlar izohi bilan tarjima qiling va tuzoqni ayting.
5. Qolgan mashqni uyga bering. Bank savollarini o'quvchi saytda o'zi tekshiradi.

Raqamli SAT Math: 2 modul, 44 savol, 70 daqiqa, Desmos butun bo'limda ruxsat. Kitob scaled ball formulasini bermaydi.

## Sayt

Jonli: [https://sat-math.abenglish.workers.dev](https://sat-math.abenglish.workers.dev)

Sayt `site/` papkasida (Next.js, Cloudflare Workers).

**O'qituvchi uchun**

- **Kalit.** Kalit yopiq bo'lsa, javoblar brauzerga umuman yuborilmaydi. Ochilganda `/api/keys` orqali keladi.
- **PIN (ixtiyoriy).** Kalitni o'quvchilardan himoyalash uchun Cloudflare'da `TEACHER_PIN` sirini qo'shing. Shundan keyin kalit PIN so'raydi, qurilma uni 30 kun eslab qoladi. Sir qo'shilmasa, hammasi avvalgidek: bir bosishda ochiladi.
- **Mashq varag'i** (`/varaq`): istalgan darsning 100 ta savolidan daraja va son tanlab varaq tuziladi. «Yangi variant» aralashtiradi, havola o'sha variantni eslab qoladi. Kalit ochiq bo'lsa, javoblar alohida sahifaga chop etiladi.
- **Ekran rejimi** (`F`): yon panel yashirinadi, matn kengayadi. Shrift hajmi `+` va `−` bilan, mavzu yorug' yoki qorong'i.
- **Qidiruv** (`/` yoki `Ctrl K`): dars, atama va sahifalar, ikki tilda.
- **Tezkor tugmalar:** `←` `→` darslar orasida, `K` kalit, `L` til, `?` hammasi.

**O'quvchi uchun**

- Har bir bank savolining ostida javob qatori. Sayt javobni serverda tekshiradi va to'g'ri yoki noto'g'ri ekanini aytadi, kalitni ochmaydi. Shakl xato bo'lsa, SAT qoidasini eslatadi: aralash son emas (7/2), vergul emas nuqta (3.5), qisqartirilgan kasr va ildiz.
- Mini-test (`/mini`): 35 daqiqalik taymer, topshirgandan keyin natija va har bir xato uchun takrorlash kerak bo'lgan dars.
- Natijalar shu brauzerda saqlanadi. Hech qanday ro'yxatdan o'tish yo'q.
- Telefonda «Bosh ekranga qo'shish» mumkin. Ochilgan darslar internet uzilganda ham ochiladi.

### PIN qo'yish

Cloudflare dashboard → Workers → **sat-math** → Settings → Variables and Secrets → **Add** → turi *Secret*, nomi `TEACHER_PIN`, qiymati PIN. Yoki terminaldan:

```bash
cd site
npx wrangler secret put TEACHER_PIN
```

Kamida 6 belgili PIN tanlang. PIN o'zgarsa, barcha qurilmalardan kalit qayta so'raladi.

### Kompyuterda ishga tushirish

```bash
cd site
npm install
npm run dev
```

Brauzerda `http://127.0.0.1:3847`. Tekshiruvlar:

```bash
npm run lint
```

```bash
npm run typecheck
```

```bash
npm test
```

Cloudflare muhitining o'zida sinash (`wrangler dev`):

```bash
npm run preview
```

### Deploy

Sayt `main` ga push bo'lganda **Cloudflare Workers Builds** orqali avtomatik deploy bo'ladi (repo Cloudflare dashboard'ida ulangan). Jonli saytda darslar tayyor sahifa sifatida beriladi.

GitHub Actions `main` da va har PR da tekshiruvni yuritadi: Python tekshiruvi, lint, tiplar, testlar, worker yig'ish va Workers muhitida smoke-test. `main` da u deploy ham qila oladi (`npx opennextjs-cloudflare deploy`), lekin buning uchun repoda ikki sir kerak: `CLOUDFLARE_API_TOKEN` va `CLOUDFLARE_ACCOUNT_ID` (GitHub → Settings → Secrets and variables → Actions). Ular qo'yilmagan bo'lsa, deploy qadami o'zini o'tkazib yuboradi va yugurish yashil qoladi.

Ikkalasi ham yoqilsa, har push ikki marta deploy bo'ladi. Zarari yo'q, lekin bittasi yetarli.

## Qayta yig'ish

```bash
python3 -m pip install -r requirements.txt
```

```bash
python3 -m guide.build_guide
```

Tekshiruv har bir javobni SymPy bilan qayta hisoblaydi. Bankdagi 4 400 savolning 3 700 dan ortig'i savol matnining o'zidan qayta o'qib hisoblanadi, shuning uchun formatdagi xato ham noto'g'ri kalitga aylanmaydi. Xato bo'lsa, Word fayl ham, sayt ma'lumoti ham yozilmaydi.

Bitta dars uchun Word fayl (bir sahifalik qisqa konspekt + batafsil dars), hozircha 1.6 va 1.7 uchun:

```bash
python3 -m guide.handout 1.7
```

Fayl `dist/Dars-1.7.docx` ga yoziladi. Faqat o'zbekcha variant (har misol va mashq yechimi bilan): `python3 -m guide.handout --uz 1.7` → `dist/Dars-1.7-uz.docx`. U har qanday dars uchun ishlaydi; qisqa konspekt faqat `SUMMARIES` da bor darslarga qo'shiladi. Boshqa dars uchun `guide/handout.py` dagi `SUMMARIES` ga konspekt qo'shing.

`build_guide` buyrug'i `site/data/guide.json`, `site/data/keys.json` va `site/public/figures/*.svg` ni yangilaydi. Mazmun o'zgarsa, shularni ham commit qiling: CI ma'lumot Python manbaiga mos kelmasa, to'xtaydi.

## Subagent

Loyihadagi mentor: `.cursor/agents/sat-math-mentor.md`.

Cursor da yangi dars yoki mashq so'rash:

```text
Use the sat-math-mentor subagent to write the next practice set for lesson 2.3.
```
