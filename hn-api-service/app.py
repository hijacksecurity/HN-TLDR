import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
import httpx
import uvicorn

app = FastAPI(title="HackerNews API Service", version="1.0.0")

DATA_DIR = "/app/data"
CACHE_FILE = f"{DATA_DIR}/hn_cache.json"
CACHE_DURATION = timedelta(minutes=5)


class HNStory:
    def __init__(self, story_data: dict):
        self.id = story_data.get("id")
        self.title = story_data.get("title", "")
        self.url = story_data.get("url", "")
        self.score = story_data.get("score", 0)
        self.by = story_data.get("by", "")
        self.time = story_data.get("time", 0)
        self.descendants = story_data.get("descendants", 0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "score": self.score,
            "by": self.by,
            "time": self.time,
            "descendants": self.descendants,
        }


async def fetch_story_details(
    client: httpx.AsyncClient, story_id: int
) -> Optional[HNStory]:
    try:
        response = await client.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        if response.status_code == 200:
            story_data = response.json()
            if (
                story_data
                and story_data.get("type") == "story"
                and story_data.get("url")
            ):
                return HNStory(story_data)
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
    return None


def load_cache() -> Optional[dict]:
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cache_data = json.load(f)
                cache_time = datetime.fromisoformat(cache_data["timestamp"])
                if datetime.now() - cache_time < CACHE_DURATION:
                    return cache_data
    except Exception:
        pass
    return None


def save_cache(stories: List[dict]):
    os.makedirs(DATA_DIR, exist_ok=True)
    cache_data = {"timestamp": datetime.now().isoformat(), "stories": stories}
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "hn-api-service"}


@app.get("/stories")
async def get_top_stories() -> List[Dict]:
    cached = load_cache()
    if cached:
        return cached["stories"]

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json"
            )
            response.raise_for_status()
            story_ids = response.json()[:25]

            tasks = [fetch_story_details(client, story_id) for story_id in story_ids]
            stories_data = await asyncio.gather(*tasks)

            stories = [story.to_dict() for story in stories_data if story is not None]

            save_cache(stories)
            return stories

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching stories: {str(e)}"
            )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7001)
