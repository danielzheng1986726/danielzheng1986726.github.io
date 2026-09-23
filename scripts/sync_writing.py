#!/usr/bin/env python3
"""从知乎账本同步「上站：是」的文章到网站。
账本：~/Projects/active/yage/periodic_jobs/zhihu_review/ledger.md
上不上站：条目里手写「上站：是/否」说了算；没写就看「主题线」，职场和 AI科技 自动上，其余不上。可选：站内标题（没有就用条目标题）。
正文用知乎 CLI 拉本人全文，转 Markdown，写到 src/content/writing/<date>-<token>.md。
已存在且正文未变则不动；上站改成否则删除对应文件。"""
import re, os, sys, json, subprocess, pathlib
sys.path.insert(0, os.path.dirname(__file__))
from zhihu_html_to_md import to_md
ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = pathlib.Path.home() / 'Projects/active/yage/periodic_jobs/zhihu_review/ledger.md'
CLI = pathlib.Path.home() / 'Library/Application Support/zhihu-cli/current/zhihu-cli'
OUT = ROOT / 'src/content/writing'
AUTO_LINES = {'职场', 'AI科技'}   # 这两条主题线默认上站；想排除就在条目里写「上站：否」
s = LEDGER.read_text()
_r = subprocess.run([str(CLI), 'me', 'contents', '--type', 'answer', '--sort', 'ts', '--order', 'desc', '--limit', '50'], capture_output=True, text=True)
try:
    QTITLE = {}
    for it in json.loads(_r.stdout)['Data']['Items']:
        m_ = re.search(r'/answer/(\d+)', it.get('Url', ''))
        if m_: QTITLE[m_.group(1)] = it.get('Title', '')
except Exception:
    QTITLE = {}
entries = re.findall(r'^### (.+?) · (\d{4}-\d{2}-\d{2})\n(.*?)(?=^### |\Z)', s, re.S | re.M)
keep = set()
for title, date, body in entries:
    link = re.search(r'链接：(https?://\S+)', body)
    onsite = re.search(r'上站：\s*(是|否)', body)
    line = re.search(r'主题线：\s*(\S+)', body)
    if not link:
        continue
    if onsite:                      # 手写的「是 / 否」说了算
        if onsite.group(1) != '是':
            continue
    elif not (line and line.group(1) in AUTO_LINES):   # 没手写就看主题线
        continue
    url = link.group(1)
    token = re.search(r'(\d{10,})/?$', url)
    if not token:
        print('skip, no token', url); continue
    site_title = re.search(r'站内标题：\s*(.+)', body)
    site_title = site_title.group(1).strip() if site_title else title.strip()
    summary = re.search(r'主钉：\s*(.+)', body)
    summary = summary.group(1).strip() if summary else ''
    fn = OUT / f'{date}-{token.group(1)}.md'
    keep.add(fn.name)
    r = subprocess.run([str(CLI), 'me', 'content', '--content-url', url], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        assert d.get('Code') == 0
    except Exception:
        print('fetch failed', url, r.stdout[:200], r.stderr[:200]); continue
    md = to_md(d['Data']['Body'])
    kind = 'answer' if '/answer/' in url else 'article'
    question = QTITLE.get(token.group(1), '') if kind == 'answer' else ''
    if kind == 'answer' and not question and fn.exists():   # 拉不到就沿用上次的
        m0 = re.search(r'^question: (.+)$', fn.read_text(), re.M)
        question = json.loads(m0.group(1)) if m0 else ''
    fm = f'''---
title: {json.dumps(site_title, ensure_ascii=False)}
kind: {kind}
question: {json.dumps(question, ensure_ascii=False)}
date: {date}
source: {url}
platform: 知乎
onsite: true
summary: {json.dumps(summary, ensure_ascii=False)}
---

'''
    new = fm + md
    if fn.exists() and fn.read_text() == new:
        continue
    fn.write_text(new); print('wrote', fn.name)
# 下架：账本里不再是「是」的（只删本脚本命名格式的文件）
for f in OUT.glob('20*-[0-9]*.md'):
    if f.name not in keep:
        f.unlink(); print('removed', f.name)
