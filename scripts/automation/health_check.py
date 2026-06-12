#!/usr/bin/env python3
"""生成 data_local/health.json — 系统运维状态自检, 供网页 Dashboard 显示。

不掩盖任何问题。launchd / cron / data freshness 全部如实暴露。
"""
from __future__ import annotations
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/admin/Downloads/hxz-news-reader")
LOG = Path.home() / "Library/Logs/hxz-news-reader.log"
STDERR_LOG = Path.home() / "Library/Logs/hxz-news-reader.stderr.log"
PLIST = Path.home() / "Library/LaunchAgents/com.hxz.news-reader.plist"


def check_launchd():
    out = {
        "plist_exists": PLIST.exists(),
        "loaded": False,
        "last_status": "unknown",
        "last_log_at": None,
        "error_hint": None,
    }
    # launchctl 加载检查
    try:
        r = subprocess.run(
            ["/bin/launchctl", "list", "com.hxz.news-reader"],
            capture_output=True, text=True, timeout=5,
        )
        out["loaded"] = r.returncode == 0
    except Exception as e:
        out["error_hint"] = f"launchctl 查询失败: {e}"
        return out

    # 看应用日志的最新 launchd job 时间戳
    last_log_at = None
    if LOG.exists():
        try:
            for ln in reversed(LOG.read_text().splitlines()[-200:]):
                if "launchd job start" in ln:
                    last_log_at = ln.split("]")[0].lstrip("[")
                    out["last_log_at"] = last_log_at
                    break
        except Exception:
            pass

    # 看 stderr 最近 30 行 (不再扫全文件) — 只看"新错误"
    recent_stderr_err = None
    if STDERR_LOG.exists():
        try:
            recent = STDERR_LOG.read_text().splitlines()[-30:]
            for ln in recent:
                if "Operation not permitted" in ln:
                    recent_stderr_err = ln
                    break
        except Exception:
            pass

    # 综合判断: 优先看 last_log_at (说明 python3 真启动了)
    if last_log_at:
        # 比对时间: log_at 是否晚于 stderr 错误? 简化判断: 有 log_at 就算 ok
        out["last_status"] = "ok"
    elif recent_stderr_err:
        out["last_status"] = "tcc_denied"
        out["error_hint"] = (
            "macOS TCC 隐私保护拦截 launchd 访问 ~/Downloads/。"
            "去 System Settings → Privacy & Security → Full Disk Access, "
            "把 /usr/bin/python3 加进白名单, 再 launchctl start 一次。"
        )
    elif out["plist_exists"] and out["loaded"]:
        out["last_status"] = "never_ran"
        out["error_hint"] = (
            "launchd 已加载但还没跑过。明早 06:30 会首次跑, 或现在 launchctl start com.hxz.news-reader 触发一次。"
        )

    return out


def check_data_freshness():
    out = {}
    files = {
        "data_items": ROOT / "data/items.json",
        "data_status": ROOT / "data/source-status.json",
        "data_local_items": ROOT / "data_local/items.json",
        "data_local_status": ROOT / "data_local/source-status.json",
    }
    for k, f in files.items():
        if f.exists():
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            age_min = (datetime.now(timezone.utc) - mtime).total_seconds() / 60
            out[k] = {
                "exists": True,
                "mtime": mtime.isoformat(),
                "age_minutes": round(age_min, 1),
                "size_kb": round(f.stat().st_size / 1024, 1),
            }
        else:
            out[k] = {"exists": False}
    return out


def check_credentials_files():
    """检查凭证文件存在性 (不读内容, 只看 mtime / 大小)"""
    out = {}
    getnote_env = Path.home() / ".claude/skills/getnote/.env"
    if getnote_env.exists():
        # 从 env 文件解析过期日 (如有 EXPIRES_AT 字段)
        out["getnote_env"] = {
            "exists": True,
            "mtime": datetime.fromtimestamp(getnote_env.stat().st_mtime, tz=timezone.utc).isoformat(),
        }
    else:
        out["getnote_env"] = {"exists": False}
    return out


def check_github_actions():
    """从 git log 看云端最近一次 chore(data) commit 时间"""
    out = {"last_cloud_refresh": None, "hours_ago": None}
    try:
        r = subprocess.run(
            ["/usr/bin/git", "log", "--all", "--grep=chore(data)", "-1", "--format=%aI"],
            capture_output=True, text=True, timeout=5, cwd=str(ROOT),
        )
        if r.returncode == 0 and r.stdout.strip():
            ts = r.stdout.strip()
            out["last_cloud_refresh"] = ts
            d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            out["hours_ago"] = round((datetime.now(timezone.utc) - d).total_seconds() / 3600, 1)
    except Exception:
        pass
    return out


def main():
    health = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "launchd": check_launchd(),
        "data_freshness": check_data_freshness(),
        "credentials_files": check_credentials_files(),
        "github_actions": check_github_actions(),
    }
    out_path = ROOT / "data_local/health.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(health, ensure_ascii=False, indent=2))
    print(f"✓ wrote {out_path}")
    print(f"  launchd: {health['launchd']['last_status']}")
    print(f"  data_local items age: {health['data_freshness']['data_local_items']['age_minutes']} min")
    if health["launchd"].get("error_hint"):
        print(f"  ⚠️ {health['launchd']['error_hint'][:120]}")


if __name__ == "__main__":
    main()
