// Smoke test against a running worker (wrangler dev) or any deployed copy.
//   node scripts/smoke.mjs http://127.0.0.1:8787
// Checks the pages and APIs the classroom depends on, on the real Workers runtime.

const base = (process.argv[2] ?? "http://127.0.0.1:8787").replace(/\/$/, "");
const failures = [];

async function waitForServer() {
  for (let attempt = 0; attempt < 90; attempt += 1) {
    try {
      const response = await fetch(base);
      if (response.ok) return;
    } catch {
      // not up yet
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  throw new Error(`no answer from ${base}`);
}

async function expectPage(path, status, text) {
  const response = await fetch(base + path);
  // React separates adjacent text with <!-- -->; read the text as a person would.
  const body = (await response.text()).replaceAll("<!-- -->", "");
  if (response.status !== status) failures.push(`${path}: status ${response.status}, expected ${status}`);
  else if (text && !body.includes(text)) failures.push(`${path}: missing ${JSON.stringify(text)}`);
  else console.log(`ok  ${status} ${path}`);
}

async function expectJson(label, request, check) {
  const response = await fetch(base + request.path, {
    method: request.method ?? "GET",
    headers: { "Content-Type": "application/json" },
    body: request.body ? JSON.stringify(request.body) : undefined,
  });
  const data = await response.json().catch(() => null);
  const problem = check(response, data);
  if (problem) failures.push(`${label}: ${problem}`);
  else console.log(`ok  ${label}`);
}

await waitForServer();

await expectPage("/", 200, "SAT Math");
await expectPage("/dars/0.1", 200, "DARS 0.1");
await expectPage("/dars/2.6", 200, "Qiyalik");
await expectPage("/dars/1.10", 200, "DARS 1.10");
await expectPage("/dars/6.4", 200, "DARS 6.4");
await expectPage("/dars/9.9", 404);
await expectPage("/mini", 200, "Mini-test");
await expectPage("/lugat", 200, "Atamalar");
await expectPage("/formulalar", 200, "Formula varaqasi");
await expectPage("/varaq?dars=3.2&soni=5&variant=7", 200, "Dars 3.2");
await expectPage("/search-index.json", 200, "\"kind\"");
await expectPage("/sitemap.xml", 200, "/dars/5.7");
await expectPage("/manifest.webmanifest", 200, "SAT Math");
await expectPage("/figures/parabola.svg", 200, "<svg");
await expectPage("/sw.js", 200, "sat-math-v1");

await expectJson("check: correct answer", { path: "/api/check", method: "POST", body: { code: "1.1", id: "001", answer: "1" } }, (r, d) =>
  r.ok && d?.result === "correct" ? null : `got ${r.status} ${JSON.stringify(d)}`,
);
await expectJson("check: wrong answer", { path: "/api/check", method: "POST", body: { code: "1.1", id: "001", answer: "2" } }, (r, d) =>
  r.ok && d?.result === "incorrect" ? null : `got ${r.status} ${JSON.stringify(d)}`,
);
await expectJson("check: mini-test", { path: "/api/check", method: "POST", body: { mini: true, answers: { 1: "11/10", 19: "48π" } } }, (r, d) =>
  r.ok && d?.results?.["1"]?.result === "correct" && d?.results?.["19"]?.result === "correct" ? null : `got ${r.status}`,
);
await expectJson("keys: no grading specs leak", { path: "/api/keys?code=2.6" }, (r, d) => {
  if (r.status === 401) return null; // a TEACHER_PIN is set on this worker
  if (!r.ok) return `status ${r.status}`;
  if (d.bank?.length !== 100) return "bank keys missing";
  return d.bank.some((row) => "check" in row) ? "grading spec sent to the browser" : null;
});
await expectJson("teacher: status", { path: "/api/teacher" }, (r, d) =>
  r.ok && typeof d?.required === "boolean" ? null : `got ${r.status}`,
);

if (failures.length) {
  console.error(`\n${failures.length} smoke check(s) failed:\n- ${failures.join("\n- ")}`);
  process.exit(1);
}
console.log("\nAll smoke checks passed.");
