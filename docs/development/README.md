# Development Documentation

This directory contains development setup guides and best practices.

## 🛠️ Development Setup

### Prerequisites
- **Docker & Docker Compose** - For containerized development
- **Node.js 18+** - For frontend development
- **Python 3.9+** - For backend services
- **kubectl** - For Kubernetes testing
- **git** - Version control

### Quick Start
1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd HN-TLDR
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Install pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Start development environment**
   ```bash
   docker-compose up --build
   ```

## 🏗️ Project Structure

```
HN-TLDR/
├── backend-api/           # Main backend service
├── frontend/             # React application
├── hn-api-service/       # HackerNews API service
├── summarization-service/ # OpenAI summarization service
├── k8s/                  # Kubernetes manifests
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── .github/              # GitHub workflows
└── tests/                # Integration tests
```

## 🐍 Python Development

### Service Structure
Each Python service follows this structure:
```
service-name/
├── app.py              # FastAPI application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container definition
├── tests/             # Service tests
└── README.md          # Service documentation
```

### Code Standards
- **FastAPI** for API development
- **Black** for code formatting
- **Flake8** for linting
- **Pytest** for testing
- **Type hints** for better code quality

### Testing
```bash
# Run service tests
cd backend-api
python -m pytest tests/

# Run all Python tests
./scripts/test.sh python
```

## ⚛️ Frontend Development

### Technology Stack
- **React 18** with functional components
- **Material-UI (MUI)** for components
- **JavaScript** (ES6+)
- **ESLint** for linting
- **Jest** for testing

### Development Server
```bash
cd frontend
npm install
npm start  # Runs on http://localhost:7003
```

### Building
```bash
cd frontend
npm run build
```

## 🐳 Container Development

### Building Images
```bash
# Build all services (development only)
docker-compose build

# Build specific service
docker-compose build backend-api
```

### Debugging Containers
```bash
# Access running container
docker-compose exec backend-api bash

# View container logs
docker-compose logs -f backend-api
```

## ☸️ Kubernetes Development

### Local Testing
```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods
kubectl get services

# Port forwarding for testing
kubectl port-forward svc/frontend 7003:7003
```

### Debugging
```bash
# View pod logs
kubectl logs deployment/backend-api

# Access pod shell
kubectl exec -it deployment/backend-api -- bash
```

## 🔧 Code Quality

### Pre-commit Hooks
- **Gitleaks** - Secret detection

### Running Manually
```bash
# Run gitleaks
pre-commit run gitleaks --all-files
```


## 📝 Contributing

### Workflow
1. **Create feature branch** from `main`
2. **Make changes** following code standards
3. **Write tests** for new functionality
4. **Run quality checks** with pre-commit
5. **Submit pull request** with clear description

### Commit Messages
Follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

## 🐛 Debugging

### Common Issues
1. **Port already in use** - Change ports in docker-compose.yml
2. **API key not working** - Verify OPENAI_API_KEY in .env
3. **Import errors** - Check Python virtual environment
4. **CORS issues** - Verify frontend/backend communication

### Debug Tools
- **Docker logs** - `docker-compose logs [service]`
- **Health endpoints** - Test service availability
- **Browser DevTools** - Frontend debugging
- **FastAPI docs** - API testing at `/docs` endpoint
