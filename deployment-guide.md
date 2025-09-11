# Google Cloud Run Deployment Guide

## Quick Deployment Options

### Option 1: Using gcloud CLI (Recommended)

1. **Set your project ID:**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy from source:**
   ```bash
   gcloud run deploy carrier-api --source . --platform managed --region us-central1 --allow-unauthenticated
   ```

### Option 2: Using Cloud Build

1. **Submit build:**
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```

### Option 3: Manual Docker Build

1. **Build the image:**
   ```bash
   docker build -t gcr.io/YOUR_PROJECT_ID/carrier-api .
   ```

2. **Push to registry:**
   ```bash
   docker push gcr.io/YOUR_PROJECT_ID/carrier-api
   ```

3. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy carrier-api --image gcr.io/YOUR_PROJECT_ID/carrier-api --platform managed --region us-central1 --allow-unauthenticated
   ```

## Required Files for Deployment

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `cloudbuild.yaml` - Build configuration (optional)

## Environment Variables

Set these in Cloud Run console or via gcloud:

- `FMCSA_API_KEY` - Your FMCSA API key
- `PORT` - Port number (default: 5000)

## Testing After Deployment

```bash
curl -X POST https://your-service-url/api/verify-carrier \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_verify_1234567890abcdef" \
  -d '{"mc_number": "MC-441100", "use_fmcsa": false}'
```