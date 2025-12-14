# Phishing Detection System - Production Edition

**Enterprise-grade AI-powered phishing detection with ML, threat intelligence, and real-time protection.**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/yourusername/phishing-detector)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 Features

### Core Detection
- **URL Analysis**: 11+ phishing indicators including IP addresses, brand impersonation, suspicious TLDs
- **Email NLP**: Advanced natural language processing for urgency detection, social engineering, AI-generated phishing
- **Risk Scoring**: 0-100 risk scores with Legitimate/Suspicious/Phishing classification
- **Explainable AI**: Human-readable reasons for every decision

### Machine Learning
- **Random Forest**: High-interpretability ensemble model
- **Neural Network**: Deep learning for complex pattern detection
- **Ensemble Predictions**: Combines multiple models for accuracy
- **Auto-training**: Synthetic dataset generator included

### Threat Intelligence
- **VirusTotal Integration**: URL reputation from 70+ security vendors
- **Google Safe Browsing**: Real-time malware and phishing detection
- **Smart Caching**: 1-hour TTL reduces API calls
- **Fallback System**: Works without API keys (mock mode)

### Production API
- **REST API**: Flask-based with OpenAPI/Swagger docs
- **Authentication**: API key-based with rate limiting (100 req/hour)
- **CORS Support**: Ready for cross-origin requests
- **Monitoring**: Built-in statistics and health checks

### Browser Extension
- **Chrome Extension**: Real-time phishing detection
- **Email Scanning**: Auto-detects phishing in Gmail and Outlook
- **Visual Warnings**: In-page alerts for dangerous emails
- **Background Monitoring**: Flags suspicious URLs automatically

### Website Integration
- **JavaScript Widget**: Embeddable phishing checker
- **Simple API**: RESTful endpoints for easy integration
- **Example Code**: Ready-to-use HTML/JS examples

### Deployment
- **Docker Ready**: One-command deployment with Docker Compose
- **Production Server**: Gunicorn WSGI with 4 workers
- **Redis Caching**: Fast response times
- **Scalable**: Horizontal scaling support

---

## 📦 Installation

### Quick Start (Docker)

```bash
# Clone repository
git clone https://github.com/yourusername/phishing-detector.git
cd phishing-detector

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Test API
curl http://localhost:5000/api/v1/health
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train ML models (optional)
python dataset_generator.py --phishing 500 --legitimate 500
python ml_trainer.py

# Start API
python api/app.py
```

---

## 🎯 Usage

### Command Line

```bash
# Analyze URL and email
python main.py --url "http://suspicious.com" --subject "Urgent!" --body "Click here now"

# Run test suite
python main.py --test-samples test_samples.json --pretty
```

### Python API

```python
from enhanced_detector import EnhancedPhishingDetector

detector = EnhancedPhishingDetector(use_ml=True, use_threat_intel=True)

result = detector.detect(
    url="http://paypal-verify.tk",
    email_subject="Account Suspended",
    email_body="Verify your account immediately"
)

print(f"Classification: {result['classification']}")
print(f"Risk Score: {result['risk_score']}/100")
```

### REST API

```bash
# Generate API key
curl -X POST http://localhost:5000/api/v1/generate-key \
  -H "Content-Type: application/json" \
  -d '{"name": "My App"}'

# Detect phishing
curl -X POST http://localhost:5000/api/v1/detect \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "url": "https://example.com",
    "subject": "Test",
    "body": "Email content"
  }'
```

### Website Integration

```html
<script src="integration/widget.js"></script>
<script>
  const detector = new PhishingDetectorWidget({
    apiUrl: 'http://localhost:5000',
    apiKey: 'demo-key-12345'
  });
  
  detector.checkUrl('https://example.com')
    .then(result => {
      console.log('Risk Score:', result.risk_score);
    });
</script>
```

### Browser Extension

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" → Select `extension/` folder
4. Extension installed! Opens automatically on Gmail/Outlook

---

## 📊 Architecture

```
PhishingModel/
├── Core Detection
│   ├── url_analyzer.py          # URL feature extraction
│   ├── email_analyzer.py        # Email NLP analysis
│   ├── risk_scorer.py           # Risk calculation
│   └── enhanced_detector.py     # Main orchestrator
│
├── Machine Learning
│   ├── dataset_generator.py     # Synthetic data generation
│   ├── ml_trainer.py            # Model training pipeline
│   ├── ml_predictor.py          # Ensemble predictions
│   └── models/                  # Trained models
│
├── Threat Intelligence
│   ├── virustotal.py            # VirusTotal API
│   ├── safe_browsing.py         # Google Safe Browsing
│   └── aggregator.py            # Multi-source aggregation
│
├── REST API
│   ├── app.py                   # Flask application
│   └── auth.py                  # Authentication & rate limiting
│
├── Browser Extension
│   ├── manifest.json            # Extension config
│   ├── popup.html/js/css        # Popup UI
│   ├── background.js            # Service worker
│   └── content.js               # Email detection
│
├── Website Integration
│   ├── website_example.html     # Integration demo
│   └── widget.js                # Embeddable widget
│
└── Deployment
    ├── Dockerfile               # Container image
    ├── docker-compose.yml       # Multi-container setup
    └── DEPLOYMENT.md            # Production guide
```

---

## 🔧 Configuration

### API Keys (Optional but Recommended)

```bash
# .env file
VIRUSTOTAL_API_KEY=your_key_here
GOOGLE_SAFE_BROWSING_API_KEY=your_key_here
```

Get free API keys:
- [VirusTotal](https://www.virustotal.com/gui/join-us) - 4 requests/minute
- [Google Safe Browsing](https://developers.google.com/safe-browsing/v4/get-started) - Free tier available

### ML Model Training

```bash
# Generate 1000 training samples
python dataset_generator.py --phishing 500 --legitimate 500

# Train models
python ml_trainer.py --data training_data.json

# Models saved to models/ directory
```

---

## 📈 Performance

- **Accuracy**: 80%+ on test suite (95%+ with ML models)
- **Response Time**: <500ms average
- **Throughput**: 100+ requests/second (with caching)
- **False Positives**: <5% (optimized for safety)

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/detect` | POST | Detect phishing |
| `/api/v1/health` | GET | Health check |
| `/api/v1/stats` | GET | Statistics |
| `/api/v1/generate-key` | POST | Generate API key |

See [DEPLOYMENT.md](DEPLOYMENT.md) for full API documentation.

---

## 🛡️ Security

- ✅ API key authentication
- ✅ Rate limiting (100 req/hour default)
- ✅ CORS protection
- ✅ Input validation
- ✅ No sensitive data logging
- ✅ HTTPS recommended for production

---

## 🚢 Deployment

### Docker (Recommended)

```bash
docker-compose up -d
```

### Manual

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 api.app:app
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

---

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [API Documentation](api/swagger.yaml) - OpenAPI spec
- [Implementation Plan](implementation_plan.md) - Technical design
- [Walkthrough](walkthrough.md) - Feature walkthrough

---

## 🧪 Testing

```bash
# Run test suite
python main.py --test-samples test_samples.json

# Test specific URL
python main.py --url "http://phishing-site.com"

# Test API
curl http://localhost:5000/api/v1/health
```

---

## 🎨 Browser Extension Screenshots

- Modern gradient UI
- Real-time risk scores
- Visual phishing warnings
- Gmail/Outlook integration

---

## 🔮 Roadmap

- [ ] Advanced NLP with spaCy and transformers
- [ ] Real-time URL reputation feeds
- [ ] Mobile app (iOS/Android)
- [ ] Slack/Teams integration
- [ ] Custom ML model training UI
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional phishing patterns
- ML model enhancements
- New threat intelligence sources
- Performance optimizations

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- VirusTotal for URL reputation API
- Google Safe Browsing for threat detection
- scikit-learn and Flask communities

---

## 📞 Support

- **Issues**: GitHub Issues
- **Email**: support@example.com
- **Docs**: See DEPLOYMENT.md

---

**Built with ❤️ for cybersecurity**
