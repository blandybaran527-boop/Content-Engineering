#!/usr/bin/env python3
"""launchd 入口 (替代 run_local.sh 避开 bash TCC 限制)。

跑 5 类本机通道 + build_local_index。
日志: ~/Library/Logs/hxz-news-reader.log
"""
from __future__ import annotations
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/admin/Downloads/hxz-news-reader")
LOG = Path.home() / "Library/Logs/hxz-news-reader.log"
PY = "/usr/bin/python3"


def load_env_file(p: Path) -> None:
    """读 ~/.claude/skills/getnote/.env 注入 os.environ"""
    if not p.exists():
        return
    for raw in p.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip('"').strip("'")
        os.environ[k.strip()] = v


def log_print(*args):
    msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + " ".join(str(a) for a in args)
    print(msg, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(msg + "\n")


def main():
    log_print("================================================================")
    log_print("hxz-news-reader launchd job start")
    log_print(f"  ROOT: {ROOT} (exists={ROOT.exists()})")
    log_print(f"  PWD: {os.getcwd()}")

    # 1) 注入 getnote 凭证
    load_env_file(Path.home() / ".claude/skills/getnote/.env")
    log_print(f"  getnote env loaded: GETNOTE_API_KEY={'set' if os.environ.get('GETNOTE_API_KEY') else 'MISSING'}")
    log_print(f"  twitter env: AUTH_TOKEN={'set' if os.environ.get('TWITTER_AUTH_TOKEN') else 'MISSING'}")

    # 2) 跑 update_news.py 全本机通道
    log_print("→ update_news.py --enable-x --enable-youtube --enable-wechat --enable-bilibili --enable-xiaoyuzhou")
    t0 = time.time()
    rc = subprocess.call([
        PY, str(ROOT / "scripts/update_news.py"),
        "--enable-x", "--enable-youtube",
        "--enable-wechat", "--enable-bilibili", "--enable-xiaoyuzhou",
        "--output-dir", str(ROOT / "data"),
        "--window-hours", "168",
    ], cwd=str(ROOT))
    log_print(f"  rc={rc} elapsed={time.time()-t0:.0f}s")

    # 3) 重建 data_local/items.json
    log_print("→ build_local_index.py")
    rc2 = subprocess.call([PY, str(ROOT / "scripts/build_local_index.py")], cwd=str(ROOT))
    log_print(f"  rc={rc2}")

    log_print("done\n")


if __name__ == "__main__":
    main()
