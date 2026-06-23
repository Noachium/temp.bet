"""
steam_build_checker_ci.py
one-shot version for github actions. runs once, checks for a change, notifies if needed.
set DISCORD_WEBHOOK_URL and STEAM_APP_ID as environment variables / github secrets.
"""
import requests
import json
import os
from datetime import datetime

STEAM_APP_ID = os.environ.get("STEAM_APP_ID", "4551040")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
JSON_FILE_PATH = "build_id.json"


def get_steam_build_info(app_id):
    depot_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    news_url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={app_id}&count=1&maxlength=0"

    store_resp = requests.get(depot_url, timeout=10).json()
    app_data = store_resp.get(str(app_id), {}).get("data", {})
    game_name = app_data.get("name", f"App {app_id}")

    # scrape the actual build id from the steam store page
    page_resp = requests.get(f"https://store.steampowered.com/app/{app_id}", timeout=10, headers={"Cookie": "birthtime=0; mature_content=1"})
    build_id = "unknown"
    for line in page_resp.text.splitlines():
        if '"buildid"' in line:
            build_id = line.split('"buildid"')[1].split('"')[1]
            break

    news_resp = requests.get(news_url, timeout=10).json()
    news_items = news_resp.get("appnews", {}).get("newsitems", [])
    latest = news_items[0] if news_items else {}

    return {
        "build_id": build_id,
        "game_name": game_name,
        "timestamp": datetime.utcnow().isoformat(),
        "news_title": latest.get("title", ""),
        "news_url": latest.get("url", f"https://store.steampowered.com/news/app/{app_id}"),
    }


def load_local_build_id():
    try:
        with open(JSON_FILE_PATH) as f:
            return json.load(f).get("build_id")
    except Exception:
        return None


def save_local_build_id(info):
    with open(JSON_FILE_PATH, "w") as f:
        json.dump({
            "build_id": info["build_id"],
            "game_name": info["game_name"],
            "last_updated": info["timestamp"],
            "latest_news_title": info["news_title"],
            "latest_news_url": info["news_url"],
        }, f, indent=2)


def send_discord_webhook(old_build_id, info):
    embed = {
        "title": "Animal Company Updated!",
        "description": "A new Animal Company update was found on steam.",
        "color": 0x1b9e4e,
        "fields": [
            {"name": "Previous Build ID", "value": f"`{old_build_id}`", "inline": True},
            {"name": "New Build ID", "value": f"`{info['build_id']}`", "inline": True},
            {"name": "\u200b", "value": "\u200b", "inline": False},
            {
                "name": "Latest Patch Notes",
                "value": f"[{info['news_title'] or 'View on Steam'}]({info['news_url']})",
                "inline": False,
            },
        ],
        "footer": {"text": f"Steam App {STEAM_APP_ID}  •  {info['timestamp']} UTC"},
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "thumbnail": {
            "url": f"https://cdn.cloudflare.steamstatic.com/steam/apps/{STEAM_APP_ID}/header.jpg"
        },
    }
    requests.post(DISCORD_WEBHOOK_URL, json={
        "embeds": [embed],
    }, timeout=10)
    print(f"[info] discord notified: {old_build_id} -> {info['build_id']}")


def main():
    current = load_local_build_id()
    info = get_steam_build_info(STEAM_APP_ID)
    new = info["build_id"]

    print(f"[info] current build id in json: {current}")
    print(f"[info] fetched build id from steam: {new}")

    if current is None:
        print(f"[info] first run, saving {new}")
        save_local_build_id(info)
    elif new != current:
        print(f"[info] build changed: {current} -> {new}")
        save_local_build_id(info)
        if DISCORD_WEBHOOK_URL:
            send_discord_webhook(current, info)
    else:
        print(f"[info] no change ({new})")


if __name__ == "__main__":
    main()
