/**
 * Bilingual surface for the portal.
 *
 * Scope is deliberately partial. The dataset record — landing page, files,
 * modality documentation, citation — stays English only: it is the scientific
 * record, it is the DOI resolution target, and the accompanying manuscript is
 * English (CheckPD_Local_Agent_Context.md, Primary language).
 *
 * Thai covers the orientation pages that Thai-speaking readers actually need:
 * what the portal is, who runs it, and how access works. Those are the pages an
 * institutional stakeholder, ethics reviewer or Thai researcher reads first.
 *
 * Adding a Thai page means adding a `PAIRS` entry so the language switcher can
 * find it. A page with no pair sends the switcher to the Thai home page rather
 * than to a 404.
 */

export type Lang = 'en' | 'th';

/** English route → Thai route, for pages that exist in both languages. */
export const PAIRS: Record<string, string> = {
  '/': '/th/',
  '/about/': '/th/about/',
  '/access/': '/th/access/',
};

const REVERSE: Record<string, string> = Object.fromEntries(
  Object.entries(PAIRS).map(([en, th]) => [th, en]),
);

export const langOf = (pathname: string): Lang =>
  pathname === '/th' || pathname.startsWith('/th/') ? 'th' : 'en';

/**
 * Where the language switcher points from `pathname`.
 * Falls back to the Thai home page for English pages with no translation, and
 * to the English home page for the reverse — never to a dead URL.
 */
export function counterpart(pathname: string): string {
  const path = pathname.endsWith('/') ? pathname : `${pathname}/`;
  if (langOf(path) === 'th') return REVERSE[path] ?? '/';
  return PAIRS[path] ?? '/th/';
}

export const hasThai = (pathname: string): boolean =>
  Object.prototype.hasOwnProperty.call(PAIRS, pathname.endsWith('/') ? pathname : `${pathname}/`);

interface NavItem {
  href: string;
  label: string;
}

export const NAV: Record<Lang, NavItem[]> = {
  en: [
    { href: '/datasets/', label: 'Datasets' },
    { href: '/documentation/', label: 'Documentation' },
    { href: '/publications/', label: 'Publications' },
    { href: '/access/', label: 'Access' },
    { href: '/about/', label: 'About' },
  ],
  th: [
    { href: '/datasets/', label: 'ชุดข้อมูล' },
    { href: '/documentation/', label: 'เอกสารประกอบ' },
    { href: '/publications/', label: 'ผลงานตีพิมพ์' },
    { href: '/th/access/', label: 'การขอใช้ข้อมูล' },
    { href: '/th/about/', label: 'เกี่ยวกับเรา' },
  ],
};

export const UI = {
  en: {
    brandName: 'CheckPD Data Portal',
    brandOrg: "Parkinson's Disease Center of Excellence · Thai Red Cross Society",
    skip: 'Skip to content',
    primaryNav: 'Primary',
    footerNav: 'Footer',
    themeToggle: 'Switch colour theme',
    switchTo: 'ภาษาไทย',
    switchToLabel: 'อ่านหน้านี้เป็นภาษาไทย',
    footerLinks: [
      { href: '/access/', label: 'Access policy' },
      { href: '/access/#dua', label: 'Data use agreement' },
      { href: '/documentation/', label: 'Documentation' },
      { href: '/contact/', label: 'Contact' },
    ],
    generatedNote: 'Figures on this site are generated from the release files at build time.',
    lastBuild: 'Last build',
    partialNotice:
      'The dataset record, documentation and citation pages are published in English only.',
  },
  th: {
    brandName: 'CheckPD Data Portal',
    brandOrg: 'ศูนย์ความเป็นเลิศทางการแพทย์โรคพาร์กินสันฯ · สภากาชาดไทย',
    skip: 'ข้ามไปยังเนื้อหา',
    primaryNav: 'เมนูหลัก',
    footerNav: 'เมนูท้ายหน้า',
    themeToggle: 'สลับธีมสีของหน้าเว็บ',
    switchTo: 'English',
    switchToLabel: 'Read this page in English',
    footerLinks: [
      { href: '/th/access/', label: 'นโยบายการเข้าถึงข้อมูล' },
      { href: '/access/#dua', label: 'ข้อตกลงการใช้ข้อมูล' },
      { href: '/documentation/', label: 'เอกสารประกอบ' },
      { href: '/contact/', label: 'ติดต่อ' },
    ],
    generatedNote: 'ตัวเลขทั้งหมดบนเว็บไซต์นี้สร้างจากไฟล์ชุดข้อมูลจริงในขั้นตอน build',
    lastBuild: 'build ล่าสุด',
    partialNotice:
      'หน้ารายละเอียดชุดข้อมูล เอกสารทางเทคนิค และการอ้างอิง เผยแพร่เป็นภาษาอังกฤษเท่านั้น',
  },
} as const;
