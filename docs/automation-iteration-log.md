# 自动化迭代日志

> 任务 1 (自动化定时跑) → 任务 2 (网页升级 + 部署) 的全程迭代记录。

## 迭代 1 · 2026-06-12 11:00 — Phase 1 基础设施

**写完**: 评分脚本 (`scripts/automation/score.py`) + GH Actions workflow 改成"只跑无本机依赖" + 本机 launchd plist + install.sh + RUNBOOK.md

**初次跑分 (quick)**: 59.4 / 100 ❌

| 维度 | 得分 | 状态 |
|---|---|---|
| GitHub Actions workflow | 15/15 | ✅ |
| 本机 launchd plist | 0/15 | ❌ 未装 |
| 8 通道端到端 | 6.9/30 | ❌ 历史数据 |
| state 增量 | 10/10 | ✅ |
| 错误日志 | 8/10 | ⚠️ 1 失败 (import-ai) |
| Runbook | 9.5/10 | ✅ |
| 资源 | 10/10 | ✅ |

## 迭代 2 · 11:09 — 装 launchd + 实跑 e2e

1. `bash scripts/automation/install.sh` → plist 写入 `~/Library/LaunchAgents/com.hxz.news-reader.plist` (chmod 600)
2. `launchctl load` → 已加载, 明早 6:30 首跑
3. 后台跑全 8 通道 `update_news.py --enable-x --enable-wechat --enable-youtube --enable-bilibili --enable-xiaoyuzhou`

实跑结果 (耗时约 1 小时):
- 公众号: **12/12 通过** (qbitai 5920字 / jiqizhixin 6466 / xinzhiyuan 7772 / latepost 5402 / waves 201 / geekpark 7116 / guicang-ai 7834 / khazix 9179 / aiwarts 6968 / agent-ju 2676 / zang-ai 4358 / zhinengyongxian 3651)
- B 站: **1/1 通过** (li-ziran BV17EdFBiEwQ, 9001 字)
- 小宇宙: **3/4 通过** (latetalk 57434字 / guigu101 33957字 / ai-weekly-talk 11595字 / **onboard 404**)
- X: **189 条 / 20s** (76 handles → list_timeline)
- YouTube / RSS / HF / Substack: 默认层全过

**总 items=337, sources=115 ok=114 failed=1, 写配额今日 16/100**

## 迭代 3 · 11:36 — 跑分 + 修 onboard 404

**跑分 (quick)**: **86.2 / 100 ✅ PASS** (达标线 85)

| 维度 | 得分 | 状态 |
|---|---|---|
| GitHub Actions workflow | 15/15 | ✅ |
| 本机 launchd plist | 12/15 | ✅ 装好 |
| 8 通道端到端 | 21.7/30 | ⚠️ X 76 handle 只有 30+ 有新推 → ok=30/76 计算后扣分 |
| state 增量 | 10/10 | ✅ |
| 错误日志 | 8/10 | ⚠️ 1 失败 (onboard 404) |
| Runbook | 9.5/10 | ✅ |
| 资源 | 10/10 | ✅ |

**bug 修复**: onboard podcast_id 改正
- 旧 (错): `6164e0d77a72e91fb7e5a14d` (小宇宙 404)
- 新 (对): `61cbaac48bb4cd867fcabe22` (验证: WebSearch + 浏览器访问 200)

**结论**: Phase 1 **首轮即达标**, 无需进一步迭代。进入 Phase 2 (网页 dashboard + 部署对比)。

## 后续动作

- ✅ build_local_index.py 重跑, 现 340 条 items (含国内 19 篇全文)
- ✅ source-status.json 复制到 data_local/ 让 dashboard 能读
- ⏳ Phase 2 components-dashboard.jsx 已写 + 接到 app.jsx, 等浏览器刷新验证渲染
- ⏳ Phase 2 部署对比 (Vercel / Cloudflare Pages / Netlify / 阿里云 OSS) 已收集候选, 待 dashboard 验证完后呈现给 PM
