// 信源 / 模态 图标。SVG 内联，单色继承 currentColor。
// 渠道：wechat / bilibili / xiaoyuzhou / youtube / x / rss / papers
// 模态：text / video / audio / longform

const ChannelIcon = ({ channel, size = 14 }) => {
  const s = size;
  const C = { width: s, height: s, viewBox: "0 0 24 24", fill: "currentColor" };
  switch (channel) {
    case "wechat":
      return (
        <svg {...C}>
          <path d="M9.5 4C5.4 4 2 6.9 2 10.4c0 2 1.1 3.8 2.9 5L4 18l3.1-1.6c.6.1 1.2.2 1.8.2h.3c-.1-.5-.2-1-.2-1.6 0-3.4 3.3-6.1 7.3-6.1.5 0 1 .1 1.4.1C17.1 5.9 13.6 4 9.5 4zM7 7.5a1 1 0 110 2 1 1 0 010-2zm5 0a1 1 0 110 2 1 1 0 010-2zM16.3 11C13 11 10.3 13.3 10.3 16c0 1.5.8 2.9 2.2 3.8l-.5 1.7 2.3-1.2c.6.2 1.3.3 2 .3.4 0 .8 0 1.1-.1l2.1 1.2-.5-1.9c1.4-.9 2.3-2.3 2.3-3.8 0-2.7-2.6-5-6-5zm-2 2.5a1 1 0 110 2 1 1 0 010-2zm4 0a1 1 0 110 2 1 1 0 010-2z"/>
        </svg>
      );
    case "bilibili":
      return (
        <svg {...C}>
          <path d="M17.8 4.2c.6.6.6 1.5 0 2.1L16.9 7.1H18c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H6c-1.7 0-3-1.3-3-3v-7c0-1.7 1.3-3 3-3h1.1L6.2 6.3c-.6-.6-.6-1.5 0-2.1.6-.6 1.5-.6 2.1 0L11 6.9V7h2v-.1l2.7-2.7c.6-.6 1.5-.6 2.1 0zM18 9H6c-.5 0-.9.4-.9.9v7.2c0 .5.4.9.9.9h12c.5 0 .9-.4.9-.9V9.9c0-.5-.4-.9-.9-.9zm-9 2.5a1 1 0 011 1V14a1 1 0 11-2 0v-1.5a1 1 0 011-1zm6 0a1 1 0 011 1V14a1 1 0 11-2 0v-1.5a1 1 0 011-1z"/>
        </svg>
      );
    case "xiaoyuzhou":
      return (
        <svg {...C}>
          <path d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 4.5a3 3 0 013 3v3a3 3 0 11-6 0v-3a3 3 0 013-3zm-5 7.5a1 1 0 011 1 4 4 0 008 0 1 1 0 112 0 6 6 0 01-5 5.9V22h2a1 1 0 110 2H9a1 1 0 010-2h2v-1.1A6 6 0 016 15a1 1 0 011-1z"/>
        </svg>
      );
    case "youtube":
      return (
        <svg {...C}>
          <path d="M21.6 7.2a2.5 2.5 0 00-1.8-1.8C18.3 5 12 5 12 5s-6.3 0-7.8.4A2.5 2.5 0 002.4 7.2C2 8.7 2 12 2 12s0 3.3.4 4.8a2.5 2.5 0 001.8 1.8c1.5.4 7.8.4 7.8.4s6.3 0 7.8-.4a2.5 2.5 0 001.8-1.8c.4-1.5.4-4.8.4-4.8s0-3.3-.4-4.8zM10 15V9l5 3-5 3z"/>
        </svg>
      );
    case "x":
      return (
        <svg {...C}>
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24h-6.66l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25h6.83l4.713 6.231 5.447-6.231z"/>
        </svg>
      );
    case "rss":
      return (
        <svg {...C}>
          <path d="M4 4a16 16 0 0116 16h-3A13 13 0 004 7V4zm0 6a10 10 0 0110 10h-3a7 7 0 00-7-7v-3zm1 7a2 2 0 110 4 2 2 0 010-4z"/>
        </svg>
      );
    case "papers":
      return (
        <svg {...C}>
          <path d="M6 2h9l5 5v13a2 2 0 01-2 2H6a2 2 0 01-2-2V4a2 2 0 012-2zm8 1.5V8h4.5L14 3.5zM7 12h10v2H7v-2zm0 4h10v2H7v-2zm0-8h6v2H7V8z"/>
        </svg>
      );
    default:
      return null;
  }
};

const ModalityIcon = ({ modality, size = 14 }) => {
  const s = size;
  const C = { width: s, height: s, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2, strokeLinecap: "round", strokeLinejoin: "round" };
  switch (modality) {
    case "video":
      return (
        <svg {...C}>
          <polygon points="9,7 9,17 17,12" fill="currentColor" stroke="none" />
          <rect x="2" y="4" width="20" height="16" rx="2" />
        </svg>
      );
    case "audio":
      return (
        <svg {...C}>
          <path d="M3 10v4M7 7v10M11 4v16M15 7v10M19 10v4" />
        </svg>
      );
    case "longform":
      return (
        <svg {...C}>
          <path d="M4 5h16M4 9h16M4 13h10M4 17h12" />
        </svg>
      );
    case "text":
    default:
      return (
        <svg {...C}>
          <path d="M5 5h14M9 9h6M5 13h14M9 17h6" />
        </svg>
      );
  }
};

// 通用图标
const ChevronLeft = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="15,18 9,12 15,6" />
  </svg>
);
const ExternalLink = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
    <polyline points="15,3 21,3 21,9" />
    <line x1="10" y1="14" x2="21" y2="3" />
  </svg>
);
const SunIcon = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
  </svg>
);
const MoonIcon = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
  </svg>
);
const SettingsIcon = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 008.5 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 8.5a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />
  </svg>
);

Object.assign(window, {
  ChannelIcon, ModalityIcon,
  ChevronLeft, ExternalLink, SunIcon, MoonIcon, SettingsIcon,
});
