import "server-only";
import { getCloudflareContext } from "@opennextjs/cloudflare";
import type { NextRequest, NextResponse } from "next/server";

/**
 * Optional teacher PIN for the answer key.
 *
 * Set a TEACHER_PIN secret on the Worker (`npx wrangler secret put TEACHER_PIN`)
 * and the key opens only after the PIN is entered. Without the secret the key
 * works exactly as before: one click, no PIN.
 *
 * The cookie holds an HMAC of a fixed label keyed by the PIN, never the PIN.
 * Changing the PIN signs everyone out.
 */

export const TEACHER_COOKIE = "sat_teacher";
const LABEL = "sat-math-teacher-key-v1";
const THIRTY_DAYS = 60 * 60 * 24 * 30;

export function teacherPin(): string | null {
  try {
    const value = (getCloudflareContext().env as unknown as Record<string, unknown>).TEACHER_PIN;
    if (typeof value === "string" && value.trim()) return value.trim();
  } catch {
    // Not running inside the Worker (next build, tests): fall back to process.env.
  }
  const fromProcess = process.env.TEACHER_PIN;
  return fromProcess && fromProcess.trim() ? fromProcess.trim() : null;
}

async function sign(pin: string): Promise<string> {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", encoder.encode(pin), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const signature = await crypto.subtle.sign("HMAC", key, encoder.encode(LABEL));
  return Array.from(new Uint8Array(signature), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function sameText(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i += 1) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

/** True when no PIN is configured, or the request carries a valid teacher cookie. */
export async function teacherUnlocked(request: NextRequest): Promise<boolean> {
  const pin = teacherPin();
  if (!pin) return true;
  const cookie = request.cookies.get(TEACHER_COOKIE)?.value;
  return Boolean(cookie) && sameText(cookie!, await sign(pin));
}

export async function pinMatches(attempt: string): Promise<boolean> {
  const pin = teacherPin();
  if (!pin) return true;
  return sameText(await sign(attempt.trim()), await sign(pin));
}

export async function setTeacherCookie(response: NextResponse): Promise<void> {
  const pin = teacherPin();
  if (!pin) return;
  response.cookies.set(TEACHER_COOKIE, await sign(pin), {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/",
    maxAge: THIRTY_DAYS,
  });
}

export function clearTeacherCookie(response: NextResponse): void {
  response.cookies.set(TEACHER_COOKIE, "", { httpOnly: true, secure: true, sameSite: "lax", path: "/", maxAge: 0 });
}

export const NO_STORE = { "Cache-Control": "no-store, max-age=0" };
