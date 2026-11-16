import { NextRequest, NextResponse } from "next/server";
import { loadKeys } from "@/lib/keys";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  const code = request.nextUrl.searchParams.get("code");
  const mini = request.nextUrl.searchParams.get("mini");
  const keys = loadKeys();

  if (mini === "1" || mini === "true") {
    return NextResponse.json({ mini: keys.mini });
  }

  if (!code) {
    return NextResponse.json({ error: "code required" }, { status: 400 });
  }

  const lesson = keys.lessons[code];
  if (!lesson) {
    return NextResponse.json({ error: "unknown lesson" }, { status: 404 });
  }

  return NextResponse.json({ code, ...lesson });
}
