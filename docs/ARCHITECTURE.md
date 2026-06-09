# Architecture

## 两层结构（与 ai-news-radar 一致）

```
┌─────────────────────────────────────────────────┐
│  默认层 (Default Layer)                          │
│  - 公开仓库 fork 后零配置可跑                     │
│  - 仅官方原生 RSS（HN / arXiv / Substack）       │
│  - 失败一律不阻塞                                 │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│  进阶层 (Advanced Layer)                         │
│  - X API（需要 X_BEARER_TOKEN）                  │
│  - wechat2rss / RSSHub / Nitter 公共桥           │
│  - 自托管 RSS 端点                                │
│  - 必须由开关显式启用                             │
└─────────────────────────────────────────────────┘
```

## 数据流

```
feeds/sources.yaml  ─┐
                     │
                     ▼
        scripts/update_news.py
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
   fetch_rss   fetch_x_handle   (future: fetch_wechat, etc.)
       │             │             │
       └─────────────┼─────────────┘
                     ▼
              normalize_items
                     │
                     ▼
       ┌─────────────┴────────────┐
       ▼                          ▼
  data/items.json     data/source-status.json
       │                          │
       └──────────► index.html ◄──┘
```

## 输出契约

### `data/items.json`

```json
{
  "generated_at": "2026-06-09T15:20:00+00:00",
  "window_hours": 48,
  "items": [
    {
      "site_id": "hackernews",
      "site_name": "Hacker News",
      "group": "聚合站",
      "category": "ai_hot",
      "title": "...",
      "url": "https://...",
      "published_at": "2026-06-09T13:15:00+00:00",
      "summary": "..."
    }
  ]
}
```

### `data/source-status.json`

```json
{
  "generated_at": "...",
  "sources": [
    {"id": "hackernews", "name": "...", "type": "rss", "ok": true, "count": 30, "error": "", "fetched_at": "..."}
  ],
  "summary": {"total_sources": 119, "ok": 119, "failed": 0, "items": 798}
}
```

字段 `error` 永远存在，要么为空字符串，要么是 `ErrType: message`，便于运维 grep。

## 与 ai-news-radar 的关系

复用了它的三个核心做法：

1. **两层产品** —— 公开默认层 + 私有进阶层，互不阻塞
2. **优雅降级** —— 单源失败只写 status，不抛
3. **官方 RSS 优先** —— 不爬，不绕 Cloudflare，不依赖第三方桥的可用性

差异点：

- ai-news-radar 是公开 demo（围绕 OPML/AgentMail/follow-builders）；本仓库是黄晓泽内容工程的私域信源台账，所以默认层更小、更聚焦
- 没有 Source Overlap Check（v0 不做去重决策，留给 v0.2）
- 没有 Story Merge 聚类（同上）

## 路线图

| 版本 | 目标 |
|---|---|
| v0.1 | ✅ 7 个稳定 RSS 跑通，前端能渲染 |
| v0.2 | wechat2rss URL 全部填齐，公众号开关跑通 |
| v0.3 | X API 配齐 80 个 handle，分组渲染 |
| v0.4 | GitHub Pages 自动部署 + 每 6 小时 cron |
| v0.5 | 与飞书 docx 双向同步（lark-cli 拉取/回写） |
