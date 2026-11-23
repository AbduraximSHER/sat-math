import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

/**
 * Every lesson page is prerendered at build time and never revalidates, so the
 * worker serves the prebuilt HTML from static assets instead of rendering it on
 * each request. Without an incremental cache the prerendered pages are not found.
 */
export default defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
});
