---
name: hxz-news-reader
description: HXZ News Reader 仓库内的开发指引。维护 feeds/sources.yaml，运行 scripts/update_news.py，调试单源，处理 GitHub Action 失败。Triggers in-repo work only.
---

# HXZ News Reader — In-Repo Skill

> 仓库根目录加载这个文件做开发指引。Claude Code 全局的 skill 文件在 `~/.claude/skills/hxz-news-reader/SKILL.md`，两个是同一份契约。

## 工作流

1. 改信源：编辑 `feeds/sources.yaml`
2. 单源探测：`python scripts/update_news.py --probe-only <id>`
3. 全量跑：`python scripts/update_news.py --output-dir data --window-hours 168`
4. 看状态：`cat data/source-status.json | jq '.summary'`
5. 本地预览：`python -m http.server 8080`
6. 提交：`git add -A && git commit -m "..." && git push`

## 上线状态（2026-06-10）

- **GitHub Pages**：https://blandybaran527-boop.github.io/Content-Engineering/（main 分支根目录直发，已开 HTTPS）
- **自动跑**：`.github/workflows/update.yml` 每天 UTC 22:00 = 北京 06:00 抓一次，自动 commit `data/` 并触发 Pages 重建
- **抓取窗口**：默认 168h（一周）；Substack/Newsletter 更新频次低，48h 经常空
- **手动触发**：Actions 页面 → update-news → Run workflow

## 全文抓取（Substack / Newsletter）

- `RawItem` 有 `content_html` 字段，从 RSS `entry.content[0].value`（即 `content:encoded`）取原文 HTML
- 失败回退：用 `entry.summary` 兜底（不至于空字段）
- 4 个 Substack 信源（lennys / generalist / newcomer / import-ai）实测均带 `content:encoded`，无需爬正文页
- `index.html` 渲染时：`content_html.length > 200` 才显示「展开全文 ▾」按钮，避免空内容/纯链接误展开

## 默认抓取层（v0 已跑通）

只允许把 **官方原生 RSS / 自托管稳定 RSS** 设为 `default: true`：

- `hackernews` / `import-ai` / `arxiv-cs-ai` / `latent-space`
- `lennys` / `generalist` / `newcomer`

要把任何其他源加入默认层，必须先在本地连续 7 天通过单源探测无失败。

## X / 公众号 / 播客

默认 `default: false`，靠开关启用：

- `--enable-x` + `X_BEARER_TOKEN` → 用 X 官方 API
- `--enable-wechat` → 走每条信源里填的 `wechat2rss.xlab.app` 链接
- `--enable-podcast` → 抓 podcast RSS（小宇宙 / Spotify / Apple Podcast 镜像）

## 失败处理优先级

1. 看 `source-status.json` 里失败信源的 `error` 字段
2. HTTP 403 / 404：换 RSS 源或下调 `default: false`
3. 第三方桥（Nitter/wechat2rss）失败：标记 `manual_only`，不要在公开默认层重新启用
4. X API 失败：检查 Token 与速率限制；写入 `source-status.json` 的 error 字段而不是 raise

## 不要做

- 不要把私有 OPML / Cookies / Token / 邮箱地址写进任何仓库文件
- 不要在 `default: true` 集合里加任何需要爬虫绕过 Cloudflare 的源
- 不要在 GitHub Action 里默认开启 `--enable-x`（除非 Secret 真的存在）
