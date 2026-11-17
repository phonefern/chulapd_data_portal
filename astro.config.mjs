import { defineConfig } from 'astro/config';

// Served as plain files by nginx on the institutional server.
//
// `trailingSlash: 'always'` + `format: 'directory'` keep every page at a
// directory URL (/datasets/checkpd/v2.0/). That URL is the resolution target of
// the dataset DOI and must never move, so the routing convention is pinned here
// rather than left to a default.

const PRODUCTION_SITE = 'https://data.chulapd.org';

const demo = process.env.CHECKPD_DEMO === '1';

/**
 * A demo build must not claim the production domain: canonical links and the
 * Dataset JSON-LD would point at a URL that does not resolve yet. Preview hosts
 * publish their own URL, so pick it up rather than asking anyone to configure
 * it. CHECKPD_SITE overrides everything, for a preview on some other host.
 */
function resolveSite() {
  if (process.env.CHECKPD_SITE) return process.env.CHECKPD_SITE;
  if (!demo) return PRODUCTION_SITE;
  if (process.env.CF_PAGES_URL) return process.env.CF_PAGES_URL;
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return 'http://localhost:4321';
}

const site = resolveSite();

/**
 * Vite refuses requests whose Host header it does not recognise, which is what
 * blocks a tunnel: ngrok forwards with Host set to its own domain, so every
 * visitor gets "Blocked request" instead of the site.
 *
 * These suffixes re-open the door for the dev and preview servers only.
 * Production is nginx serving static files and never runs this code, so the
 * host check is not protecting anything there. Listing suffixes rather than
 * setting `allowedHosts: true` keeps the check working against everything else.
 *
 * This belongs to Astro's own top-level `server`, not to `vite.server` — Astro
 * builds the dev and preview servers itself and ignores the Vite-level option,
 * silently, so a misplaced setting looks configured but blocks every visitor.
 */
const TUNNEL_HOSTS = [
  '.ngrok-free.app',
  '.ngrok.app',
  '.ngrok.io',
  '.trycloudflare.com',
  '.loca.lt',
  '.serveo.net',
];

const allowedHosts = [
  ...TUNNEL_HOSTS,
  ...(process.env.CHECKPD_SITE ? [new URL(process.env.CHECKPD_SITE).hostname] : []),
];

if (demo) {
  console.log(`\n  demo build — site: ${site}, noindex, preview banner on\n`);
}

export default defineConfig({
  site,
  output: 'static',
  trailingSlash: 'always',
  build: {
    format: 'directory',
    assets: 'assets',
  },
  devToolbar: { enabled: false },
  server: { allowedHosts },
  vite: {
    define: {
      'import.meta.env.PUBLIC_CHECKPD_DEMO': JSON.stringify(demo ? '1' : '0'),
    },
  },
});
