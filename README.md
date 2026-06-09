# HXZ News Reader

> 黄晓泽内容工程的信源雷达。与飞书文档「[内容工程-0609](https://tcnih12gszer.feishu.cn/wiki/W5HTw1hAOiTc57kLCYEcQ5H0nLf)」一一对应。
> 技术方案参考 [`ai-news-radar`](https://github.com/LearnPrompt/ai-news-radar) 的"小闭环优先 → 逐类放大"策略。

## 它解决什么

把飞书表格里登记的 **80 个 X 账号 + 11 个公众号 + 15 个播客 + 4 个聚合站 + 7 个商科信源** 自动汇总成一个 24/48 小时的内容雷达 JSON，前端用一个零依赖的 `index.html` 渲染，也可以塞进 GitHub Actions 每 6 小时跑一次推到 Pages。

## 当前已跑通的小闭环（v0）

5 个 RSS 信源，零 API Key，单次抓取近 800 条：

| ID | 名字 | 类型 | URL |
|---|---|---|---|
| `hackernews` | Hacker News | 聚合站 | `https://news.ycombinator.com/rss` |
| `import-ai` | Import AI | 聚合站 | `https://importai.substack.com/feed` |
| `arxiv-cs-ai` | arXiv cs.AI | 聚合站 | `http://export.arxiv.org/rss/cs.AI` |
| `latent-space` | Latent Space | 聚合站 | `https://www.latent.space/feed` |
| `lennys` | Lenny's Newsletter | 商科 | `https://www.lennysnewsletter.com/feed` |
| `generalist` | The Generalist | 商科 | `https://www.generalist.com/feed` |
| `newcomer` | Newcomer | 商科 | `https://www.newcomer.co/feed` |

X / 公众号 / 播客都已经登记在 `feeds/sources.yaml`，默认不抓（避免不稳定的桥），通过开关启用：

```bash
python scripts/update_news.py --enable-x          # 需要 X_BEARER_TOKEN
python scripts/update_news.py --enable-wechat     # 需要先在 sources.yaml 里填 wechat2rss URL
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

- **第三方桥默认关**：Nitter / wechat2rss / RSSHub 公共实例都不稳定，关掉它们能保证仓库始终能跑通
- **官方 RSS / 自托管优先**：所有默认抓取的源都是官方原生 RSS（HN / arXiv / Substack）
- **失败不阻塞**：任何信源失败只写入 `source-status.json`，不让整个流程崩
- **零 API Key 跑通**：fork 后无需配置任何 Secret 就能看到内容
- **X / WeChat 是 advanced**：要抓 X，自己配 `X_BEARER_TOKEN`；要抓公众号，自己去 wechat2rss 申请并填 URL

更多细节看 `docs/ARCHITECTURE.md` 和 `docs/SOURCES.md`。

## 与飞书联动

飞书文档（[wiki 链接](https://tcnih12gszer.feishu.cn/wiki/W5HTw1hAOiTc57kLCYEcQ5H0nLf)）是"信源台账的人写视图"，本仓库的 `feeds/sources.yaml` 是"机器执行视图"。两边人工同步即可：

1. 在飞书里增删/调整某个信源
2. 改 `sources.yaml` 对应项
3. 提交 / push，下次 Action 自动跑

## 鸣谢

- 抓取分层 / 安全规则借鉴 [LearnPrompt/ai-news-radar](https://github.com/LearnPrompt/ai-news-radar)
- 信源清单来自飞书文档「内容工程-0609」
