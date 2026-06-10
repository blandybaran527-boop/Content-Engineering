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
- **公众号通道已上线**：12 个公众号通过本地 WeWe-RSS 桥接入（见下节），189 条总文章中 69 条来自公众号
- **抓取窗口**：默认 168h（一周）；Substack/Newsletter 更新频次低，48h 经常空；个别公众号（暗涌Waves）168h 也可能为空（号本身更新慢），**不要**因此扩窗口或换号
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

X 和 podcast 默认 `default: false`，公众号在 v0.2 起默认 `default: true`（因为接的是本地 WeWe-RSS）：

- `--enable-x` + `X_BEARER_TOKEN` → 用 X 官方 API
- `--enable-wechat` → 走本地 WeWe-RSS（`127.0.0.1:4000`），见下一节
- `--enable-podcast` → 抓 podcast RSS（小宇宙 / Spotify / Apple Podcast 镜像）
- `--enable-youtube` → 抓 YouTube 频道 RSS + youtube-transcript-api 字幕，**必须挂住宅 IP**（见下下节）

## 公众号通道（本地 WeWe-RSS）

完整命令清单 + mpId 对照表见 `docs/SOURCES.md` D 节，要点：

- **为什么不用 wechat2rss.xlab.app**：公共版只收录 12 个目标号中的 4 个，缺 8 个 AI 自媒体号无法等收录
- **本地服务位置**：`/Users/admin/Downloads/wewe-rss-work/wewe-rss`
- **启动**（每天第一次抓之前确认它跑着）：
  ```bash
  cd /Users/admin/Downloads/wewe-rss-work/wewe-rss
  DATABASE_URL="file:../data/wewe-rss.db" DATABASE_TYPE="sqlite" \
    AUTH_CODE="wewe2026" SERVER_ORIGIN_URL="http://127.0.0.1:4000" \
    pnpm run start:server
  ```
- **管理界面**：`http://127.0.0.1:4000/dash`（AuthCode: `wewe2026`）
- **加号**：浏览器粘贴 mp.weixin 文章链接 / 或调 `/trpc/platform.getMpInfo` + `/trpc/feed.add` API（详见 SOURCES.md）
- **严禁连续手动调 refresh**：短时间反复 `feed.refreshArticles` 会触发微信读书 `WeReadError401`，账号 token 实际失效 —— SQL 改 status=1 也立刻被打回，唯一恢复办法是**用户重新扫码**。加完订阅 fire 1 次全量 refresh 就够，剩下交给 WeWe-RSS 自带 cron（默认 5:35 / 17:35）。新加的号首轮没拉到不要补，等下一轮自然进
- **本地代理踩坑**：`127.0.0.1` 走系统代理（梯子）会 502；`update_news.py` 在 import 段自动注入 `NO_PROXY="127.0.0.1,localhost"`，命令行手动 curl 时需要带 `--noproxy '*'`

## YouTube 通道（频道 RSS + youtube-transcript-api，2026-06 新增）

### 决策背景

YouTube 在 2024–2025 上线 SABR + PO Token 反爬：机房/常见 VPN 出口 IP 调 `timedtext` 返回 HTTP 200 + 空字节；youtube-transcript-api 直接 `RequestBlocked`。**必须挂住宅 IP** 才能稳定抓字幕原文。Whisper 本地转写方案因为吃 Mac 性能被否，最终选住宅 IP 直抓原字幕。

### 一次性配置

- **梯子**：Clash Verge 切到「🏠 美国家宽选这个」（静态住宅节点，实测 AS7029 Windstream，能拿到字幕原文）
- **依赖**：`pip install youtube-transcript-api`（已在 `requirements.txt`）

### 当前 7 个 YouTube 频道

`feeds/sources.yaml` 的 `D2.` 节，全部 `type: youtube`，`default: false`，需要 `--enable-youtube` 才会跑。`max_videos: 1` 字段限制每个频道每次最多抓 1 条新视频。

The TED AI Show 在 YouTube 上无独立频道（音频播客发在 Apple / Spotify），sources.yaml 里以 TODO 注释占位，若要收录走 audio + Whisper 路线。

### 每日抓取

```bash
python scripts/update_news.py --enable-youtube --window-hours 168 --output-dir data
```

- 字幕拼成 `<p>...</p>` 段落写入 `content_html`，`index.html` 的「展开全文」组件直接渲染
- 字幕抓不到不阻塞整源；summary 末尾加 `[transcript fail: XXX]` 标记，元数据仍记录

### 不要做

- 不要在调试时反复 yt-dlp / transcript-api 同一 video / channel —— 连续命中触发 YouTube 反爬，住宅 IP 链路被降级，整批视频空字节
- 不要凭印象写 channel_id，用 `curl https://www.youtube.com/@HANDLE | grep -oE 'youtube\.com/channel/UC[A-Za-z0-9_-]{22}'` 一次性拿
- 新加 channel 必须先 `--probe-only` 单测，再写进默认抓取

## 失败处理优先级

1. 看 `source-status.json` 里失败信源的 `error` 字段
2. HTTP 403 / 404：换 RSS 源或下调 `default: false`
3. 第三方桥（Nitter/wechat2rss）失败：标记 `manual_only`，不要在公开默认层重新启用
4. X API 失败：检查 Token 与速率限制；写入 `source-status.json` 的 error 字段而不是 raise

## 不要做

- 不要把私有 OPML / Cookies / Token / 邮箱地址 / SQLite 库（含 WeWe-RSS 读书账号 token）写进任何仓库文件
- 不要在 `default: true` 集合里加任何需要爬虫绕过 Cloudflare 的源
- 不要在 GitHub Action 里默认开启 `--enable-x`（除非 Secret 真的存在）
- 不要短时间内反复调 WeWe-RSS 的 `feed.refreshArticles`（参见上一节）
- 不要因为某个公众号 168h 没文章就扩窗口或换号 —— 信源不可达只换通道不换源（详见 `docs/SOURCES.md` 通道选型记录）
