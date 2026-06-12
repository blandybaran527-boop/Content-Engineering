#!/usr/bin/env python3
"""扫 data_local/items.json 找字幕短 (<10K) 的 YouTube 条目, 逐条重抓.

YouTube 反爬 SABR + PO Token 经常返回 200 但中途空字节 → 字幕只拿前几句.
这里串行重抓 + 间隔 60s 避免住宅 IP 被再次降级.

用法:
    python3 scripts/refetch_youtube.py                     # 自动模式
    python3 scripts/refetch_youtube.py --threshold 30000   # 调阈值
    python3 scripts/refetch_youtube.py --dry-run           # 只看清单不重抓
    python3 scripts/refetch_youtube.py --sleep 90          # 改间隔
"""
from __future__ import annotations
import argparse, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data_local/items.json"

VIDEO_ID_RE = re.compile(r"(?:youtu\.be/|/shorts/|[?&]v=)([A-Za-z0-9_-]{11})")
SHORTS_RE = re.compile(r"/shorts/")


def extract_vid(url: str) -> str | None:
    if not url:
        return None
    m = VIDEO_ID_RE.search(url)
    return m.group(1) if m else None


def refetch_one(vid: str, languages: list[str]):
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    tr = api.fetch(vid, languages=languages)
    snippets = list(tr)
    lines = [(s.text or "").strip() for s in snippets if (s.text or "").strip()]
    paragraphs = []
    buf = []
    for i, ln in enumerate(lines, 1):
        buf.append(ln)
        if i % 8 == 0:
            paragraphs.append(" ".join(buf))
            buf = []
    if buf:
        paragraphs.append(" ".join(buf))
    return "\n\n".join(f"<p>{p}</p>" for p in paragraphs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=10000,
                    help="字符数低于这个的 YouTube 条目重抓 (默认 10000)")
    ap.add_argument("--sleep", type=int, default=60,
                    help="每条间隔秒数 (默认 60, 避免 IP 降级)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max", type=int, default=99, help="最多重抓 N 条")
    args = ap.parse_args()

    payload = json.loads(ITEMS.read_text())
    items = payload["items"]

    targets = []
    skipped_shorts = 0
    for idx, it in enumerate(items):
        if it.get("group") != "YouTube":
            continue
        chl = len(it.get("content_html", "") or "")
        if chl >= args.threshold:
            continue
        url = it.get("url", "")
        # Shorts 短视频字幕本来就短, 跳过 (除非 --include-shorts)
        if SHORTS_RE.search(url):
            skipped_shorts += 1
            continue
        vid = extract_vid(url)
        if vid:
            targets.append((idx, it, vid, chl))
    if skipped_shorts:
        print(f"  (跳过 {skipped_shorts} 条 YouTube Shorts — 字幕本来就短)")

    print(f"找到 {len(targets)} 条 YouTube 短字幕 (<{args.threshold} 字符):")
    for _, it, vid, chl in targets:
        print(f"  [{it['site_id']:20s}] vid={vid}  当前={chl}字 — {it['title'][:60]}")

    if args.dry_run:
        return

    if not targets:
        print("✓ 无需重抓")
        return

    targets = targets[:args.max]
    fixed = 0
    failed = 0
    for i, (idx, it, vid, old) in enumerate(targets):
        print(f"\n[{i+1}/{len(targets)}] 重抓 {vid} ({it['site_id']}) 旧={old}字...", flush=True)
        try:
            new_html = refetch_one(vid, languages=["en"])
            new_len = len(new_html)
            if new_len > old:
                items[idx]["content_html"] = new_html
                fixed += 1
                print(f"  ✓ 新={new_len}字 (+{new_len-old})", flush=True)
            else:
                print(f"  ⚠️ 新={new_len}字 没改善, 保留旧版", flush=True)
        except Exception as e:
            failed += 1
            print(f"  ❌ {type(e).__name__}: {str(e)[:120]}", flush=True)
        if i < len(targets) - 1:
            print(f"  sleep {args.sleep}s...", flush=True)
            time.sleep(args.sleep)

    ITEMS.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"\n✓ 完成: 修了 {fixed} 条, 失败 {failed}, 写回 {ITEMS}")


if __name__ == "__main__":
    main()
