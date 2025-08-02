# Deployment Guide 🚀

This guide covers deploying HackerNews TLDR to various environments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Compose](#docker-compose)
- [Kubernetes](#kubernetes)
- [Production Considerations](#production-considerations)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/hn-tldr.git
cd hn-tldr

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Running Services Individually

```bash
# Terminal 1: HN API Service
cd hn-api-service
pip install -r requirements.txt
python app.py

# Terminal 2: Summarization Service
cd summarization-service
pip install -r requirements.txt
OPENAI_API_KEY=your_key python app.py

# Terminal 3: Backend API
cd backend-api
pip install -r requirements.txt
python app.py

# Terminal 4: Frontend
cd frontend
npm install
npm start
```

### Access Points

- Frontend: http://localhost:3000
- Backend API: http://localhost:7000
- HN API Service: http://localhost:7001
- Summarization Service: http://localhost:7002

## Docker Compose

### Development Environment

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Test Environment

```bash
# Use test configuration
docker-compose -f docker-compose.test.yml up --build
```

### Production Environment

```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up --build
```

### Access Points

- Frontend: http://localhost:7003
- Backend API: http://localhost:7000
- API Documentation: http://localhost:7000/docs

## Kubernetes

### Prerequisites

- Kubernetes cluster (local or cloud)
- kubectl configured
- Docker for building images

### Local Kubernetes (Docker Desktop/minikube)

#### 1. Build Images

```bash
# Build all service images
docker build -t hn-api-service:latest ./hn-api-service
docker build -t summarization-service:latest ./summarization-service
docker build -t backend-api:latest ./backend-api
docker build -t frontend:latest ./frontend
```

#### 2. Configure Secrets

```bash
# Encode your OpenAI API key
echo -n "your-openai-api-key" | base64

# Update k8s/secret.yaml with the encoded key
# Replace 'eW91ci1vcGVuYWktYXBpLWtleS1iYXNlNjQtZW5jb2RlZA==' with your encoded key
```

#### 3. Deploy

```bash
cd k8s
./deploy.sh
```

#### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n hn-tldr-test

# Check services
kubectl get services -n hn-tldr-test

# Check logs
kubectl logs -n hn-tldr-test deployment/backend-api
```

#### 5. Access Application

```bash
# Port forward to access locally
kubectl port-forward -n hn-tldr-test service/frontend 7003:7003

# Open browser
open http://localhost:7003
```

### Cloud Kubernetes (GKE, EKS, AKS)

#### 1. Build and Push Images

```bash
# Tag images for your registry
docker tag hn-api-service:latest your-registry/hn-api-service:latest
docker tag summarization-service:latest your-registry/summarization-service:latest
docker tag backend-api:latest your-registry/backend-api:latest
docker tag frontend:latest your-registry/frontend:latest

# Push to registry
docker push your-registry/hn-api-service:latest
docker push your-registry/summarization-service:latest
docker push your-registry/backend-api:latest
docker push your-registry/frontend:latest
```

#### 2. Update Kubernetes Manifests

Update image references in k8s/*.yaml files:

```yaml
# Example: k8s/backend-api.yaml
containers:
- name: backend-api
  image: your-registry/backend-api:latest
```

#### 3. Configure Ingress (Optional)

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hn-tldr-ingress
  namespace: hn-tldr-test
spec:
  rules:
  - host: hn-tldr.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 7003
```

#### 4. Deploy

```bash
kubectl apply -f k8s/
```

## Production Considerations

### Security

1. **Secrets Management**
   ```bash
   # Use external secret management
   kubectl create secret generic hn-tldr-secrets \
     --from-literal=OPENAI_API_KEY=your-key \
     -n hn-tldr-test
   ```

2. **Network Policies**
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: hn-tldr-network-policy
   spec:
     podSelector: {}
     policyTypes:
     - Ingress
     - Egress
   ```

3. **Security Contexts**
   ```yaml
   securityContext:
     runAsNonRoot: true
     runAsUser: 1000
     fsGroup: 2000
   ```

### Scaling

1. **Horizontal Pod Autoscaler**
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: backend-api-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: backend-api
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

2. **Resource Limits**
   ```yaml
   resources:
     requests:
       memory: "128Mi"
       cpu: "100m"
     limits:
       memory: "512Mi"
       cpu: "500m"
   ```

### Monitoring

1. **Health Checks**
   ```yaml
   livenessProbe:
     httpGet:
       path: /health
       port: 7000
     initialDelaySeconds: 30
     periodSeconds: 10

   readinessProbe:
     httpGet:
       path: /health
       port: 7000
     initialDelaySeconds: 5
     periodSeconds: 5
   ```

2. **Logging**
   ```yaml
   # Add logging sidecar or use centralized logging
   volumeMounts:
   - name: logs
     mountPath: /app/logs
   ```

### Persistence

1. **Persistent Volumes**
   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: hn-tldr-data-pvc
   spec:
     accessModes:
     - ReadWriteOnce
     resources:
       requests:
         storage: 10Gi
     storageClassName: fast-ssd
   ```

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `ENV` | Environment name | `DEV` |
| `HN_API_URL` | HN API service URL | `http://hn-api-service:7001` |
| `SUMMARIZATION_URL` | Summarization service URL | `http://summarization-service:7002` |
| `REACT_APP_API_URL` | Frontend API URL | `http://localhost:7000` |

## Troubleshooting

### Common Issues

#### 1. Pod CrashLoopBackOff

```bash
# Check logs
kubectl logs -n hn-tldr-test pod-name

# Check events
kubectl describe pod -n hn-tldr-test pod-name

# Common causes:
# - Missing environment variables
# - Image pull errors
# - Health check failures
```

#### 2. Service Connection Issues

```bash
# Test service connectivity
kubectl exec -n hn-tldr-test deployment/frontend -- wget -qO- http://backend-api:7000/health

# Check service endpoints
kubectl get endpoints -n hn-tldr-test
```

#### 3. OpenAI API Errors

```bash
# Check secret
kubectl get secret hn-tldr-secrets -n hn-tldr-test -o yaml

# Verify API key format
echo "your-key" | base64 -d
```

#### 4. Frontend Not Loading

```bash
# Check frontend logs
kubectl logs -n hn-tldr-test deployment/frontend

# Verify service
kubectl get service frontend -n hn-tldr-test

# Test port forward
kubectl port-forward -n hn-tldr-test service/frontend 7003:7003
```

### Debug Commands

```bash
# Get all resources
kubectl get all -n hn-tldr-test

# Describe deployment
kubectl describe deployment backend-api -n hn-tldr-test

# Get pod logs
kubectl logs -f -n hn-tldr-test deployment/backend-api

# Execute into container
kubectl exec -it -n hn-tldr-test deployment/backend-api -- /bin/sh

# Check resource usage
kubectl top pods -n hn-tldr-test
```

### Performance Tuning

1. **Caching**
   - Stories are cached for 5 minutes
   - Summaries are cached indefinitely
   - Adjust cache duration in code if needed

2. **Concurrency**
   - Summarization requests are processed concurrently
   - Adjust concurrency limits based on OpenAI rate limits

3. **Resource Allocation**
   - Monitor CPU/memory usage
   - Adjust resource requests/limits
   - Consider node affinity for performance-critical pods

## Cleanup

### Docker Compose

```bash
# Stop and remove containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Kubernetes

```bash
# Delete namespace (removes all resources)
kubectl delete namespace hn-tldr-test

# Or delete individual resources
kubectl delete -f k8s/
```

---

For more help, see our [Contributing Guide](CONTRIBUTING.md) or open an issue on GitHub.
