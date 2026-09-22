# daniel-site

郑晓东的个人网站。Astro 5 静态生成，内容全是 Markdown 和一个 JSON，发到 GitHub Pages。

- 首页 `/`：标题句 + 做过的三条 + 写过的三篇 + 拍过的最近五条
- `/works/`、`/works/<slug>/`：作品，每件四段（问题、做法、验证、边界），源在 `src/content/works/`
- `/writing/`、`/writing/<slug>/`：文章全文，源在 `src/content/writing/`，只有 `onsite: true` 的上站
- `/talks/`（讲过的）：播客《在路上》最近节目（`src/content/podcast/episodes.json`，从小宇宙公开页自动同步）+ 口播清单（`src/content/videos/videos.json`，有 `bvid` 的嵌 B 站播放器）；旧地址 `/videos/` 跳转过来
- `/about/`：能力块、工作之外、联系方式。不写公司名、不写年份、不写在职状态
- `/ai.txt`：给 AI 读的纯文本，从同一份内容生成

## 本地

```bash
npm install
npm run dev
```

## 规矩

- 首页不放任何读数（播放、阅读、粉丝）。验证栏只放定格的事实和别人的反应。
- 网站不出现简历里没有的东西，也不比简历更精确。
- 新视频：在 `videos.json` 加一条（id、date、title、cover、bvid）。新文章：在 `src/content/writing/` 放一个 md，frontmatter 写 `onsite: true`。推上去自动重建。
