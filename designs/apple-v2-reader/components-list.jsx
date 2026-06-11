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
            <h2 className="entry-title">{it.title || "(无标题)"}</h2>
            {it.summary && <p className="entry-summary">{stripBoiler(it.summary)}</p>}
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
