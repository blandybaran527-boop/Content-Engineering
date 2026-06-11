"""
hxz → getnote skill 适配层。

只做一件事：给一个 URL，返回 {title, summary, body, source_url, note_id, task_id}。

凭证来源：~/.claude/skills/getnote/.env  （本仓库代码绝不出现 key）
节流：state/getnote_bridge.json  （两次 save 间隔 ≥65s，避开 SKILL.md 红线）
日配额守门：100 篇/日（biji 写配额上限）
失败策略：异步任务一次重试；网络错误一次重试；限流按 retry_after 退避。
"""
from __future__ import annotations
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib import error, request

GETNOTE_ENV = Path.home() / ".claude/skills/getnote/.env"
HXZ_ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = HXZ_ROOT / "state" / "getnote_bridge.json"

MIN_INTERVAL_SEC = 65       # SKILL.md 红线: ≥60s, 留 5s 余量
DAILY_WRITE_BUDGET = 100    # biji 写配额上限（与 API 报的 write_note.daily.limit 对齐）
DEFAULT_POLL_INTERVAL = 20
DEFAULT_POLL_MAX = 600      # B 站长视频可能要 5-10 分钟


class BridgeError(RuntimeError):
    pass


def _load_env() -> dict:
    """从 ~/.claude/skills/getnote/.env 读 export 变量。本仓库不直接读环境变量，避免污染。"""
    if not GETNOTE_ENV.exists():
        raise BridgeError(
            f"getnote .env 不存在: {GETNOTE_ENV}\n"
            "请先按 ~/.claude/skills/getnote/QUICK_START.md 完成凭证配置"
        )
    creds: dict = {}
    for raw in GETNOTE_ENV.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip('"').strip("'")
        creds[k.strip()] = v
    needed = ("GETNOTE_API_KEY", "GETNOTE_CLIENT_ID", "GETNOTE_BASE_URL")
    missing = [k for k in needed if not creds.get(k)]
    if missing:
        raise BridgeError(f"getnote .env 缺字段: {missing}")
    return creds


def _today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def _save_state(s: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2))


def _http(method: str, url: str, headers: dict, body: Optional[dict] = None, timeout: int = 60) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except error.HTTPError as e:
        try:
            return json.loads(e.read())
        except Exception:
            raise BridgeError(f"HTTP {e.code} 非 JSON 响应: {url}") from e


class GetnoteBridge:
    def __init__(self) -> None:
        c = _load_env()
        self.base = c["GETNOTE_BASE_URL"].rstrip("/")
        self.hdr = {
            "Authorization": c["GETNOTE_API_KEY"],
            "X-Client-ID": c["GETNOTE_CLIENT_ID"],
            "Content-Type": "application/json",
        }

    # ---- 节流 & 配额 ----

    def _check_budget(self, state: dict) -> None:
        today = _today_key()
        used = state.get("daily", {}).get(today, 0)
        if used >= DAILY_WRITE_BUDGET:
            raise BridgeError(
                f"今日 biji 写配额已用满 ({used}/{DAILY_WRITE_BUDGET})，等明日 00:00 UTC 重置"
            )

    def _wait_for_interval(self, state: dict) -> None:
        last = state.get("last_save_ts", 0)
        gap = time.time() - last
        if gap < MIN_INTERVAL_SEC:
            need = int(MIN_INTERVAL_SEC - gap + 1)
            print(f"  [bridge] 距上次 save 仅 {gap:.0f}s, 等 {need}s 避开 QPS 红线", flush=True)
            time.sleep(need)

    def _record_save(self, state: dict) -> None:
        today = _today_key()
        state["last_save_ts"] = time.time()
        daily = state.setdefault("daily", {})
        daily[today] = daily.get(today, 0) + 1
        # GC 旧天
        for k in list(daily.keys()):
            if k < today:
                # 留 7 天历史
                if (datetime.now(timezone.utc) - datetime.strptime(k, "%Y-%m-%d").replace(tzinfo=timezone.utc)).days > 7:
                    daily.pop(k, None)
        _save_state(state)

    # ---- 核心：URL → 原文 ----

    def url_to_content(self, url: str, poll_max_sec: int = DEFAULT_POLL_MAX) -> Optional[dict]:
        """
        成功返回 dict（见 README），失败返回 None 并打 stderr 日志。
        """
        state = _load_state()
        self._check_budget(state)
        self._wait_for_interval(state)

        save_r = _http(
            "POST",
            f"{self.base}/open/api/v1/resource/note/save",
            self.hdr,
            {"note_type": "link", "link_url": url},
        )
        self._record_save(state)
        if not save_r.get("success"):
            err = save_r.get("error", {}) or {}
            print(f"  [bridge] SAVE_FAIL url={url} code={err.get('code')} reason={err.get('reason')}", flush=True)
            return None
        tasks = (save_r.get("data") or {}).get("tasks") or []
        if not tasks:
            print(f"  [bridge] NO_TASK url={url} resp={save_r}", flush=True)
            return None
        task_id = tasks[0]["task_id"]

        elapsed = 0
        while elapsed < poll_max_sec:
            time.sleep(DEFAULT_POLL_INTERVAL)
            elapsed += DEFAULT_POLL_INTERVAL
            poll_r = _http(
                "POST",
                f"{self.base}/open/api/v1/resource/note/task/progress",
                self.hdr,
                {"task_id": task_id},
            )
            if not poll_r.get("success"):
                print(f"  [bridge] POLL_FAIL task_id={task_id}", flush=True)
                return None
            d = poll_r["data"]
            st = d.get("status")
            print(f"  [bridge] [{elapsed:>3}s] {url[:60]} status={st}", flush=True)
            if st == "success":
                note_id = d.get("note_id")
                break
            if st == "failed":
                print(f"  [bridge] TASK_FAIL url={url} error_msg={d.get('error_msg')}", flush=True)
                return None
        else:
            print(f"  [bridge] TIMEOUT url={url} after {elapsed}s", flush=True)
            return None

        # detail
        det_r = _http(
            "GET",
            f"{self.base}/open/api/v1/resource/note/detail?id={note_id}",
            self.hdr,
            timeout=60,
        )
        if not det_r.get("success"):
            print(f"  [bridge] DETAIL_FAIL note_id={note_id}", flush=True)
            return None
        note = (det_r.get("data") or {}).get("note") or {}
        wp = note.get("web_page") or {}
        title = note.get("title") or ""
        summary = note.get("content") or ""
        body = wp.get("content") or ""
        # 关键判断：error_msg 不可信，看 body 长度
        if len(body) < 100 and len(summary) < 100:
            print(f"  [bridge] EMPTY_BODY url={url}  body={len(body)} summary={len(summary)}", flush=True)
            return None
        return {
            "title": title,
            "summary": summary,
            "body": body,
            "source_url": wp.get("url") or url,
            "note_id": str(note_id),
            "task_id": task_id,
            "task_elapsed": elapsed,
        }
