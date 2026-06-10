"""一次性脚本：把 sources.yaml 里 type=x_handle 的账号加进指定 X List。

实现：用 cookie + httpx 直接调 X 内部 GraphQL（ListAddMember mutation）。
不依赖 twikit（其 client-transaction-id 算法已被 X 改前端打挂）。

用法：
    # 干跑看清单
    python3 scripts/x_list/add_members.py --list-id <ID> --dry-run
    # 加 1 个验证写权限
    python3 scripts/x_list/add_members.py --list-id <ID> --limit 1 --sleep 0
    # 第一天加 0-37
    python3 scripts/x_list/add_members.py --list-id <ID> --start 0 --end 38
    # 第二天加 38-76
    python3 scripts/x_list/add_members.py --list-id <ID> --start 38 --end 76

环境变量：TWITTER_AUTH_TOKEN, TWITTER_CT0
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "feeds" / "sources.yaml"

# 公开的 web bearer，所有 x.com 浏览器请求共用同一个
BEARER = (
    "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
    "%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
)
LIST_ADD_QID = "lLNsL7mW6gSEQG6rXP7TNw"
LIST_ADD_URL = f"https://x.com/i/api/graphql/{LIST_ADD_QID}/ListAddMember"
LIST_FEATURES = {
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True,
}
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def load_handles() -> list[str]:
    data = yaml.safe_load(SOURCES.read_text())
    items = data if isinstance(data, list) else data.get("sources", [])
    handles = []
    for item in items:
        if item.get("type") == "x_handle":
            h = item.get("x_handle") or item.get("name")
            if h:
                handles.append(h)
    return handles


TWSCRAPE_DB = os.environ.get("TWSCRAPE_DB", "/Users/admin/accounts.db")


def get_user_id(handle: str) -> str:
    """用 twscrape CLI 拿 user_id（twscrape 已配代理和 cookie 池）。"""
    out = subprocess.run(
        ["twscrape", "--db", TWSCRAPE_DB, "user_by_login", handle],
        capture_output=True, text=True, timeout=60,
    )
    # 末尾一行是 JSON（stderr 是日志，stdout 是 JSON 输出）
    for line in reversed(out.stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return str(json.loads(line)["id"])
            except Exception:
                continue
    raise RuntimeError(f"user_by_login 失败: stderr={out.stderr[:200]} stdout={out.stdout[:200]}")


def add_member(client: httpx.Client, list_id: str, user_id: str, ct0: str, auth: str):
    payload = {
        "variables": {"listId": list_id, "userId": user_id},
        "features": LIST_FEATURES,
        "queryId": LIST_ADD_QID,
    }
    headers = {
        "authorization": f"Bearer {BEARER}",
        "x-csrf-token": ct0,
        "cookie": f"auth_token={auth}; ct0={ct0}",
        "content-type": "application/json",
        "user-agent": UA,
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
    }
    r = client.post(LIST_ADD_URL, json=payload, headers=headers, timeout=30)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-id", required=True)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=None, help="exclusive")
    ap.add_argument("--limit", type=int, default=None, help="alias: end = start + limit")
    ap.add_argument("--sleep", type=float, default=60.0)
    ap.add_argument("--proxy", default="http://127.0.0.1:7890")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    auth = os.environ.get("TWITTER_AUTH_TOKEN")
    ct0 = os.environ.get("TWITTER_CT0")
    if not auth or not ct0:
        print("缺少 TWITTER_AUTH_TOKEN / TWITTER_CT0", file=sys.stderr)
        sys.exit(1)

    handles = load_handles()
    if args.limit is not None:
        args.end = args.start + args.limit
    if args.end is None:
        args.end = len(handles)
    batch = handles[args.start:args.end]

    print(f"将处理 {len(batch)} 个 handle (index {args.start}~{args.end-1} / 共 {len(handles)})")
    print(f"list_id={args.list_id}  间隔 {args.sleep}s  代理 {args.proxy}")
    print(f"预计耗时 ~{int(len(batch) * (args.sleep + 12) / 60)} 分钟（每个 ~12s 拿 user_id + {int(args.sleep)}s 间隔）")
    if args.dry_run:
        for i, h in enumerate(batch, start=args.start):
            print(f"  [{i:2d}] {h}")
        return

    client = httpx.Client(proxy=args.proxy)
    ok, fail = 0, 0
    consecutive_fail = 0
    for idx, h in enumerate(batch, start=args.start):
        try:
            uid = get_user_id(h)
            r = add_member(client, args.list_id, uid, ct0, auth)
            try:
                resp = r.json()
            except Exception:
                resp = {}
            # X 返回会带 banner media 解码 errors（与 add_member 无关），看 data.list 是否存在为准
            list_obj = (resp or {}).get("data", {}).get("list") if isinstance(resp, dict) else None
            if r.status_code == 200 and list_obj:
                ok += 1
                consecutive_fail = 0
                print(f"  [{idx:2d}] ✅ {h:25s}  user_id={uid}", flush=True)
            else:
                fail += 1
                consecutive_fail += 1
                print(f"  [{idx:2d}] ❌ {h:25s}  HTTP {r.status_code}  {r.text[:200]}", flush=True)
        except Exception as e:
            fail += 1
            consecutive_fail += 1
            print(f"  [{idx:2d}] ❌ {h:25s}  {type(e).__name__}: {str(e)[:120]}", flush=True)
        if consecutive_fail >= 3:
            print(f"\n⚠️  连续 {consecutive_fail} 次失败，中止以避免风控。已成功 {ok}，从 index {idx+1} 续跑", flush=True)
            break
        if idx < args.start + len(batch) - 1:
            time.sleep(args.sleep)

    print(f"\n完成：成功 {ok}  失败 {fail}")
    client.close()


if __name__ == "__main__":
    main()
