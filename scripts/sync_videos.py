#!/usr/bin/env python3
"""从口播线的 B 站清单同步到网站的 videos.json。
源：~/Projects/active/talking-head-shorts/_bilibili/manifest.json（做视频流程写入：slug/date/title/cover/bvid/xhs）
封面缩到 540x960 拷进 public/covers/<slug>.jpg。"""
import json, pathlib, os
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = pathlib.Path.home() / 'Projects/active/talking-head-shorts/_bilibili/manifest.json'
OUT = ROOT / 'src/content/videos/videos.json'
COV = ROOT / 'public/covers'
man = json.load(open(SRC))
old = {e['id']: e for e in json.load(open(OUT))} if OUT.exists() else {}
out = []
for m in man:
    e = {'id': m['slug'], 'date': m['date'], 'title': m['title']}
    if m.get('cover') and os.path.exists(m['cover']):
        dst = COV / f"{m['slug']}.jpg"
        if not dst.exists():
            im = Image.open(m['cover']).convert('RGB').resize((540, 960), Image.LANCZOS)
            im.save(dst, 'JPEG', quality=80, optimize=True)
        e['cover'] = f"/covers/{m['slug']}.jpg"
    for k in ('bvid', 'xhs', 'douyin'):
        if m.get(k): e[k] = m[k]
        elif old.get(m['slug'], {}).get(k): e[k] = old[m['slug']][k]
    out.append(e)
new = json.dumps(out, ensure_ascii=False, indent=2)
if not OUT.exists() or OUT.read_text() != new:
    OUT.write_text(new); print('videos.json updated', len(out))
else:
    print('videos.json unchanged')
