import { NextRequest, NextResponse } from "next/server";
import { loadKeys, publicLessonKeys, publicMiniKeys } from "@/lib/keys";
import { NO_STORE, teacherUnlocked } from "@/lib/teacher";

export const dynamic = "force-dynamic";

/** Answers and solutions. Sent only when the teacher opens the key, never cached. */
export async function GET(request: NextRequest) {
  if (!(await teacherUnlocked(request))) {
    return NextResponse.json({ error: "pin" }, { status: 401, headers: NO_STORE });
  }

  const code = request.nextUrl.searchParams.get("code");
  const mini = request.nextUrl.searchParams.get("mini");
  const keys = loadKeys();

  if (mini === "1" || mini === "true") {
    return NextResponse.json({ mini: publicMiniKeys(keys.mini) }, { headers: NO_STORE });
  }

  if (!code) {
    return NextResponse.json({ error: "code required" }, { status: 400, headers: NO_STORE });
  }

  const lesson = keys.lessons[code];
  if (!lesson) {
    return NextResponse.json({ error: "unknown lesson" }, { status: 404, headers: NO_STORE });
  }

  return NextResponse.json({ code, ...publicLessonKeys(lesson) }, { headers: NO_STORE });
}
