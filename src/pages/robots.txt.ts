import type { APIRoute } from 'astro';
import { isDemo } from '../data/deploy';

/**
 * Generated rather than kept in public/ so a demo build can close the door.
 *
 * The production file deliberately disallows nothing. The release files are not
 * served from this origin — they sit behind nginx secure_link — and naming their
 * path in robots.txt would advertise it.
 */
export const GET: APIRoute = ({ site }) => {
  const body = isDemo
    ? ['User-agent: *', 'Disallow: /', ''].join('\n')
    : ['User-agent: *', 'Allow: /', `Sitemap: ${new URL('sitemap-index.xml', site)}`, ''].join('\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
