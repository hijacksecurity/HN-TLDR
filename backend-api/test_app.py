import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app import app, TLDRStory

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_tldr_story_model():
    story_data = {
        "id": 123,
        "title": "Test Story",
        "url": "https://example.com",
        "score": 100,
        "by": "testuser",
        "time": 1234567890,
        "descendants": 50,
        "summary": "Test summary",
        "summary_generated_at": "2023-01-01T00:00:00",
    }
    story = TLDRStory(**story_data)
    assert story.id == 123
    assert story.title == "Test Story"
    assert story.summary == "Test summary"


@patch("app.fetch_stories")
@patch("app.summarize_story")
@pytest.mark.asyncio
async def test_get_tldr_stories_mock(mock_summarize, mock_fetch):
    mock_fetch.return_value = [
        {
            "id": 123,
            "title": "Test Story",
            "url": "https://example.com",
            "score": 100,
            "by": "testuser",
            "time": 1234567890,
            "descendants": 50,
        }
    ]

    mock_summarize.return_value = "Test summary"

    response = client.get("/tldr")
    assert response.status_code == 200
    data = response.json()
    assert "stories" in data
    assert "generated_at" in data
    assert "total_stories" in data
