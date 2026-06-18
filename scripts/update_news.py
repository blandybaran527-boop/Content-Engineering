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
import random
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
DEFAULT_LOCAL_OUTPUT = ROOT / "data_local"  # 国内信源原文落地（gitignored）
DEFAULT_STATE_DIR = ROOT / "state"
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


def fetch_youtube(src: dict[str, Any], session: requests.Session, window_hours: int, discover_only: bool = False) -> tuple[list[RawItem], SourceStatus]:
    """YouTube 频道：RSS 拉新视频 + youtube-transcript-api 抓字幕。

    依赖住宅 IP 节点（梯子）才能稳定拿到 transcript；
    与 ai-news-radar 风格一致：单源失败不阻塞整体流程。
    discover_only=True 时只取 RSS 标题+描述、跳过字幕（字幕=全文，留给第二段）。
    """
    status = SourceStatus(id=src["id"], name=src["name"], type=src["type"], ok=False, fetched_at=datetime.now(timezone.utc).isoformat())
    url = (src.get("url") or "").strip()
    if not url:
        status.error = "empty url"
        return [], status

    # 延迟导入：让没装 youtube-transcript-api 的环境也能跑别的源
    api = None
    if not discover_only:
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            api = YouTubeTranscriptApi()
        except Exception as e:
            status.error = f"youtube_transcript_api not installed: {e}"
            return [], status

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    # discover-only 拉深做 30 天回填；常规模式默认 3 条防历史回灌
    max_videos = 15 if discover_only else int(src.get("max_videos") or 3)
    languages = src.get("languages") or ["en"]
    items: list[RawItem] = []
    try:
        resp = _get_with_retry(session, url)
        feed = feedparser.parse(resp.content)
        for entry in feed.entries[:max_videos]:
            published = parse_dt(entry.get("published_parsed") or entry.get("updated_parsed") or entry.get("published") or entry.get("updated"))
            if published is None:
                published = datetime.now(timezone.utc)
            if published < cutoff:
                continue
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            vid = (entry.get("yt_videoid") or "").strip()
            if not vid:
                # link 形如 https://www.youtube.com/watch?v=XXXX
                m = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", link)
                vid = m.group(1) if m else ""
            if not title or not vid:
                continue
            summary = re.sub(r"<[^>]+>", "", entry.get("summary") or "")[:280]

            # 抓字幕（核心）；discover-only 跳过——字幕=全文，留给第二段
            transcript_text = ""
            if not discover_only:
              try:
                tr = api.fetch(vid, languages=languages)
                snippets = list(tr)
                # 拼成 HTML：每段一行，方便 index.html "展开全文" 渲染
                lines = [(s.text or "").strip() for s in snippets if (s.text or "").strip()]
                # 简单分段：每 8 句空一行
                paragraphs: list[str] = []
                buf: list[str] = []
                for i, ln in enumerate(lines, 1):
                    buf.append(ln)
                    if i % 8 == 0:
                        paragraphs.append(" ".join(buf))
                        buf = []
                if buf:
                    paragraphs.append(" ".join(buf))
                transcript_text = "\n\n".join(f"<p>{p}</p>" for p in paragraphs)
              except Exception as e:
                # 字幕抓不到不阻塞整源；仍然记录这条视频元数据
                transcript_text = ""
                # 在 summary 末尾标记
                summary = (summary + f" [transcript fail: {type(e).__name__}]")[:280]

            items.append(RawItem(
                site_id=src["id"],
                site_name=src["name"],
                group=src.get("group", ""),
                category=src.get("category", ""),
                title=title,
                url=link or f"https://youtu.be/{vid}",
                published_at=published.astimezone(timezone.utc).isoformat(),
                summary=summary,
                content_html=transcript_text,
            ))
        status.ok = True
        status.count = len(items)
    except Exception as e:
        status.error = f"{type(e).__name__}: {e}"
    return items, status


# ============================================================
# 国内信源（D3）: B站 + 小宇宙 — 第一层 discover + 第二层 getnote_bridge
# ============================================================

def _load_discover_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def _save_discover_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2))


_TITLE_SAFE_RE = re.compile(r"[^\w一-鿿-]+")


def _safe_slug(s: str, maxlen: int = 40) -> str:
    out = _TITLE_SAFE_RE.sub("_", s or "")[:maxlen].strip("_")
    return out or "untitled"


def _write_local_post(out_root: Path, channel: str, src_id: str, pub_date: str, item_id: str, title: str, fetched: dict) -> Path:
    """落盘到 data_local/<channel>/<src_id>/<date>__<item_id>__<title>.md"""
    out_dir = out_root / channel / src_id
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{pub_date}__{item_id}__{_safe_slug(title)}.md"
    title_esc = (title or "").replace('"', '\\"')
    md = f"""---
title: "{title_esc}"
channel: {channel}
src_id: {src_id}
item_id: {item_id}
source_url: {fetched.get('source_url', '')}
note_id: {fetched.get('note_id', '')}
task_id: {fetched.get('task_id', '')}
task_elapsed: {fetched.get('task_elapsed', 0)}
fetched_at: {datetime.now(timezone.utc).isoformat()}
summary_len: {len(fetched.get('summary', ''))}
body_len: {len(fetched.get('body', ''))}
---

# {title}

> 原文: {fetched.get('source_url', '')}

## AI 总结

{fetched.get('summary', '')}

## 原文 / 逐字稿

{fetched.get('body', '')}
"""
    (out_dir / fname).write_text(md, encoding="utf-8")
    return out_dir / fname


def _fetch_via_getnote(src: dict, channel: str, items_meta: list, output_local: Path, state_file: Path) -> tuple[list[RawItem], SourceStatus]:
    """两层管线：第二层 = getnote_bridge.url_to_content（节流 + 配额内置）。

    items_meta 由各 channel 第一层 discover 准备好：[{item_id, url, title, published_at}]
    """
    ts = datetime.now(timezone.utc).isoformat()
    status = SourceStatus(id=src["id"], name=src["name"], type=channel, ok=False, fetched_at=ts)
    items: list[RawItem] = []

    # 延迟导入 bridge：未配置 getnote 凭证时不影响整体流程
    try:
        from bridges.getnote_bridge import GetnoteBridge, BridgeError
    except Exception as e:
        status.error = f"getnote_bridge import fail: {e}"
        return items, status

    try:
        bridge = GetnoteBridge()
    except Exception as e:
        status.error = f"getnote_bridge init: {type(e).__name__}: {e}"
        return items, status

    state = _load_discover_state(state_file)
    src_state = state.setdefault(src["id"], {})
    last_seen = src_state.get("last_seen_id")

    # 增量：跳过已抓的 item_id
    todo = [m for m in items_meta if m["item_id"] != last_seen]
    max_per_run = int(src.get("max_per_run", 1))
    todo = todo[:max_per_run]

    if not todo:
        status.ok = True
        status.count = 0
        status.error = f"no new items (last_seen={last_seen})"
        return items, status

    for meta in todo:
        url = meta["url"]
        item_id = meta["item_id"]
        try:
            fetched = bridge.url_to_content(url)
        except Exception as e:
            print(f"  [{channel}/{src['id']}] bridge exception: {type(e).__name__}: {e}", flush=True)
            continue
        if not fetched:
            # 失败兜底：留空壳（用户选 A）— title 来自第一层，body 标记失败
            title = meta.get("title") or f"[{channel}] {item_id}"
            items.append(RawItem(
                site_id=src["id"],
                site_name=src["name"],
                group=src.get("group", "国内信源"),
                category=src.get("category", "ai_hot"),
                title=title,
                url=url,
                published_at=meta.get("published_at", ts),
                summary="[transcript fail: getnote bridge 未取到原文，详见 state/getnote_bridge.json]",
                content_html="",
            ))
            # 仍推进 state，下次不重复尝试同一条
            src_state["last_seen_id"] = item_id
            src_state["last_seen_url"] = url
            src_state["last_run_at"] = ts
            _save_discover_state(state_file, state)
            continue

        title = fetched.get("title") or meta.get("title") or item_id
        # 落盘 markdown（含原文 + 总结）
        try:
            md_path = _write_local_post(
                output_local, channel, src["id"], meta.get("published_at", ts)[:10] or "0000-00-00",
                item_id, title, fetched,
            )
            print(f"  [{channel}/{src['id']}] ✓ {md_path.name} body={len(fetched.get('body',''))} 字", flush=True)
        except Exception as e:
            print(f"  [{channel}/{src['id']}] 落盘异常: {e}", flush=True)

        # 写进 items.json（只放摘要 + 元数据，不放全文，避免 GitHub Pages 流量爆 / 版权）
        items.append(RawItem(
            site_id=src["id"],
            site_name=src["name"],
            group=src.get("group", "国内信源"),
            category=src.get("category", "ai_hot"),
            title=title,
            url=fetched.get("source_url") or url,
            published_at=meta.get("published_at", ts),
            summary=(fetched.get("summary") or "")[:600],  # items.json 公开发布，只放短摘要
            content_html="",  # 全文在 data_local/，不入公开 data/items.json
        ))
        src_state["last_seen_id"] = item_id
        src_state["last_seen_url"] = url
        src_state["last_run_at"] = ts
        _save_discover_state(state_file, state)

    status.ok = True
    status.count = len(items)
    return items, status


def _fetch_discover_summary(
    src: dict, channel: str, items_meta: list, window_hours: int,
    discover_workers: int = 6,
) -> tuple[list[RawItem], SourceStatus]:
    """发现层：title + 便宜摘要，不烧 biji、不取全文/逐字稿、不走增量 state。

    选题漏斗发现层用——闸门①聚类只吃 title+summary。全文/逐字稿留给闸门②打分时
    再抓（见 选题漏斗/闸门2-抓全文.py，只抓热点池长文成员）。摘要来源见 discover/cheap_summary.py。

    wechat 通道每条都要独立 GET og:description，串行最慢；用 ThreadPoolExecutor
    并发抓取（discover_workers>1 时），每请求前加随机 jitter 降反爬。结果按
    items_meta 原顺序组装，字段/顺序与串行一致。小宇宙/B站逻辑不变（仍串行）。
    """
    ts = datetime.now(timezone.utc).isoformat()
    status = SourceStatus(id=src["id"], name=src["name"], type=channel, ok=False, fetched_at=ts)
    try:
        from discover.cheap_summary import wechat_summary, xiaoyuzhou_detail, bilibili_detail
    except Exception as e:
        status.error = f"cheap_summary import fail: {e}"
        return [], status

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    items: list[RawItem] = []
    antibot = 0

    # wechat: 每条独立 HTTP，线程池并发（workers>1）。先把每条 meta 的 summary
    # 算出来（按原 index 回填，保持顺序），再统一做窗口过滤 + 组装。
    summaries: list[str] = [""] * len(items_meta)
    if channel == "wechat":
        def _one(url: str) -> str:
            # 每请求前随机 jitter，错开并发对 mp.weixin 的瞬时压力，降反爬
            time.sleep(random.uniform(0, 0.3))
            try:
                return wechat_summary(url)
            except Exception:
                return ""

        workers = max(1, int(discover_workers))
        if workers == 1:
            for i, meta in enumerate(items_meta):
                summaries[i] = _one(meta["url"])
        else:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=min(workers, len(items_meta) or 1)) as ex:
                # map 保序：返回顺序与 items_meta 一致
                for i, s in enumerate(ex.map(_one, [m["url"] for m in items_meta])):
                    summaries[i] = s

    for idx, meta in enumerate(items_meta):
        url = meta["url"]
        title = meta.get("title") or ""
        pub = meta.get("published_at") or ts
        summary = ""
        try:
            if channel == "wechat":
                summary = summaries[idx]
                if not summary:
                    antibot += 1
            elif channel == "xiaoyuzhou":
                d = xiaoyuzhou_detail(url)
                title = d["title"] or title
                pub = d["published_at"] or pub
                summary = d["summary"]
            elif channel == "bilibili":
                d = bilibili_detail(url)
                title = d["title"] or title
                pub = d["published_at"] or pub
                summary = d["summary"]
        except Exception as e:
            print(f"  [{channel}/{src['id']}] cheap_summary 异常: {type(e).__name__}: {e}", flush=True)
        pdt = parse_dt(pub)
        if pdt is not None and pdt < cutoff:
            continue
        if not title:
            continue
        items.append(RawItem(
            site_id=src["id"], site_name=src["name"],
            group=src.get("group", "国内信源"), category=src.get("category", "ai_hot"),
            title=title, url=url,
            published_at=(pdt.astimezone(timezone.utc).isoformat() if pdt else pub),
            summary=summary, content_html="",
        ))
    status.ok = True
    status.count = len(items)
    if not items:
        status.error = "discover-only: 0 items in window"
    elif antibot:
        status.error = f"discover-only ok, {antibot} 条 og:description 空(反爬/无摘要)"
    return items, status


def fetch_bilibili(src: dict, output_local: Path, state_file: Path, discover_only: bool = False, window_hours: int = 720) -> tuple[list[RawItem], SourceStatus]:
    ts = datetime.now(timezone.utc).isoformat()
    status = SourceStatus(id=src["id"], name=src["name"], type="bilibili", ok=False, fetched_at=ts)
    uid = str(src.get("uid") or "").strip()
    if not uid:
        status.error = "missing 'uid'"
        return [], status
    try:
        from discover.bilibili import discover_uploader_videos
        # discover-only 拉深一些做 30 天回填；getnote 模式多抓几条防 max_per_run=1 漏 take
        max_v = 30 if discover_only else max(int(src.get("max_per_run", 1)) + 2, 3)
        candidates = discover_uploader_videos(uid, max_videos=max_v)
    except Exception as e:
        status.error = f"discover.bilibili fail: {type(e).__name__}: {e}"
        return [], status
    meta = [{"item_id": v["bvid"], "url": v["url"], "title": v["title"], "published_at": v["published_at"]} for v in candidates]
    if discover_only:
        return _fetch_discover_summary(src, "bilibili", meta, window_hours)
    return _fetch_via_getnote(src, "bilibili", meta, output_local, state_file)


def fetch_xiaoyuzhou(src: dict, output_local: Path, state_file: Path, discover_only: bool = False, window_hours: int = 720) -> tuple[list[RawItem], SourceStatus]:
    ts = datetime.now(timezone.utc).isoformat()
    status = SourceStatus(id=src["id"], name=src["name"], type="xiaoyuzhou", ok=False, fetched_at=ts)
    pid = str(src.get("podcast_id") or "").strip()
    if not pid:
        status.error = "missing 'podcast_id'"
        return [], status
    try:
        from discover.xiaoyuzhou import discover_podcast_episodes
        max_e = 30 if discover_only else max(int(src.get("max_per_run", 1)) + 2, 3)
        candidates = discover_podcast_episodes(pid, max_episodes=max_e)
    except Exception as e:
        status.error = f"discover.xiaoyuzhou fail: {type(e).__name__}: {e}"
        return [], status
    meta = [{"item_id": e["episode_id"], "url": e["url"], "title": e["title"], "published_at": e["published_at"]} for e in candidates]
    if discover_only:
        return _fetch_discover_summary(src, "xiaoyuzhou", meta, window_hours)
    return _fetch_via_getnote(src, "xiaoyuzhou", meta, output_local, state_file)


def fetch_wechat(src: dict, output_local: Path, state_file: Path, discover_only: bool = False, window_hours: int = 720, discover_workers: int = 6) -> tuple[list[RawItem], SourceStatus]:
    """公众号: WeWe-RSS atom 拿"哪些号出新文章" + URL 列表 → getnote_bridge 取正文。

    背景 (2026-06-11 确认): WeWe-RSS sqlite articles 表只有 7 字段
    (id/mp_id/title/pic_url/publish_time/created_at/updated_at)，**不存正文**。
    atom/rss 输出也不含 content 标签。正文必须由 getnote_bridge 第二层补。
    """
    ts = datetime.now(timezone.utc).isoformat()
    status = SourceStatus(id=src["id"], name=src["name"], type="wechat", ok=False, fetched_at=ts)
    rss_url = (src.get("url") or "").strip()
    if not rss_url:
        status.error = "missing 'url' (WeWe-RSS atom)"
        return [], status
    # discover-only 深翻: atom 默认只回 10 条/号，加 ?limit=N 拿满 ~15 天历史。
    # WeWe-RSS 支持 limit query param（实测 limit=50→50 条）。
    if discover_only and "limit=" not in rss_url:
        sep = "&" if "?" in rss_url else "?"
        rss_url = f"{rss_url}{sep}limit=80"
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        status.error = f"feedparser fail: {type(e).__name__}: {e}"
        return [], status
    if not feed.entries:
        status.ok = True
        status.count = 0
        status.error = "no entries (token失效? 168h 无更新? 去 http://127.0.0.1:4000/dash 看)"
        return [], status

    max_n = 80 if discover_only else max(int(src.get("max_per_run", 1)) + 2, 3)
    meta = []
    for e in feed.entries[:max_n]:
        link = e.get("link") or ""
        if not link or "mp.weixin.qq.com" not in link:
            continue
        # mp 文章 URL 末段（/s/XXX）作为 item_id
        # 注意: 不用 e.get("id") — feedparser 会把 atom 相对 id 拼成绝对 URL
        # (base = feed URL)，结果含 '/'，污染落盘路径
        item_id = link.rsplit("/", 1)[-1].split("?")[0]
        pub_iso = ts
        if e.get("updated_parsed"):
            try:
                pub_iso = datetime(*e.updated_parsed[:6], tzinfo=timezone.utc).isoformat()
            except Exception:
                pass
        meta.append({"item_id": item_id, "url": link, "title": e.get("title", ""), "published_at": pub_iso})
    if not meta:
        status.ok = True
        status.count = 0
        status.error = "no mp.weixin entries (feed shape changed?)"
        return [], status
    if discover_only:
        return _fetch_discover_summary(src, "wechat", meta, window_hours, discover_workers)
    return _fetch_via_getnote(src, "wechat", meta, output_local, state_file)


def fetch_x_list(
    list_id: str,
    x_sources: list[dict[str, Any]],
    window_hours: int,
    per_handle_limit: int = 50,
    timeout: int = 180,
    pages_override: int = 0,
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

    # 2026-06: twscrape 因 X 前端升级 client-transaction-id 算法已挂
    # (XClIdGen creation attempt failed), 改用 scripts/x_list/fetch_timeline.py
    # 直调 GraphQL ListLatestTweetsTimeline (镜像 add_members.py 模式)
    fetch_script = ROOT / "scripts" / "x_list" / "fetch_timeline.py"
    # 默认仍封顶 5 页（~3-5 天）；pages_override>0 时解锁深翻拉更长历史
    pages = pages_override if pages_override > 0 else min(max(1, total_limit // 100 + 1), 5)
    eff_timeout = max(timeout, pages * 25)  # 深翻要更长超时，每页约 25s 预算
    try:
        r = subprocess.run(
            [sys.executable, str(fetch_script),
             "--list-id", list_id, "--count", "100", "--pages", str(pages)],
            capture_output=True, text=True, timeout=eff_timeout,
        )
        if r.returncode != 0:
            err = f"fetch_timeline exit {r.returncode}: {r.stderr.strip()[:300]}"
            return [], [_x_skip_status(s, err, now_iso) for s in x_sources]
    except subprocess.TimeoutExpired:
        err = f"fetch_timeline timeout > {timeout}s"
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
    ap.add_argument("--x-pages", type=int, default=0, help="X list_timeline 翻页数；>0 时解开默认 5 页上限以拉更深历史（每页约 100 条）")
    ap.add_argument("--discover-only", action="store_true", help="国内/YouTube 通道只取标题+便宜摘要（og:description/__NEXT_DATA__/yt-dlp desc），跳过 getnote 全文 + transcript，不烧 biji，不走增量 state")
    ap.add_argument("--discover-workers", type=int, default=6, help="discover-only 下 wechat 逐篇 og:description 抓取的线程池并发度（默认 6；=1 退回串行）。仅影响 wechat，小宇宙/B站不受影响")
    ap.add_argument("--enable-wechat", action="store_true", help="Fetch wechat sources that have RSS URL")
    ap.add_argument("--enable-podcast", action="store_true", help="Fetch podcast sources that have RSS URL")
    ap.add_argument("--enable-youtube", action="store_true", help="Fetch YouTube channel sources (RSS + transcripts)")
    ap.add_argument("--enable-bilibili", action="store_true", help="Fetch Bilibili UP via yt-dlp + getnote_bridge (gated)")
    ap.add_argument("--enable-xiaoyuzhou", action="store_true", help="Fetch Xiaoyuzhou podcast via HTML+getnote_bridge (gated)")
    ap.add_argument("--output-local-dir", default=str(DEFAULT_LOCAL_OUTPUT), help="国内信源原文落盘根（gitignored）")
    ap.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR), help="discover/state JSON 目录")
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
        elif t == "youtube":
            should_fetch = args.enable_youtube and bool((src.get("url") or "").strip())
        elif t == "bilibili":
            should_fetch = args.enable_bilibili and bool((src.get("uid") or "").strip())
        elif t == "xiaoyuzhou":
            should_fetch = args.enable_xiaoyuzhou and bool((src.get("podcast_id") or "").strip())

        if not should_fetch:
            statuses.append(SourceStatus(id=src["id"], name=src["name"], type=t, ok=True, count=0, error="skipped (not in default layer)", fetched_at=datetime.now(timezone.utc).isoformat()))
            continue

        if t in ("rss", "podcast"):
            items, status = fetch_rss(src, session, args.window_hours)
        elif t == "wechat":
            items, status = fetch_wechat(src, Path(args.output_local_dir), Path(args.state_dir) / "discover.json", args.discover_only, args.window_hours, args.discover_workers)
        elif t == "hf_api":
            items, status = fetch_hf_papers(src, session, args.window_hours)
        elif t == "youtube":
            items, status = fetch_youtube(src, session, args.window_hours, args.discover_only)
        elif t == "bilibili":
            items, status = fetch_bilibili(src, Path(args.output_local_dir), Path(args.state_dir) / "discover.json", args.discover_only, args.window_hours)
        elif t == "xiaoyuzhou":
            items, status = fetch_xiaoyuzhou(src, Path(args.output_local_dir), Path(args.state_dir) / "discover.json", args.discover_only, args.window_hours)
        else:
            status = SourceStatus(id=src["id"], name=src["name"], type=t or "?", ok=False, error=f"unknown type: {t}", fetched_at=datetime.now(timezone.utc).isoformat())
            items = []
        all_items.extend(items)
        statuses.append(status)

    # X 渠道：一次 list_timeline 调用拉回 List 里所有成员的最新推文
    if args.enable_x and x_sources and not args.probe_only:
        print(f"[hxz-news-reader] X list_timeline list_id={args.x_list_id} handles={len(x_sources)}", flush=True)
        t0 = time.time()
        x_items, x_statuses = fetch_x_list(args.x_list_id, x_sources, args.window_hours, args.x_per_handle, pages_override=args.x_pages)
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
