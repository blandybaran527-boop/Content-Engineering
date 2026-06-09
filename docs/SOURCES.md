# 信源策略

## A. 聚合站（默认抓取，最稳定）

| Source | URL | 备注 |
|---|---|---|
| Hacker News | `https://news.ycombinator.com/rss` | 官方 |
| Import AI | `https://importai.substack.com/feed` | Anthropic 联创 Jack Clark |
| arXiv cs.AI | `http://export.arxiv.org/rss/cs.AI` | 学术兜底 |
| Latent Space | `https://www.latent.space/feed` | swyx 的 AI 工程师 newsletter |

❌ 不可用：
- **The Rundown AI** 官网无公开 RSS，他们的 newsletter 是邮件订阅，不强行抓取
- **HuggingFace Daily Papers** 没有官方 RSS，社区代理 `jamesg.blog/hf-papers.xml` 已 403

## B. 商科创新故事（默认抓取）

| Source | URL | 备注 |
|---|---|---|
| Lenny's Newsletter | `https://www.lennysnewsletter.com/feed` | Substack 原生 |
| The Generalist | `https://www.generalist.com/feed` | Substack 原生 |
| Newcomer | `https://www.newcomer.co/feed` | Substack 原生 |

⚠️ 公众号系（晚点 LatePost / 暗涌 / 智能涌现 / 潜望）默认关，靠 wechat2rss 填齐后开。

## C. X / Twitter（80 个，默认关）

抓取策略优先级：

1. **X 官方 API**：`/2/users/by/username/<handle>` → `/2/users/<id>/tweets`
   - 需要 `X_BEARER_TOKEN`
   - Free tier: 50 req/day; Basic tier: 10k req/month
   - 80 个 handle 单次拉取需要 160 次调用（一次 lookup + 一次 tweets），跑一次/天就要消耗 160 调用，Free tier 不够
   - **建议**：要么升 Basic（$200/月），要么分批：每天抓不同子集
2. **Nitter 公共实例**：极不稳，仅做应急
3. **手动维护**：所有 80 个 handle 都有完整 `https://x.com/<handle>` URL，作为展示链接始终可用

代码已实现 (1)，(2)(3) 留给后续。

## D. 公众号（11 个，默认关）

**wechat2rss.xlab.app** 是当前最稳定的公众号 → RSS 公共桥。流程：

1. 打开 https://wechat2rss.xlab.app/
2. 搜公众号名称（如「数字生命卡兹克」）
3. 复制返回的 RSS URL
4. 填回 `feeds/sources.yaml` 对应条目的 `url` 字段
5. `python scripts/update_news.py --enable-wechat --probe-only <id>` 验证

⚠️ wechat2rss 偶尔限流，要做好 5xx 重试。

## E. 优质播客 / 长视频（15 个，默认关）

| 类型 | RSS 策略 |
|---|---|
| YouTube | `https://www.youtube.com/feeds/videos.xml?channel_id=<CHANNEL_ID>` |
| 小宇宙 | 节目页右下角"订阅 RSS"按钮可直接拿到原始 podcast RSS |
| Spotify-only | 无公开 RSS，仅展示链接 |
| Substack 播客 | `<host>/feed` |

⚠️ 小宇宙的 RSS 是节目的 Apple Podcast 镜像 feed，需要在节目页面手动复制。

## F. 兜底：所有信源都登记 URL

无论 `default` 是不是 `true`，信源在 `sources.yaml` 里都有一个 `url`（X 是 `https://x.com/<handle>`），这样前端始终能渲染信源名 + 链接，即使没抓到任何条目也能用作"导航页"。
