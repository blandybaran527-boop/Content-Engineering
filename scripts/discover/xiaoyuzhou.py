"""小宇宙节目 → 最新 episode 列表。

无公开 RSS，直接抓节目页 HTML 解析。第一层只取 episode_id + URL，
标题/发布日交给第二层 getnote_bridge 从 detail 里拿（biji 后端已经做了完整 ASR + 标题）。

输出 [{"episode_id", "url", "title", "published_at"}]
"""
from __future__ import annotations
import re
from datetime import datetime, timezone
from typing import List
from urllib import request

EPISODE_PATH_RE = re.compile(r'/episode/([a-f0-9]{24})')
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"


def discover_podcast_episodes(podcast_id: str, max_episodes: int = 1) -> List[dict]:
    url = f"https://www.xiaoyuzhoufm.com/podcast/{podcast_id}"
    req = request.Request(url, headers={"User-Agent": UA})
    with request.urlopen(req, timeout=15) as r:
        html = r.read().decode("utf-8", errors="ignore")
    # 节目页按时间倒序列出 episode，正则取前 max 个不重复 ID
    seen: List[str] = []
    for m in EPISODE_PATH_RE.finditer(html):
        eid = m.group(1)
        if eid not in seen:
            seen.append(eid)
        if len(seen) >= max_episodes:
            break
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "episode_id": eid,
            "url": f"https://www.xiaoyuzhoufm.com/episode/{eid}",
            "title": "",  # 留空，bridge detail 里有
            "published_at": now,  # 同上，biji 端没明确暴露发布日，先用 fetch 时间
        }
        for eid in seen
    ]
