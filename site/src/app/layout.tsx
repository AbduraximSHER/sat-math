import type { Metadata, Viewport } from "next";
import { Fraunces, Source_Sans_3 } from "next/font/google";
import { PREFS_SCRIPT } from "@/components/prefs";
import { Shell } from "@/components/shell";
import { guide } from "@/lib/guide";
import { SITE_URL } from "@/lib/site";
import "./globals.css";

const sans = Source_Sans_3({
  subsets: ["latin", "latin-ext"],
  variable: "--font-source",
  display: "swap",
});

const serif = Fraunces({
  subsets: ["latin", "latin-ext"],
  variable: "--font-fraunces",
  display: "swap",
});

const DESCRIPTION =
  "Kasr amallaridan raqamli SAT Math gacha: 44 dars inglizcha va o'zbekcha, har darsda 100 ta tekshiriladigan mashq, mini-test va o'qituvchi kaliti.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "SAT Math — O'qituvchi qo'llanmasi",
    template: "%s · SAT Math",
  },
  description: DESCRIPTION,
  applicationName: "SAT Math",
  openGraph: {
    type: "website",
    siteName: "SAT Math",
    title: "SAT Math — O'qituvchi qo'llanmasi",
    description: DESCRIPTION,
    locale: "uz_UZ",
  },
  twitter: { card: "summary_large_image" },
  icons: {
    icon: [
      { url: "/favicon.svg", type: "image/svg+xml" },
      { url: "/icon", type: "image/png", sizes: "32x32" },
    ],
    apple: [{ url: "/apple-icon", sizes: "180x180" }],
  },
  formatDetection: { telephone: false },
};

export const viewport: Viewport = {
  themeColor: "#1b3a4b",
  width: "device-width",
  initialScale: 1,
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
    <html lang="uz" data-lang="both" data-focus="off" suppressHydrationWarning className={`${sans.variable} ${serif.variable}`}>
      <head>
        <script dangerouslySetInnerHTML={{ __html: PREFS_SCRIPT }} />
      </head>
      <body className="antialiased">
        <Shell units={index}>{children}</Shell>
      </body>
    </html>
  );
}
