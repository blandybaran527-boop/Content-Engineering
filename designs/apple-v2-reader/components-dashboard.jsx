// "今日通道健康" Dashboard — 顶部折叠面板
//
// 数据源 (优先 data_local 跟 loadItems 对齐):
//   - data_local/source-status.json → data/source-status.json (兜底)
//   - state/discover.json (国内通道增量 state)
//   - state/getnote_bridge.json (写配额账本)

// 显式 source id 清单 (因 source-status.json 的 group 字段经 normalize_items 会丢)
const ID_RSS_AGG     = ["hackernews", "import-ai", "rundown-ai"];
const ID_SUBSTACK    = ["lennys", "generalist", "newcomer"];

const CHANNEL_GROUPS = [
  { key: "rss",        label: "RSS 聚合",  category: "海外",  match: (s) => s.type === "rss" && ID_RSS_AGG.includes(s.id) },
  { key: "substack",   label: "Substack",  category: "海外",  match: (s) => s.type === "rss" && ID_SUBSTACK.includes(s.id) },
  { key: "papers",     label: "HF Papers", category: "海外",  match: (s) => s.type === "hf_api" },
  { key: "wechat",     label: "公众号",    category: "国内",  match: (s) => s.type === "wechat" },
  { key: "youtube",    label: "YouTube",   category: "海外",  match: (s) => s.type === "youtube" },
  { key: "x",          label: "X (推特)",  category: "海外",  match: (s) => s.type === "x_handle" },
  { key: "bilibili",   label: "B 站",      category: "国内",  match: (s) => s.type === "bilibili" },
  { key: "xiaoyuzhou", label: "小宇宙",    category: "国内",  match: (s) => s.type === "xiaoyuzhou" || s.type === "podcast" },
];

async function loadDashboardData() {
  const tryFetch = async (urls) => {
    for (const u of urls) {
      try {
        const r = await fetch(u + "?_=" + Date.now());
        if (r.ok) return await r.json();
      } catch (e) {}
    }
    return null;
  };
  const [status, discoverState, bridgeState, health] = await Promise.all([
    tryFetch(["../../data_local/source-status.json", "../../data/source-status.json", "data/source-status.json"]),
    tryFetch(["../../state/discover.json"]),
    tryFetch(["../../state/getnote_bridge.json"]),
    tryFetch(["../../data_local/health.json"]),
  ]);
  return { status, discoverState, bridgeState, health };
}

function summarizeChannel(status, group) {
  if (!status || !status.sources) return { state: "unknown", srcs: [] };
  const srcs = status.sources.filter((s) => group.match(s) && !(s.error || "").includes("skipped"));
  const skipped = status.sources.filter((s) => group.match(s) && (s.error || "").includes("skipped"));
  if (srcs.length === 0 && skipped.length > 0) return { state: "skipped", srcs: skipped, total: skipped.length };
  if (srcs.length === 0) return { state: "unknown", srcs: [] };
  const ok = srcs.filter((s) => s.ok);
  const okWithItems = ok.filter((s) => (s.count || 0) > 0);
  const okEmpty = ok.length - okWithItems.length;
  const failed = srcs.filter((s) => !s.ok);
  const total_items = srcs.reduce((a, s) => a + (s.count || 0), 0);
  let state = "ok";
  if (failed.length > 0) state = failed.length === srcs.length ? "fail" : "partial";
  else if (okWithItems.length === 0) state = "empty";
  return {
    state, srcs,
    ok_count: ok.length,
    ok_with_items: okWithItems.length,
    ok_empty: okEmpty,
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

function diagnoseCredentials(status, bridgeState, channelInfos) {
  const out = [];

  // biji API key (getnote bridge)
  const writes_today = bridgeState ? Object.values(bridgeState.daily || {}).reduce((a, b) => a + b, 0) : 0;
  out.push({
    key: "biji",
    label: "biji API Key",
    state: bridgeState ? "ok" : "unknown",
    hint: bridgeState ? `今日写配额 ${writes_today}/100` : "未初始化 (跑过 1 次 update_news.py)",
    action_url: "https://www.biji.com/openapi",
    action_label: "去 biji 开放平台",
  });

  // X cookie: 看 X 通道的 ok_with_items
  const xInfo = channelInfos.find((c) => c.key === "x")?.info;
  if (xInfo && xInfo.total_count > 0) {
    let state = "ok";
    let hint = `${xInfo.ok_with_items}/${xInfo.total_count} 个号有新推`;
    if (xInfo.ok_with_items === 0) {
      state = "fail";
      hint = `${xInfo.total_count}/${xInfo.total_count} 全空 — cookie 可能过期`;
    } else if (xInfo.ok_with_items < xInfo.total_count * 0.2) {
      state = "warn";
      hint += " (偏低, 可能 cookie 弱)";
    }
    out.push({
      key: "x_cookie",
      label: "X cookie",
      state, hint,
      action_url: "https://x.com",
      action_label: "去 chrome 重 export cookie",
    });
  }

  // 微信读书 token: 看 wechat 通道 ok_with_items
  const wcInfo = channelInfos.find((c) => c.key === "wechat")?.info;
  if (wcInfo && wcInfo.total_count > 0) {
    let state = "ok";
    let hint = `${wcInfo.ok_with_items}/${wcInfo.total_count} 个号有新文章`;
    if (wcInfo.ok_with_items === 0 && wcInfo.total_count >= 5) {
      state = "warn";
      hint = `${wcInfo.total_count}/${wcInfo.total_count} 都 168h 无新 — token 可能失效`;
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
    error:   { color: "#ef4444",   label: "加载错误" },
  };
  const d = dotByState[state] || dotByState.unknown;
  return (
    <span className="health-dot" style={{ background: d.color }} title={d.label}></span>
  );
}

function OpsSection({ health }) {
  if (!health) return (
    <div className="dashboard-section">
      <div className="dashboard-section-title">🔧 运维状态</div>
      <div className="ops-row state-warn">
        <HealthChip state="warn" />
        <span className="cred-label">健康检查</span>
        <span className="cred-hint">data_local/health.json 不存在 — 跑 `python3 scripts/automation/health_check.py`</span>
      </div>
    </div>
  );
  const ld = health.launchd || {};
  const df = health.data_freshness || {};
  const gh = health.github_actions || {};

  const ld_state = ld.last_status === "ok" ? "ok"
                 : ld.last_status === "tcc_denied" ? "fail"
                 : ld.last_status === "never_ran" ? "warn"
                 : "warn";
  const ld_hint = ld.last_status === "ok" && ld.last_log_at
    ? `上次跑 ${ld.last_log_at}`
    : ld.error_hint || "状态未知";

  // 数据时效: data_local 应该最新 (本机跑), data 应该 ~24h (云端 cron)
  const dl_items = df.data_local_items || {};
  const dl_age_h = dl_items.age_minutes ? (dl_items.age_minutes / 60).toFixed(1) : null;
  const dl_state = !dl_items.exists ? "fail"
                 : dl_items.age_minutes > 1440 ? "warn"   // > 24h
                 : "ok";

  const cloud_state = gh.hours_ago == null ? "unknown"
                    : gh.hours_ago > 26 ? "warn"
                    : "ok";

  return (
    <div className="dashboard-section">
      <div className="dashboard-section-title">🔧 运维状态</div>
      <div className="ops-grid">
        <div className={"ops-row state-" + ld_state}>
          <HealthChip state={ld_state} />
          <span className="cred-label">本机 launchd 定时任务</span>
          <span className="cred-hint">{ld_hint}</span>
          {ld.last_status === "tcc_denied" && (
            <a className="cred-action" href="x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles" target="_blank" rel="noopener">
              去 Settings 加 Full Disk Access →
            </a>
          )}
        </div>
        <div className={"ops-row state-" + cloud_state}>
          <HealthChip state={cloud_state} />
          <span className="cred-label">GitHub Actions cron</span>
          <span className="cred-hint">
            {gh.hours_ago != null ? `上次跑 ${gh.hours_ago} 小时前 (云端公开层)` : "暂无 commit 记录"}
          </span>
        </div>
        <div className={"ops-row state-" + dl_state}>
          <HealthChip state={dl_state} />
          <span className="cred-label">本机数据时效</span>
          <span className="cred-hint">
            {dl_items.exists
              ? `data_local/items.json: ${dl_age_h} 小时前 (${dl_items.size_kb} KB)`
              : "data_local/items.json 不存在"}
          </span>
        </div>
      </div>
    </div>
  );
}

function Dashboard({ status, discoverState, bridgeState, health, expanded, onToggle, loadError }) {
  // 加载失败优先显示
  if (loadError) {
    return (
      <div className="dashboard" data-screen-label="Dashboard">
        <div className="dashboard-bar">
          <HealthChip state="error" />
          <span className="dashboard-title">通道健康</span>
          <span className="dashboard-sub" style={{ color: "#ef4444" }}>数据未加载: {loadError}</span>
        </div>
      </div>
    );
  }

  const channels = CHANNEL_GROUPS.map((g) => ({ ...g, info: summarizeChannel(status, g) }));
  const creds = diagnoseCredentials(status, bridgeState, channels);
  const generated_at = status?.generated_at || "";
  const total_items = channels.reduce((a, c) => a + (c.info.total_items || 0), 0);

  const sev = { fail: 5, warn: 4, partial: 3, empty: 2, skipped: 1, ok: 0, unknown: 0 };
  const worst = channels.reduce((a, c) => Math.max(a, sev[c.info.state] || 0), 0);
  const overall = worst >= 5 ? "fail" : worst >= 4 ? "warn" : worst >= 3 ? "partial" : worst >= 2 ? "empty" : "ok";
  const ok_count = channels.filter((c) => c.info.state === "ok").length;

  return (
    <div className={"dashboard" + (expanded ? " expanded" : "")} data-screen-label="Dashboard">
      <button className="dashboard-bar" onClick={onToggle} aria-expanded={expanded}>
        <HealthChip state={overall} />
        <span className="dashboard-title">通道健康</span>
        <span className="dashboard-sub">
          {ok_count}/{channels.length} 正常
          · {total_items} 条
          · 上次 {fmtTimeShort(generated_at)}
        </span>
        <span className="dashboard-toggle">{expanded ? "收起" : "展开"}</span>
      </button>

      {expanded && (
        <div className="dashboard-body">
          <OpsSection health={health} />

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
                        <span>{c.info.ok_with_items ?? c.info.ok_count}/{c.info.total_count} 有新</span>
                        <span className="dot">·</span>
                        <span>{c.info.total_items} 条</span>
                        {c.info.ok_empty > 0 && (
                          <>
                            <span className="dot">·</span>
                            <span className="muted">{c.info.ok_empty} 空</span>
                          </>
                        )}
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
