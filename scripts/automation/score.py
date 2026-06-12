#!/usr/bin/env python3
"""Phase 1 自动化健康打分 — 任务清单 1A 评分卡的实现。

跑法:
    python3 scripts/automation/score.py              # 跑全套打分
    python3 scripts/automation/score.py --json       # 机读 JSON 输出
    python3 scripts/automation/score.py --quick      # 跳过 e2e (不实跑 update_news.py)

输出: stdout 表格 + 总分 + 推荐修复点。退出码: 0 = 达标 (≥85), 1 = 未达标。
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[2]
PASS = 85

# ============================================================
# 各维度评分函数 - 返回 (score, max, message)
# ============================================================

def score_github_workflow() -> tuple[float, float, str]:
    """15 分: GitHub Actions workflow 配置"""
    f = ROOT / ".github/workflows/update.yml"
    if not f.exists():
        return 0, 15, "缺 .github/workflows/update.yml"
    text = f.read_text()
    pts = 0
    notes = []
    if "schedule:" in text and "cron:" in text:
        pts += 5; notes.append("cron 触发器 ✓")
    if "update_news.py" in text:
        pts += 5; notes.append("跑 update_news.py ✓")
    if "git commit" in text and "git push" in text:
        pts += 3; notes.append("auto-commit ✓")
    # workflow 明确不跑需要本机凭证的渠道 (X / wechat / youtube / 国内)
    has_x = "--enable-x" in text
    has_wechat = "--enable-wechat" in text
    has_youtube = "--enable-youtube" in text
    if not (has_x or has_wechat or has_youtube):
        pts += 2; notes.append("无本机依赖通道 ✓")
    else:
        notes.append(f"⚠️ workflow 含本机依赖通道: x={has_x} wechat={has_wechat} yt={has_youtube}")
    return pts, 15, " / ".join(notes)


def score_launchd() -> tuple[float, float, str]:
    """15 分: 本机 launchd plist 配置"""
    plist = Path.home() / "Library/LaunchAgents/com.hxz.news-reader.plist"
    pts = 0; notes = []
    if not plist.exists():
        return 0, 15, "缺 ~/Library/LaunchAgents/com.hxz.news-reader.plist"
    pts += 5; notes.append("plist 存在 ✓")
    text = plist.read_text()
    if "StartCalendarInterval" in text or "StartInterval" in text:
        pts += 3; notes.append("有触发时间 ✓")
    if "update_news.py" in text:
        pts += 3; notes.append("跑 update_news.py ✓")
    # 检查 launchctl 是否加载
    try:
        r = subprocess.run(
            ["launchctl", "list", "com.hxz.news-reader"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0:
            pts += 4; notes.append("launchctl 已加载 ✓")
        else:
            notes.append("⚠️ launchctl 未加载, 跑 `launchctl load <plist>`")
    except Exception:
        notes.append("⚠️ launchctl 查不到, 可能未 load")
    return pts, 15, " / ".join(notes)


def score_e2e_channels(quick: bool = False) -> tuple[float, float, str]:
    """30 分: 全 8 通道端到端跑通率 (每通道 3.75)"""
    if quick:
        # quick 模式只看最近一次跑的 status, 不实跑
        latest = _find_latest_status()
        if not latest:
            return 0, 30, "quick 模式找不到 source-status.json"
        return _score_from_status(latest), 30, f"quick 模式, 用 {latest}"
    # full 模式: 实跑
    out_dir = "/tmp/hxz_score_e2e"
    subprocess.run(["/bin/rm", "-rf", out_dir], check=False)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(ROOT / "scripts/update_news.py"),
           "--enable-x", "--enable-wechat", "--enable-youtube",
           "--enable-bilibili", "--enable-xiaoyuzhou",
           "--output-dir", out_dir,
           "--window-hours", "168"]
    print(f"  跑端到端 (预计 5-15 分钟)...", flush=True)
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=ROOT)
        elapsed = time.time() - t0
    except subprocess.TimeoutExpired:
        return 0, 30, "e2e timeout > 30 分钟"
    if r.returncode != 0:
        return 0, 30, f"e2e exit {r.returncode}: {r.stderr[-300:]}"
    sf = Path(out_dir) / "source-status.json"
    if not sf.exists():
        return 0, 30, "未产出 source-status.json"
    return _score_from_status(sf), 30, f"实跑 OK, {elapsed:.0f}s"


def _find_latest_status() -> Path | None:
    candidates = [
        ROOT / "data/source-status.json",
        Path("/tmp/hxz_score_e2e/source-status.json"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _score_from_status(sf: Path) -> float:
    """从 source-status.json 计算 8 通道得分 (30 分制)"""
    d = json.loads(sf.read_text())
    channels = {"rss": [], "podcast": [], "hf_api": [], "wechat": [],
                "youtube": [], "x_handle": [], "bilibili": [], "xiaoyuzhou": []}
    for s in d.get("sources", []):
        t = s.get("type")
        if t in channels:
            err = s.get("error", "")
            if "skipped" in err:
                continue
            channels[t].append(s)
    # 8 类: rss/substack/hf/wechat/youtube/x/bilibili/xiaoyuzhou
    # rss 合并聚合 + Substack (都 type=rss)
    pts = 0
    per = 30 / 8
    for t, srcs in channels.items():
        if not srcs:
            continue
        ok = sum(1 for s in srcs if s.get("ok") and s.get("count", 0) > 0)
        ratio = ok / len(srcs) if srcs else 0
        pts += per * ratio
    return pts


def score_state_files() -> tuple[float, float, str]:
    """10 分: state 增量推进正确"""
    pts = 0; notes = []
    discover = ROOT / "state/discover.json"
    bridge = ROOT / "state/getnote_bridge.json"
    if discover.exists():
        pts += 4; notes.append(f"discover.json ({len(json.loads(discover.read_text()))} 源)")
    else:
        notes.append("⚠️ discover.json 缺")
    if bridge.exists():
        b = json.loads(bridge.read_text())
        used = sum(b.get("daily", {}).values())
        pts += 3; notes.append(f"bridge.json (今日 {used}/100)")
        if used < 50:
            pts += 3; notes.append("配额健康 ✓")
        elif used < 90:
            pts += 1; notes.append("⚠️ 配额过半")
    else:
        notes.append("⚠️ getnote_bridge.json 缺")
    return pts, 10, " / ".join(notes)


def score_error_log() -> tuple[float, float, str]:
    """10 分: 错误日志干净, source-status.json 中 failed ≤ 1"""
    sf = _find_latest_status()
    if not sf:
        return 0, 10, "找不到 source-status.json"
    d = json.loads(sf.read_text())
    failed = [s for s in d.get("sources", []) if not s.get("ok")]
    n = len(failed)
    if n == 0: return 10, 10, "0 失败 ✓"
    if n == 1: return 8, 10, f"1 失败: {failed[0]['id']}"
    if n <= 3: return 5, 10, f"{n} 失败"
    if n <= 6: return 2, 10, f"{n} 失败 ⚠️"
    return 0, 10, f"{n} 失败 ❌"


def score_runbook() -> tuple[float, float, str]:
    """10 分: 凭证维护文档"""
    runbook = ROOT / "docs/RUNBOOK.md"
    if not runbook.exists():
        return 0, 10, "缺 docs/RUNBOOK.md"
    text = runbook.read_text()
    pts = 2; notes = ["存在 ✓"]
    keywords = ["biji", "TWITTER", "WeWe-RSS", "queryId", "凭证"]
    for k in keywords:
        if k in text:
            pts += 1.5; notes.append(f"含 {k} ✓")
    return min(pts, 10), 10, " / ".join(notes)


def score_resource() -> tuple[float, float, str]:
    """10 分: 资源占用合理"""
    pts = 0; notes = []
    # 检查 data_local 大小
    if (ROOT / "data_local").exists():
        size_mb = sum(f.stat().st_size for f in (ROOT / "data_local").rglob("*") if f.is_file()) / 1024 / 1024
        if size_mb < 100:
            pts += 5; notes.append(f"data_local {size_mb:.1f}MB ✓")
        else:
            pts += 2; notes.append(f"⚠️ data_local {size_mb:.1f}MB 偏大")
    # 检查写配额今日
    bridge = ROOT / "state/getnote_bridge.json"
    if bridge.exists():
        b = json.loads(bridge.read_text())
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        used_today = b.get("daily", {}).get(today, 0)
        if used_today <= 30:
            pts += 5; notes.append(f"今日写 {used_today}/100 ✓")
        else:
            pts += 2; notes.append(f"⚠️ 今日写 {used_today}/100")
    else:
        pts += 2; notes.append("state 未初始化")
    return pts, 10, " / ".join(notes)


# ============================================================
# 汇总
# ============================================================

DIMENSIONS = [
    ("GitHub Actions workflow",  score_github_workflow,   "workflow.yml"),
    ("本机 launchd plist",        score_launchd,           "plist"),
    ("8 通道端到端跑通",          score_e2e_channels,      "e2e"),
    ("state 增量正确",            score_state_files,       "state"),
    ("错误日志干净",              score_error_log,         "errors"),
    ("Runbook 完整",              score_runbook,           "runbook"),
    ("资源占用合理",              score_resource,          "resource"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    results = []
    total = 0; max_total = 0
    for name, fn, key in DIMENSIONS:
        try:
            if key == "e2e":
                got, mx, msg = fn(quick=args.quick)
            else:
                got, mx, msg = fn()
        except Exception as e:
            got, mx, msg = 0, 0, f"评分异常: {type(e).__name__}: {e}"
        results.append({"name": name, "score": got, "max": mx, "msg": msg, "key": key})
        total += got
        max_total += mx

    pct = total / max_total * 100 if max_total else 0
    verdict = "PASS" if total >= PASS else "FAIL"

    if args.json:
        print(json.dumps({"total": total, "max": max_total, "pct": pct,
                          "pass": PASS, "verdict": verdict, "dims": results},
                         ensure_ascii=False, indent=2))
        return 0 if total >= PASS else 1

    print(f"\n=== HXZ News Reader 自动化健康打分 · {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
    print(f"{'维度':25s} {'得分':>10s}  说明")
    print("-" * 80)
    for r in results:
        print(f"{r['name']:25s} {r['score']:5.1f} / {r['max']:>3d}  {r['msg']}")
    print("-" * 80)
    print(f"{'总分':25s} {total:5.1f} / {max_total:>3d}  ({pct:.1f}%)")
    print(f"达标线: {PASS}     状态: {'✅ PASS' if total >= PASS else '❌ FAIL'}")

    if total < PASS:
        print(f"\n推荐修复（按低分优先）:")
        for r in sorted(results, key=lambda x: x["score"] / (x["max"] or 1)):
            if r["max"] > 0 and r["score"] < r["max"]:
                print(f"  → {r['name']}: {r['msg']}")
    return 0 if total >= PASS else 1


if __name__ == "__main__":
    sys.exit(main())
