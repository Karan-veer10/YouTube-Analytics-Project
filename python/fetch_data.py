import os
import csv
from googleapiclient.discovery import build

# ================================
# CONFIG
# ================================
API_KEY = ""   # Replace with your actual API key
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Replace with your channel ID

youtube = build("youtube", "v3", developerKey=API_KEY)


def get_uploads_playlist(channel_id):
    """Fetch the uploads playlist ID of the channel"""
    print("🔎 Fetching uploads playlist ID...")
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_ids(playlist_id, max_results=50):
    """Fetch video IDs from the uploads playlist"""
    print("📺 Fetching video IDs...")
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=max_results,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    print(f"✅ Found {len(video_ids)} videos.")
    return video_ids


def get_video_stats(video_ids):
    """Fetch statistics for a list of videos"""
    print("📊 Fetching video statistics...")
    stats = []
    for i in range(0, len(video_ids), 50):  # YouTube API allows max 50 IDs at once
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(video_ids[i:i+50])
        )
        response = request.execute()

        for item in response["items"]:
            stats.append({
                "VideoID": item["id"],
                "Title": item["snippet"]["title"],
                "PublishedAt": item["snippet"]["publishedAt"],
                "Category": item["snippet"].get("categoryId", "Unknown"),
                "Duration": item["contentDetails"].get("duration", "PT0S"),
                "Views": item["statistics"].get("viewCount", 0),
                "Likes": item["statistics"].get("likeCount", 0),
                "Comments": item["statistics"].get("commentCount", 0),
            })
    return stats


def save_to_csv(stats, filename="../data/raw/YouTubeData.csv"):
    """Save video stats to CSV"""
    keys = stats[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(stats)
    print(f"📂 Data saved to {filename}")


if __name__ == "__main__":
    playlist_id = get_uploads_playlist(CHANNEL_ID)
    video_ids = get_video_ids(playlist_id)
    video_stats = get_video_stats(video_ids)
    save_to_csv(video_stats)
