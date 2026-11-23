/*
 * SAT Math offline support.
 *
 * Pages: network first, so a connected visit always gets the newest lesson;
 * when the classroom internet drops, any page opened before still loads.
 * Build assets, fonts and figures: cache first (their names change when they change).
 * /api/*: never cached. Answer keys and grading always go to the server.
 */
const VERSION = "sat-math-v1";
const PAGES = `${VERSION}-pages`;
const ASSETS = `${VERSION}-assets`;
const MAX_ASSETS = 300;

const OFFLINE_HTML = `<!doctype html><html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Internet yo'q · SAT Math</title><style>body{font-family:system-ui,sans-serif;background:#f4f0e6;color:#1f2933;display:grid;place-items:center;min-height:100vh;margin:0;padding:16px}main{max-width:28rem;text-align:center}h1{color:#1b3a4b}a{color:#0f6e6b}</style></head><body><main><h1>Internet yo'q</h1><p>Bu sahifa hali bu qurilmada ochilmagan. Oldin ochilgan darslar internetsiz ham ishlaydi.</p><p><a href="/">Bosh sahifa</a></p></main></body></html>`;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(PAGES)
      .then((cache) => cache.addAll(["/", "/formulalar", "/lugat"]))
      .catch(() => undefined)
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((key) => !key.startsWith(VERSION)).map((key) => caches.delete(key))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || url.pathname.startsWith("/api/")) return;

  if (url.pathname.startsWith("/_next/static/") || url.pathname.startsWith("/figures/") || url.pathname.startsWith("/icons/")) {
    event.respondWith(cacheFirst(request));
    return;
  }
  const isPage = request.mode === "navigate";
  const isData = request.headers.get("RSC") === "1" || url.searchParams.has("_rsc") || url.pathname === "/search-index.json";
  if (isPage || isData) event.respondWith(networkFirst(request, isPage));
});

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(ASSETS);
    await cache.put(request, response.clone());
    const keys = await cache.keys();
    for (const old of keys.slice(0, Math.max(0, keys.length - MAX_ASSETS))) await cache.delete(old);
  }
  return response;
}

async function networkFirst(request, isPage) {
  const cache = await caches.open(PAGES);
  try {
    const response = await fetch(request);
    if (response.ok) await cache.put(request, response.clone());
    return response;
  } catch (error) {
    const cached = await cache.match(request, { ignoreVary: true });
    if (cached) return cached;
    if (isPage) return new Response(OFFLINE_HTML, { headers: { "Content-Type": "text/html; charset=utf-8" } });
    throw error;
  }
}
