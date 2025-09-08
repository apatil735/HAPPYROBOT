# Carrier Sales Automation API - Deployment Guide

This guide covers deploying the Flask API to various cloud platforms for production use.

## 🚀 Quick Start (Local Testing)

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Local Setup
```bash
# Clone or download the project
cd HappyRobot

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The API will be available at `http://localhost:5000`

### Test the API
```bash
# Health check
curl http://localhost:5000/api/health

# Search loads
curl -X POST http://localhost:5000/api/search-loads \
  -H "Content-Type: application/json" \
  -d '{"equipment_type": "Flatbed", "min_rate": 1000}'
```

## 🐳 Docker Deployment

### Build and Run Locally
```bash
# Build the Docker image
docker build -t carrier-api .

# Run the container
docker run -p 5000:5000 carrier-api
```

### Docker Compose (Recommended)
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  carrier-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PORT=5000
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## ☁️ Cloud Platform Deployments

### 1. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Git repository

#### Steps
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-carrier-api

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git add .
git commit -m "Deploy carrier API"
git push heroku main

# Open the app
heroku open
```

#### Heroku-specific files needed:
Create `Procfile`:
```
web: gunicorn app:app
```

### 2. Google Cloud Run

#### Prerequisites
- Google Cloud SDK installed
- Docker installed

#### Steps
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/carrier-api

# Deploy to Cloud Run
gcloud run deploy carrier-api \
  --image gcr.io/YOUR_PROJECT_ID/carrier-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000
```

### 3. AWS Elastic Beanstalk

#### Prerequisites
- AWS CLI configured
- EB CLI installed

#### Steps
```bash
# Initialize EB application
eb init

# Create environment
eb create production

# Deploy
eb deploy

# Open the application
eb open
```

### 4. Railway

#### Prerequisites
- Railway account
- Railway CLI (optional)

#### Steps
1. Connect your GitHub repository to Railway
2. Railway will auto-detect the Flask app
3. Set environment variables in Railway dashboard
4. Deploy automatically on git push

## 🔧 Environment Variables

Set these in your cloud platform:

```bash
FLASK_ENV=production
PORT=5000
```

## 📊 Monitoring and Health Checks

### Health Check Endpoint
```
GET /api/health
```

### Statistics Endpoint
```
GET /api/stats
```

### Example Monitoring Setup
```bash
# Check API health
curl https://your-api-url.com/api/health

# Get system stats
curl https://your-api-url.com/api/stats
```

## 🔒 Security Considerations

### Production Checklist
- [ ] Use HTTPS (most cloud platforms provide this)
- [ ] Set up proper CORS policies
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Use environment variables for secrets
- [ ] Set up logging and monitoring
- [ ] Regular security updates

### CORS Configuration
The API currently allows all origins. For production:
```python
CORS(app, origins=["https://your-frontend-domain.com"])
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use a load balancer
- Implement session storage (Redis)
- Use a proper database (PostgreSQL/MongoDB)

### Database Migration
Replace in-memory storage with:
```python
# Example with SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
```

## 🧪 Testing

### API Testing Script
Create `test_api.py`:
```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    print("Health Check:", response.json())

def test_search_loads():
    data = {"equipment_type": "Flatbed", "min_rate": 1000}
    response = requests.post(f"{BASE_URL}/api/search-loads", json=data)
    print("Search Loads:", response.json())

if __name__ == "__main__":
    test_health()
    test_search_loads()
```

Run tests:
```bash
python test_api.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process
   kill -9 PID
   ```

2. **Docker build fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   ```

3. **CORS errors**
   - Check CORS configuration
   - Verify frontend URL is allowed

4. **Database connection issues**
   - Check database credentials
   - Verify network connectivity

### Logs
```bash
# Docker logs
docker logs container_name

# Heroku logs
heroku logs --tail

# Google Cloud logs
gcloud logging read "resource.type=cloud_run_revision"
```

## 📞 Support

For issues with this API:
1. Check the health endpoint
2. Review logs
3. Verify environment variables
4. Test locally first

## 🔄 Updates and Maintenance

### Updating the API
1. Make changes to code
2. Test locally
3. Commit to git
4. Deploy to cloud platform
5. Monitor health endpoints

### Database Migrations
When moving from in-memory to persistent storage:
1. Export current data
2. Set up new database
3. Import data
4. Update connection strings
5. Test thoroughly

