# Deployment Guide

## Overview

This guide covers deployment options for DDSP-Piano in various environments, from development to enterprise production.

## Deployment Options

### 1. Local Development
### 2. Docker Containers
### 3. Cloud Deployment (AWS, GCP, Azure)
### 4. Kubernetes
### 5. On-Premises Enterprise

---

## Local Development

### Prerequisites

```bash
# Python 3.8+
python --version

# CUDA-capable GPU (recommended)
nvidia-smi

# Dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/yksanjo/ddsp-piano.git
cd ddsp-piano

# Install dependencies
pip install -r requirements.txt

# Test installation
python synthesize_midi_file.py test.mid output.wav
```

### Development Server

```bash
# Run API server locally
python -m ddsp_piano.api.server --port 8080 --host 0.0.0.0
```

---

## Docker Deployment

### Basic Dockerfile

```dockerfile
FROM tensorflow/tensorflow:2.8.0-gpu

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose API port
EXPOSE 8080

# Run API server
CMD ["python", "-m", "ddsp_piano.api.server", "--port", "8080", "--host", "0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t ddsp-piano:latest .

# Run container
docker run -d \
    --name ddsp-piano \
    --gpus all \
    -p 8080:8080 \
    -v $(pwd)/models:/app/models \
    ddsp-piano:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./models:/app/models
      - ./input:/app/input
      - ./output:/app/output
    environment:
      - LOG_LEVEL=INFO
      - API_KEY=${API_KEY}
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped
```

---

## Cloud Deployment

### AWS Deployment

#### EC2 with GPU

```bash
# Launch EC2 instance (g4dn.xlarge or larger)
# AMI: Deep Learning AMI (Ubuntu)

# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip docker.io nvidia-docker2

# Clone and build
git clone https://github.com/yksanjo/ddsp-piano.git
cd ddsp-piano
docker build -t ddsp-piano .

# Run container
docker run -d \
    --gpus all \
    -p 8080:8080 \
    ddsp-piano
```

#### ECS with Fargate

```yaml
# ecs-task-definition.json
{
  "family": "ddsp-piano",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "4096",
  "memory": "8192",
  "containerDefinitions": [{
    "name": "ddsp-piano",
    "image": "your-account.dkr.ecr.region.amazonaws.com/ddsp-piano:latest",
    "portMappings": [{
      "containerPort": 8080,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "LOG_LEVEL", "value": "INFO"}
    ]
  }]
}
```

#### Lambda (Serverless)

```python
# lambda_handler.py
import json
import boto3
from ddsp_piano import PianoSynthesizer

synthesizer = PianoSynthesizer()

def lambda_handler(event, context):
    midi_data = event['midi_file']
    piano_type = event.get('piano_type', 9)
    
    # Synthesize
    audio = synthesizer.synthesize_from_bytes(midi_data, piano_type)
    
    # Upload to S3
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket='your-bucket',
        Key='output.wav',
        Body=audio.tobytes()
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'s3_key': 'output.wav'})
    }
```

### Google Cloud Platform

#### Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/ddsp-piano

# Deploy to Cloud Run
gcloud run deploy ddsp-piano \
    --image gcr.io/PROJECT_ID/ddsp-piano \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 8Gi \
    --cpu 4
```

#### GKE (Kubernetes)

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ddsp-piano
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ddsp-piano
  template:
    metadata:
      labels:
        app: ddsp-piano
    spec:
      containers:
      - name: api
        image: gcr.io/PROJECT_ID/ddsp-piano:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            nvidia.com/gpu: 1
          limits:
            nvidia.com/gpu: 1
```

### Azure Deployment

#### Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry myregistry --image ddsp-piano:latest .

# Deploy to ACI
az container create \
    --resource-group myResourceGroup \
    --name ddsp-piano \
    --image myregistry.azurecr.io/ddsp-piano:latest \
    --cpu 4 \
    --memory 8 \
    --ports 8080
```

#### Azure Kubernetes Service

```yaml
# azure-k8s.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ddsp-piano
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: myregistry.azurecr.io/ddsp-piano:latest
        resources:
          requests:
            nvidia.com/gpu: 1
```

---

## Kubernetes Deployment

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ddsp-piano
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ddsp-piano
  template:
    metadata:
      labels:
        app: ddsp-piano
    spec:
      containers:
      - name: api
        image: ddsp-piano:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            nvidia.com/gpu: 1
            memory: "8Gi"
            cpu: "4"
          limits:
            nvidia.com/gpu: 1
            memory: "16Gi"
            cpu: "8"
        env:
        - name: LOG_LEVEL
          value: "INFO"
---
apiVersion: v1
kind: Service
metadata:
  name: ddsp-piano-service
spec:
  selector:
    app: ddsp-piano
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ddsp-piano-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ddsp-piano
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## On-Premises Enterprise

### Infrastructure Requirements

#### Minimum
- **GPU**: 1x NVIDIA GPU (8GB VRAM minimum)
- **CPU**: 8 cores
- **RAM**: 16GB
- **Storage**: 100GB SSD
- **Network**: 1Gbps

#### Recommended
- **GPU**: 2x NVIDIA GPU (16GB+ VRAM each)
- **CPU**: 16+ cores
- **RAM**: 32GB+
- **Storage**: 500GB+ NVMe SSD
- **Network**: 10Gbps

### Installation Steps

```bash
# 1. Install NVIDIA drivers
sudo apt-get update
sudo apt-get install -y nvidia-driver-470

# 2. Install Docker and NVIDIA Container Toolkit
sudo apt-get install -y docker.io
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 3. Deploy application
git clone https://github.com/yksanjo/ddsp-piano.git
cd ddsp-piano
docker-compose up -d
```

### High Availability Setup

```yaml
# docker-compose.ha.yaml
version: '3.8'

services:
  api-1:
    build: .
    ports:
      - "8080:8080"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['0']
              capabilities: [gpu]
  
  api-2:
    build: .
    ports:
      - "8081:8080"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['1']
              capabilities: [gpu]
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api-1
      - api-2
```

---

## Monitoring & Observability

### Prometheus Metrics

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

synthesis_requests = Counter('synthesis_requests_total', 'Total synthesis requests')
synthesis_duration = Histogram('synthesis_duration_seconds', 'Synthesis duration')
active_requests = Gauge('active_requests', 'Currently active requests')
```

### Logging

```python
# logging_config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ddsp-piano.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

```python
# health_check.py
from flask import Flask, jsonify
import psutil
import GPUtil

app = Flask(__name__)

@app.route('/health')
def health():
    gpus = GPUtil.getGPUs()
    return jsonify({
        'status': 'healthy',
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'gpu_available': len(gpus) > 0,
        'gpu_memory': gpus[0].memoryUsed if gpus else 0
    })
```

---

## Security

### API Authentication

```python
# auth.py
from functools import wraps
from flask import request, jsonify
import os

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.environ.get('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function
```

### SSL/TLS Configuration

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name api.ddsp-piano.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Performance Tuning

### GPU Optimization

```python
# Enable mixed precision
import tensorflow as tf
tf.keras.mixed_precision.set_global_policy('mixed_float16')

# Optimize GPU memory
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
```

### Batch Processing

```python
# Process multiple files in parallel
from concurrent.futures import ThreadPoolExecutor

def process_batch(midi_files):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(synthesize, midi_files)
    return list(results)
```

---

## Troubleshooting

### Common Issues

#### GPU Not Detected
```bash
# Check NVIDIA driver
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

#### Out of Memory
```python
# Reduce batch size
# Use model quantization
# Enable memory growth
```

#### Slow Performance
```bash
# Check GPU utilization
nvidia-smi -l 1

# Profile code
python -m cProfile synthesize_midi_file.py input.mid output.wav
```

---

## Support

For deployment assistance:
- **Documentation**: This guide
- **Issues**: GitHub Issues
- **Enterprise Support**: See [SUPPORT.md](SUPPORT.md)
- **Email**: support@ddsp-piano.com (placeholder)

