import { NextRequest, NextResponse } from "next/server";
import { NO_STORE, clearTeacherCookie, pinMatches, setTeacherCookie, teacherPin, teacherUnlocked } from "@/lib/teacher";

export const dynamic = "force-dynamic";

/** Whether a PIN is configured, and whether this browser already entered it. */
export async function GET(request: NextRequest) {
  return NextResponse.json(
    { required: Boolean(teacherPin()), unlocked: await teacherUnlocked(request) },
    { headers: NO_STORE },
  );
}

/** Enter the PIN. A wrong PIN waits a moment before answering. */
export async function POST(request: NextRequest) {
  let pin = "";
  try {
    const body = (await request.json()) as { pin?: unknown };
    pin = typeof body.pin === "string" ? body.pin.slice(0, 128) : "";
  } catch {
    return NextResponse.json({ error: "invalid json" }, { status: 400, headers: NO_STORE });
  }
  if (!(await pinMatches(pin))) {
    await new Promise((resolve) => setTimeout(resolve, 700));
    return NextResponse.json({ unlocked: false }, { status: 401, headers: NO_STORE });
  }
  const response = NextResponse.json({ unlocked: true }, { headers: NO_STORE });
  await setTeacherCookie(response);
  return response;
}

/** Forget the PIN on this browser. */
export async function DELETE() {
  const response = NextResponse.json({ unlocked: false }, { headers: NO_STORE });
  clearTeacherCookie(response);
  return response;
}
