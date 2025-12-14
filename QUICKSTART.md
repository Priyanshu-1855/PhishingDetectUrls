# Quick Start Guide (No Docker Required)

## Running the Phishing Detection System

Since Docker is not installed, you can run the system directly with Python. Here's how:

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd c:\Users\priya\OneDrive\Desktop\PhishingModel

# Install required packages
pip install Flask Flask-CORS scikit-learn numpy joblib requests
```

### Step 2: Start the API Server

```bash
# Start the Flask API server
python api/app.py
```

The API will start on `http://localhost:5000`

### Step 3: Test the API

Open a new terminal and test:

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Or open in browser:
# http://localhost:5000/api/v1/health
```

### Step 4: Use the System

#### Option A: Command Line Detection

```bash
# Test with a phishing example
python main.py --url "http://paypal-verify.tk" --subject "Urgent" --body "Click here now" --pretty
```

#### Option B: Use the Browser Extension

1. Open Chrome: `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select: `c:\Users\priya\OneDrive\Desktop\PhishingModel\extension`
5. Extension installed!

#### Option C: Open the Website Demo

```bash
# Open in browser:
c:\Users\priya\OneDrive\Desktop\PhishingModel\integration\website_example.html
```

### Step 5: Train ML Models (Optional)

```bash
# Generate training data
python dataset_generator.py --phishing 500 --legitimate 500

# Train models (takes 2-3 minutes)
python ml_trainer.py --data training_data.json
```

---

## What You Can Do Now

1. **Test Detection**: Run `python main.py --test-samples test_samples.json`
2. **Start API**: Run `python api/app.py` for REST API
3. **Install Extension**: Load the Chrome extension for real-time protection
4. **Try Website Demo**: Open `integration/website_example.html` in browser

---

## Installing Docker (Optional)

If you want to use Docker later:

1. Download Docker Desktop for Windows: https://www.docker.com/products/docker-desktop
2. Install and restart your computer
3. Then run: `docker-compose up -d`

---

## Need Help?

- API not starting? Make sure port 5000 is free
- Import errors? Run `pip install -r requirements.txt`
- Extension not working? Check that API is running on localhost:5000
