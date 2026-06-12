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

# ============================================================
# Body 渲染 — 公众号 = Markdown→HTML, B站/小宇宙 = 时间戳保持
# ============================================================

_IMG_RE   = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_LINK_RE  = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE  = re.compile(r"\*\*([^*]+?)\*\*")
_ITAL_RE  = re.compile(r"(?<!\*)\*([^*\n]+?)\*(?!\*)")
_CODE_RE  = re.compile(r"`([^`\n]+?)`")
_HEAD_RE  = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_QUOTE_RE = re.compile(r"^>\s?(.+)$", re.MULTILINE)


def _escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _render_inline(s: str) -> str:
    # 不 escape 全文（公众号有些原始字符其实是 HTML 转义后给的），只对 emphasis 提取
    out = _IMG_RE.sub(lambda m: f'<img src="{m.group(2)}" alt="{_escape_html(m.group(1))}" loading="lazy">', s)
    out = _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>', out)
    out = _BOLD_RE.sub(r"<strong>\1</strong>", out)
    out = _ITAL_RE.sub(r"<em>\1</em>", out)
    out = _CODE_RE.sub(r"<code>\1</code>", out)
    return out


_LIST_BULLET_RE = re.compile(r"^[\-\*\+]\s+(.+)$")
_LIST_ORDERED_RE = re.compile(r"^\d+\.\s+(.+)$")


def render_markdown(md: str) -> str:
    """极简 Markdown→HTML 渲染。公众号 / AI 摘要 共用。"""
    if not md:
        return ""
    md = md.strip()
    # 1) heading 行
    md = _HEAD_RE.sub(lambda m: f"<h{min(len(m.group(1))+1, 6)}>{_render_inline(m.group(2))}</h{min(len(m.group(1))+1, 6)}>", md)
    # 强制让 heading 标签独立成段（即使原 md heading 行后没空行）
    md = re.sub(r"(<h[1-6]>[^\n]*?</h[1-6]>)\n(?!\n)", r"\1\n\n", md)
    md = re.sub(r"(?<!\n\n)(<h[1-6]>)", r"\n\n\1", md)
    # 2) 把空行作为段落分隔
    paras = re.split(r"\n\s*\n", md)
    html_parts = []
    for para in paras:
        para = para.strip()
        if not para:
            continue
        # 已经是 heading 标签
        if para.startswith("<h") and re.match(r"<h[1-6]>", para):
            html_parts.append(para)
            continue
        # 整段引用：只要任一行以 > 开头就当 blockquote
        lines = para.split("\n")
        if any(ln.lstrip().startswith(">") for ln in lines):
            cleaned_lines = []
            for ln in lines:
                ln = ln.strip()
                if ln in (">", ""):
                    cleaned_lines.append("")
                else:
                    cleaned_lines.append(re.sub(r"^>\s?", "", ln).strip())
            sub_parts = []
            cur: list[str] = []
            for cl in cleaned_lines:
                if not cl:
                    if cur:
                        sub_parts.append("<br>".join(cur))
                        cur = []
                else:
                    cur.append(_render_inline(cl))
            if cur:
                sub_parts.append("<br>".join(cur))
            inner = "</p><p>".join(sub_parts) if len(sub_parts) > 1 else (sub_parts[0] if sub_parts else "")
            if len(sub_parts) > 1:
                inner = f"<p>{inner}</p>"
            html_parts.append(f"<blockquote>{inner}</blockquote>")
            continue
        # 列表：所有行都是 - / * / + / "n." 开头 → <ul> / <ol>
        all_bullet = all(_LIST_BULLET_RE.match(ln.strip()) for ln in lines if ln.strip())
        all_ordered = all(_LIST_ORDERED_RE.match(ln.strip()) for ln in lines if ln.strip())
        if (all_bullet or all_ordered) and lines:
            tag = "ol" if all_ordered else "ul"
            re_ = _LIST_ORDERED_RE if all_ordered else _LIST_BULLET_RE
            items = []
            for ln in lines:
                m = re_.match(ln.strip())
                if m:
                    items.append(f"<li>{_render_inline(m.group(1))}</li>")
            html_parts.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        # 图片单独成段：保持原样，inline 渲染
        if _IMG_RE.match(para) and "\n" not in para:
            html_parts.append(f"<p>{_render_inline(para)}</p>")
            continue
        # 普通段：把 inline 换行变 <br>，再包 <p>
        inner = _render_inline(para).replace("\n", "<br>")
        html_parts.append(f"<p>{inner}</p>")
    return "\n".join(html_parts)


def md_to_plain(md: str, maxlen: int = 600) -> str:
    """Markdown 去标签变纯文本（列表条目用）"""
    if not md:
        return ""
    txt = md
    txt = _IMG_RE.sub("", txt)
    txt = _LINK_RE.sub(r"\1", txt)
    txt = _BOLD_RE.sub(r"\1", txt)
    txt = _ITAL_RE.sub(r"\1", txt)
    txt = _CODE_RE.sub(r"\1", txt)
    txt = re.sub(r"^#{1,6}\s+", "", txt, flags=re.MULTILINE)
    txt = re.sub(r"^[\-\*\+]\s+", "• ", txt, flags=re.MULTILINE)
    txt = re.sub(r"^>\s?", "", txt, flags=re.MULTILINE)
    # 多空行折成单空行
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
    if len(txt) > maxlen:
        txt = txt[:maxlen].rstrip() + "…"
    return txt


def render_transcript(text: str) -> str:
    """B 站 / 小宇宙的带时间戳逐字稿。<pre> 保留时间戳排版。"""
    if not text:
        return ""
    safe = _escape_html(text)
    return f"<pre class='transcript'>{safe}</pre>"


def render_body(channel: str, body: str) -> str:
    if not body:
        return ""
    if channel == "wechat":
        return render_markdown(body)
    # B 站 / 小宇宙 / 其它默认走 transcript
    return render_transcript(body)


def load_sources_map() -> dict:
    """src_id → {name, category, group}"""
    if not SOURCES.exists():
        return {}
    with SOURCES.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    return {s["id"]: s for s in data}


# 渠道细粒度分组 + 优先级权重 (Phase 2)
# 数字大 = 排前面
GROUP_PRIORITY = {
    "海外播客":  100,  # bg2-pod / dwarkesh / a16z / TED / lex-fridman (type=podcast 国外, 不在 YouTube 单类)
    "YouTube":   95,   # yt-* (Lex / Dwarkesh / Matt Wolfe / 20VC / No Priors / BG2 / a16z)
    "X-国外":    90,
    "Substack":  80,   # lennys / generalist / newcomer / import-ai
    "聚合站":    70,   # hackernews / rundown-ai
    "HF Papers": 65,
    "国内播客":  60,   # 小宇宙 + B 站 (latetalk / onboard / guigu101 / ai-weekly-talk / li-ziran)
    "公众号":    50,
    "X-国内":    30,
}

# 标准 group 名 → 显示名 (sidebar 顺序)
GROUP_ORDER = [
    "海外播客", "YouTube", "X-国外", "Substack", "聚合站", "HF Papers",
    "国内播客", "公众号", "X-国内",
]


def normalize_group(item: dict, src_info: dict) -> str:
    """按 type / site_id / 原 group 推断细粒度分组"""
    site_id = item.get("site_id", "") or ""
    src_type = src_info.get("type", "")
    orig_group = src_info.get("group", "") or item.get("group", "") or ""

    # 优先按 src type 判断 (源数据明确)
    if src_type == "x_handle":
        return "X-国外" if "国外" in orig_group else ("X-国内" if "国内" in orig_group else "X-国外")
    if src_type == "youtube" or site_id.startswith("yt-"):
        return "YouTube"
    if src_type == "podcast":
        # podcast 类型在 sources.yaml 里都是国外 (lex/dwarkesh/bg2/a16z/ted)
        return "海外播客"
    if src_type == "bilibili" or site_id == "li-ziran":
        return "国内播客"  # B 站归到国内播客
    if src_type == "xiaoyuzhou":
        return "国内播客"
    if src_type == "wechat":
        return "公众号"
    if src_type == "hf_api":
        return "HF Papers"
    if src_type == "rss":
        # Substack vs 聚合站
        if site_id in ("lennys", "generalist", "newcomer", "import-ai"):
            return "Substack"
        return "聚合站"

    # 回退到原 group, 再到默认
    if orig_group == "X-国外": return "X-国外"
    if orig_group == "X-国内": return "X-国内"
    if orig_group == "优质播客": return "海外播客"  # 数据层修正: 优质播客旧分类拆 YouTube / 海外播客 / 国内播客
    if orig_group == "聚合站": return "聚合站"
    if orig_group == "商科信源": return "Substack"
    if orig_group == "公众号": return "公众号"
    return orig_group or "其他"


def group_priority(group: str) -> int:
    return GROUP_PRIORITY.get(group, 0)


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
    channel = fm.get("channel", "")
    # Phase 1: 重新分组 (拆 优质播客 → YouTube / 海外播客 / 国内播客)
    fake_item = {"site_id": src_id, "group": src.get("group", "")}
    new_group = normalize_group(fake_item, src)
    return {
        "site_id": src_id,
        "site_name": src.get("name", src_id),
        "group": new_group,
        "_priority": group_priority(new_group),
        "category": src.get("category", "ai_hot"),
        "title": fm.get("title", ""),
        "url": fm.get("source_url", ""),
        "published_at": pub,
        # summary 走纯文本（列表 preview 用 -webkit-line-clamp 截断）
        "summary": md_to_plain(summary, maxlen=600),
        # summary_html 是 markdown 渲染版（阅读视图里展示）
        "summary_html": render_markdown(summary),
        # 按渠道分: wechat=Markdown→HTML; bilibili/xiaoyuzhou=<pre> 时间戳
        "content_html": render_body(channel, body),
        # 本地扩展字段（公开版没有）
        "channel": channel,
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
            # 公开版没经过 parse_md, 也补一下 group / _priority
            site_id = it.get("site_id", "") or ""
            src = src_map.get(site_id, {})
            fake = {"site_id": site_id, "group": it.get("group", "")}
            new_g = normalize_group(fake, src)
            it["group"] = new_g
            it["_priority"] = group_priority(new_g)
            local_items.append(it)
            seen.add(k)

    # Phase 4: 保留上一版的翻译字段 (title_zh / summary_zh) — 避免重建覆盖
    out_path = DATA_LOCAL / "items.json"
    if out_path.exists():
        try:
            old = json.loads(out_path.read_text())
            zh_map = {}
            for it in old.get("items", []):
                k = (it.get("site_id"), it.get("url"))
                if it.get("title_zh") or it.get("summary_zh"):
                    zh_map[k] = {
                        "title_zh": it.get("title_zh"),
                        "summary_zh": it.get("summary_zh"),
                    }
            restored = 0
            for it in local_items:
                k = (it.get("site_id"), it.get("url"))
                if k in zh_map:
                    if zh_map[k]["title_zh"]:
                        it["title_zh"] = zh_map[k]["title_zh"]
                    if zh_map[k]["summary_zh"]:
                        it["summary_zh"] = zh_map[k]["summary_zh"]
                    restored += 1
            if restored:
                print(f"  ✓ 恢复 {restored} 条旧翻译字段")
        except Exception as e:
            print(f"  ! 旧 items.json 解析失败: {e}", file=sys.stderr)

    # Phase 2: 排序按 (priority DESC, published_at DESC)
    local_items.sort(
        key=lambda x: (x.get("_priority", 0), x.get("published_at", "")),
        reverse=True,
    )

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
