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
DEFAULT_X_LIST_ID = "2064609881357975740"  # HXZ-AI-Sources List
TWSCRAPE_DB = os.environ.get("TWSCRAPE_DB", "/Users/admin/accounts.db")


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


def fetch_x_list(
    list_id: str,
    x_sources: list[dict[str, Any]],
    window_hours: int,
    per_handle_limit: int = 50,
    timeout: int = 180,
) -> tuple[list[RawItem], list[SourceStatus]]:
    """一次调用 twscrape list_timeline 抓 List 里所有成员的最新推文。
    按 user.username 反向匹配 sources 得到 site_id。
    返回 (items, statuses)，statuses 覆盖所有 x_sources（每个 handle 一条）。
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    # handle -> source dict（小写 key 避免大小写不一致）
    handle_to_src = {}
    for s in x_sources:
        h = (s.get("x_handle") or s.get("name") or "").lower()
        if h:
            handle_to_src[h] = s

    # 全 list 的拉取上限 = handles 数 × per_handle_limit
    total_limit = max(100, len(x_sources) * per_handle_limit)

    try:
        r = subprocess.run(
            ["twscrape", "--db", TWSCRAPE_DB, "list_timeline", list_id, "--limit", str(total_limit)],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode != 0:
            err = f"twscrape exit {r.returncode}: {r.stderr.strip()[:300]}"
            return [], [_x_skip_status(s, err, now_iso) for s in x_sources]
    except subprocess.TimeoutExpired:
        err = f"twscrape list_timeline timeout > {timeout}s"
        return [], [_x_skip_status(s, err, now_iso) for s in x_sources]
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        return [], [_x_skip_status(s, err, now_iso) for s in x_sources]

    # twscrape 输出：JSONL，每行一条推文
    tweets = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            tweets.append(json.loads(line))
        except Exception:
            continue

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    items: list[RawItem] = []
    counts: dict[str, int] = {}

    for tw in tweets:
        # 跳过转推：用户只想听原账号的声音
        if tw.get("retweetedTweet"):
            continue
        user = tw.get("user") or {}
        handle = (user.get("username") or "").strip()
        src = handle_to_src.get(handle.lower())
        if not src:
            continue  # List 里有但 sources.yaml 没收录的，忽略
        published = parse_dt(tw.get("date"))
        if published is None or published < cutoff:
            continue
        text = (tw.get("rawContent") or "").strip()
        text = re.sub(r"\s+https?://t\.co/\S+\s*$", "", text).strip()
        if not text:
            continue
        # 抽图：photos 优先，没图就空
        media_obj = tw.get("media") or {}
        photos = (media_obj.get("photos") or []) if isinstance(media_obj, dict) else []
        media_list = [{"type": "photo", "url": p.get("url") or p.get("media_url_https") or ""} for p in photos if p.get("url") or p.get("media_url_https")]
        author_slim = {
            "name": user.get("displayname", ""),
            "screenName": handle,
            "profileImageUrl": user.get("profileImageUrl", ""),
        }
        tid = tw.get("id_str") or str(tw.get("id") or "")
        items.append(RawItem(
            site_id=src["id"],
            site_name=src["name"],
            group=src.get("group", ""),
            category=src.get("category", ""),
            title=text[:120],
            url=tw.get("url") or f"https://x.com/{handle}/status/{tid}",
            published_at=published.astimezone(timezone.utc).isoformat(),
            summary=text[:280],
            media=media_list or None,
            author=author_slim,
        ))
        counts[src["id"]] = counts.get(src["id"], 0) + 1

    statuses = []
    for s in x_sources:
        c = counts.get(s["id"], 0)
        statuses.append(SourceStatus(
            id=s["id"], name=s["name"], type=s["type"],
            ok=True, count=c,
            error="" if c > 0 else "no items in window",
            fetched_at=now_iso,
        ))
    return items, statuses


def _x_skip_status(s: dict[str, Any], err: str, ts: str) -> SourceStatus:
    return SourceStatus(id=s["id"], name=s["name"], type=s["type"], ok=False, count=0, error=err, fetched_at=ts)


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
    ap.add_argument("--enable-x", action="store_true", help="Fetch X via List timeline (one call for all handles)")
    ap.add_argument("--x-list-id", default=DEFAULT_X_LIST_ID, help="X List ID (须把所有 x_handle 加进此 List)")
    ap.add_argument("--x-per-handle", type=int, default=50, help="X 平均每号最多拉多少条（用于 list_timeline 总上限）")
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

    session = requests.Session()

    all_items: list[RawItem] = []
    statuses: list[SourceStatus] = []

    # 先把 X 源单独拎出来，最后一次性走 list_timeline
    x_sources = [s for s in sources if s.get("type") == "x_handle"]

    for src in sources:
        t = src.get("type")
        default_on = bool(src.get("default", False))

        should_fetch = False
        if args.probe_only:
            should_fetch = True
        elif t in ("rss", "hf_api"):
            should_fetch = default_on
        elif t == "x_handle":
            continue  # X 集中处理，跳过单条循环
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
        else:
            status = SourceStatus(id=src["id"], name=src["name"], type=t or "?", ok=False, error=f"unknown type: {t}", fetched_at=datetime.now(timezone.utc).isoformat())
            items = []
        all_items.extend(items)
        statuses.append(status)

    # X 渠道：一次 list_timeline 调用拉回 List 里所有成员的最新推文
    if args.enable_x and x_sources and not args.probe_only:
        print(f"[hxz-news-reader] X list_timeline list_id={args.x_list_id} handles={len(x_sources)}", flush=True)
        t0 = time.time()
        x_items, x_statuses = fetch_x_list(args.x_list_id, x_sources, args.window_hours, args.x_per_handle)
        elapsed = time.time() - t0
        print(f"[hxz-news-reader] X 完成: items={len(x_items)} 耗时 {elapsed:.1f}s", flush=True)
        all_items.extend(x_items)
        statuses.extend(x_statuses)
    elif x_sources:
        # X 关闭或 probe_only 时仍要给出 status 占位
        ts = datetime.now(timezone.utc).isoformat()
        for s in x_sources:
            statuses.append(SourceStatus(id=s["id"], name=s["name"], type=s["type"], ok=True, count=0, error="skipped (X disabled)", fetched_at=ts))

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
