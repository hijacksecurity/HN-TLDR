# Architecture Documentation

This directory contains architecture and design documentation for the HackerNews TLDR system.

## 📋 Contents

- **[system-architecture.md](system-architecture.md)** - Overall system architecture
- **[microservices-design.md](microservices-design.md)** - Microservices design patterns
- **[data-flow.md](data-flow.md)** - Data flow and processing pipeline
- **[deployment-architecture.md](deployment-architecture.md)** - Deployment and infrastructure

## 🏗️ System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │ HN API Service  │
│   React App     │◄───┤   FastAPI       │◄───┤   FastAPI       │
│   Port 7003     │    │   Port 7000     │    │   Port 7001     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Summarization   │
                       │ Service         │
                       │ OpenAI + FastAPI│
                       │ Port 7002       │
                       └─────────────────┘
```

## 🎯 Design Principles

- **Microservices Architecture** - Independent, loosely coupled services
- **API-First Design** - RESTful APIs with clear contracts
- **Containerization** - Docker containers for consistency
- **Scalability** - Horizontal scaling capabilities
- **Observability** - Health checks and monitoring
- **Security** - Defense in depth with multiple layers
