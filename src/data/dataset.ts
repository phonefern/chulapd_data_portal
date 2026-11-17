/**
 * Hand-maintained descriptor for the CheckPD v2.0 release.
 *
 * Everything that is a COUNT lives in summary.json and is derived from the
 * release files at build time (Local Agent Context Sec. 23 rule 9). Only
 * editorial and bibliographic facts belong in this file.
 *
 * Fields marked TODO are blocked on the clinical team / institution and are
 * rendered as visible placeholders rather than being quietly omitted.
 */

export interface Citation {
  vancouver: string;
  apa: string;
  bibtex: string;
}

export const portal = {
  name: 'CheckPD Data Portal',
  operator: "Parkinson's Disease Center of Excellence",
  institution: 'King Chulalongkorn Memorial Hospital, Thai Red Cross Society',
  contactEmail: 'TODO-portal-contact@chulapd.org',
} as const;

export const dataset = {
  id: 'checkpd',
  version: '2.0',
  /** Frozen DOI resolution target. Never change this path. */
  path: '/datasets/checkpd/v2.0/',
  title:
    'CheckPD v2.0: A Smartphone-Based Multimodal Dataset for ' +
    "Parkinson's Disease Screening and Digital Biomarker Research",
  shortTitle: 'CheckPD v2.0',
  tagline:
    'Real-world, clinician-confirmed smartphone assessments for ' +
    "Parkinson's disease screening research.",

  /** Not yet released. Drives the pre-release banner. */
  status: 'in-preparation' as 'in-preparation' | 'released',
  releaseDate: null as string | null,

  accessLevel: 'Credentialed',
  license: 'TODO - pending institutional decision',
  irb: 'TODO - IRB approval number pending',

  authors: ['TODO - author list pending'],
  publisher: 'Thai Red Cross Society Data Portal',

  /**
   * Short-term DOI bridge: a Zenodo record carrying documentation and the
   * access protocol only, pointing back at this landing page. The dataset files
   * themselves are never deposited there.
   *
   * Long-term: an institutional DataCite DOI resolving to the same URL.
   */
  doi: {
    zenodo: null as string | null,
    datacite: null as string | null,
    /** What the Zenodo record is allowed to contain. */
    zenodoRecordTitle: 'CheckPD v2.0: Dataset Documentation and Access Record',
    zenodoContents: [
      'README.md',
      'data_dictionary.csv',
      'questionnaire_schema.csv',
      'file_manifest.csv',
      'validation_summary.csv',
      'data_access_protocol.pdf',
      'sample_data.zip',
    ],
  },

  // Dual-tap and pinch-to-size were withdrawn from the public dataset: their
  // circle-size calibration is not comparable across handsets, so the recorded
  // geometry cannot be interpreted between participants.
  modalityDocs: [
    { slug: 'voice', label: 'Voice', blurb: 'Sustained phonation and connected speech, 16 kHz mono WAV.' },
    { slug: 'tremor-resting', label: 'Tremor - resting', blurb: 'Six-channel smartphone inertial-sensor recording.' },
    { slug: 'tremor-postural', label: 'Tremor - postural', blurb: 'Six-channel smartphone inertial-sensor recording.' },
    { slug: 'balance', label: 'Balance', blurb: 'Six-channel smartphone inertial-sensor recording.' },
    { slug: 'gaitwalk', label: 'Gait', blurb: 'Six-channel smartphone inertial-sensor recording.' },
    { slug: 'questionnaire', label: 'Questionnaire', blurb: 'Binary screening questionnaire with Thai and English item text.' },
  ],
} as const;

/** Current portal focus. Frozen v2.0 citation/access descriptors stay above. */
export const currentDataset = {
  version: '2.1',
  path: '/datasets/checkpd/v2.1/',
  shortTitle: 'CheckPD v2.1',
  title: 'CheckPD v2.1: Smartphone-Based Multimodal Dataset',
  tagline: 'Clinician-confirmed smartphone assessments with processed voice and documented sensor completeness.',
  status: 'in-preparation' as const,
  accessLevel: 'Credentialed',
} as const;

const doiText = (d: string | null) => d ?? '<DOI pending>';

/**
 * Citations always name the permanent institutional URL, even in a preview
 * build. A citation records where the dataset will live for good; pointing it at
 * a throwaway preview host would be wrong in a way a reader could not detect.
 * This is the one place that should not follow `Astro.site`.
 */
const PERMANENT_URL = 'https://data.chulapd.org';

export function citations(doi: string | null): Citation {
  const authors = dataset.authors.join(', ');
  const year = dataset.releaseDate?.slice(0, 4) ?? '<year>';

  return {
    vancouver:
      `${authors}. ${dataset.title}. ${dataset.publisher}; ${year}. ` +
      `doi:${doiText(doi)}`,
    apa:
      `${authors} (${year}). ${dataset.title} [Data set]. ` +
      `${dataset.publisher}. https://doi.org/${doiText(doi)}`,
    bibtex: [
      `@dataset{checkpd_v2_${year},`,
      `  title     = {${dataset.title}},`,
      `  author    = {${authors}},`,
      `  year      = {${year}},`,
      `  version   = {${dataset.version}},`,
      `  publisher = {${dataset.publisher}},`,
      `  doi       = {${doiText(doi)}},`,
      `  url       = {${PERMANENT_URL}${dataset.path}},`.slice(0, -1),
      `}`,
    ].join('\n'),
  };
}
