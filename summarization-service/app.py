import os
import json
import hashlib
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
import openai
import uvicorn

app = FastAPI(title="Summarization Service", version="1.0.0")

DATA_DIR = "/app/data"
SUMMARY_CACHE_FILE = f"{DATA_DIR}/summaries_cache.json"

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SummarizeRequest(BaseModel):
    url: str
    title: str


class SummarizeResponse(BaseModel):
    summary: str
    success: bool
    error: Optional[str] = None


def load_summary_cache() -> dict:
    try:
        if os.path.exists(SUMMARY_CACHE_FILE):
            with open(SUMMARY_CACHE_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_summary_cache(cache: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SUMMARY_CACHE_FILE, "w") as f:
        json.dump(cache, f)


def get_cache_key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


async def fetch_article_content(url: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                for script in soup(["script", "style"]):
                    script.decompose()

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (
                    phrase.strip() for line in lines for phrase in line.split("  ")
                )
                text = " ".join(chunk for chunk in chunks if chunk)

                return text[:4000]
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
    return None


async def generate_summary(title: str, content: Optional[str]) -> str:
    try:
        if content:
            prompt = f"""
            Summarize this article in exactly one engaging paragraph (3-4 sentences).
            Make it fun and informative, highlighting the key points.

            Title: {title}
            Content: {content[:2000]}
            """
        else:
            prompt = f"""
            Based only on this title, create an engaging one-paragraph summary (3-4 sentences)
            of what this article is likely about. Make it fun and informative.

            Title: {title}
            """

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a fun tech journalist who writes engaging summaries.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return f"🤖 This article about '{title}' looks interesting but we couldn't fetch the full summary right now. Check it out yourself!"


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "summarization-service"}


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_article(request: SummarizeRequest):
    try:
        cache = load_summary_cache()
        cache_key = get_cache_key(request.url)

        if cache_key in cache:
            return SummarizeResponse(summary=cache[cache_key], success=True)

        content = await fetch_article_content(request.url)
        summary = await generate_summary(request.title, content)

        cache[cache_key] = summary
        save_summary_cache(cache)

        return SummarizeResponse(summary=summary, success=True)

    except Exception as e:
        return SummarizeResponse(
            summary=f"Error summarizing: {str(e)}", success=False, error=str(e)
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7002)
