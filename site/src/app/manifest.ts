import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "SAT Math — O'qituvchi qo'llanmasi",
    short_name: "SAT Math",
    description: "44 dars inglizcha va o'zbekcha, har darsda 100 ta tekshiriladigan mashq, mini-test va mashq varag'i.",
    lang: "uz",
    start_url: "/",
    scope: "/",
    display: "standalone",
    background_color: "#f4f0e6",
    theme_color: "#1b3a4b",
    categories: ["education"],
    icons: [
      { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
      { src: "/icons/maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
    shortcuts: [
      { name: "Mini-test", url: "/mini" },
      { name: "Mashq varag'i", url: "/varaq" },
      { name: "Atamalar", url: "/lugat" },
    ],
  };
}
