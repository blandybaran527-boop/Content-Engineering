# 国内信源通道 — getnote_bridge 设计

> 关联：[../scripts/bridges/getnote_bridge.py](../scripts/bridges/getnote_bridge.py)
> 关联：[../scripts/discover/](../scripts/discover/)
> 关联：[~/.claude/skills/getnote/](~/.claude/skills/getnote/) （独立 skill，凭证唯一来源）

## ⚠️ WeWe-RSS 已知事实（2026-06-11 实测确认）

**WeWe-RSS 设计上只存元数据，不存正文**。sqlite `articles` 表只有 7 个字段：
```
id, mp_id, title, pic_url, publish_time, created_at, updated_at
```
atom / rss / json 三种输出格式都只含 `<title> / <link> / <pubDate>`，**不含 `<content>` 或 `<description>`**。

→ 因此公众号通道必须双层：**第一层 WeWe-RSS 拿"哪些号出新文章"+ URL；第二层 getnote_bridge 拿正文**。

### token 失效 vs 没正文 — 别混淆

| 症状 | 诊断 | 修法 |
|---|---|---|
| sources.yaml 里某号 168h 窗口空，但你知道刚发了文章 | 微信读书 token 失效 | http://127.0.0.1:4000/dash 重扫码 |
| atom 拉到了，但 entry 没有正文 | 正常 — WeWe-RSS 本就不存正文 | 走 getnote_bridge 第二层 |
| atom entry 数量正常 + getnote 第二层正常 | 全部 OK |  |

**关键**：token 失效只影响"有没有抓到新文章通知"，跟"有没有正文"无关。即使 token 永远活着，WeWe-RSS 也永远不会给你正文。

## 1. 这个通道解决什么问题

hxz 国外管线靠 RSS / Atom + 公开 API + youtube-transcript-api 就能取到原文。
国内三个高价值渠道做不到：

| 渠道 | hxz 原方案 | 痛点 |
|---|---|---|
| 公众号 | WeWe-RSS (主路径，已上线 12 个号) | 微信读书 token 周期性失效；不在订阅里的号没法临时取 |
| B 站长视频 | 无 | 没有官方字幕，没有简单可靠的转写源 |
| 小宇宙播客 | 节目目录展示 (无原文) | 无公开 RSS，节目页是 SPA |

**解法**：复用独立的 `getnote` skill。biji.com 后端做了完整 ASR + 网页正文提取，URL → 原文/逐字稿。我们在 hxz 里加一层薄 bridge 调它。

## 2. 两层架构

```
第一层：账号 → 作品 URL                        (hxz 自己做)
        │
        ├── B 站 UP    → yt-dlp 抓 space.bilibili.com/<UID>
        ├── 小宇宙节目 → curl + 正则解析节目页 HTML
        └── 公众号(fallback) → WeWe-RSS atom feed
                           │
                           ▼ 增量取最新 N 条 URL
                           │
第二层：URL → 原文                              (调 getnote skill)
                           │
                           ▼
                  getnote_bridge.url_to_content(url)
                           │
                           ├── POST /note/save (异步 task)
                           ├── 轮询 /task/progress (10-30s 间隔)
                           └── GET /note/detail
                                   ↓
                            {title, summary (AI总结),
                             body (原文/逐字稿+时间戳),
                             source_url, note_id, task_id}
```

## 3. 凭证 / 安全边界

- **凭证位置**：`~/.claude/skills/getnote/.env`（chmod 600）
- **hxz 仓库代码不出现任何 key**（公开 GitHub repo）
- bridge 在导入时显式从 `~/.claude/skills/getnote/.env` 读，**不依赖环境变量**（避免别的进程污染）
- `.env` 不在 hxz 仓库，不被 git track；hxz `.gitignore` 也加了 `*.env` 防御性兜底

## 4. 限流 / 配额 / 节流

biji 写配额：100 篇/日。

bridge 内置守门：
- **每两次 save 间隔 ≥65s**（SKILL.md L48 的"建议 ≥1 分钟"红线，留 5s 余量）
- **每天 100 篇守门**：用满抛 `BridgeError`，不会暴走
- **失败处理**：异步任务失败不自动重试（避免双扣配额）；网络错误调用方决定

state 文件 `state/getnote_bridge.json` 形如：
```json
{
  "last_save_ts": 1781150859.0,
  "daily": {"2026-06-11": 4}
}
```

## 5. 数据落地策略（按用户决策 T5）

**国内逐字稿 → 本地 `data_local/`，gitignored，不进 GitHub Pages**

```
data_local/
├── bilibili/
│   └── li-ziran/
│       └── 2026-06-11__BV1DwVw6dEcE__标题.md
└── xiaoyuzhou/
    ├── ai-weekly-talk/
    │   └── 2026-06-11__6a298cdb...__标题.md
    ├── latetalk/
    ├── onboard/
    └── guigu101/
```

每个 .md 含 frontmatter（channel / src_id / item_id / source_url / note_id / fetched_at / body_len）+ AI 总结 + 原文。

公开 `data/items.json` 只放：标题 + URL + ≤600 字 summary（避免版权 + 流量）。

## 6. 增量同步

state 文件 `state/discover.json` 形如：
```json
{
  "li-ziran":       {"last_seen_id": "BV1xxx", "last_run_at": "2026-06-11..."},
  "ai-weekly-talk": {"last_seen_id": "6a298cdb...", "last_run_at": "2026-06-11..."}
}
```

discover 拿 max_per_run + 2 条候选，过滤掉 `last_seen_id` 之前的，取 max_per_run 条进 bridge。

## 7. 失败兜底（按用户决策 T2）

biji 取原文失败时（视频删除 / 公众号 404 / biji 后端打不开）：
- `items.json` 里仍留一条，`summary` 填 `[transcript fail: ...]`，与 YouTube 通道现有失败模式一致
- `data_local/` 不写文件（避免空壳混进知识库）
- state 仍推进 `last_seen_id`，下次不重复尝试同一条

## 8. CLI 用法

```bash
# 同时跑国内 B 站 + 小宇宙
python scripts/update_news.py --enable-bilibili --enable-xiaoyuzhou

# 单独跑某个源（测试时用）
python scripts/update_news.py --enable-xiaoyuzhou --probe-only ai-weekly-talk

# 主流程（与原方式完全兼容，原 5 个通道一行不改）
python scripts/update_news.py --enable-x --enable-wechat --enable-youtube
```

输出：
- `data/items.json` 公开新增国内条目（仅摘要）
- `data/source-status.json` 包含国内 source 状态
- `data_local/<channel>/<src_id>/...md` 全文（本地保留）
- `state/discover.json` + `state/getnote_bridge.json` 增量锚点

## 9. 与 hxz 其他通道的关系

| 通道 | 是否动 |
|---|---|
| RSS / Substack / HF Papers | 一行不动 |
| WeChat (WeWe-RSS) | 一行不动，仍是公众号主路径 |
| YouTube | 一行不动 |
| X (twscrape list_timeline) | 一行不动 |
| Bilibili / Xiaoyuzhou (新) | 纯加 |

bridge / discover 模块完全独立，不引入也不修改任何现有 fetcher。
