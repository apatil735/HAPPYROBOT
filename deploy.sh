#!/bin/bash
# Manual deployment script for Google Cloud Run

echo "🚀 Deploying Carrier API to Google Cloud Run..."

# Set your project ID (you'll need to replace this with your actual project ID)
PROJECT_ID="your-project-id-here"
SERVICE_NAME="carrier-api"
REGION="us-central1"

echo "📦 Building and deploying..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --project=$PROJECT_ID \
  --memory=512Mi \
  --cpu=1 \
  --max-instances=10 \
  --timeout=300

echo "✅ Deployment complete!"
echo "🌐 Your API will be available at: https://$SERVICE_NAME-$PROJECT_ID.$REGION.run.app"
