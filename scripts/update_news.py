#!/usr/bin/env python3
"""HXZ News Reader: 拉取 feeds/sources.yaml 中的 RSS 信源，输出 data/items.json + data/source-status.json。

设计原则（与 ai-news-radar 一致）：
- 公开默认层无需任何 API Key
- 单个信源失败不阻塞整体流程
- X / WeChat 等不稳定桥默认跳过，由开关启用
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import feedparser
import requests
import yaml


# 本地 WeWe-RSS 桥（127.0.0.1）不走系统代理（梯子），否则 502
_no_proxy = os.environ.get("NO_PROXY", "")
for _host in ("127.0.0.1", "localhost"):
    if _host not in _no_proxy:
        _no_proxy = (_no_proxy + "," + _host).strip(",")
os.environ["NO_PROXY"] = _no_proxy
os.environ["no_proxy"] = _no_proxy


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = ROOT / "feeds" / "sources.yaml"
X_STATE_FILE = ROOT / "data" / "x-state.json"
X_FAIL_THRESHOLD = 3  # 连续失败超过即降级


@dataclass
class RawItem:
    site_id: str
    site_name: str
    group: str
    category: str
    title: str
    url: str
    published_at: str  # ISO8601
    summary: str = ""
    content_html: str = ""  # 原文 HTML（Substack 等 RSS 的 content:encoded 全文）
    media: Optional[list] = None  # [{type, url, width, height}] 仅 X 模态用
    author: Optional[dict] = None  # {name, screenName, profileImageUrl} 仅 X 模态用

    def key(self) -> str:
        return f"{self.site_id}::{self.url}"


@dataclass
class SourceStatus:
    id: str
    name: str
    type: str
    ok: bool
    count: int = 0
    error: str = ""
    fetched_at: str = ""


def load_sources(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    if not isinstance(data, list):
        raise ValueError(f"sources.yaml must be a list, got {type(data)}")
    return data


def parse_dt(value: Any) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, time.struct_time):
        return datetime(*value[:6], tzinfo=timezone.utc)
    if isinstance(value, str):
        # feedparser already gives struct_time for known formats; fall back to dateutil-lite
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return None
    return None


def _get_with_retry(session: requests.Session, url: str, retries: int = 3, backoff: float = 1.5):
    last_exc = None
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=20, headers={"User-Agent": "hxz-news-reader/0.1 (+https://github.com/blandybaran527-boop/Content-Engineering)"})
            if resp.status_code in (500, 502, 503, 504):
                last_exc = requests.HTTPError(f"{resp.status_code} {resp.reason}", response=resp)
                time.sleep(backoff * (attempt + 1))
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            last_exc = e
            time.sleep(backoff * (attempt + 1))
    raise last_exc


def fetch_rss(src: dict[str, Any], session: requests.Session, window_hours: int) -> tuple[list[RawItem], SourceStatus]:
    status = SourceStatus(id=src["id"], name=src["name"], type=src["type"], ok=False, fetched_at=datetime.now(timezone.utc).isoformat())
    url = (src.get("url") or "").strip()
    if not url:
        status.error = "empty url"
        return [], status

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    items: list[RawItem] = []
    try:
        resp = _get_with_retry(session, url)
        feed = feedparser.parse(resp.content)
        for entry in feed.entries:
            published = parse_dt(entry.get("published_parsed") or entry.get("updated_parsed") or entry.get("published") or entry.get("updated"))
            if published is None:
                # Some feeds (HN) provide pubDate via 'published' string
                published = datetime.now(timezone.utc)
            if published < cutoff:
                continue
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            if not title or not link:
                continue
            summary = re.sub(r"<[^>]+>", "", entry.get("summary") or "")[:280]
            # content:encoded 全文（Substack/Newsletter 通常带）
            content_html = ""
            content_list = entry.get("content") or []
            if content_list and isinstance(content_list, list):
                content_html = (content_list[0].get("value") or "").strip()
            if not content_html:
                content_html = (entry.get("summary") or "").strip()
            items.append(RawItem(
                site_id=src["id"],
                site_name=src["name"],
                group=src.get("group", ""),
                category=src.get("category", ""),
                title=title,
                url=link,
                published_at=published.astimezone(timezone.utc).isoformat(),
                summary=summary,
                content_html=content_html,
            ))
        status.ok = True
        status.count = len(items)
    except Exception as e:
        status.error = f"{type(e).__name__}: {e}"
    return items, status


def fetch_hf_papers(src: dict[str, Any], session: requests.Session, window_hours: int) -> tuple[list[RawItem], SourceStatus]:
    """HuggingFace Daily Papers 走官方 API（无 RSS）。"""
    status = SourceStatus(id=src["id"], name=src["name"], type=src["type"], ok=False, fetched_at=datetime.now(timezone.utc).isoformat())
    url = (src.get("url") or "").strip()
    if not url:
        status.error = "empty url"
        return [], status
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    try:
        resp = session.get(url, timeout=20, params={"limit": 100}, headers={"User-Agent": "hxz-news-reader/0.1"})
        resp.raise_for_status()
        data = resp.json()
        items: list[RawItem] = []
        for entry in data:
            paper = entry.get("paper", {}) or {}
            pid = paper.get("id")
            if not pid:
                continue
            published = parse_dt(paper.get("publishedAt") or entry.get("publishedAt"))
            if published is None:
                published = datetime.now(timezone.utc)
            if published < cutoff:
                continue
            title = (paper.get("title") or "").strip()
            summary = (paper.get("summary") or "").strip()[:280]
            items.append(RawItem(
                site_id=src["id"],
                site_name=src["name"],
                group=src.get("group", ""),
                category=src.get("category", ""),
                title=title,
                url=f"https://huggingface.co/papers/{pid}",
                published_at=published.astimezone(timezone.utc).isoformat(),
                summary=summary,
            ))
        status.ok = True
        status.count = len(items)
        return items, status
    except Exception as e:
        status.error = f"{type(e).__name__}: {e}"
        return [], status


def load_x_state() -> dict[str, dict[str, Any]]:
    if not X_STATE_FILE.exists():
        return {}
    try:
        return json.loads(X_STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_x_state(state: dict[str, dict[str, Any]]) -> None:
    X_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    X_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def cookie_probe(handle: str = "AnthropicAI", timeout: int = 15) -> tuple[bool, str]:
    """跑批前用 1 个号探 1 条，验证 Cookie 还活着。"""
    if not shutil.which("twitter"):
        return False, "twitter-cli not installed (uv tool install twitter-cli)"
    if not (os.environ.get("TWITTER_AUTH_TOKEN") and os.environ.get("TWITTER_CT0")):
        return False, "TWITTER_AUTH_TOKEN / TWITTER_CT0 not set"
    try:
        r = subprocess.run(
            ["twitter", "user-posts", handle, "-n", "1", "--json"],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode != 0:
            return False, f"twitter exit {r.returncode}: {r.stderr.strip()[:200]}"
        data = json.loads(r.stdout or "{}")
        if not data.get("ok") or not data.get("data"):
            return False, f"empty/invalid response: {str(data)[:200]}"
        return True, "ok"
    except subprocess.TimeoutExpired:
        return False, f"probe timeout > {timeout}s"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def fetch_x_handle_via_cli(
    src: dict[str, Any],
    state: dict[str, dict[str, Any]],
    window_hours: int,
    n_per_handle: int = 30,
    timeout: int = 30,
) -> tuple[list[RawItem], SourceStatus]:
    """走 twitter-cli (Cookie) 抓单个 handle。增量 + 失败计数。"""
    status = SourceStatus(
        id=src["id"], name=src["name"], type=src["type"], ok=False,
        fetched_at=datetime.now(timezone.utc).isoformat(),
    )
    handle = src.get("x_handle") or src["name"]
    handle_state = state.setdefault(handle, {"last_seen_id": None, "fail_count": 0, "last_success_at": None})

    # 连续失败 >= 阈值：降级为"仅展示链接"，不再尝试
    if handle_state.get("fail_count", 0) >= X_FAIL_THRESHOLD:
        status.error = f"degraded after {handle_state['fail_count']} consecutive failures; link-only"
        status.ok = True  # 不视为本次错误
        return [], status

    try:
        r = subprocess.run(
            ["twitter", "user-posts", handle, "-n", str(n_per_handle), "--json"],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode != 0:
            raise RuntimeError(f"twitter exit {r.returncode}: {r.stderr.strip()[:200]}")
        data = json.loads(r.stdout or "{}")
        if not data.get("ok"):
            raise RuntimeError(f"twitter ok=false: {str(data)[:200]}")
        tweets = data.get("data") or []
    except Exception as e:
        handle_state["fail_count"] = handle_state.get("fail_count", 0) + 1
        status.error = f"{type(e).__name__}: {e}"
        return [], status

    # 成功：重置失败计数
    handle_state["fail_count"] = 0
    handle_state["last_success_at"] = datetime.now(timezone.utc).isoformat()

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    last_seen_id = handle_state.get("last_seen_id")
    items: list[RawItem] = []
    newest_id_this_run = None

    for tw in tweets:
        tid = str(tw.get("id") or "")
        if not tid:
            continue
        # 记录本次最大 id 用于增量
        if newest_id_this_run is None or tid > newest_id_this_run:
            newest_id_this_run = tid
        # 增量去重：比 last_seen_id 旧的全跳
        if last_seen_id and tid <= last_seen_id:
            continue
        # 过滤转推：用户说订阅这些号是为了听他们自己的声音
        if tw.get("isRetweet"):
            continue
        # 时间窗过滤
        published = parse_dt(tw.get("createdAtISO") or tw.get("createdAt"))
        if published is None:
            published = datetime.now(timezone.utc)
        if published < cutoff:
            continue
        text = (tw.get("text") or "").strip()
        # 清理文末的 t.co 短链（媒体本体），避免渲染时显示冗余尾巴
        text = re.sub(r"\s+https?://t\.co/\S+\s*$", "", text).strip()
        if not text:
            continue
        # 保留媒体字段（缩略图渲染用）和作者信息（头像）
        media = tw.get("media") or []
        author = tw.get("author") or {}
        author_slim = {
            "name": author.get("name", ""),
            "screenName": author.get("screenName", handle),
            "profileImageUrl": author.get("profileImageUrl", ""),
        } if author else None
        items.append(RawItem(
            site_id=src["id"],
            site_name=src["name"],
            group=src.get("group", ""),
            category=src.get("category", ""),
            title=text[:120],
            url=f"https://x.com/{handle}/status/{tid}",
            published_at=published.astimezone(timezone.utc).isoformat(),
            summary=text[:280],
            media=media if media else None,
            author=author_slim,
        ))

    if newest_id_this_run:
        handle_state["last_seen_id"] = newest_id_this_run
    status.ok = True
    status.count = len(items)
    return items, status


def fetch_x_handle(src: dict[str, Any], session: requests.Session, window_hours: int, bearer: Optional[str]) -> tuple[list[RawItem], SourceStatus]:
    status = SourceStatus(id=src["id"], name=src["name"], type=src["type"], ok=False, fetched_at=datetime.now(timezone.utc).isoformat())
    handle = src.get("x_handle") or src["name"]
    if not bearer:
        status.error = "X_BEARER_TOKEN not set; skip cleanly"
        return [], status
    try:
        # Step 1: lookup user id
        r = session.get(
            f"https://api.twitter.com/2/users/by/username/{handle}",
            headers={"Authorization": f"Bearer {bearer}"},
            timeout=15,
        )
        r.raise_for_status()
        user_id = r.json()["data"]["id"]
        # Step 2: recent tweets
        start_time = (datetime.now(timezone.utc) - timedelta(hours=window_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
        r = session.get(
            f"https://api.twitter.com/2/users/{user_id}/tweets",
            params={
                "max_results": 20,
                "exclude": "retweets,replies",
                "start_time": start_time,
                "tweet.fields": "created_at",
            },
            headers={"Authorization": f"Bearer {bearer}"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json().get("data", []) or []
        items = []
        for tw in data:
            published = parse_dt(tw.get("created_at")) or datetime.now(timezone.utc)
            items.append(RawItem(
                site_id=src["id"],
                site_name=src["name"],
                group=src.get("group", ""),
                category=src.get("category", ""),
                title=(tw.get("text") or "")[:120],
                url=f"https://x.com/{handle}/status/{tw['id']}",
                published_at=published.astimezone(timezone.utc).isoformat(),
                summary=(tw.get("text") or "")[:280],
            ))
        status.ok = True
        status.count = len(items)
        return items, status
    except Exception as e:
        status.error = f"{type(e).__name__}: {e}"
        return [], status


def normalize_items(items: list[RawItem]) -> list[dict[str, Any]]:
    seen = set()
    out = []
    for it in items:
        k = it.key()
        if k in seen:
            continue
        seen.add(k)
        out.append(asdict(it))
    out.sort(key=lambda x: x["published_at"], reverse=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default=str(DEFAULT_SOURCES))
    ap.add_argument("--output-dir", default=str(ROOT / "data"))
    ap.add_argument("--window-hours", type=int, default=48)
    ap.add_argument("--enable-x", action="store_true", help="Fetch X handles (default: twitter-cli with Cookie; fallback to Bearer)")
    ap.add_argument("--x-via", choices=("cli", "bearer"), default="cli", help="X 抓取通道：cli=twitter-cli+Cookie（免费稳定），bearer=官方 API（付费）")
    ap.add_argument("--x-sleep", type=float, default=5.0, help="X handle 之间的节流秒数")
    ap.add_argument("--x-per-handle", type=int, default=30, help="X 每号最多拉多少条")
    ap.add_argument("--enable-wechat", action="store_true", help="Fetch wechat sources that have RSS URL")
    ap.add_argument("--enable-podcast", action="store_true", help="Fetch podcast sources that have RSS URL")
    ap.add_argument("--probe-only", help="Run a single source by id only")
    args = ap.parse_args()

    sources_path = Path(args.sources)
    if not sources_path.exists():
        print(f"sources.yaml not found: {sources_path}", file=sys.stderr)
        sys.exit(1)

    sources = load_sources(sources_path)
    if args.probe_only:
        sources = [s for s in sources if s["id"] == args.probe_only]
        if not sources:
            print(f"no source with id={args.probe_only}", file=sys.stderr)
            sys.exit(1)

    bearer = os.environ.get("X_BEARER_TOKEN", "").strip() or None
    session = requests.Session()

    # X 路径决策：默认 CLI（免费），bearer 模式才用官方 API
    x_via = args.x_via
    x_state = load_x_state() if args.enable_x else {}
    x_first = True  # 控制节流：第一个 handle 不睡

    # Cookie 探针：CLI 模式下跑批前先确认 Cookie 活着
    if args.enable_x and x_via == "cli" and not args.probe_only:
        ok, msg = cookie_probe()
        if not ok:
            print(f"[hxz-news-reader] X Cookie 探针失败：{msg}", file=sys.stderr)
            print("[hxz-news-reader] 跳过本次 X 抓取。重新导出 Cookie 后再跑。", file=sys.stderr)
            args.enable_x = False
        else:
            print(f"[hxz-news-reader] X Cookie 探针 OK")

    all_items: list[RawItem] = []
    statuses: list[SourceStatus] = []

    for src in sources:
        t = src.get("type")
        default_on = bool(src.get("default", False))

        # Decide whether to fetch
        should_fetch = False
        if args.probe_only:
            should_fetch = True
        elif t in ("rss", "hf_api"):
            should_fetch = default_on
        elif t == "x_handle":
            should_fetch = args.enable_x and (x_via == "cli" or bool(bearer))
        elif t == "wechat":
            should_fetch = args.enable_wechat and bool((src.get("url") or "").strip())
        elif t == "podcast":
            should_fetch = args.enable_podcast and bool((src.get("url") or "").strip())

        if not should_fetch:
            statuses.append(SourceStatus(id=src["id"], name=src["name"], type=t, ok=True, count=0, error="skipped (not in default layer)", fetched_at=datetime.now(timezone.utc).isoformat()))
            continue

        if t in ("rss", "wechat", "podcast"):
            items, status = fetch_rss(src, session, args.window_hours)
        elif t == "hf_api":
            items, status = fetch_hf_papers(src, session, args.window_hours)
        elif t == "x_handle":
            if not x_first:
                time.sleep(args.x_sleep)
            x_first = False
            if x_via == "cli":
                items, status = fetch_x_handle_via_cli(src, x_state, args.window_hours, args.x_per_handle)
            else:
                items, status = fetch_x_handle(src, session, args.window_hours, bearer)
            # 每号跑完打印进度，方便 tail -f 看
            marker = "✓" if status.ok and not status.error else ("◐" if status.ok else "✗")
            print(f"  {marker} {src.get('x_handle', src['name']):25s}  items={status.count}  {status.error[:60]}", flush=True)
        else:
            status = SourceStatus(id=src["id"], name=src["name"], type=t or "?", ok=False, error=f"unknown type: {t}", fetched_at=datetime.now(timezone.utc).isoformat())
            items = []
        all_items.extend(items)
        statuses.append(status)

    # 保存 X 增量 state
    if args.enable_x and x_via == "cli":
        save_x_state(x_state)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    items_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_hours": args.window_hours,
        "items": normalize_items(all_items),
    }
    (out_dir / "items.json").write_text(json.dumps(items_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    status_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": [asdict(s) for s in statuses],
        "summary": {
            "total_sources": len(statuses),
            "ok": sum(1 for s in statuses if s.ok),
            "failed": sum(1 for s in statuses if not s.ok),
            "items": len(items_payload["items"]),
        },
    }
    (out_dir / "source-status.json").write_text(json.dumps(status_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[hxz-news-reader] sources={status_payload['summary']['total_sources']} ok={status_payload['summary']['ok']} failed={status_payload['summary']['failed']} items={status_payload['summary']['items']}")
    for s in statuses:
        if not s.ok and s.error and "skipped" not in s.error:
            print(f"  ! {s.id} ({s.type}): {s.error}")


if __name__ == "__main__":
    main()
