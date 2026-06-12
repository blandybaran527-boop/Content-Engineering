# HXZ News Reader · Runbook

> 给"零运维"日常用，遇到异常翻这一份。

## 1. 系统架构 · 谁在跑什么

| 通道 | 跑在哪 | 触发时间 |
|---|---|---|
| RSS 聚合 / Substack / HF Papers | **GitHub Actions** | 每天 UTC 22:00 (北京 06:00) |
| X / YouTube / WeChat / Bilibili / Xiaoyuzhou | **本机 launchd** | 每天本机 06:30 |

云端跑无依赖、不需要你电脑开；本机 5 类需要电脑开 + 凭证活。

详细配置:
- 云端 workflow: `.github/workflows/update.yml`
- 本机定时: `~/Library/LaunchAgents/com.hxz.news-reader.plist`
- 本机脚本: `scripts/automation/run_local.sh`
- 自检打分: `scripts/automation/score.py`

## 2. 首次安装本机定时

```bash
cd ~/Downloads/hxz-news-reader

# 确认凭证存在
ls ~/.claude/skills/getnote/.env       # getnote API Key / Client ID
echo $TWITTER_AUTH_TOKEN | head -c 10  # 应该有输出
echo $TWITTER_CT0 | head -c 10

# 装定时任务
bash scripts/automation/install.sh

# 立即手动跑一次 (测试)
launchctl start com.hxz.news-reader

# 看日志
tail -f ~/Library/Logs/hxz-news-reader.log
```

## 3. 凭证维护清单

| 凭证 | 多久过期 | 哪里找新值 | 改在哪 |
|---|---|---|---|
| `GETNOTE_API_KEY` / `GETNOTE_CLIENT_ID` | 1 年 | https://www.biji.com/openapi → 应用管理 → 「Get 笔记 Skill & Cli」生成 Key | `~/.claude/skills/getnote/.env` |
| `TWITTER_AUTH_TOKEN` / `TWITTER_CT0` | 几个月或登出时 | chrome 装 Cookie-Editor → x.com → export `auth_token` + `ct0` | `~/.zshrc` (export) + `~/Library/LaunchAgents/com.hxz.news-reader.plist` 的 EnvironmentVariables |
| 微信读书 token | 不定期, WeWe-RSS 显示 401 | 浏览器开 http://127.0.0.1:4000/dash → AuthCode `wewe2026` → 「重新绑定账号」扫码 | WeWe-RSS 自管 db |
| X GraphQL queryId | X 升级前端时 | [fa0311/TwitterInternalAPIDocument](https://github.com/fa0311/TwitterInternalAPIDocument) → 搜 `ListLatestTweetsTimeline` → 抄 queryId | `scripts/x_list/fetch_timeline.py` 顶部 `LIST_TIMELINE_QID` |
| YouTube 住宅 IP | 偶尔被降级 | Clash Verge 切「🏠 美国家宽选这个」节点 | Clash Verge GUI |

**改完后**：
```bash
# 改了 plist 里的 cookie 后必须 reload
launchctl unload ~/Library/LaunchAgents/com.hxz.news-reader.plist
launchctl load ~/Library/LaunchAgents/com.hxz.news-reader.plist
```

## 4. 日常排查 (按从轻到重)

### 4.1 网页打不开
```bash
# 1. server 在吗
lsof -i :8080
# 2. 没在就启
cd ~/Downloads/hxz-news-reader && nohup python3 -m http.server 8080 > /tmp/hxz_server.log 2>&1 &
```

### 4.2 网页空 / dashboard 全灰
```bash
# data_local/items.json 不存在 = 还没跑过 build_local_index
cd ~/Downloads/hxz-news-reader
python3 scripts/build_local_index.py
```

### 4.3 某通道几天没新内容
```bash
# 跑自检看分
python3 scripts/automation/score.py
# 看 source-status.json 具体哪个源失败
python3 -c "
import json
d = json.load(open('data/source-status.json'))
for s in d['sources']:
    if not s.get('ok') and 'skipped' not in s.get('error',''):
        print(f\"{s['id']}: {s['error']}\")
"
```

### 4.4 凭证失效自检
凭证状态会反映到 `state/getnote_bridge.json` (biji 写配额过载就会抛) 和 `source-status.json` (X 401 / WeWe-RSS 401)。
网页 dashboard 也会显示「⚠️ 凭证可能失效」+ 修复入口。

### 4.5 本机定时不跑
```bash
# 1. 看 launchctl 加载没
launchctl list com.hxz.news-reader
# 2. 看日志
tail -100 ~/Library/Logs/hxz-news-reader.log
# 3. 手动触发
launchctl start com.hxz.news-reader
```

## 5. 自检评分 (验证系统健康)

```bash
cd ~/Downloads/hxz-news-reader
python3 scripts/automation/score.py
# 总分 ≥85 = PASS, <85 = 看推荐修复点
```

各维度:
- GitHub Actions workflow 配置 (15)
- 本机 launchd plist 配置 (15)
- 8 通道端到端跑通 (30)
- state 增量正确 (10)
- 错误日志干净 (10)
- Runbook 完整 (10)
- 资源占用合理 (10)

## 6. 常见红线 (违反 = 麻烦)

- ❌ 不要把 `~/Library/LaunchAgents/com.hxz.news-reader.plist` 推 GitHub (含 X cookie)
- ❌ 不要短时间内重复跑 update_news.py 测试 X 通道 (消耗 cookie quota)
- ❌ 不要短时间内反复 WeWe-RSS feed.refreshArticles (微信读书 token 会被风控失效)
- ❌ 不要把 `data_local/` push 到公开仓库 (版权风险)
- ❌ 不要把 `accounts.db` push 到公开仓库 (含 cookie)
- ❌ 不要在 yt-dlp 跑 B 站时走梯子代理 (SSL EOF, discover/bilibili.py 已强制 proxy="")

## 7. 想看分数怎么打的

`scripts/automation/score.py` 用 Python 写, 每个维度独立函数, 看源码就知道。
机读 JSON: `python3 scripts/automation/score.py --json`
不跑 e2e (省时间): `python3 scripts/automation/score.py --quick`

## 8. 部署

页面默认本机 http.server 8080 访问。`data_local/items.json` 含国内全文不公开。
公开 GitHub Pages 只放 `data/items.json` 海外+国内摘要。

如要在外面看国内全文 → 私有云端部署 (待 PM 选定)。
