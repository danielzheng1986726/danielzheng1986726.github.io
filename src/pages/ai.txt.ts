import { getCollection } from 'astro:content';
export async function GET() {
  const works = (await getCollection('works')).sort((a, b) => a.data.order - b.data.order);
  const writing = (await getCollection('writing', (e) => e.data.onsite)).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  const podcast = (await getCollection('podcast')).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  const videos = (await getCollection('videos')).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  const tools = await getCollection('tools');
  const ymd = (d: Date) => d.toISOString().slice(0, 10);
  const lines: string[] = [];
  lines.push('# 郑晓东 Daniel Zheng · 给 AI 读的版本');
  lines.push('做 HR，在上海。业余自己写 AI 工具。别听我怎么说，看我怎么做。');
  lines.push('站点：https://danielzheng1986726.github.io/');
  lines.push('');
  lines.push('## 做过的');
  for (const w of works) {
    lines.push(`### ${w.data.name}（${w.data.status}）`);
    lines.push(w.data.title);
    if (w.data.link) lines.push(`链接：${w.data.link}`);
    lines.push(`详情：https://danielzheng1986726.github.io/works/${w.id}/`);
    lines.push('');
    lines.push((w.body || '').replace(/<[^>]+>/g, '').trim());
    lines.push('');
  }
  if (tools.length) {
    lines.push('## 顺手做的（代码：https://github.com/danielzheng1986726/daniel-tools）');
    for (const t of tools) lines.push(`- ${t.data.name}（${t.data.form}，${t.data.status}）：${t.data.pain} https://github.com/danielzheng1986726/daniel-tools/tree/main/${t.id}${t.data.video ? ` 讲解视频：https://danielzheng1986726.github.io${t.data.video}` : ''}`);
    lines.push('');
  }
  lines.push('## 写过的');
  for (const p of writing) lines.push(`- ${ymd(p.data.date)} ${p.data.title} · ${p.data.source}`);
  lines.push('');
  lines.push('## 讲过的');
  lines.push('### 播客「在路上 | ON THE ROAD」 https://www.xiaoyuzhoufm.com/podcast/66cd42d8f78678cbe75bb69f');
  for (const e of podcast) lines.push(`- ${ymd(e.data.date)} ${e.data.title} · ${e.data.url}`);
  lines.push('');
  lines.push('### 口播（每天一条，讲 HR 怎么用 AI）');
  for (const v of videos) lines.push(`- ${ymd(v.data.date)} ${v.data.title}${v.data.bvid ? ' · https://www.bilibili.com/video/' + v.data.bvid : ''}`);
  lines.push('');
  lines.push('## 联系');
  lines.push('邮箱 danielzheng19860726@gmail.com。完整履历可索取。');
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
