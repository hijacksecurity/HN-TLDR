#!/bin/bash

echo "🚀 Deploying HN-TLDR to Kubernetes TEST environment..."

# Apply all manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f storage.yaml
kubectl apply -f hn-api-service.yaml
kubectl apply -f summarization-service.yaml
kubectl apply -f backend-api.yaml
kubectl apply -f frontend.yaml

echo "✅ Deployment complete!"
echo ""
echo "Check deployment status:"
echo "kubectl get pods -n hn-tldr-test"
echo ""
echo "Access the application:"
echo "kubectl port-forward -n hn-tldr-test service/frontend 7003:7003"
echo "Or directly via LoadBalancer: http://localhost:7003"
