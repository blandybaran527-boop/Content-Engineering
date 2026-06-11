#!/usr/bin/env python3
"""扫 data_local/<channel>/<src_id>/*.md → 构造 data_local/items.json (含正文)。

供本机 HXZ Reader 页面优先读取，避免公开 data/items.json 暴露版权内容。

frontmatter (YAML) + 正文用 `## 原文 / 逐字稿` 分段。
"""
from __future__ import annotations
import json
import re
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_LOCAL = ROOT / "data_local"
PUB_ITEMS = ROOT / "data" / "items.json"  # 海外信源合并
SOURCES = ROOT / "feeds" / "sources.yaml"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
ORIG_SECTION_RE = re.compile(r"## 原文 / 逐字稿\n(.*)$", re.DOTALL)
SUMMARY_SECTION_RE = re.compile(r"## AI 总结\n(.*?)(?=\n## |\Z)", re.DOTALL)


def load_sources_map() -> dict:
    """src_id → {name, category, group}"""
    if not SOURCES.exists():
        return {}
    with SOURCES.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    return {s["id"]: s for s in data}


def parse_md(path: Path, src_map: dict) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = yaml.safe_load(m.group(1)) or {}
    body_section = ORIG_SECTION_RE.search(text)
    body = body_section.group(1).strip() if body_section else ""
    summary_section = SUMMARY_SECTION_RE.search(text)
    summary = summary_section.group(1).strip() if summary_section else ""
    src_id = fm.get("src_id", "")
    src = src_map.get(src_id, {})
    pub = fm.get("fetched_at", "")
    if isinstance(pub, datetime):
        pub = pub.isoformat()
    return {
        "site_id": src_id,
        "site_name": src.get("name", src_id),
        "group": src.get("group", "国内信源"),
        "category": src.get("category", "ai_hot"),
        "title": fm.get("title", ""),
        "url": fm.get("source_url", ""),
        "published_at": pub,
        "summary": summary[:600],  # 摘要短点
        # 用 <p> 包装段落以兼容页面 innerHTML 渲染
        "content_html": "<pre style='white-space:pre-wrap;font-family:inherit'>" + body + "</pre>" if body else "",
        # 本地扩展字段（公开版没有）
        "channel": fm.get("channel", ""),
        "note_id": fm.get("note_id", ""),
        "body_len": fm.get("body_len", 0),
    }


def main():
    src_map = load_sources_map()
    if not DATA_LOCAL.exists():
        print(f"!! data_local 不存在: {DATA_LOCAL}", file=sys.stderr)
        sys.exit(1)

    local_items: list[dict] = []
    md_count = 0
    for md in sorted(DATA_LOCAL.rglob("*.md")):
        md_count += 1
        try:
            item = parse_md(md, src_map)
            if item:
                local_items.append(item)
        except Exception as e:
            print(f"!! parse fail {md.name}: {e}", file=sys.stderr)

    # 合并公开 data/items.json (海外信源摘要 + 国内摘要)
    public_items: list[dict] = []
    if PUB_ITEMS.exists():
        try:
            pub = json.loads(PUB_ITEMS.read_text())
            public_items = pub.get("items", [])
        except Exception as e:
            print(f"!! pub items.json load fail: {e}", file=sys.stderr)

    # 用 (site_id, url) 去重：本地版优先（带正文），公开版补充（不在本地的海外条目）
    seen = {(it["site_id"], it["url"]) for it in local_items}
    for it in public_items:
        k = (it.get("site_id"), it.get("url"))
        if k not in seen:
            local_items.append(it)
            seen.add(k)

    # 时间倒序
    local_items.sort(key=lambda x: x.get("published_at", ""), reverse=True)

    out_path = DATA_LOCAL / "items.json"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_hours": 168,
        "items": local_items,
        "_note": "本地版含国内信源正文。公开 data/items.json 只有海外+国内摘要。",
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"✓ 扫了 {md_count} 个 .md, 输出 {len(local_items)} 条到 {out_path}")
    by_channel = {}
    for it in local_items:
        ch = it.get("channel") or it.get("group", "外部")
        by_channel[ch] = by_channel.get(ch, 0) + 1
    for ch, n in sorted(by_channel.items()):
        print(f"  {ch:15s} {n} 条")


if __name__ == "__main__":
    main()
