import type { Metadata } from "next";
import { Fraunces, Source_Sans_3 } from "next/font/google";
import { PrefsProvider } from "@/components/prefs";
import { Shell } from "@/components/shell";
import { guide } from "@/lib/guide";
import "./globals.css";

const sans = Source_Sans_3({
  subsets: ["latin"],
  variable: "--font-source",
});

const serif = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
});

export const metadata: Metadata = {
  title: "SAT Math — O'qituvchi qo'llanmasi",
  description:
    "Kasr amallaridan raqamli SAT Math gacha. Inglizcha va o'zbekcha darslar, misollar va o'qituvchi kaliti.",
  icons: {
    icon: [
      { url: "/favicon.svg", type: "image/svg+xml" },
      { url: "/icon", type: "image/png" },
    ],
    apple: [{ url: "/apple-icon" }],
  },
};

const index = guide.units.map((unit) => ({
  code: unit.code,
  titleEn: unit.titleEn,
  titleUz: unit.titleUz,
  lessons: unit.lessons.map((lesson) => ({
    code: lesson.code,
    titleEn: lesson.titleEn,
    titleUz: lesson.titleUz,
  })),
}));

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="uz">
      <body className={`${sans.variable} ${serif.variable} antialiased`}>
        <PrefsProvider>
          <Shell units={index}>{children}</Shell>
        </PrefsProvider>
      </body>
    </html>
  );
}
