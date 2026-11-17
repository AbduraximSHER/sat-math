import { ImageResponse } from "next/og";

export const size = { width: 32, height: 32 };
export const contentType = "image/png";

export default function Icon() {
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
          borderRadius: 8,
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 3,
            width: 18,
          }}
        >
          <div style={{ height: 4, background: "#f7f4ec", borderRadius: 1 }} />
          <div style={{ height: 4, background: "#2e7d7a", borderRadius: 1 }} />
          <div style={{ height: 4, background: "#f7f4ec", borderRadius: 1 }} />
        </div>
      </div>
    ),
    size,
  );
}
