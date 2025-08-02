# Deployment Documentation

This directory contains environment-specific deployment guides and configurations.

## 🚀 Deployment Environments

### Development (Local Docker Compose)
- **File:** `../DEPLOYMENT.md#local-development`
- **Ports:** 7000-7003
- **Data:** Local volume mounts
- **Command:** `docker-compose up --build`

### Testing (Local Kubernetes)
- **File:** `../DEPLOYMENT.md#kubernetes-local-testing`
- **Namespace:** `default`
- **Services:** LoadBalancer type
- **Command:** `kubectl apply -f k8s/`

### Production
- **File:** `../DEPLOYMENT.md#production-deployment`
- **Status:** Template ready, configuration needed
- **Requirements:** External load balancer, persistent storage

## 📁 Configuration Files

### Docker Compose
- **`docker-compose.yml`** - Local development only

### Kubernetes
- **`k8s/deployment.yaml`** - Service deployments
- **`k8s/service.yaml`** - Service definitions
- **`k8s/secret.yaml`** - Secret template (requires API key)
- **`k8s/configmap.yaml`** - Configuration maps

## 🔧 Environment Variables

### Required for All Environments
- **`OPENAI_API_KEY`** - OpenAI API key for summarization service

### Optional Configuration
- **`HN_API_BASE_URL`** - HackerNews API base URL (default: https://hacker-news.firebaseio.com/v0)
- **`CACHE_TTL`** - Cache time-to-live in seconds (default: 300)
- **`MAX_STORIES`** - Maximum stories to fetch (default: 25)

## 🔍 Health Checks

All services expose health endpoints:
- **Backend API:** `http://localhost:7000/health`
- **HN API Service:** `http://localhost:7001/health`
- **Summarization Service:** `http://localhost:7002/health`
- **Frontend:** `http://localhost:7003` (React health)

## 📊 Monitoring

### Logs
- Docker Compose: `docker-compose logs -f [service]`
- Kubernetes: `kubectl logs -f deployment/[service]`

### Metrics
- Service health endpoints return basic metrics
- Container resource usage via Docker/Kubernetes tools

## 🚨 Troubleshooting

### Common Issues
1. **Port conflicts** - Ensure 7000-7003 are available
2. **API key missing** - Check OPENAI_API_KEY environment variable
3. **Network connectivity** - Verify service-to-service communication
4. **Storage permissions** - Check volume mount permissions

### Debug Commands
```bash
# Check service status
docker-compose ps
kubectl get pods

# View logs
docker-compose logs summarization-service
kubectl logs deployment/summarization-service

# Test connectivity
curl http://localhost:7000/health
kubectl port-forward svc/backend-api 7000:7000
```
