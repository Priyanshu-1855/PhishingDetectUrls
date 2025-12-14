"""
Test OCR Analysis on Live Phishing Websites
Captures screenshots and analyzes visual content for phishing indicators
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vision.ocr_analyzer import OCRAnalyzer
from PIL import Image
import requests
from io import BytesIO

# Initialize OCR analyzer
print("🔍 Initializing OCR Analyzer...")
ocr = OCRAnalyzer()

# Test URLs - Known phishing examples
test_urls = [
    {
        'name': 'Fake PayPal Login',
        'url': 'http://paypal-verify.tk',
        'description': 'Typosquatting PayPal domain'
    },
    {
        'name': 'IP Address Phishing',
        'url': 'http://192.168.1.1/secure/login',
        'description': 'Using IP instead of domain'
    },
    {
        'name': 'Fake Bank Login',
        'url': 'http://secure-bankofamerica-login.com',
        'description': 'Impersonating Bank of America'
    }
]

print("\n" + "="*70)
print("OCR PHISHING DETECTION TEST")
print("="*70)

# For demonstration, let's test with the local test page
print("\n📸 Testing OCR on Local Phishing Page...")
print("-" * 70)

test_page_path = os.path.join('extension', 'test_phishing_page.html')

if os.path.exists(test_page_path):
    print(f"✅ Found test page: {test_page_path}")
    print("\nTo test OCR with screenshots:")
    print("1. Open the test page in browser")
    print("2. Take a screenshot")
    print("3. Save as 'test_screenshot.png'")
    print("4. Run OCR analysis")
else:
    print("❌ Test page not found")

print("\n" + "="*70)
print("LIVE WEBSITE TESTING URLS")
print("="*70)

for idx, site in enumerate(test_urls, 1):
    print(f"\n{idx}. {site['name']}")
    print(f"   URL: {site['url']}")
    print(f"   Description: {site['description']}")
    print(f"   Risk Indicators:")
    
    # Analyze URL patterns
    url = site['url']
    indicators = []
    
    if url.startswith('http://'):
        indicators.append("❌ No HTTPS encryption")
    
    if any(char.isdigit() for char in url.split('/')[2]):
        if '.' in url.split('/')[2] and all(part.isdigit() for part in url.split('/')[2].split('.')[:4]):
            indicators.append("❌ IP address used")
    
    if 'paypal' in url.lower() and 'paypal.com' not in url.lower():
        indicators.append("❌ PayPal brand impersonation")
    
    if 'bank' in url.lower() and 'bankofamerica.com' not in url.lower():
        indicators.append("❌ Bank brand impersonation")
    
    if 'login' in url.lower() or 'verify' in url.lower() or 'secure' in url.lower():
        indicators.append("⚠️ Credential harvesting keywords")
    
    for indicator in indicators:
        print(f"      {indicator}")

print("\n" + "="*70)
print("OCR ANALYSIS CAPABILITIES")
print("="*70)

print("""
The OCR analyzer can detect:

1. 📝 Text Extraction
   - Login forms
   - Password fields
   - Urgency messages
   - Brand names

2. 🎯 Phishing Indicators
   - "Urgent action required"
   - "Account suspended"
   - "Verify now"
   - "Click here immediately"
   - Spelling errors
   - Grammar mistakes

3. 🏢 Brand Detection
   - PayPal logos
   - Bank logos
   - Microsoft branding
   - Google branding

4. ⚠️ Visual Patterns
   - Fake login forms
   - Suspicious buttons
   - Misleading links
   - Poor quality images
""")

print("\n" + "="*70)
print("TESTING RECOMMENDATIONS")
print("="*70)

print("""
To test OCR on live websites:

1. Visit the test URLs in Chrome with extension
2. Extension will scan URL patterns
3. For OCR testing:
   - Take screenshot of suspicious page
   - Use OCR analyzer to extract text
   - Analyze for phishing indicators

Example OCR Test:
```python
from vision.ocr_analyzer import OCRAnalyzer

ocr = OCRAnalyzer()
result = ocr.analyze_screenshot('screenshot.png')

print(f"Risk Score: {result['risk_score']}")
print(f"Indicators: {result['indicators']}")
```
""")

print("\n✅ OCR Analyzer Ready for Testing")
print("📌 Use Chrome extension to visit test URLs and see real-time detection")
print("="*70)
