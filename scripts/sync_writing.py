#!/usr/bin/env python3
"""从知乎账本同步「上站：是」的文章到网站。
账本：~/Projects/active/yage/periodic_jobs/zhihu_review/ledger.md
上不上站：条目里手写「上站：是/否」说了算；没写就看「主题线」，职场和 AI科技 自动上，其余不上。
上站必须写「站内标题」（给第一次来的人看的完整标题），没写的不上站，日志里打 NEED。
正文用知乎 CLI 拉本人全文，转 Markdown，写到 src/content/writing/<date>-<token>.md。
已存在且正文未变则不动；上站改成否则删除对应文件。"""
import re, os, sys, json, subprocess, pathlib, time
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
# 只解析「## 条目」以下；标题限定在一行内。09-25 教训：模板里的「### [标题缩写] · YYYY-MM-DD」不是数字日期，
# 旧正则 (.+?) 在 re.S 下跨行一路吞到第一个真实条目，站内标题变成整段模板。
s = s.split('\n## 条目\n', 1)[-1]
# 10-13：「·」两边的空格可有可无，10-11 起有条目写成「…）· 日期」，旧正则要求两边都有空格，整条被悄悄跳过。
entries = re.findall(r'^### ([^\n]+?)\s*·\s*(\d{4}-\d{2}-\d{2})\n(.*?)(?=^### |\Z)', s, re.S | re.M)
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
    fn = OUT / f'{date}-{token.group(1)}.md'
    # 10-13 教训：条目名是账本速记（模板写的就是「标题缩写」），拿它兜底，站上就出现「先问跟谁比」这种
    # 没上下文的标题。上站必须手写「站内标题」，没写就不上；已经在站上的保持原样，不删也不改。
    site_title = re.search(r'站内标题：\s*(.+)', body)
    if not site_title:
        print('NEED 站内标题，本篇不上站：', title.strip(), date)
        if fn.exists():
            keep.add(fn.name)
        continue
    site_title = site_title.group(1).strip()
    summary = re.search(r'主钉：\s*(.+)', body)
    summary = summary.group(1).strip() if summary else ''
    if not summary or '未填' in summary:
        print('WARN 主钉没填，转发卡片的描述会是空的：', title.strip(), date)
    keep.add(fn.name)
    time.sleep(4)   # 知乎 CLI 连着调会报 rate limit
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
