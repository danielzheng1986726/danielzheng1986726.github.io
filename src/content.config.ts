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
    kind: z.enum(['answer', 'article']).default('article'),
    question: z.string().default(''),
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

const podcast = defineCollection({
  loader: file('./src/content/podcast/episodes.json'),
  schema: z.object({ id: z.string(), date: z.coerce.date(), title: z.string(), minutes: z.number(), url: z.string().url() }),
});

const tools = defineCollection({
  loader: file('./src/content/tools/tools.json'),
  schema: z.object({
    id: z.string(),                 // 同时是 daniel-tools 仓库里的文件夹名
    name: z.string(),
    form: z.string(),               // 形态：命令行 / 浏览器脚本 / iOS App …
    status: z.enum(['在用', '用过一次', '已停']),
    pain: z.string(),               // 一句痛点
    updated: z.string(),            // 最后改动 YYYY-MM
    video: z.string().optional(),   // 讲解短片，放在 public/clips/
  }),
});

export const collections = { works, writing, videos, podcast, tools };
