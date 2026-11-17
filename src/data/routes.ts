/**
 * Every route the portal publishes, for the sitemap.
 *
 * Kept as an explicit list rather than derived from the filesystem: dynamic
 * routes would need expanding anyway, and an explicit list is reviewable.
 * `npm run check:routes` compares it against what the build actually emitted,
 * so it cannot silently drift.
 *
 * Modality documentation pages are expanded from the content collection at
 * build time and are deliberately absent here.
 */
export const STATIC_ROUTES = [
  '/',
  '/datasets/',
  '/datasets/checkpd/v2.0/',
  '/datasets/checkpd/v2.0/access/',
  '/datasets/checkpd/v2.0/citation/',
  '/datasets/checkpd/v2.0/documentation/',
  '/datasets/checkpd/v2.0/files/',
  '/datasets/checkpd/v2.1/',
  '/datasets/checkpd/versions/',
  '/documentation/',
  '/publications/',
  '/access/',
  '/about/',
  '/contact/',
  '/th/',
  '/th/about/',
  '/th/access/',
] as const;
