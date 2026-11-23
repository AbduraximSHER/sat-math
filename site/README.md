# SAT Math site

The classroom site for the bilingual teacher guide. Next.js on Cloudflare Workers via OpenNext.

```bash
npm install
npm run dev
```

Then open http://127.0.0.1:3847.

## Data

Lesson text comes from `data/guide.json` and answers from `data/keys.json`, both written by `python3 -m guide.build_guide` in the parent project. `keys.json` is server-only: `/api/keys` sends answers when the teacher opens the key (specs stripped, `no-store`), and `/api/check` grades typed answers against the specs in it (`src/lib/answer-check.ts`).

## Layout

| Path | What |
| --- | --- |
| `src/app/dars/[code]` | Lesson page, prerendered; client islands in `src/components/lesson/` |
| `src/app/mini` | Interactive 20-question mini-test |
| `src/app/varaq` | Printable worksheet from a lesson's bank |
| `src/app/api/check` | Grades a bank or mini-test answer without revealing it |
| `src/app/api/keys` | Answer key, behind the optional `TEACHER_PIN` |
| `src/app/api/teacher` | PIN status, unlock, lock |
| `src/lib/answer-check.ts` | Rational and expression parser, SAT entry rules, hints |
| `public/sw.js` | Offline support for pages already opened |
| `scripts/smoke.mjs` | Smoke test against a running worker |

Language, theme, font size and projector mode live on `<html>` as attributes, set by an inline script before first paint (`PREFS_SCRIPT` in `src/components/prefs.tsx`); CSS does the hiding. Progress is stored in `localStorage` (`src/lib/progress.ts`).

## Checks

```bash
npm run lint
```

```bash
npm run typecheck
```

```bash
npm test
```

`npm test` includes a round trip of every keyed answer in `data/keys.json` through the checker.

To run the real Workers runtime locally:

```bash
npm run preview
```

```bash
node scripts/smoke.mjs http://127.0.0.1:8787
```

## Teacher PIN

Optional. Set a `TEACHER_PIN` secret on the Worker (`npx wrangler secret put TEACHER_PIN`); for local development put `TEACHER_PIN=...` in `.dev.vars`. Without it, the key opens with one click as before.
