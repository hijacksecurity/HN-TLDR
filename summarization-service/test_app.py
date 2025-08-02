import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app import app, SummarizeRequest, get_cache_key, fetch_article_content

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_cache_key():
    url = "https://example.com"
    key = get_cache_key(url)
    assert isinstance(key, str)
    assert len(key) == 32


@pytest.mark.asyncio
async def test_fetch_article_content():
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.content = "<html><body><p>Test content</p></body></html>"

        mock_client.return_value.__aenter__.return_value.get.return_value = (
            mock_response
        )

        content = await fetch_article_content("https://example.com")
        assert "Test content" in content


def test_summarize_request_model():
    request = SummarizeRequest(url="https://example.com", title="Test Title")
    assert request.url == "https://example.com"
    assert request.title == "Test Title"


@patch("app.openai_client")
def test_summarize_endpoint_without_openai_key(mock_openai):
    mock_openai.chat.completions.create.side_effect = Exception("API key not set")

    response = client.post(
        "/summarize", json={"url": "https://example.com", "title": "Test Article"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
