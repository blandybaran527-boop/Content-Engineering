#!/usr/bin/env python3
"""批量翻译 items.json 里的英文条目 (X / YouTube / Substack / HF / 聚合站).

策略:
  - 用 Google Translate 公开端点 (translate.googleapis.com/translate_a/single)
    免费, 不需要 API key, 但有限速 → 加退避 + 缓存
  - 缓存到 data_local/translation_cache.json (按 sha1(text) 索引), 复用避免重译
  - 只翻 group ∈ {X-国外, YouTube, Substack, 聚合站, HF Papers, 海外播客} 的条目
  - 翻 title + summary 两个字段, 写回 title_zh / summary_zh
  - content_html (YouTube 字幕 / Substack 全文) 不翻: 字数太大太慢
"""
from __future__ import annotations
import json, hashlib, sys, time, re
from pathlib import Path
from urllib.parse import urlencode
from urllib import request, error

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data_local/items.json"
CACHE = ROOT / "data_local/translation_cache.json"

OVERSEAS_GROUPS = {"X-国外", "YouTube", "Substack", "聚合站", "HF Papers", "海外播客"}

CN_PROBABLY = re.compile(r"[一-鿿]")


def is_chinese(text: str) -> bool:
    if not text:
        return False
    cjk = CN_PROBABLY.findall(text)
    return len(cjk) / max(len(text), 1) > 0.15


def load_cache() -> dict:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text())
        except Exception:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))


def cache_key(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def mymemory_translate(text: str, retries: int = 3) -> str | None:
    """MyMemory API. 免费匿名 5000 词/天, 加邮箱 50000 词/天.
    端点国内国外都能通, 不受梯子影响."""
    if not text or not text.strip():
        return text
    text = text[:500]  # MyMemory 单次最多 500 字符
    params = {
        "q": text,
        "langpair": "en|zh-CN",
        "de": "hxz-reader@example.com",  # 加邮箱拿 50000 词/日
    }
    url = "https://api.mymemory.translated.net/get?" + urlencode(params)
    for attempt in range(retries):
        try:
            req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            t = data.get("responseData", {}).get("translatedText")
            # 偶尔返回字面 "PLEASE SELECT TWO DISTINCT LANGUAGES" 类错误
            if t and "QUERY LENGTH LIMIT" in t.upper():
                return None
            if t and "PLEASE SELECT" in t.upper():
                return None
            return t
        except error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt + 1)
                continue
            if e.code == 403:
                print(f"  ! 403 - 配额可能用完", file=sys.stderr)
                return None
            return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.5 ** attempt)
                continue
            return None
    return None


def google_translate(text: str, target: str = "zh-CN", source: str = "auto", retries: int = 2) -> str | None:
    """Google Translate 公开端点 — fallback. 走梯子可能 SSL EOF, 失败就跳"""
    if not text or not text.strip():
        return text
    text = text[:4800]
    params = {"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text}
    url = "https://translate.googleapis.com/translate_a/single?" + urlencode(params)
    for attempt in range(retries):
        try:
            req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            return "".join(seg[0] for seg in data[0] if seg and seg[0])
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            return None
    return None


def translate_text(text: str) -> str | None:
    """主翻译入口: MyMemory → Google fallback"""
    r = mymemory_translate(text)
    if r:
        return r
    return google_translate(text)


def translate_with_cache(text: str, cache: dict) -> str | None:
    """带缓存"""
    if not text or not text.strip():
        return text
    if is_chinese(text):
        return text  # 已经是中文不翻
    k = cache_key(text)
    if k in cache:
        return cache[k]
    out = translate_text(text)
    if out is not None:
        cache[k] = out
    return out


def main():
    if not ITEMS.exists():
        print(f"!! {ITEMS} not found", file=sys.stderr)
        sys.exit(1)
    payload = json.loads(ITEMS.read_text())
    items = payload.get("items", [])
    cache = load_cache()
    cache_hits = 0
    api_calls = 0
    skipped = 0
    fails = 0

    todo = [it for it in items if it.get("group") in OVERSEAS_GROUPS]
    print(f"  待翻: {len(todo)} / 总 {len(items)} (海外 group)")

    for i, it in enumerate(todo):
        title = it.get("title", "") or ""
        summary = it.get("summary", "") or ""

        # 已翻过且 cache 命中
        if it.get("title_zh") and it.get("summary_zh"):
            skipped += 1
            continue

        # 翻 title
        if title and not is_chinese(title):
            k = cache_key(title)
            if k in cache:
                cache_hits += 1
            else:
                api_calls += 1
            tr = translate_with_cache(title, cache)
            if tr:
                it["title_zh"] = tr
            else:
                fails += 1

        # 翻 summary
        if summary and not is_chinese(summary):
            k = cache_key(summary)
            if k in cache:
                cache_hits += 1
            else:
                api_calls += 1
                # API 调用间隔 0.3s 避免 429
                time.sleep(0.3)
            tr = translate_with_cache(summary, cache)
            if tr:
                it["summary_zh"] = tr
            else:
                fails += 1

        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{len(todo)}] cache={cache_hits} api={api_calls} fail={fails}", flush=True)
            save_cache(cache)  # 中间存
            ITEMS.write_text(json.dumps(payload, ensure_ascii=False, indent=2))  # 同步 items.json

    save_cache(cache)
    ITEMS.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"\n✓ 完成: skipped={skipped} cache_hits={cache_hits} api_calls={api_calls} fails={fails}")
    print(f"  cache 总 entries: {len(cache)}")


if __name__ == "__main__":
    main()
