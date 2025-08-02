# API Documentation

This directory contains API documentation for all microservices.

## 📋 Available APIs

### Backend API (Port 7000)
- **`GET /api/summaries`** - Retrieve all cached article summaries
- **`POST /api/refresh`** - Force refresh of HackerNews articles and summaries
- **`GET /health`** - Service health check

### HN API Service (Port 7001)
- **`GET /api/top-stories`** - Fetch top 25 HackerNews stories
- **`GET /health`** - Service health check

### Summarization Service (Port 7002)
- **`POST /api/summarize`** - Summarize article content using OpenAI
- **`GET /health`** - Service health check

## 🔍 API Details

### Backend API

#### GET /api/summaries
Returns cached article summaries with metadata.

**Response:**
```json
{
  "summaries": [
    {
      "id": 12345,
      "title": "Article Title",
      "url": "https://example.com",
      "summary": "Generated summary text...",
      "score": 150,
      "by": "username",
      "time": 1640995200,
      "descendants": 25
    }
  ],
  "last_updated": "2024-01-01T00:00:00Z",
  "total_count": 25
}
```

#### POST /api/refresh
Triggers a fresh fetch of HackerNews stories and regenerates summaries.

**Response:**
```json
{
  "status": "success",
  "message": "Summaries refreshed successfully",
  "count": 25,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### HN API Service

#### GET /api/top-stories
Fetches the top 25 stories from HackerNews API.

**Response:**
```json
{
  "stories": [
    {
      "id": 12345,
      "title": "Story Title",
      "url": "https://example.com",
      "score": 150,
      "by": "username",
      "time": 1640995200,
      "descendants": 25,
      "text": "Full article content..."
    }
  ],
  "fetched_at": "2024-01-01T00:00:00Z"
}
```

### Summarization Service

#### POST /api/summarize
Generates summaries using OpenAI API.

**Request:**
```json
{
  "title": "Article Title",
  "content": "Full article content to summarize..."
}
```

**Response:**
```json
{
  "summary": "Generated summary paragraph...",
  "model": "gpt-3.5-turbo",
  "tokens_used": 245,
  "generated_at": "2024-01-01T00:00:00Z"
}
```

## 🔐 Authentication

The Summarization Service requires an OpenAI API key set in the environment variable `OPENAI_API_KEY`.

## 🚨 Error Handling

All services return standard HTTP status codes:
- **200** - Success
- **400** - Bad Request
- **404** - Not Found
- **500** - Internal Server Error
- **503** - Service Unavailable

Error responses include:
```json
{
  "error": "Error description",
  "status": 500,
  "timestamp": "2024-01-01T00:00:00Z"
}
```
