#!/bin/zsh
# 每日同步：文章（知乎账本 上站=是）+ 视频（B 站清单）→ 有变化才 commit + push → GitHub Actions 自动重建
set -e
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
PY=/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
$PY scripts/sync_writing.py
$PY scripts/sync_videos.py
$PY scripts/sync_podcast.py
if [[ -n "$(git status --porcelain src/content public/covers)" ]]; then
  git add src/content public/covers
  git -c user.name="Daniel.Z" -c user.email="danielzheng19860726@gmail.com" commit -q -m "sync: $(date +%F) 内容同步"
  git push -q origin main
  echo "pushed $(date)"
else
  echo "nothing to sync $(date)"
fi
