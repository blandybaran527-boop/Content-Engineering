// 数据加载 + 信源分类 + 渠道/模态推断

// 加载顺序: data_local (本机, 含国内全文) → data (公开, 海外+摘要)
async function loadItems() {
  const candidates = ["../../data_local/items.json", "../../data/items.json", "data/items.json"];
  let lastErr = null;
  for (const url of candidates) {
    try {
      const r = await fetch(url + "?_=" + Date.now());
      if (r.ok) {
        const d = await r.json();
        return { items: d.items || [], generated_at: d.generated_at, source: url };
      }
      lastErr = new Error(`HTTP ${r.status} for ${url}`);
    } catch (e) { lastErr = e; }
  }
  throw lastErr ?? new Error("items.json not found");
}

// 从 url / channel / group 推断渠道 key（用于 chip + 颜色）
function inferChannel(item) {
  if (item.channel) {
    if (["wechat", "bilibili", "xiaoyuzhou", "youtube"].includes(item.channel)) return item.channel;
  }
  const url = (item.url || "").toLowerCase();
  if (url.includes("mp.weixin.qq.com")) return "wechat";
  if (url.includes("bilibili.com")) return "bilibili";
  if (url.includes("xiaoyuzhoufm.com")) return "xiaoyuzhou";
  if (url.includes("youtube.com") || url.includes("youtu.be")) return "youtube";
  if (url.includes("x.com/") || url.includes("twitter.com/")) return "x";
  if (url.includes("huggingface.co")) return "papers";
  if (url.includes("news.ycombinator.com")) return "rss";
  if (url.includes("substack.com")) return "rss";
  // group fallback
  const g = item.group || "";
  if (g.includes("聚合")) return "rss";
  if (g.includes("商科")) return "rss";
  if (g.includes("X-")) return "x";
  return "rss";
}

function inferModality(channel) {
  if (channel === "bilibili") return "video";
  if (channel === "youtube") return "video";
  if (channel === "xiaoyuzhou") return "audio";
  return "text";
}

const CHANNEL_LABEL = {
  wechat: "公众号",
  bilibili: "B站",
  xiaoyuzhou: "小宇宙",
  youtube: "YouTube",
  x: "X",
  rss: "RSS",
  papers: "Papers",
};

function enrichItem(it) {
  const ch = inferChannel(it);
  return {
    ...it,
    _channel: ch,
    _channelLabel: CHANNEL_LABEL[ch],
    _modality: inferModality(ch),
    _key: `${it.site_id}|${it.url}`,
  };
}

function fmtTime(iso) {
  if (!iso) return "";
  try {
    const d = new Date(iso);
    const now = new Date();
    const diff = (now - d) / 1000;
    if (diff < 60) return "刚刚";
    if (diff < 3600) return `${Math.floor(diff/60)} 分钟前`;
    if (diff < 86400) return `${Math.floor(diff/3600)} 小时前`;
    if (diff < 86400 * 7) return `${Math.floor(diff/86400)} 天前`;
    const m = d.getMonth() + 1;
    const day = d.getDate();
    if (d.getFullYear() === now.getFullYear()) return `${m}月${day}日`;
    return `${d.getFullYear()}-${String(m).padStart(2,"0")}-${String(day).padStart(2,"0")}`;
  } catch (e) {
    return "";
  }
}

function fmtBodyLen(html) {
  if (!html) return "";
  // 去 HTML tag 估算字数
  const txt = html.replace(/<[^>]+>/g, "").trim();
  const len = txt.length;
  if (len < 100) return "";
  if (len < 1000) return `${len} 字`;
  if (len < 10000) return `${(len/1000).toFixed(1)}k 字`;
  return `${Math.round(len/1000)}k 字`;
}

// Group 分类
function buildGroups(items) {
  const byGroup = new Map();
  for (const it of items) {
    const g = it.group || "其他";
    if (!byGroup.has(g)) byGroup.set(g, []);
    byGroup.get(g).push(it);
  }
  return Array.from(byGroup.entries())
    .map(([name, items]) => ({ name, count: items.length, items }))
    .sort((a, b) => b.count - a.count);
}

function buildChannels(items) {
  const by = new Map();
  for (const it of items) {
    const c = it._channel;
    if (!by.has(c)) by.set(c, []);
    by.get(c).push(it);
  }
  // 排序: 国内 (有 channel 字段的) 在前，海外在后
  const order = ["wechat", "bilibili", "xiaoyuzhou", "youtube", "x", "rss", "papers"];
  return order
    .filter((c) => by.has(c))
    .map((c) => ({
      channel: c,
      label: CHANNEL_LABEL[c],
      items: by.get(c).sort((a, b) => (b.published_at || "").localeCompare(a.published_at || "")),
    }));
}

Object.assign(window, {
  loadItems, enrichItem, fmtTime, fmtBodyLen,
  buildGroups, buildChannels,
  CHANNEL_LABEL, inferChannel, inferModality,
});
