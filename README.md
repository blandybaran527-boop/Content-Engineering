# HXZ News Reader

> 黄晓泽内容工程的信源雷达。与飞书文档「[内容工程-0609](https://tcnih12gszer.feishu.cn/wiki/W5HTw1hAOiTc57kLCYEcQ5H0nLf)」一一对应。
> 技术方案参考 [`ai-news-radar`](https://github.com/LearnPrompt/ai-news-radar) 的"小闭环优先 → 逐类放大"策略。

## 它解决什么

把飞书表格里登记的 **80 个 X 账号 + 12 个公众号 + 15 个播客 + 4 个聚合站 + 7 个商科信源** 自动汇总成一个 24/48 小时的内容雷达 JSON，前端用一个零依赖的 `index.html` 渲染，也可以塞进 GitHub Actions 每 6 小时跑一次推到 Pages。

## 当前已跑通的链路（v0.2）

19 个信源（4 聚合站 + 3 商科 Substack + 12 公众号），零 API Key，168h 窗口约 170+ 条：

| 类型 | 通道 | 信源 |
|---|---|---|
| 聚合站 | 官方 RSS / API | Hacker News、Import AI、HuggingFace Daily Papers、The Rundown AI（走 YouTube 频道 RSS） |
| 商科 Substack | 官方 `/feed` | Lenny's Newsletter、The Generalist、Newcomer |
| 公众号 | **本地 WeWe-RSS 桥**（`127.0.0.1:4000`） | 量子位、机器之心、新智元、晚点LatePost、暗涌Waves、极客公园、歸藏的AI工具箱、数字生命卡兹克、卡尔的AI沃茨、AGENT橘、葬AI、智能涌现 |

> **原则**：信源不可达时**只换通道，不换信源**。HF Papers 没有官方 RSS 就走它的 `/api/daily_papers` 接口；The Rundown AI 网站 RSS 被拦就走它的 YouTube 频道 RSS。绝不替换成"同类的别家"。

### 公众号通道：本地 WeWe-RSS（替代了原计划的 wechat2rss.xlab.app）

公共版 `wechat2rss.xlab.app` 只收录我们 12 个目标号中的 4 个，缺 8 个 AI 自媒体号无法等收录。改为：本地自建 [`cooderl/wewe-rss`](https://github.com/cooderl/wewe-rss)，原理是走微信读书 API（一次性扫码绑定微信读书账号），输出标准 Atom RSS。

部署位置：`/Users/admin/Downloads/wewe-rss-work/wewe-rss`，详细启停与增删订阅命令见 `docs/SOURCES.md` D 节。

X / 播客都已经登记在 `feeds/sources.yaml`，默认不抓（避免不稳定的桥），通过开关启用：

```bash
python scripts/update_news.py --enable-x          # 需要 X_BEARER_TOKEN
python scripts/update_news.py --enable-wechat     # 需要本地 WeWe-RSS 跑着（默认 127.0.0.1:4000）
python scripts/update_news.py --enable-podcast    # 抓 podcast 类型有 RSS 的源
```

## 快速开始

```bash
git clone https://github.com/blandybaran527-boop/Content-Engineering.git
cd Content-Engineering
pip install -r requirements.txt
python scripts/update_news.py --output-dir data --window-hours 48
python -m http.server 8080
# 浏览 http://localhost:8080
```

## 仓库结构

```
.
├── README.md                # 本文档
├── SKILL.md                 # Claude Code skill 入口（自动加载）
├── requirements.txt         # feedparser / requests / PyYAML
├── index.html               # 零依赖静态前端
├── scripts/
│   └── update_news.py       # 单文件抓取器，输出 data/*.json
├── feeds/
│   └── sources.yaml         # 全部信源台账（与飞书表格一一对应）
├── data/
│   ├── items.json           # 抓取结果
│   └── source-status.json   # 每个信源的健康状态
├── docs/
│   ├── ARCHITECTURE.md      # 技术分层与决策
│   └── SOURCES.md           # 各信源类型对应的抓取策略
└── .github/workflows/
    └── update.yml           # 每 6 小时跑一次
```

## 增删信源

直接编辑 `feeds/sources.yaml`，每条信源的字段：

```yaml
- id: example                # 全局唯一短 ID
  name: Example              # 显示名
  type: rss                  # rss | x_handle | wechat | podcast
  url: https://example.com/feed
  category: ai_hot           # ai_hot | business_innovation
  group: 聚合站              # 飞书表格的分组
  default: true              # 是否默认抓取
```

单源探测：

```bash
python scripts/update_news.py --probe-only example
```

## 设计取舍

- **公共第三方桥默认关**：Nitter / wechat2rss 公共版 / RSSHub 公共实例都不稳定，关掉它们能保证仓库始终能跑通
- **官方 RSS / 自托管优先**：所有默认抓取的源都是官方原生 RSS（HN / Substack）或本地自部署（WeWe-RSS）
- **失败不阻塞**：任何信源失败只写入 `source-status.json`，不让整个流程崩
- **本地 RSS 桥不走代理**：`update_news.py` 启动时自动把 `127.0.0.1` / `localhost` 加到 `NO_PROXY`，避免梯子导致 502
- **零 API Key 跑通（公共部分）**：fork 后无需配置任何 Secret 就能看到 7 个公共信源
- **公众号要本地 WeWe-RSS**：扫一次微信读书码即可，自己一个号一辈子用（详见 docs/SOURCES.md D 节）

更多细节看 `docs/ARCHITECTURE.md` 和 `docs/SOURCES.md`。

## 与飞书联动

飞书文档（[wiki 链接](https://tcnih12gszer.feishu.cn/wiki/W5HTw1hAOiTc57kLCYEcQ5H0nLf)）是"信源台账的人写视图"，本仓库的 `feeds/sources.yaml` 是"机器执行视图"。两边人工同步即可：

1. 在飞书里增删/调整某个信源
2. 改 `sources.yaml` 对应项
3. 提交 / push，下次 Action 自动跑

## 鸣谢

- 抓取分层 / 安全规则借鉴 [LearnPrompt/ai-news-radar](https://github.com/LearnPrompt/ai-news-radar)
- 信源清单来自飞书文档「内容工程-0609」
