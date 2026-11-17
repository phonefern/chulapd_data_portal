/**
 * Build the gated preview and serve it for a tunnel (ngrok, cloudflared, ...).
 *
 * Serves the BUILT site rather than the dev server: a tunnelled dev server ships
 * unminified sources and an HMR websocket that will not survive the hop, and it
 * is the dev build rather than the one that would be deployed.
 *
 * Usage:
 *   npm run share                              # canonical URLs -> localhost
 *   npm run share https://abc.ngrok-free.app   # canonical URLs -> the tunnel
 *
 * The URL only affects canonical/JSON-LD/sitemap. The build is noindex either
 * way, so starting without it is fine for a quick look.
 */
import { spawnSync, spawn } from 'node:child_process';

const site = process.argv[2] ?? process.env.CHECKPD_SITE;
const env = { ...process.env, CHECKPD_DEMO: '1' };
if (site) {
  try {
    env.CHECKPD_SITE = new URL(site).origin;
  } catch {
    console.error(`not a URL: ${site}`);
    process.exit(1);
  }
}

const build = spawnSync('npx', ['astro', 'build'], { stdio: 'inherit', shell: true, env });
if (build.status !== 0) process.exit(build.status ?? 1);

console.log(`
  Preview build ready${site ? ` for ${env.CHECKPD_SITE}` : ''}.

  In a second terminal:
      ngrok http 4321

  Anyone with the ngrok URL can open it, so send it only to people who should
  see an unreleased dataset record. The tunnel dies when you close this.
`);

spawn('npx', ['astro', 'preview', '--port', '4321'], { stdio: 'inherit', shell: true, env });
