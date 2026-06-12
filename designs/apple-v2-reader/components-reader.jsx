// 页内阅读视图：点击列表条目进入沉浸阅读
// 不跳外链，长文直接在页内展开。提供"去原文"按钮 + serif/sans 切换 + ESC 关闭。

function ReaderView({ item, onClose, serif, onToggleSerif }) {
  // ESC 关闭
  React.useEffect(() => {
    const h = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  if (!item) return null;

  const hasFull = item.content_html && item.content_html.length > 200;
  const langAttr = isProbablyChinese(item.title) ? "zh" : "en";

  return (
    <div className="reader-overlay" lang={langAttr}>
      <div className="reader-bar">
        <button className="reader-back" onClick={onClose}>
          <window.ChevronLeft size={16} />
          <span>返回列表</span>
          <span style={{ marginLeft: 4, color: "var(--text-mute)", fontSize: 12 }}>ESC</span>
        </button>
        <span className="spacer"></span>
        <button className="open-source" onClick={onToggleSerif} title="切换衬线/无衬线">
          {serif ? "Sans-serif" : "Serif"}
        </button>
        {item.url && (
          <a className="open-source" href={item.url} target="_blank" rel="noopener noreferrer">
            <span>原文</span>
            <window.ExternalLink size={13} />
          </a>
        )}
      </div>

      <div className="reader-body">
        <div className="reader-eyebrow">
          <window.ChannelChip channel={item._channel} label={item._channelLabel} modality={item._modality} />
          <span style={{ color: "var(--text)" }}>{item.site_name || item.site_id}</span>
          <span style={{ opacity: 0.5 }}>·</span>
          <time>{window.fmtTime(item.published_at)}</time>
          {hasFull && (
            <>
              <span style={{ opacity: 0.5 }}>·</span>
              <span>{window.fmtBodyLen(item.content_html)}</span>
            </>
          )}
        </div>

        <h1 className="reader-title">{window.pickTitle(item) || "(无标题)"}</h1>
        {item.title_zh && item.title_zh !== item.title && (
          <div style={{ color: "var(--text-mute)", fontSize: 14, marginTop: -16, marginBottom: 24, fontStyle: "italic" }}>
            {item.title}
          </div>
        )}

        {(item.summary_html || item.summary) && (item.summary || "").length > 50 && (
          <div className="reader-summary">
            <div className="label">AI 摘要</div>
            {item.summary_html ? (
              <div className="body" dangerouslySetInnerHTML={{ __html: item.summary_html }} />
            ) : (
              <div className="body">{stripBoilerLong(item.summary)}</div>
            )}
          </div>
        )}

        {hasFull ? (
          <div
            className={"reader-content" + (serif ? " serif" : "")}
            dangerouslySetInnerHTML={{ __html: item.content_html }}
          />
        ) : (item.summary && item.summary.length > 30) ? (
          // X / RSS 短条目: 没 content_html 时把 summary 当正文 (优先 zh)
          <div className={"reader-content" + (serif ? " serif" : "")}>
            {item.summary_zh ? (
              <>
                <p style={{ whiteSpace: "pre-wrap" }}>{item.summary_zh}</p>
                <details style={{ marginTop: 24, color: "var(--text-mute)", fontSize: 14 }}>
                  <summary style={{ cursor: "pointer" }}>查看原文 ({item.summary.length} 字符)</summary>
                  <p style={{ whiteSpace: "pre-wrap", marginTop: 12 }}>{item.summary}</p>
                </details>
              </>
            ) : (
              <p style={{ whiteSpace: "pre-wrap" }}>{item.summary}</p>
            )}
          </div>
        ) : (
          <div className="state" style={{ minHeight: 200 }}>
            <h2>本条无内置全文</h2>
            <p style={{ color: "var(--text-mute)" }}>
              这是海外信源条目，原文未本地化。点右上「原文」跳转外链阅读。
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

function isProbablyChinese(s) {
  if (!s) return false;
  const cjk = s.match(/[一-鿿]/g);
  return cjk && cjk.length / s.length > 0.3;
}

function stripBoilerLong(s) {
  if (!s) return "";
  // 去常见的"~专业/及时/全面的报告~"等 公众号 boilerplate 头部
  return s.replace(/^[~\s➤➢]+/, "").trim();
}

Object.assign(window, { ReaderView });
