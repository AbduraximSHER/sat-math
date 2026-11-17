import { ImageResponse } from "next/og";

export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#1b3a4b",
          borderRadius: 36,
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 14,
            width: 96,
          }}
        >
          <div style={{ height: 22, background: "#f7f4ec", borderRadius: 4 }} />
          <div style={{ height: 22, background: "#2e7d7a", borderRadius: 4 }} />
          <div style={{ height: 22, background: "#f7f4ec", borderRadius: 4 }} />
        </div>
      </div>
    ),
    size,
  );
}
