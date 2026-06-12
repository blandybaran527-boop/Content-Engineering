#!/bin/bash
# 一键安装本机 launchd 定时任务
# 1. 把 plist 复制到 ~/Library/LaunchAgents/
# 2. 用真实环境变量填充 PLACEHOLDER
# 3. launchctl load
#
# 用法: bash scripts/automation/install.sh
set -e

ROOT="${HOME}/Downloads/hxz-news-reader"
PLIST_SRC="${ROOT}/scripts/automation/com.hxz.news-reader.plist"
PLIST_DST="${HOME}/Library/LaunchAgents/com.hxz.news-reader.plist"

if [ -z "${TWITTER_AUTH_TOKEN:-}" ] || [ -z "${TWITTER_CT0:-}" ]; then
  echo "❌ TWITTER_AUTH_TOKEN / TWITTER_CT0 未设. 请先在当前 shell 设好再跑:" >&2
  echo "    export TWITTER_AUTH_TOKEN=..." >&2
  echo "    export TWITTER_CT0=..." >&2
  exit 1
fi

mkdir -p "${HOME}/Library/LaunchAgents" "${HOME}/Library/Logs"

# 复制并替换 PLACEHOLDER
cp "${PLIST_SRC}" "${PLIST_DST}"
/usr/bin/plutil -replace EnvironmentVariables.TWITTER_AUTH_TOKEN -string "${TWITTER_AUTH_TOKEN}" "${PLIST_DST}"
/usr/bin/plutil -replace EnvironmentVariables.TWITTER_CT0 -string "${TWITTER_CT0}" "${PLIST_DST}"
/bin/chmod 600 "${PLIST_DST}"  # cookie 在里面, 严格保护
echo "✓ plist 写入 ${PLIST_DST} (chmod 600)"

# 卸载旧的 (如有)
/bin/launchctl unload "${PLIST_DST}" 2>/dev/null || true

# 加载
/bin/launchctl load "${PLIST_DST}"
echo "✓ launchctl load 完成"

# 验证
if /bin/launchctl list com.hxz.news-reader >/dev/null 2>&1; then
  echo "✓ launchctl 已加载, 明早 6:30 首次跑"
else
  echo "❌ launchctl 加载失败" >&2
  exit 1
fi

# 提示
echo ""
echo "日志位置:"
echo "  应用日志: ~/Library/Logs/hxz-news-reader.log"
echo "  stdout:   ~/Library/Logs/hxz-news-reader.stdout.log"
echo "  stderr:   ~/Library/Logs/hxz-news-reader.stderr.log"
echo ""
echo "立即手动触发一次 (测试):"
echo "  /bin/launchctl start com.hxz.news-reader"
echo ""
echo "卸载:"
echo "  /bin/launchctl unload ${PLIST_DST}"
echo "  /bin/rm ${PLIST_DST}"
