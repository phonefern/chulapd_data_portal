/**
 * Deployment mode.
 *
 * The portal is built twice from the same source: once for the institutional
 * server, and once as a shareable preview on a throwaway host.
 *
 * A preview build of this site is not a neutral thing. It carries the Thai Red
 * Cross emblem, the hospital's name, and a dataset record whose licence, DOI and
 * ethics approval are still unresolved — so an indexed preview reads as an
 * official launch. Demo mode therefore does three things at once: it keeps
 * crawlers out, it points canonical URLs at the host actually serving the page
 * instead of at a domain that does not exist yet, and it says on every page that
 * this is a preview.
 *
 *   npm run build         production — data.chulapd.org, indexable
 *   npm run build:demo    preview    — noindex, banner, deploy-host URLs
 *
 * Demo builds resolve their own URL from the host's environment, so no
 * configuration is needed on Cloudflare Pages or Vercel.
 */

export const PRODUCTION_SITE = 'https://data.chulapd.org';

/**
 * Resolved at build time in astro.config.mjs, which is the only place with
 * access to process.env. Exposed through import.meta.env so pages can read it.
 */
export const isDemo = import.meta.env.PUBLIC_CHECKPD_DEMO === '1';

export const banner = {
  en: {
    label: 'Preview',
    text: 'This is an internal preview build, not an official release. The dataset is not yet published, and the licence, DOI and ethics approval shown as Pending are still being decided.',
  },
  th: {
    label: 'ตัวอย่าง',
    text: 'หน้านี้เป็นเวอร์ชันตัวอย่างสำหรับตรวจสอบภายใน ไม่ใช่การเผยแพร่อย่างเป็นทางการ ชุดข้อมูลยังไม่ได้เปิดให้เข้าถึง และรายการที่แสดงว่ายังไม่สรุปอยู่ระหว่างการพิจารณาของสถาบัน',
  },
} as const;
