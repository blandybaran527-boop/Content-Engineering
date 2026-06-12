#!/bin/bash
# 本机 launchd 启动脚本: 跑全本机依赖的 5 类通道
#   X (twitter cookie) + YouTube (住宅 IP) + 国内 3 类 (WeWe-RSS + getnote)
# 然后 build_local_index.py 刷新 data_local/items.json
#
# 调用方: launchd via com.hxz.news-reader.plist
# 日志: ~/Library/Logs/hxz-news-reader.log
set -uo pipefail

ROOT="${HOME}/Downloads/hxz-news-reader"
LOG="${HOME}/Library/Logs/hxz-news-reader.log"
PY=/usr/bin/python3

# 加载凭证 - getnote .env (含 GETNOTE_API_KEY / CLIENT_ID / BASE_URL)
if [ -f "${HOME}/.claude/skills/getnote/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "${HOME}/.claude/skills/getnote/.env"
  set +a
fi

# TWITTER_AUTH_TOKEN / TWITTER_CT0 应在 ~/.zshrc 或 LaunchAgents plist 的
# EnvironmentVariables 里; launchd 不读 .zshrc, 必须在 plist 里设
# (这是 launchd 的设计, 不是 bug)

cd "${ROOT}" || exit 1

{
  echo "================================================================"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] hxz-news-reader local cron start"
  echo "================================================================"

  # 1) 5 类本机通道
  "${PY}" scripts/update_news.py \
    --enable-x --enable-youtube \
    --enable-wechat --enable-bilibili --enable-xiaoyuzhou \
    --output-dir data \
    --window-hours 168
  RC=$?
  echo "[$(date '+%H:%M:%S')] update_news.py rc=${RC}"

  # 2) 刷新本地索引 (扫 data_local/ 重建 items.json)
  "${PY}" scripts/build_local_index.py
  RC2=$?
  echo "[$(date '+%H:%M:%S')] build_local_index.py rc=${RC2}"

  echo "[$(date '+%H:%M:%S')] done"
  echo
} >> "${LOG}" 2>&1
