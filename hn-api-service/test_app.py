import pytest
import asyncio
from fastapi.testclient import TestClient
from app import app, HNStory, fetch_story_details
import httpx

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_hn_story_creation():
    story_data = {
        "id": 123,
        "title": "Test Story",
        "url": "https://example.com",
        "score": 100,
        "by": "testuser",
        "time": 1234567890,
        "descendants": 50,
    }
    story = HNStory(story_data)
    assert story.id == 123
    assert story.title == "Test Story"
    assert story.url == "https://example.com"


def test_hn_story_to_dict():
    story_data = {
        "id": 123,
        "title": "Test Story",
        "url": "https://example.com",
        "score": 100,
        "by": "testuser",
        "time": 1234567890,
        "descendants": 50,
    }
    story = HNStory(story_data)
    result = story.to_dict()
    assert result == story_data


@pytest.mark.asyncio
async def test_fetch_story_details():
    async with httpx.AsyncClient() as http_client:
        story = await fetch_story_details(http_client, 1)
        if story:
            assert isinstance(story, HNStory)
            assert story.id == 1
