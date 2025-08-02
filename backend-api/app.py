import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import uvicorn

app = FastAPI(title="HackerNews TLDR Backend API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HN_API_URL = os.getenv("HN_API_URL", "http://localhost:8001")
SUMMARIZATION_URL = os.getenv("SUMMARIZATION_URL", "http://localhost:8002")
DATA_DIR = "/app/data"
TLDR_CACHE_FILE = f"{DATA_DIR}/tldr_cache.json"
CACHE_DURATION = timedelta(minutes=10)


class TLDRStory(BaseModel):
    id: int
    title: str
    url: str
    score: int
    by: str
    time: int
    descendants: int
    summary: str
    summary_generated_at: str


class TLDRResponse(BaseModel):
    stories: List[TLDRStory]
    generated_at: str
    total_stories: int


def load_tldr_cache() -> Optional[dict]:
    try:
        if os.path.exists(TLDR_CACHE_FILE):
            with open(TLDR_CACHE_FILE, "r") as f:
                cache_data = json.load(f)
                cache_time = datetime.fromisoformat(cache_data["generated_at"])
                if datetime.now() - cache_time < CACHE_DURATION:
                    return cache_data
    except Exception:
        pass
    return None


def save_tldr_cache(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TLDR_CACHE_FILE, "w") as f:
        json.dump(data, f)


async def fetch_stories() -> List[Dict]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{HN_API_URL}/stories")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching stories: {str(e)}"
            )


async def summarize_story(client: httpx.AsyncClient, story: Dict) -> str:
    try:
        if not story.get("url"):
            return f"📰 '{story.get('title', 'Untitled')}' - This appears to be a discussion post on HackerNews. Check it out for community insights!"

        response = await client.post(
            f"{SUMMARIZATION_URL}/summarize",
            json={"url": story["url"], "title": story["title"]},
            timeout=30.0,
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("summary", "Summary unavailable")
        else:
            return f"🤖 Couldn't summarize '{story['title']}' right now, but it looks interesting!"

    except Exception as e:
        return f"📝 '{story.get('title', 'Untitled')}' - Summary temporarily unavailable, but worth checking out!"


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend-api"}


@app.get("/tldr", response_model=TLDRResponse)
async def get_tldr_stories():
    cached = load_tldr_cache()
    if cached:
        return TLDRResponse(**cached)

    stories = await fetch_stories()

    async with httpx.AsyncClient() as client:
        summary_tasks = [summarize_story(client, story) for story in stories]
        summaries = await asyncio.gather(*summary_tasks)

    now = datetime.now().isoformat()
    tldr_stories = []

    for story, summary in zip(stories, summaries):
        tldr_story = TLDRStory(
            id=story["id"],
            title=story["title"],
            url=story["url"],
            score=story["score"],
            by=story["by"],
            time=story["time"],
            descendants=story["descendants"],
            summary=summary,
            summary_generated_at=now,
        )
        tldr_stories.append(tldr_story)

    response_data = {
        "stories": [story.dict() for story in tldr_stories],
        "generated_at": now,
        "total_stories": len(tldr_stories),
    }

    save_tldr_cache(response_data)

    return TLDRResponse(**response_data)


@app.get("/stories/{story_id}")
async def get_story_details(story_id: int):
    cached = load_tldr_cache()
    if cached:
        for story in cached["stories"]:
            if story["id"] == story_id:
                return story

    raise HTTPException(status_code=404, detail="Story not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
