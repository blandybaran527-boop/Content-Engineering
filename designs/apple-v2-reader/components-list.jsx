// Inbox 主列表：Substack 收件箱风
// 锁定为基线 (2026-06-11)。Magazine / Lens 两个变体在 git 历史里 (commit 325f56f → 删除)。

function ChannelChip({ channel, label, modality }) {
  return (
    <span className="chan-chip" data-channel={channel} title={`${label} · ${modality}`}>
      <span className="chan-dot"></span>
      <window.ChannelIcon channel={channel} size={11} />
      <span>{label}</span>
    </span>
  );
}

function InboxList({ items, onOpen }) {
  return (
    <div className="reading-inner" data-screen-label="Inbox">
      <div className="page-head">
        <div className="page-eyebrow">收件箱 · Inbox</div>
        <h1 className="page-title">今日内容</h1>
        <div className="page-meta">{items.length} 条 · 按时间倒序 · 点击进入页内阅读</div>
      </div>
      <div className="feed">
        {items.map((it) => (
          <article className="entry" key={it._key} onClick={() => onOpen(it)}>
            <div className="entry-row">
              <ChannelChip channel={it._channel} label={it._channelLabel} modality={it._modality} />
              <span className="pub-name">{it.site_name || it.site_id}</span>
              <span className="dot">·</span>
              <time>{window.fmtTime(it.published_at)}</time>
              <span className="spacer"></span>
              {it.content_html && it.content_html.length > 200 && (
                <span className="body-len">{window.fmtBodyLen(it.content_html)} · 全文</span>
              )}
            </div>
            <h2 className="entry-title">{window.pickTitle(it) || "(无标题)"}</h2>
            {window.pickSummary(it) && <p className="entry-summary">{stripBoiler(window.pickSummary(it))}</p>}
            {it.title_zh && it.title_zh !== it.title && (
              <div style={{ fontSize: 11, color: "var(--text-mute)", fontFamily: "var(--font-mono)" }}>原: {it.title.slice(0, 80)}</div>
            )}
            {/* YouTube 短字幕警示 (反爬导致前 N 句就被打断的不完整字幕) */}
            {it.group === "YouTube" && (it.content_html || "").length > 0 && (it.content_html || "").length < 10000 && !(it.url || "").includes("/shorts/") && (
              <div style={{ fontSize: 11, color: "#f59e0b", fontFamily: "var(--font-mono)", marginTop: 4 }}>
                ⚠️ 字幕不完整 ({(it.content_html.length/1000).toFixed(1)}K 字, YT 反爬截断), 点跳原文看完整
              </div>
            )}
          </article>
        ))}
      </div>
    </div>
  );
}

function stripBoiler(s) {
  if (!s) return "";
  return s.replace(/^[~\s➤➢]+|[~\s]+$/g, "").trim();
}

Object.assign(window, { InboxList, ChannelChip });
