import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

const works = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/works' }),
  schema: z.object({
    title: z.string(),
    name: z.string(),
    status: z.enum(['在运行', '方法', '进行中', '已停']),
    order: z.number(),
    cover: z.string().optional(),
    link: z.string().optional(),
    linkText: z.string().optional(),
    tags: z.array(z.string()).default([]),
  }),
});

const writing = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/writing' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    source: z.string().url(),
    platform: z.string().default('知乎'),
    onsite: z.boolean().default(true),
    summary: z.string().optional(),
  }),
});

const videos = defineCollection({
  loader: file('./src/content/videos/videos.json'),
  schema: z.object({
    id: z.string(),
    date: z.coerce.date(),
    title: z.string(),
    cover: z.string().optional(),
    bvid: z.string().optional(),
    xhs: z.string().optional(),
    douyin: z.string().optional(),
  }),
});

export const collections = { works, writing, videos };
