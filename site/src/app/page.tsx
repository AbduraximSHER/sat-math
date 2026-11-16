import Link from "next/link";
import { guide } from "@/lib/guide";

export default function HomePage() {
  return (
    <article>
      <p className="text-sm font-semibold tracking-wide text-[var(--teal)]">DIGITAL SAT · SINF UCHUN</p>
      <h1 className="mt-2 font-serif text-5xl leading-tight text-[var(--navy)]">SAT Math</h1>
      <p className="mt-2 font-serif text-2xl text-[#5c6b73]">O&apos;qituvchi qo&apos;llanmasi</p>
      <p className="mt-6 text-[17px] leading-relaxed">
        Bu sayt kasrlarni qo&apos;shish, ayirish, ko&apos;paytirish va bo&apos;lishni biladigan sinf uchun. 44 dars
        raqamli SAT Math bo&apos;limining qolganini tartib bilan o&apos;tadi. Har bir dars ikki tilda: chuqur
        tushuntirish, ikki yechilgan misol, beshta sinf mashqi va 100 ta qo&apos;shimcha bank.
      </p>
      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        <Note title="1. Maqsad" body="Darsni o'zbekcha maqsaddan boshlang. Tildagi tugma bilan faqat o'zbekcha qoldiring." />
        <Note title="2. Misol" body="Foundation misolni doskada yeching. SAT misolini inglizcha matn bilan tarjima qiling." />
        <Note
          title="3. Kalit"
          body="Ekranni sinfga ko'rsatishdan oldin «Kalit yopiq» qiling. Mashq va bank javoblari sahifaga umuman yuborilmaydi."
        />
      </div>
      <section className="mt-10">
        <h2 className="font-serif text-2xl text-[var(--navy)]">Imtihon</h2>
        <p className="mt-2 leading-relaxed">
          Ikki modul, 44 savol, 70 daqiqa. Desmos har bir savolda ruxsat. Noto&apos;g&apos;ri javob uchun alohida jarima
          yo&apos;q. Nuqta o&apos;nli kasr belgisi: 3.5 — uch butun besh o&apos;ndan. 3,500 — uch ming besh yuz.
        </p>
      </section>
      <section className="mt-10 space-y-4">
        <h2 className="font-serif text-2xl text-[var(--navy)]">Bo&apos;limlar</h2>
        {guide.units.map((unit) => (
          <Link
            key={unit.code}
            href={`/dars/${unit.lessons[0].code}`}
            className="block rounded-xl border border-[#e4ddd0] bg-white p-4 hover:border-[var(--teal)]"
          >
            <p className="text-xs font-semibold text-[var(--teal)]">
              {unit.code}-bo&apos;lim · {unit.lessons.length} dars
            </p>
            <p className="mt-1 font-serif text-xl text-[var(--navy)]">{unit.titleUz}</p>
            <p className="text-sm italic text-[#5c6b73]">{unit.titleEn}</p>
          </Link>
        ))}
      </section>
    </article>
  );
}

function Note({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-xl border border-[#e4ddd0] bg-white p-4">
      <p className="font-semibold text-[var(--navy)]">{title}</p>
      <p className="mt-1 text-sm leading-relaxed">{body}</p>
    </div>
  );
}
