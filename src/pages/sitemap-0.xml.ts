import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { STATIC_ROUTES } from '../data/routes';
import { dataset } from '../data/dataset';
import { counterpart, hasThai, langOf } from '../data/i18n';

/**
 * Built from `Astro.site`, so a demo deployment never advertises production
 * URLs. Translated pages carry xhtml:link alternates in both directions.
 */
export const GET: APIRoute = async ({ site }) => {
  const modalities = await getCollection('modalities');
  const routes = [
    ...STATIC_ROUTES,
    ...modalities.map((m) => `${dataset.path}documentation/${m.data.slug}/`),
  ].sort();

  const abs = (route: string) => new URL(route.slice(1), site).href;

  const entries = routes.map((route) => {
    const paired = langOf(route) === 'th' || hasThai(route);
    const alternates = paired
      ? [route, counterpart(route)]
          .map(
            (r) =>
              `\n    <xhtml:link rel="alternate" hreflang="${langOf(r)}" href="${abs(r)}"/>`,
          )
          .join('')
      : '';
    return `  <url><loc>${abs(route)}</loc>${alternates}${alternates ? '\n  ' : ''}</url>`;
  });

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${entries.join('\n')}
</urlset>
`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
  );
};
