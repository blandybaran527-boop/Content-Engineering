# 信源策略

## A. 聚合站（默认抓取，最稳定）

| Source | 通道 | 备注 |
|---|---|---|
| Hacker News | 官方 RSS `news.ycombinator.com/rss` | YC 旗下 |
| Import AI | 官方 RSS `importai.substack.com/feed` | Jack Clark |
| HuggingFace Daily Papers | 官方 **API** `huggingface.co/api/daily_papers` | 无公开 RSS，走 API；`fetch_hf_papers` 自定义解析器 |
| The Rundown AI | YouTube 频道 RSS `channel_id=UCOoKOPoTsf6gcDKvERU9BeA` | newsletter 本身无公开 RSS，靠 YouTube 频道兜底 |

### 通道选型记录

- **HF Daily Papers**：社区代理 `jamesg.blog/hf-papers.xml` 已 403；改用 HuggingFace 官方 `/api/daily_papers` JSON 接口，每次返回最近 N 篇精选论文，含 publishedAt、title、summary、id
- **The Rundown AI**：官网 `/rss` `/feed` 都 403/404；改用其 YouTube 官方频道的标准 RSS（YouTube 提供 `feeds/videos.xml?channel_id=<id>`）。Newsletter 内容稍微滞后但作者重叠

⚠️ **原则**：抓不到时**只换通道，不换信源**。永远不要把 HF Papers 替换成 arXiv，也不要把 Rundown 替换成 Latent Space——这些是不同的策展口味，用户的信源清单不能被偷偷改。

## B. 商科创新故事（默认抓取）

| Source | URL | 备注 |
|---|---|---|
| Lenny's Newsletter | `https://www.lennysnewsletter.com/feed` | Substack 原生 |
| The Generalist | `https://www.generalist.com/feed` | Substack 原生 |
| Newcomer | `https://www.newcomer.co/feed` | Substack 原生 |

⚠️ 公众号系（晚点 LatePost / 暗涌 Waves / 智能涌现）默认开，通过本地 WeWe-RSS 桥拉取，详见 D 节。

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

## D. 公众号（12 个，默认开，走本地 WeWe-RSS 桥）

**当前方案：本地自建 WeWe-RSS（[cooderl/wewe-rss](https://github.com/cooderl/wewe-rss)）作为公众号 → RSS 桥**，部署在 `http://127.0.0.1:4000`。

### 为什么不用 wechat2rss.xlab.app

公共版 `wechat2rss.xlab.app` 只收录约 4/12 我们的目标号（量子位、机器之心、新智元、极客公园），剩 8 个（晚点 LatePost、暗涌 Waves、归藏的AI工具箱、数字生命卡兹克、卡尔的AI沃茨、AGENT橘、葬AI、智能涌现）需要等收录或自部署。WeWe-RSS 一次性覆盖全部。

### 部署位置

- 仓库：`/Users/admin/Downloads/wewe-rss-work/wewe-rss`
- 数据库：SQLite，文件位置 `data/wewe-rss.db`
- 启动命令：
  ```bash
  cd /Users/admin/Downloads/wewe-rss-work/wewe-rss
  DATABASE_URL="file:../data/wewe-rss.db" DATABASE_TYPE="sqlite" \
    AUTH_CODE="wewe2026" SERVER_ORIGIN_URL="http://127.0.0.1:4000" \
    pnpm run start:server
  ```
- 管理界面：`http://127.0.0.1:4000/dash`（AuthCode：`wewe2026`）

### 当前订阅清单（mpId 跟 sources.yaml 对齐）

| 飞书分组 | id | 公众号 | WeWe-RSS mpId |
|---|---|---|---|
| AI 热点 | qbitai | 量子位 | `MP_WXS_3236757533` |
| AI 热点 | jiqizhixin | 机器之心 | `MP_WXS_3073282833` |
| AI 热点 | xinzhiyuan | 新智元 | `MP_WXS_3271041950` |
| AI 热点 | latepost | 晚点LatePost | `MP_WXS_3572959446` |
| AI 热点 | waves | 暗涌Waves | `MP_WXS_3940324519` |
| AI 热点 | geekpark | 极客公园 | `MP_WXS_1304308441` |
| AI 热点 | guicang-ai | 歸藏的AI工具箱 | `MP_WXS_3540975510` |
| AI 热点 | khazix | 数字生命卡兹克 | `MP_WXS_3223096120` |
| AI 热点 | aiwarts | 卡尔的AI沃茨 | `MP_WXS_3871977637` |
| AI 热点 | agent-ju | AGENT橘 | `MP_WXS_3903697567` |
| AI 热点 | zang-ai | 葬AI | `MP_WXS_3988614169` |
| 商科 | zhinengyongxian | 智能涌现 | `MP_WXS_3900464567` |

### 增减公众号

调 WeWe-RSS 后端 API（不需要浏览器操作）：

```bash
# 1. 查链接归属
curl -s --noproxy '*' -X POST -H "Authorization: wewe2026" -H "Content-Type: application/json" \
  -d '{"wxsLink":"https://mp.weixin.qq.com/s/xxxx"}' \
  http://127.0.0.1:4000/trpc/platform.getMpInfo

# 2. 加订阅（用上一步返回的 id/name/cover/intro/updateTime）
curl -s --noproxy '*' -X POST -H "Authorization: wewe2026" -H "Content-Type: application/json" \
  -d '{"id":"MP_WXS_xxx","mpName":"...","mpCover":"...","mpIntro":"...","updateTime":...}' \
  http://127.0.0.1:4000/trpc/feed.add

# 3. 拿到 mpId 后，写回 feeds/sources.yaml
# url 字段为：http://127.0.0.1:4000/feeds/MP_WXS_xxx.atom
```

### 本地代理踩坑

WeWe-RSS 跑在 `127.0.0.1`，本机走系统代理（梯子）时会 502。`update_news.py` 已自动注入 `NO_PROXY=127.0.0.1,localhost`；命令行手动跑时需要带上 `NO_PROXY="127.0.0.1,localhost"` 前缀，或者 curl 加 `--noproxy '*'`。

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
