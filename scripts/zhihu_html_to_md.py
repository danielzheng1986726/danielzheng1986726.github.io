#!/usr/bin/env python3
"""把知乎 CLI `me content` 返回的 Body（HTML）转成简单 Markdown。只处理知乎回答里常见的标签。"""
import html, re, sys, json

def to_md(body: str) -> str:
    s = body
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', s, flags=re.S)
    s = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', s, flags=re.S)
    s = re.sub(r'<(b|strong)[^>]*>(.*?)</\1>', r'**\2**', s, flags=re.S)
    s = re.sub(r'<(i|em)[^>]*>(.*?)</\1>', r'*\2*', s, flags=re.S)
    def _a(m):
        href = html.unescape(m.group(1)); text = re.sub(r'<[^>]+>', '', m.group(2)).strip().strip('\u200b')
        if re.match(r'^[（(\s]*https?://', text) or href.split('?target=')[-1] in text:
            return href  # 正文里本来就是裸链接，不套一层
        return f'[{text}]({href})'
    s = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', _a, s, flags=re.S)
    s = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n' + '\n'.join('> ' + l for l in re.sub(r'</?p[^>]*>', '\n', m.group(1)).strip().split('\n')) + '\n', s, flags=re.S)
    s = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', s, flags=re.S)
    s = re.sub(r'</?(ul|ol)[^>]*>', '\n', s)
    s = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', s, flags=re.S)
    s = re.sub(r'<figure[^>]*>.*?</figure>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    # 知乎外链跳转还原
    s = re.sub(r'https://link\.zhihu\.com/\?target=([^)\s]+)', lambda m: html.unescape(__import__('urllib.parse').parse.unquote(m.group(1))), s)
    s = re.sub(r'\n{3,}', '\n\n', s).strip() + '\n'
    return s

if __name__ == '__main__':
    d = json.load(open(sys.argv[1]))
    print(to_md(d['Data']['Body']))
