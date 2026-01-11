import requests

TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
REVIEW_URL = "https://open.tiktokapis.com/v2/research/tts/review/"

def get_client_token(client_key: str, client_secret: str) -> str:
    """
    Obtain a client access token (client_credentials).
    Docs: Client Access Token Management (open.tiktokapis.com).
    """
    data = {
        "client_key": client_key,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(TOKEN_URL, data=data, headers=headers, timeout=15)
    resp.raise_for_status()
    j = resp.json()
    # expected: { "access_token": "...", "expires_in": 7200, ... }
    return j["access_token"]

def fetch_reviews_client(product_id: int, token: str,
                         fields: str = "product_name,review_text,display_name,review_like_count,create_time,review_rating",
                         page_start: int = 1, page_size: int = 10):
    """
    Single-page call to the Research shop review endpoint.
    page_start is 1-based per docs; page_size max ~10 for shop reviews.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "product_id": product_id,
        "fields": fields,
        "page_start": page_start,
        "page_size": page_size
    }
    resp = requests.post(REVIEW_URL, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()

# Example usage:
if __name__ == "__main__":
    CLIENT_KEY = "awr13c616xr0fhhv"
    CLIENT_SECRET = "mGyedVzZ75Wd3ogodFay1iFKhaGFY5Wd"
    PRODUCT_ID = 12345678901234   # replace with TikTok Shop product id

    token = get_client_token(CLIENT_KEY, CLIENT_SECRET)
    print("Got token (truncated):", token[:20])

    # fetch first page
    data = fetch_reviews_client(PRODUCT_ID, token, page_start=1, page_size=10)
    # data structure (see docs): data.review_data is the list
    reviews = data.get("data", {}).get("review_data", [])
    print(f"Received {len(reviews)} reviews (sample):")
    for r in reviews[:5]:
        print(r)
