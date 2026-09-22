import { getCollection } from 'astro:content';
export async function GET() {
  const works = (await getCollection('works')).sort((a, b) => a.data.order - b.data.order);
  const writing = (await getCollection('writing', (e) => e.data.onsite)).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  const videos = (await getCollection('videos')).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
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
  lines.push('## 写过的');
  for (const p of writing) lines.push(`- ${ymd(p.data.date)} ${p.data.title} · ${p.data.source}`);
  lines.push('');
  lines.push('## 拍过的（每天一条口播，讲 HR 怎么用 AI）');
  for (const v of videos) lines.push(`- ${ymd(v.data.date)} ${v.data.title}${v.data.bvid ? ' · https://www.bilibili.com/video/' + v.data.bvid : ''}`);
  lines.push('');
  lines.push('## 联系');
  lines.push('邮箱 danielzheng19860726@gmail.com。完整履历可索取。');
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
