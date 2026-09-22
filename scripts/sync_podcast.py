#!/usr/bin/env python3
"""从小宇宙公开页同步播客《在路上》的最近节目到 src/content/podcast/episodes.json（不需要登录）。
封面第一次同步时存到 public/shots/podcast-cover.jpg。"""
import re, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
PID = '66cd42d8f78678cbe75bb69f'
OUT = ROOT / 'src/content/podcast/episodes.json'
COVER = ROOT / 'public/shots/podcast-cover.jpg'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh) Chrome/120'}
html = urllib.request.urlopen(urllib.request.Request(f'https://www.xiaoyuzhoufm.com/podcast/{PID}', headers=UA), timeout=30).read().decode()
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
pod = json.loads(m.group(1))['props']['pageProps']['podcast']
eps = []
for e in pod.get('episodes', [])[:15]:
    eps.append({'id': e['eid'], 'date': e['pubDate'][:10], 'title': e['title'], 'minutes': round((e.get('duration') or 0) / 60),
                'url': f"https://www.xiaoyuzhoufm.com/episode/{e['eid']}"})
OUT.parent.mkdir(parents=True, exist_ok=True)
new = json.dumps(eps, ensure_ascii=False, indent=2)
if not OUT.exists() or OUT.read_text() != new:
    OUT.write_text(new); print('episodes.json updated', len(eps))
else:
    print('episodes.json unchanged')
if not COVER.exists():
    pic = (pod.get('image') or {}).get('picUrl')
    if pic:
        COVER.write_bytes(urllib.request.urlopen(urllib.request.Request(pic, headers=UA), timeout=30).read()); print('cover saved')
