"""国内信源「便宜摘要」层：单次轻量请求拿到真摘要，绝不烧 biji 配额。

选题漏斗发现层只需 title + 真摘要做聚类（闸门①）；全文/逐字稿留给闸门②打分时
再抓（见 选题漏斗/闸门2-抓全文.py：热点池长文成员才抓，X 推文不抓）。
本模块就是发现层那个便宜的摘要来源，只服务闸门①聚类：

- wechat:     手机版 MicroMessenger UA 裸 GET → og:description（作者导语）。
              普通 UA 会撞「环境异常」反爬墙、拿不到 og 标签 —— 必须用手机微信 UA。
- xiaoyuzhou: episode 页内联 <script id="__NEXT_DATA__"> 的 JSON → title/description/pubDate
              （description 1k+ 字，shownotes 更长）。零 cookie、零 API key。
- bilibili:   yt-dlp 单视频(非 flat)元数据 → description + 真实 upload_date。

依据：2026-06-17 GitHub 侦察实测三条路径均免费可得（og:description / __NEXT_DATA__ /
yt-dlp description），无需任何登录态。stdlib 优先（wechat/xiaoyuzhou 纯 urllib），
bilibili 复用已装的 yt-dlp。
"""
from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from urllib import request

# 手机版微信 UA —— 公众号 /s/ 页只有带这个 UA 才返回完整静态 HTML 含 og 标签；
# 否则返回 ~18KB「环境异常」反爬页。无需 cookie / referer。
_WX_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "MicroMessenger/8.0.5(0x18000528) NetType/WIFI Language/zh_CN"
)
_DESKTOP_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"

_WX_ANTIBOT = "环境异常"

_OG_DESC_RE = re.compile(
    r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']', re.I | re.S
)
_OG_TITLE_RE = re.compile(
    r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', re.I | re.S
)
_META_DESC_RE = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', re.I | re.S
)
_NEXT_DATA_RE = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)


def _get(url: str, ua: str, timeout: int = 15) -> str:
    req = request.Request(
        url,
        headers={"User-Agent": ua, "Accept-Language": "zh-CN,zh;q=0.9"},
    )
    with request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")


def _clean(s: str, maxlen: int = 600) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", "", s)  # 去残留 HTML
    return re.sub(r"\s+", " ", s).strip()[:maxlen]


def _norm_date(s: str) -> str:
    if not s:
        return ""
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
    except (ValueError, AttributeError):
        return ""


def wechat_summary(url: str, timeout: int = 15) -> str:
    """公众号 /s/ 文章 → og:description（作者导语）。

    撞反爬（「环境异常」且无 og 标签）或异常时返回 ''——调用方据此标记重试。
    """
    try:
        page = _get(url, _WX_UA, timeout)
    except Exception:
        return ""
    if _WX_ANTIBOT in page and "og:description" not in page:
        return ""
    m = _OG_DESC_RE.search(page) or _META_DESC_RE.search(page)
    return _clean(m.group(1)) if m else ""


def _walk_find(obj, must_keys):
    """深度优先找第一个同时含 must_keys 全部键的 dict。

    防御式解析：不写死 props.pageProps.episode 路径，Next.js 升级移动字段也不挂。
    """
    if isinstance(obj, dict):
        if all(k in obj for k in must_keys):
            return obj
        for v in obj.values():
            hit = _walk_find(v, must_keys)
            if hit is not None:
                return hit
    elif isinstance(obj, list):
        for v in obj:
            hit = _walk_find(v, must_keys)
            if hit is not None:
                return hit
    return None


def xiaoyuzhou_detail(url: str, timeout: int = 15) -> dict:
    """小宇宙 episode 页 __NEXT_DATA__ → {title, summary, published_at}。

    title/date 在第一层 discover 是空的，这里一并补齐。
    """
    out = {"title": "", "summary": "", "published_at": ""}
    try:
        page = _get(url, _DESKTOP_UA, timeout)
    except Exception:
        return out

    m = _NEXT_DATA_RE.search(page)
    if m:
        try:
            data = json.loads(m.group(1))
            ep = _walk_find(data, ("eid", "title")) or {}
            desc = ep.get("description") or ""
            if not desc:
                desc = ep.get("shownotes") or ""
            out["summary"] = _clean(desc)
            out["title"] = _clean(ep.get("title") or "", maxlen=200)
            out["published_at"] = _norm_date(
                ep.get("pubDate") or ep.get("publishDate") or ep.get("publishedAt") or ""
            )
        except (ValueError, TypeError):
            pass

    if not out["summary"]:
        mo = _OG_DESC_RE.search(page)
        if mo:
            out["summary"] = _clean(mo.group(1))
    if not out["title"]:
        mt = _OG_TITLE_RE.search(page)
        if mt:
            out["title"] = _clean(mt.group(1), maxlen=200)
    return out


def bilibili_detail(url: str, timeout: int = 25) -> dict:
    """B 站单视频(非 flat) yt-dlp → {title, summary, published_at}。

    flat 模式无 description、常无 upload_date；这里对单条 bvid 取完整元数据。
    proxy='' 强制直连（境外节点触发 B 站 SSL EOF）。
    """
    out = {"title": "", "summary": "", "published_at": ""}
    try:
        import yt_dlp  # type: ignore
    except ImportError:
        return out
    opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,
        "ignoreerrors": True,
        "proxy": "",
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False) or {}
    except Exception:
        return out
    out["title"] = _clean(info.get("title") or "", maxlen=200)
    out["summary"] = _clean(info.get("description") or "")
    ud = info.get("upload_date") or ""  # YYYYMMDD
    if ud:
        try:
            out["published_at"] = datetime.strptime(ud, "%Y%m%d").replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            pass
    return out
