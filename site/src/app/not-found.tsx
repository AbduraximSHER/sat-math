import Link from "next/link";

export default function NotFound() {
  return (
    <article>
      <h1 className="font-serif text-4xl text-[var(--navy)]">Bu dars yo&apos;q</h1>
      <p className="mt-3 leading-relaxed">
        Raqam noto&apos;g&apos;ri yozilgan yoki dars hali kitobga kirmagan. Chapdagi ro&apos;yxatdan darsni tanlang.
      </p>
      <Link href="/" className="mt-4 inline-block text-[var(--teal)] hover:underline">
        Kirish sahifasiga qaytish
      </Link>
    </article>
  );
}
