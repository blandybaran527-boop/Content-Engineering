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
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import feedparser
import requests
import yaml


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = ROOT / "feeds" / "sources.yaml"


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


def fetch_rss(src: dict[str, Any], session: requests.Session, window_hours: int) -> tuple[list[RawItem], SourceStatus]:
    status = SourceStatus(id=src["id"], name=src["name"], type=src["type"], ok=False, fetched_at=datetime.now(timezone.utc).isoformat())
    url = (src.get("url") or "").strip()
    if not url:
        status.error = "empty url"
        return [], status

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    items: list[RawItem] = []
    try:
        resp = session.get(url, timeout=20, headers={"User-Agent": "hxz-news-reader/0.1 (+https://github.com/blandybaran527-boop/Content-Engineering)"})
        resp.raise_for_status()
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
            items.append(RawItem(
                site_id=src["id"],
                site_name=src["name"],
                group=src.get("group", ""),
                category=src.get("category", ""),
                title=title,
                url=link,
                published_at=published.astimezone(timezone.utc).isoformat(),
                summary=summary,
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
    ap.add_argument("--enable-x", action="store_true", help="Fetch X handles via X API (requires X_BEARER_TOKEN)")
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
            should_fetch = args.enable_x and bool(bearer)
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
            items, status = fetch_x_handle(src, session, args.window_hours, bearer)
        else:
            status = SourceStatus(id=src["id"], name=src["name"], type=t or "?", ok=False, error=f"unknown type: {t}", fetched_at=datetime.now(timezone.utc).isoformat())
            items = []
        all_items.extend(items)
        statuses.append(status)

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
