import requests

video_id = "7504081537235815687"

url = "https://www.tiktok.com/api/comment/list/"

params = {
    "aid": 1988,            # TikTok web app ID
    "aweme_id": video_id,   # video ID
    "cursor": 0,            # pagination cursor
    "count": 20,            # comments per page
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": f"https://www.tiktok.com/video/{video_id}",
    "Accept": "application/json",
}

resp = requests.get(url, params=params, headers=headers, timeout=15)
data = resp.json()

for c in data["comments"][:50]:
    print(c["text"])
