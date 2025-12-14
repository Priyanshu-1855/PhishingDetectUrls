# Phishing Detection Model - Production Deployment Guide

## Overview

This guide covers deploying the phishing detection system to production, including Docker deployment, API configuration, and website integration.

---

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- API keys for threat intelligence services (optional but recommended):
  - VirusTotal API key
  - Google Safe Browsing API key

---

## Quick Start with Docker

### 1. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### 2. Build and Run

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

### 3. Test the API

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Generate API key
curl -X POST http://localhost:5000/api/v1/generate-key \
  -H "Content-Type: application/json" \
  -d '{"name": "My App", "rate_limit": 100}'

# Test detection
curl -X POST http://localhost:5000/api/v1/detect \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-key-12345" \
  -d '{"url": "http://example.com", "subject": "Test", "body": "Test email"}'
```

---

## Manual Deployment (Without Docker)

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Train ML Models (Optional)

```bash
# Generate training data
python dataset_generator.py --phishing 500 --legitimate 500

# Train models
python ml_trainer.py --data training_data.json
```

### 3. Start the API Server

```bash
# Development mode
python api/app.py

# Production mode with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 api.app:app
```

---

## Website Integration

### Option 1: JavaScript Widget

Add the widget to your website:

```html
<script src="https://your-domain.com/widget.js"></script>
<script>
  const detector = new PhishingDetectorWidget({
    apiUrl: 'https://your-api-domain.com',
    apiKey: 'your-api-key'
  });
  
  // Check a URL
  detector.checkUrl('https://example.com')
    .then(result => {
      console.log('Classification:', result.classification);
      console.log('Risk Score:', result.risk_score);
    });
</script>
```

### Option 2: Direct API Integration

```javascript
async function checkPhishing(url, subject, body) {
  const response = await fetch('https://your-api-domain.com/api/v1/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key'
    },
    body: JSON.stringify({ url, subject, body })
  });
  
  return await response.json();
}
```

---

## Browser Extension Installation

### Development Mode

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `extension/` folder
5. The extension is now installed!

### Production Distribution

1. Create a ZIP file of the `extension/` folder
2. Upload to Chrome Web Store Developer Dashboard
3. Follow Chrome's review process
4. Publish to users

---

## API Endpoints

### POST /api/v1/detect

Detect phishing in URLs and emails.

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: your-api-key`

**Request Body:**
```json
{
  "url": "https://example.com",
  "subject": "Email subject",
  "body": "Email body text"
}
```

**Response:**
```json
{
  "classification": "Phishing|Suspicious|Legitimate",
  "risk_score": 85,
  "reasons": ["Reason 1", "Reason 2"],
  "confidence": "High",
  "ml_prediction": {...},
  "threat_intelligence": {...}
}
```

### GET /api/v1/health

Check API health status.

### GET /api/v1/stats

Get detection statistics (requires API key).

### POST /api/v1/generate-key

Generate a new API key.

---

## Configuration

### API Keys

Set environment variables:

```bash
export VIRUSTOTAL_API_KEY="your_key_here"
export GOOGLE_SAFE_BROWSING_API_KEY="your_key_here"
```

Or add to `.env` file.

### Rate Limiting

Default: 100 requests/hour per API key

Modify in `api/auth.py`:
```python
api_key_manager.generate_api_key(name="My App", rate_limit=1000)
```

---

## Scaling Considerations

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      replicas: 3
```

### Load Balancing

Use nginx as reverse proxy:

```nginx
upstream phishing_api {
    server api1:5000;
    server api2:5000;
    server api3:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://phishing_api;
    }
}
```

### Caching

Redis is included in Docker Compose for caching threat intelligence results.

---

## Monitoring

### Logs

```bash
# View API logs
docker-compose logs -f api

# Local logs
tail -f logs/phishing_detector.log
```

### Metrics

Access statistics endpoint:
```bash
curl -H "X-API-Key: your-key" http://localhost:5000/api/v1/stats
```

---

## Security Best Practices

1. **Always use HTTPS** in production
2. **Rotate API keys** regularly
3. **Set up rate limiting** to prevent abuse
4. **Monitor logs** for suspicious activity
5. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`
6. **Use environment variables** for sensitive data (never commit .env)

---

## Troubleshooting

### API not responding

```bash
# Check if container is running
docker-compose ps

# Restart services
docker-compose restart

# Check logs for errors
docker-compose logs api
```

### ML models not loading

```bash
# Train models
python ml_trainer.py

# Verify models exist
ls -la models/
```

### Threat intelligence not working

- Verify API keys are set correctly
- Check API quotas (VirusTotal free tier: 4 requests/minute)
- System will fall back to mock data if APIs unavailable

---

## Support

For issues or questions:
1. Check logs for error messages
2. Verify all dependencies are installed
3. Ensure API keys are configured correctly
4. Test with the demo API key first

---

## Performance Optimization

- **Enable caching**: Redis caches threat intelligence for 1 hour
- **Use ML models**: Improves accuracy by 15-20%
- **Batch requests**: Process multiple URLs together
- **CDN for widget**: Serve widget.js from CDN for faster loading

---

## Next Steps

1. Train ML models with your own data for better accuracy
2. Set up monitoring and alerting
3. Configure backup and disaster recovery
4. Implement A/B testing for model improvements
5. Add custom phishing patterns for your industry
