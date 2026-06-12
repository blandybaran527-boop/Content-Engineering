// "今日通道健康" Dashboard — 顶部折叠面板
//
// 数据源:
//   - data/source-status.json (每次跑后产出, 含 sources[])
//   - state/discover.json (国内通道增量 state)
//   - state/getnote_bridge.json (写配额账本)
//
// 显示 8 个通道维度:
//   RSS 聚合 / Substack / HF Papers / WeChat / YouTube / X / Bilibili / Xiaoyuzhou
// 每个通道: 跑通比 + 总 items + 上次跑时间 + 颜色(绿/黄/红/灰)
// + 凭证状态自检 (推断 + 修复入口)

const CHANNEL_GROUPS = [
  { key: "rss",        label: "RSS 聚合",  category: "海外",  match: (s) => s.type === "rss" && (s.id?.startsWith("hf-") || s.group === "聚合站") },
  { key: "substack",   label: "Substack",  category: "海外",  match: (s) => s.type === "rss" && s.group === "商科信源" },
  { key: "papers",     label: "HF Papers", category: "海外",  match: (s) => s.type === "hf_api" },
  { key: "wechat",     label: "公众号",    category: "国内",  match: (s) => s.type === "wechat" },
  { key: "youtube",    label: "YouTube",   category: "海外",  match: (s) => s.type === "youtube" },
  { key: "x",          label: "X (推特)",  category: "海外",  match: (s) => s.type === "x_handle" },
  { key: "bilibili",   label: "B 站",      category: "国内",  match: (s) => s.type === "bilibili" },
  { key: "xiaoyuzhou", label: "小宇宙",    category: "国内",  match: (s) => s.type === "xiaoyuzhou" },
];

async function loadDashboardData() {
  // 尽量并行 fetch
  const tryFetch = async (urls) => {
    for (const u of urls) {
      try {
        const r = await fetch(u + "?_=" + Date.now());
        if (r.ok) return await r.json();
      } catch (e) {}
    }
    return null;
  };
  const [status, discoverState, bridgeState] = await Promise.all([
    tryFetch(["../../data/source-status.json", "data/source-status.json"]),
    tryFetch(["../../state/discover.json"]),
    tryFetch(["../../state/getnote_bridge.json"]),
  ]);
  return { status, discoverState, bridgeState };
}

function summarizeChannel(status, group) {
  if (!status || !status.sources) return { state: "unknown", srcs: [] };
  const srcs = status.sources.filter((s) => group.match(s) && !(s.error || "").includes("skipped"));
  const skipped = status.sources.filter((s) => group.match(s) && (s.error || "").includes("skipped"));
  if (srcs.length === 0 && skipped.length > 0) return { state: "skipped", srcs: skipped, total: skipped.length };
  if (srcs.length === 0) return { state: "unknown", srcs: [] };
  const ok = srcs.filter((s) => s.ok);
  const okWithItems = ok.filter((s) => (s.count || 0) > 0);
  const failed = srcs.filter((s) => !s.ok);
  const total_items = srcs.reduce((a, s) => a + (s.count || 0), 0);
  let state = "ok";
  if (failed.length > 0) state = failed.length === srcs.length ? "fail" : "partial";
  else if (okWithItems.length === 0) state = "empty";
  return {
    state, srcs,
    ok_count: ok.length,
    total_count: srcs.length,
    failed,
    okWithItems,
    total_items,
  };
}

function fmtTimeShort(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  const now = new Date();
  const diff = (now - d) / 1000;
  if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} 小时前`;
  return `${Math.floor(diff / 86400)} 天前`;
}

function diagnoseCredentials(status, bridgeState) {
  /**
   * 从 source-status 的错误模式 + bridge state 推断凭证状态
   * 返回 [{key, label, state, hint, action_url}]
   */
  const out = [];
  const srcs = (status?.sources) || [];

  // biji API key (getnote bridge): 看 bridge state 是否在
  const writes_today = bridgeState ? Object.values(bridgeState.daily || {}).reduce((a, b) => a + b, 0) : 0;
  out.push({
    key: "biji",
    label: "biji API Key",
    state: bridgeState ? "ok" : "unknown",
    hint: bridgeState ? `今日写配额 ${writes_today}/100` : "未初始化 (跑过 1 次 update_news.py)",
    action_url: "https://www.biji.com/openapi",
    action_label: "去 biji 开放平台",
  });

  // X cookie
  const x_srcs = srcs.filter((s) => s.type === "x_handle" && !(s.error || "").includes("skipped"));
  const x_failed = x_srcs.filter((s) => !s.ok);
  if (x_srcs.length > 0) {
    let state = "ok";
    let hint = `${x_srcs.length - x_failed.length}/${x_srcs.length} 个号正常`;
    if (x_failed.length === x_srcs.length) {
      state = "fail";
      hint = "76/76 失败 — cookie 可能过期";
    } else if (x_failed.length > x_srcs.length * 0.5) {
      state = "warn";
      hint = `${x_failed.length}/${x_srcs.length} 失败`;
    }
    out.push({
      key: "x_cookie",
      label: "X cookie",
      state, hint,
      action_url: "chrome://settings/cookies/detail?site=x.com",
      action_label: "去 chrome export cookie",
    });
  }

  // 微信读书 token: 看 wechat 通道有没有大批 168h 无新
  const wc_srcs = srcs.filter((s) => s.type === "wechat" && !(s.error || "").includes("skipped"));
  const wc_empty = wc_srcs.filter((s) => s.ok && (s.count || 0) === 0);
  if (wc_srcs.length > 0) {
    let state = "ok";
    let hint = `${wc_srcs.length - wc_empty.length}/${wc_srcs.length} 个号有新文章`;
    if (wc_empty.length === wc_srcs.length) {
      state = "warn";
      hint = "12/12 都 168h 无新 — token 可能失效";
    }
    out.push({
      key: "wechat_token",
      label: "微信读书 token",
      state, hint,
      action_url: "http://127.0.0.1:4000/dash",
      action_label: "去 WeWe-RSS 重扫码",
    });
  }

  return out;
}

function HealthChip({ state }) {
  const dotByState = {
    ok:      { color: "var(--ok)", label: "正常" },
    partial: { color: "#f59e0b",   label: "部分" },
    empty:   { color: "#fbbf24",   label: "无新" },
    fail:    { color: "#ef4444",   label: "失败" },
    skipped: { color: "var(--text-mute)", label: "未跑" },
    warn:    { color: "#f59e0b",   label: "警告" },
    unknown: { color: "var(--text-mute)", label: "未知" },
  };
  const d = dotByState[state] || dotByState.unknown;
  return (
    <span className="health-dot" style={{ background: d.color }} title={d.label}></span>
  );
}

function Dashboard({ status, discoverState, bridgeState, expanded, onToggle }) {
  const channels = CHANNEL_GROUPS.map((g) => ({ ...g, info: summarizeChannel(status, g) }));
  const creds = diagnoseCredentials(status, bridgeState);
  const generated_at = status?.generated_at || "";
  const total_items = channels.reduce((a, c) => a + (c.info.total_items || 0), 0);

  // 严重程度排序: fail > warn > partial > empty > skipped > ok
  const sev = { fail: 5, warn: 4, partial: 3, empty: 2, skipped: 1, ok: 0, unknown: 0 };
  const worst = channels.reduce((a, c) => Math.max(a, sev[c.info.state] || 0), 0);
  const overall = worst >= 5 ? "fail" : worst >= 4 ? "warn" : worst >= 3 ? "partial" : worst >= 2 ? "empty" : "ok";

  return (
    <div className={"dashboard" + (expanded ? " expanded" : "")} data-screen-label="Dashboard">
      <button className="dashboard-bar" onClick={onToggle} aria-expanded={expanded}>
        <HealthChip state={overall} />
        <span className="dashboard-title">通道健康</span>
        <span className="dashboard-sub">
          {channels.filter((c) => c.info.state === "ok").length}/{channels.length} 正常
          · {total_items} 条
          · 上次 {fmtTimeShort(generated_at)}
        </span>
        <span className="dashboard-toggle">{expanded ? "收起" : "展开"}</span>
      </button>

      {expanded && (
        <div className="dashboard-body">
          <div className="dashboard-section">
            <div className="dashboard-section-title">8 通道</div>
            <div className="channel-grid">
              {channels.map((c) => (
                <div className={"channel-card state-" + c.info.state} key={c.key}>
                  <div className="channel-head">
                    <HealthChip state={c.info.state} />
                    <span className="channel-name">{c.label}</span>
                    <span className="channel-region">{c.category}</span>
                  </div>
                  <div className="channel-stats">
                    {c.info.state === "skipped" ? (
                      <span className="muted">本次未跑</span>
                    ) : c.info.state === "unknown" ? (
                      <span className="muted">尚无数据</span>
                    ) : (
                      <>
                        <span>{c.info.ok_count}/{c.info.total_count} 源</span>
                        <span className="dot">·</span>
                        <span>{c.info.total_items} 条</span>
                      </>
                    )}
                  </div>
                  {c.info.failed && c.info.failed.length > 0 && (
                    <details className="channel-errors">
                      <summary>{c.info.failed.length} 个失败</summary>
                      <ul>
                        {c.info.failed.slice(0, 5).map((s) => (
                          <li key={s.id}>
                            <code>{s.id}</code>: {(s.error || "").slice(0, 80)}
                          </li>
                        ))}
                      </ul>
                    </details>
                  )}
                </div>
              ))}
            </div>
          </div>

          {creds.length > 0 && (
            <div className="dashboard-section">
              <div className="dashboard-section-title">⚙️ 凭证状态自检</div>
              <div className="creds-list">
                {creds.map((c) => (
                  <div className={"cred-row state-" + c.state} key={c.key}>
                    <HealthChip state={c.state} />
                    <span className="cred-label">{c.label}</span>
                    <span className="cred-hint">{c.hint}</span>
                    {(c.state === "warn" || c.state === "fail") && (
                      <a className="cred-action" href={c.action_url} target="_blank" rel="noopener">
                        {c.action_label} →
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

Object.assign(window, { Dashboard, loadDashboardData });
