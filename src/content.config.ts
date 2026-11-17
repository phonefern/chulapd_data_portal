import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const modalities = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/modalities' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    summary: z.string(),
    flag: z.string(),
    status: z.enum(['complete', 'partial']),
  }),
});

export const collections = { modalities };
