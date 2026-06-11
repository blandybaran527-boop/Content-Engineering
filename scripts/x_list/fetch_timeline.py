"""拉 X List 内所有成员最新推文 — chrome cookie + httpx 直调 GraphQL。

替代失效的 twscrape (其 client-transaction-id 算法已被 X 改前端打挂,
同 add_members.py 早就遇到的 twikit 失效)。

用法:
    python3 scripts/x_list/fetch_timeline.py --list-id <ID> --count 100
    # 输出 JSONL 到 stdout 或 --output, 字段 schema 兼容 twscrape

环境变量: TWITTER_AUTH_TOKEN, TWITTER_CT0 (从 chrome Cookie-Editor 在 x.com 域 export)
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.parse import quote

import httpx

# 公开的 web bearer (同 add_members.py 用的, 所有浏览器请求共用)
BEARER = (
    "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
    "%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
)

# 抓自 fa0311/TwitterInternalAPIDocument (2026-06 截止)
# 如失效, 重新抓 https://github.com/fa0311/TwitterInternalAPIDocument
LIST_TIMELINE_QID = "VqgCZ0jBFrSTE9A27-ToGQ"
LIST_TIMELINE_URL = f"https://x.com/i/api/graphql/{LIST_TIMELINE_QID}/ListLatestTweetsTimeline"

FEATURES = {
    "rweb_video_screen_enabled": False,
    "rweb_cashtags_enabled": True,
    "profile_label_improvements_pcf_label_in_post_enabled": True,
    "responsive_web_profile_redirect_enabled": False,
    "rweb_tipjar_consumption_enabled": False,
    "verified_phone_label_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "premium_content_api_read_enabled": False,
    "communities_web_enable_tweet_community_results_fetch": True,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
    "responsive_web_grok_analyze_post_followups_enabled": False,
    "responsive_web_jetfuel_frame": True,
    "responsive_web_grok_share_attachment_enabled": True,
    "responsive_web_grok_annotations_enabled": True,
    "articles_preview_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "content_disclosure_indicator_enabled": True,
    "content_disclosure_ai_generated_indicator_enabled": True,
    "responsive_web_grok_show_grok_translated_post": True,
    "responsive_web_grok_analysis_button_from_backend": True,
    "post_ctas_fetch_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": False,
    "responsive_web_grok_image_annotation_enabled": True,
    "responsive_web_grok_imagine_annotation_enabled": True,
    "responsive_web_grok_community_note_auto_translation_is_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
}

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def make_headers(auth: str, ct0: str) -> dict:
    return {
        "authorization": f"Bearer {BEARER}",
        "x-csrf-token": ct0,
        "cookie": f"auth_token={auth}; ct0={ct0}",
        "content-type": "application/json",
        "user-agent": UA,
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "accept": "*/*",
        "referer": "https://x.com/",
    }


def fetch_page(client: httpx.Client, list_id: str, count: int, cursor: str | None, headers: dict) -> dict:
    variables = {"listId": list_id, "count": count}
    if cursor:
        variables["cursor"] = cursor
    params = {
        "variables": json.dumps(variables, separators=(",", ":")),
        "features": json.dumps(FEATURES, separators=(",", ":")),
    }
    r = client.get(LIST_TIMELINE_URL, params=params, headers=headers, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:400]}")
    return r.json()


def walk_timeline_instructions(data: dict):
    """Timeline GraphQL 返回结构: data.list.tweets_timeline.timeline.instructions[].entries[]"""
    try:
        tt = data["data"]["list"]["tweets_timeline"]["timeline"]
    except (KeyError, TypeError):
        return [], None
    instructions = tt.get("instructions") or []
    entries = []
    cursor = None
    for ins in instructions:
        if ins.get("type") == "TimelineAddEntries":
            for e in ins.get("entries", []):
                entries.append(e)
        elif ins.get("type") == "TimelineReplaceEntry":
            entry = ins.get("entry") or {}
            entries.append(entry)
    # cursor 在最后一个 entry (TimelineTimelineCursor)
    for e in reversed(entries):
        content = e.get("content") or {}
        if content.get("entryType") == "TimelineTimelineCursor" and content.get("cursorType") == "Bottom":
            cursor = content.get("value")
            break
    return entries, cursor


def parse_entry(e: dict) -> dict | None:
    """从 entry 提取一条 tweet, 返回 twscrape-兼容 schema"""
    content = e.get("content") or {}
    if content.get("entryType") != "TimelineTimelineItem":
        return None
    item_content = content.get("itemContent") or {}
    if item_content.get("itemType") != "TimelineTweet":
        return None
    tweet_results = (item_content.get("tweet_results") or {}).get("result") or {}
    # tweet_results 有时是 TweetWithVisibilityResults
    if tweet_results.get("__typename") == "TweetWithVisibilityResults":
        tweet_results = tweet_results.get("tweet") or {}
    legacy = tweet_results.get("legacy") or {}
    user = ((tweet_results.get("core") or {}).get("user_results") or {}).get("result") or {}
    user_legacy = user.get("legacy") or {}
    user_core = user.get("core") or {}
    # 核心字段
    tweet_id = tweet_results.get("rest_id") or legacy.get("id_str") or ""
    user_id = user.get("rest_id") or ""
    username = user_core.get("screen_name") or user_legacy.get("screen_name") or ""
    name = user_core.get("name") or user_legacy.get("name") or ""
    avatar = (user.get("avatar") or {}).get("image_url") or user_legacy.get("profile_image_url_https") or ""
    # 推文
    raw_content = legacy.get("full_text") or ""
    # note_tweet (长文)
    note = (tweet_results.get("note_tweet") or {}).get("note_tweet_results", {}).get("result") or {}
    if note.get("text"):
        raw_content = note["text"]
    # X 原格式: "Thu Jun 11 09:35:58 +0000 2026" → ISO 8601 (兼容 hxz parse_dt)
    raw_date = legacy.get("created_at") or ""
    date = raw_date
    if raw_date:
        try:
            date = datetime.strptime(raw_date, "%a %b %d %H:%M:%S %z %Y").astimezone(timezone.utc).isoformat()
        except Exception:
            pass
    is_retweet = "retweeted_status_result" in legacy or legacy.get("full_text", "").startswith("RT @")
    rt = None
    if is_retweet:
        rt = {"present": True}
    # media
    media_legacy = (legacy.get("extended_entities") or {}).get("media") or []
    photos = []
    for m in media_legacy:
        if m.get("type") == "photo":
            photos.append({"url": m.get("media_url_https")})
    return {
        "id": tweet_id,
        "id_str": tweet_id,
        "url": f"https://x.com/{username}/status/{tweet_id}" if username and tweet_id else "",
        "date": date,
        "user": {
            "id": user_id,
            "username": username,
            "displayname": name,
            "profileImageUrl": avatar,
        },
        "rawContent": raw_content,
        "retweetedTweet": rt,
        "media": {"photos": photos} if photos else {},
        "replyCount": legacy.get("reply_count", 0),
        "retweetCount": legacy.get("retweet_count", 0),
        "likeCount": legacy.get("favorite_count", 0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-id", required=True)
    ap.add_argument("--count", type=int, default=100)
    ap.add_argument("--pages", type=int, default=3, help="最多翻几页")
    ap.add_argument("--proxy", default="http://127.0.0.1:7890")
    ap.add_argument("--output", default="-", help="- = stdout; 否则文件路径 (JSONL)")
    args = ap.parse_args()

    auth = os.environ.get("TWITTER_AUTH_TOKEN")
    ct0 = os.environ.get("TWITTER_CT0")
    if not auth or not ct0:
        print("缺少 TWITTER_AUTH_TOKEN / TWITTER_CT0 环境变量", file=sys.stderr)
        sys.exit(1)

    headers = make_headers(auth, ct0)
    client = httpx.Client(proxy=args.proxy)
    out_f = sys.stdout if args.output == "-" else open(args.output, "w")

    total = 0
    cursor = None
    try:
        for page in range(args.pages):
            data = fetch_page(client, args.list_id, args.count, cursor, headers)
            entries, next_cursor = walk_timeline_instructions(data)
            page_count = 0
            for e in entries:
                tw = parse_entry(e)
                if tw:
                    out_f.write(json.dumps(tw, ensure_ascii=False) + "\n")
                    page_count += 1
            print(f"[fetch_timeline] page {page+1}: {page_count} tweets (cursor={cursor[:30] if cursor else 'None'}...)", file=sys.stderr, flush=True)
            total += page_count
            if not next_cursor or next_cursor == cursor or page_count == 0:
                break
            cursor = next_cursor
            time.sleep(2)
        print(f"[fetch_timeline] 完成: 共 {total} 条 tweets", file=sys.stderr)
    finally:
        client.close()
        if out_f is not sys.stdout:
            out_f.close()


if __name__ == "__main__":
    main()
