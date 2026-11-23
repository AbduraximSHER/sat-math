import { NextRequest, NextResponse } from "next/server";
import { MAX_ANSWER_LENGTH, checkAnswer, type Verdict } from "@/lib/answer-check";
import { loadKeys } from "@/lib/keys";
import { NO_STORE } from "@/lib/teacher";

export const dynamic = "force-dynamic";

/**
 * Grade typed answers without revealing them.
 *
 * Bank item:  { "code": "2.6", "id": "014", "answer": "3/4" }  → Verdict
 * Mini-test:  { "mini": true, "answers": { "1": "11/10", ... } } → { results: { "1": Verdict | {result: "blank"} } }
 */
export async function POST(request: NextRequest) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "invalid json" }, { status: 400, headers: NO_STORE });
  }
  if (!body || typeof body !== "object") {
    return NextResponse.json({ error: "invalid body" }, { status: 400, headers: NO_STORE });
  }
  const keys = loadKeys();
  const input = body as Record<string, unknown>;

  if (input.mini === true) {
    const answers = input.answers;
    if (!answers || typeof answers !== "object" || Array.isArray(answers)) {
      return NextResponse.json({ error: "answers required" }, { status: 400, headers: NO_STORE });
    }
    const given = answers as Record<string, unknown>;
    const results: Record<string, Verdict | { result: "blank" }> = {};
    for (const row of keys.mini) {
      const raw = given[String(row.number)];
      results[row.number] =
        typeof raw === "string" && raw.trim()
          ? checkAnswer(row.check, raw.slice(0, MAX_ANSWER_LENGTH + 1))
          : { result: "blank" };
    }
    return NextResponse.json({ results }, { headers: NO_STORE });
  }

  const { code, id, answer } = input;
  if (typeof code !== "string" || typeof id !== "string" || typeof answer !== "string") {
    return NextResponse.json({ error: "code, id and answer are required" }, { status: 400, headers: NO_STORE });
  }
  const row = keys.lessons[code]?.bank.find((item) => item.id === id);
  if (!row) {
    return NextResponse.json({ error: "unknown item" }, { status: 404, headers: NO_STORE });
  }
  return NextResponse.json(checkAnswer(row.check, answer.slice(0, MAX_ANSWER_LENGTH + 1)), { headers: NO_STORE });
}
