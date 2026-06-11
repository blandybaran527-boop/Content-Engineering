"""B 站 UP 主 → 最新视频列表。

依赖 yt-dlp 模块（hxz YouTube 通道已装）。不调 B 站 wbi 签名，避开反爬。

输出 [{"bvid", "url", "title", "upload_date"(YYYYMMDD), "published_at"(ISO8601)}]
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import List

try:
    import yt_dlp  # type: ignore
except ImportError:
    yt_dlp = None


def discover_uploader_videos(uid: str, max_videos: int = 1) -> List[dict]:
    if yt_dlp is None:
        raise RuntimeError("yt_dlp 未安装。pip install yt-dlp")
    space_url = f"https://space.bilibili.com/{uid}"
    opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "playlistend": max_videos,
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(space_url, download=False)
    entries = (info or {}).get("entries") or []
    out: List[dict] = []
    for e in entries[:max_videos]:
        if not e:
            continue
        bvid = e.get("id") or ""
        if not bvid.startswith("BV"):
            continue
        title = e.get("title") or ""
        # upload_date 来自 entry 可能为 None（flat extract），下次拿 detail 时再补
        upload_date = e.get("upload_date") or ""
        try:
            pub_iso = (
                datetime.strptime(upload_date, "%Y%m%d")
                .replace(tzinfo=timezone.utc)
                .isoformat()
                if upload_date
                else datetime.now(timezone.utc).isoformat()
            )
        except ValueError:
            pub_iso = datetime.now(timezone.utc).isoformat()
        out.append(
            {
                "bvid": bvid,
                "url": f"https://www.bilibili.com/video/{bvid}/",
                "title": title,
                "upload_date": upload_date,
                "published_at": pub_iso,
            }
        )
    return out
