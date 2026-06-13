// 顶层 App: Inbox 主视图 + 分组过滤 + 主题切换 + 页内阅读

const { useState, useEffect, useMemo } = React;

function App() {
  const [data, setData] = useState({ items: null, generated_at: null, source: null });
  const [dashboardData, setDashboardData] = useState({ status: null, discoverState: null, bridgeState: null, health: null });
  const [dashboardLoadError, setDashboardLoadError] = useState(null);
  const [dashboardExpanded, setDashboardExpanded] = useState(() => localStorage.getItem("hxzv2-dash") === "1");
  const [error, setError] = useState(null);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("hxzv2-theme") ||
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  });
  const [groupFilter, setGroupFilter] = useState("all");
  const [siteFilter, setSiteFilter] = useState(null);
  const [openItem, setOpenItem] = useState(null);
  const [serif, setSerif] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("hxzv2-theme", theme);
  }, [theme]);
  useEffect(() => {
    localStorage.setItem("hxzv2-dash", dashboardExpanded ? "1" : "0");
  }, [dashboardExpanded]);

  useEffect(() => {
    window.loadItems()
      .then((d) => setData(d))
      .catch((e) => setError(e));
    window.loadDashboardData()
      .then((d) => setDashboardData(d))
      .catch((e) => setDashboardLoadError(e.message || String(e)));
  }, []);

  const items = useMemo(() => (data.items || []).map(window.enrichItem), [data.items]);
  const groups = useMemo(() => window.buildGroups(items), [items]);
  const filtered = useMemo(() => {
    let arr = items;
    if (groupFilter !== "all") arr = arr.filter((it) => it.group === groupFilter);
    if (siteFilter) arr = arr.filter((it) => it.site_id === siteFilter);
    return arr;
  }, [items, groupFilter, siteFilter]);

  if (error) {
    return (
      <div style={{ padding: 48 }}>
        <h2>加载失败</h2>
        <p style={{ color: "var(--text-mute)" }}>找不到 <code>data_local/items.json</code> 或 <code>data/items.json</code>。请先跑：</p>
        <pre style={{ background: "var(--surface-2)", padding: 16, borderRadius: 8 }}>{`cd hxz-news-reader
python3 scripts/build_local_index.py`}</pre>
      </div>
    );
  }
  if (data.items === null) {
    return <div className="state"><h2>加载中…</h2><span>正在读取 items.json</span></div>;
  }

  return (
    <>
      <nav className="nav">
        <div className="brand">
          <span className="brand-mark"></span>
          <span className="brand-name">HXZ Reader</span>
          <span className="brand-kicker">内容工程信源雷达</span>
        </div>
        <span className="nav-spacer"></span>
        <div className="nav-actions">
          <button
            className="icon-btn"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            title="切换主题"
          >
            {theme === "dark" ? <window.SunIcon /> : <window.MoonIcon />}
          </button>
        </div>
      </nav>

      <div className="shell">
        <Sidebar
          groups={groups}
          activeGroup={groupFilter}
          activeSite={siteFilter}
          onSelectGroup={(g) => { setGroupFilter(g); setSiteFilter(null); }}
          onSelectSite={setSiteFilter}
          total={items.length}
        />
        <main className="reading">
          <window.Dashboard
            status={dashboardData.status}
            discoverState={dashboardData.discoverState}
            bridgeState={dashboardData.bridgeState}
            health={dashboardData.health}
            expanded={dashboardExpanded}
            onToggle={() => setDashboardExpanded((v) => !v)}
            loadError={dashboardLoadError}
          />
          <window.InboxList items={filtered} onOpen={setOpenItem} />
        </main>
      </div>

      {openItem && (
        <window.ReaderView
          item={openItem}
          onClose={() => setOpenItem(null)}
          serif={serif}
          onToggleSerif={() => setSerif((s) => !s)}
        />
      )}
    </>
  );
}

function Sidebar({ groups, activeGroup, activeSite, onSelectGroup, onSelectSite, total }) {
  return (
    <aside className="sidebar">
      <div className="nav-section">
        <div className="nav-label">视图</div>
        <ul className="nav-list">
          <li>
            <button
              className="nav-item"
              aria-selected={activeGroup === "all"}
              onClick={() => onSelectGroup("all")}
            >
              <span className="label">全部</span>
              <span className="count">{total}</span>
            </button>
          </li>
        </ul>
      </div>
      <div className="nav-section">
        <div className="nav-label">分组 → 渠道</div>
        <ul className="nav-list">
          {groups.map((g) => {
            const isOpen = activeGroup === g.name;
            return (
              <React.Fragment key={g.name}>
                <li>
                  <button
                    className="nav-item"
                    aria-selected={isOpen && !activeSite}
                    onClick={() => onSelectGroup(g.name)}
                  >
                    <span className="label">{g.name}</span>
                    <span className="count">{g.count}</span>
                  </button>
                </li>
                {isOpen && g.subs && g.subs.map((sub) => (
                  <li key={g.name + "::" + sub.site_id}>
                    <button
                      className="nav-item sub"
                      aria-selected={activeSite === sub.site_id}
                      onClick={() => onSelectSite(activeSite === sub.site_id ? null : sub.site_id)}
                      title={sub.site_id}
                    >
                      <span className="label">{sub.site_name}</span>
                      <span className="count">{sub.count}</span>
                    </button>
                  </li>
                ))}
              </React.Fragment>
            );
          })}
        </ul>
      </div>
    </aside>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
