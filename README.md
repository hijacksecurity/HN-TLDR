# HackerNews TLDR 📰

A fun, modern microservices web application that fetches the top 25 HackerNews stories and summarizes each article using OpenAI's GPT-3.5-turbo. Get the gist of tech news without the time commitment!

![Demo](https://img.shields.io/badge/demo-live-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Docker](https://img.shields.io/badge/docker-enabled-2496ED)
![Kubernetes](https://img.shields.io/badge/kubernetes-ready-326CE5)

## 🌟 Features

- ⚡ **Lightning Fast**: Intelligent caching for both stories and summaries
- 🎨 **Modern UI**: Beautiful React interface with Material-UI and smooth animations
- 📱 **Responsive Design**: Works seamlessly on all device sizes
- 🤖 **AI-Powered**: OpenAI GPT-3.5-turbo generates engaging summaries
- 🔄 **Auto-refresh**: Stories update automatically every 10 minutes
- 🐳 **Fully Containerized**: Complete Docker and Kubernetes support
- ☸️ **Production Ready**: Scalable microservices architecture
- 🧪 **Well Tested**: Comprehensive test suite for all components
- 🔧 **Configurable**: Environment-based configuration for DEV/TEST/PROD

## 🏗️ Architecture

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

### Services

- **🌐 Frontend**: Modern React SPA with Material-UI, animations, and responsive design
- **🔄 Backend API**: Main orchestration service handling requests and data flow
- **📰 HN API Service**: Fetches and caches stories from HackerNews API
- **🤖 Summarization Service**: Uses OpenAI GPT-3.5-turbo to generate article summaries
- **💾 Data Layer**: File-based JSON storage with volume mounting for persistence

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (for containerized deployment)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Kubernetes** (optional, for k8s deployment)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hn-tldr.git
cd hn-tldr
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application

- **🌐 Frontend**: http://localhost:7003
- **🔧 Backend API**: http://localhost:7000
- **📊 API Documentation**: http://localhost:7000/docs

## 🧪 Testing

### Run All Tests
```bash
# Execute comprehensive test suite
./scripts/test_all.sh
```

### Test Individual Services
```bash
# Backend services
cd hn-api-service && python -m pytest test_app.py -v
cd summarization-service && python -m pytest test_app.py -v
cd backend-api && python -m pytest test_app.py -v

# Frontend
cd frontend && npm test -- --coverage --watchAll=false
```

## ☸️ Kubernetes Deployment

### Prerequisites
- Local Kubernetes cluster (Docker Desktop, minikube, etc.)
- kubectl configured

### Build Images
```bash
# Build all service images
docker build -t hn-api-service:latest ./hn-api-service
docker build -t summarization-service:latest ./summarization-service
docker build -t backend-api:latest ./backend-api
docker build -t frontend:latest ./frontend
```

### Configure Secrets
```bash
# Encode your OpenAI API key
echo -n "your-openai-api-key" | base64

# Update k8s/secret.yaml with the encoded key
```

### Deploy
```bash
cd k8s
./scripts/deploy.sh
```

### Access
```bash
# Check deployment status
kubectl get pods -n hn-tldr-test

# Access via port-forward
kubectl port-forward -n hn-tldr-test service/frontend 7003:7003

# Or use LoadBalancer (if available)
open http://localhost:7003
```

## 🎯 API Documentation

### Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/tldr` | Get all summarized stories |
| `GET` | `/stories/{id}` | Get specific story details |

### Example Response

```json
{
  "stories": [
    {
      "id": 123456,
      "title": "Amazing Tech Discovery",
      "url": "https://example.com/article",
      "score": 250,
      "by": "author",
      "time": 1640995200,
      "descendants": 42,
      "summary": "🚀 An engaging AI-generated summary of the article...",
      "summary_generated_at": "2024-01-01T12:00:00"
    }
  ],
  "total_stories": 25,
  "generated_at": "2024-01-01T12:00:00"
}
```

## 🔧 Development

### Local Development Setup

```bash
# Install Python dependencies
cd hn-api-service && pip install -r requirements.txt
cd ../summarization-service && pip install -r requirements.txt
cd ../backend-api && pip install -r requirements.txt

# Install Node.js dependencies
cd ../frontend && npm install

# Run services individually
# Terminal 1: HN API Service
cd hn-api-service && python app.py

# Terminal 2: Summarization Service
cd summarization-service && OPENAI_API_KEY=your_key python app.py

# Terminal 3: Backend API
cd backend-api && python app.py

# Terminal 4: Frontend
cd frontend && npm start
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for summarization | - | ✅ |
| `ENV` | Environment (DEV/TEST/PROD) | DEV | ❌ |
| `HN_API_URL` | HackerNews API service URL | http://hn-api-service:7001 | ❌ |
| `SUMMARIZATION_URL` | Summarization service URL | http://summarization-service:7002 | ❌ |

## 🛠️ Tech Stack

### Backend
- **🐍 Python 3.11+** - Modern Python with async support
- **⚡ FastAPI** - High-performance async web framework
- **🌐 httpx** - Async HTTP client for API calls
- **🤖 OpenAI API** - GPT-3.5-turbo for text summarization
- **📦 Pydantic** - Data validation and serialization

### Frontend
- **⚛️ React 18** - Modern React with hooks
- **🎨 Material-UI** - Beautiful, accessible components
- **✨ Framer Motion** - Smooth animations and transitions
- **📡 Axios** - HTTP client for API communication
- **🎯 TypeScript Ready** - Full TypeScript support available

### Infrastructure
- **🐳 Docker** - Containerization for all services
- **☸️ Kubernetes** - Container orchestration and scaling
- **🔧 Docker Compose** - Local development environment
- **📊 JSON Storage** - Simple, reliable file-based persistence

### Testing
- **🧪 pytest** - Python testing framework
- **🃏 Jest** - JavaScript testing framework
- **📝 React Testing Library** - Component testing utilities

## 📁 Project Structure

```
hn-tldr/
├── 📁 hn-api-service/          # HackerNews API service
│   ├── app.py                  # FastAPI application
│   ├── test_app.py            # Unit tests
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Container configuration
├── 📁 summarization-service/   # OpenAI summarization service
│   ├── app.py                  # FastAPI application
│   ├── test_app.py            # Unit tests
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Container configuration
├── 📁 backend-api/             # Main backend orchestration
│   ├── app.py                  # FastAPI application
│   ├── test_app.py            # Unit tests
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Container configuration
├── 📁 frontend/                # React frontend application
│   ├── src/                   # Source code
│   │   ├── App.js             # Main React component
│   │   └── index.js           # Entry point
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   └── Dockerfile             # Container configuration
├── 📁 k8s/                    # Kubernetes manifests
│   ├── namespace.yaml         # Namespace definition
│   ├── configmap.yaml         # Configuration
│   ├── secret.yaml            # Secrets template
│   └── *.yaml                 # Service manifests
├── 📄 docker-compose.yml      # Development environment
├── 📄 .env.example            # Environment template
├── 📄 .gitignore              # Git ignore rules
├── 📁 scripts/                # Utility scripts
│   ├── test_all.sh            # Test runner script
│   └── deploy.sh              # Deployment script
└── 📄 README.md               # This file
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HackerNews** for providing the excellent API
- **OpenAI** for the powerful GPT-3.5-turbo model
- **Material-UI** team for the beautiful React components
- **FastAPI** team for the amazing Python framework

## 📚 Documentation

- 📖 **[Full Documentation](docs/README.md)** - Complete project documentation
- 🏗️ **[Architecture Guide](docs/architecture/README.md)** - System design and architecture
- 🚀 **[Deployment Guide](docs/DEPLOYMENT.md)** - Deployment instructions
- 🛠️ **[Development Setup](docs/development/README.md)** - Development environment setup
- 🔌 **[API Documentation](docs/api/README.md)** - API specifications and examples

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/hn-tldr/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/hn-tldr/discussions)
- 🔒 **Security**: See [Security Policy](docs/SECURITY.md)

---

**Made with ❤️ for the HackerNews community**
