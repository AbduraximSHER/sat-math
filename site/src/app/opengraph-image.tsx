import { ImageResponse } from "next/og";

export const alt = "SAT Math — O'qituvchi qo'llanmasi";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

/** The preview card shown when a link to the site is shared. */
export default function OpenGraphImage() {
  const bar = (color: string) => ({ height: 34, width: 190, borderRadius: 8, background: color });
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "72px 80px",
          background: "#1b3a4b",
          color: "#f7f4ec",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", fontSize: 30, letterSpacing: 4, color: "#9fd8d3" }}>DIGITAL SAT · SINF UCHUN</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <div style={bar("#f7f4ec")} />
            <div style={bar("#2e9c97")} />
            <div style={bar("#f7f4ec")} />
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <div style={{ display: "flex", fontSize: 128, fontWeight: 700, lineHeight: 1 }}>SAT Math</div>
          <div style={{ display: "flex", marginTop: 18, fontSize: 48, color: "#d9e6ec" }}>O&apos;qituvchi qo&apos;llanmasi</div>
        </div>
        <div style={{ display: "flex", fontSize: 30, color: "#b8cbd4" }}>
          44 dars · English / O&apos;zbekcha · 4 400 tekshiriladigan mashq
        </div>
      </div>
    ),
    size,
  );
}
