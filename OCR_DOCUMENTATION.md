# OCR Module for Text Extraction

## Overview
The OCR (Optical Character Recognition) module extracts text from website screenshots using Tesseract OCR, enabling detection of phishing indicators in visual content.

## Installation

### 1. Install Python Package
```bash
pip install pytesseract
```

### 2. Install Tesseract OCR Engine

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location: `C:\Program Files\Tesseract-OCR\`
3. Add to PATH or specify path in code

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

## Features

### Text Extraction
- Extracts all visible text from screenshots
- Provides confidence scores for each detected word
- Preprocesses images for optimal OCR accuracy

### Phishing Detection Capabilities

1. **Urgency Keywords**
   - Detects: "urgent", "immediate", "act now", "suspended", "locked"
   - Flags time-based urgency: "within 24 hours"

2. **Sensitive Information Requests**
   - Detects requests for: password, SSN, credit card, CVV, PIN
   - Identifies account number and routing number requests

3. **Spelling Errors**
   - Common phishing misspellings: "verfiy", "confrim", "acount"
   - Indicates low-quality phishing attempts

4. **URL Extraction**
   - Extracts URLs from text
   - Detects suspicious patterns: IP addresses, URL shorteners
   - Flags domains with suspicious keywords

5. **Brand Mentions**
   - Identifies brand impersonation attempts
   - Detects multiple brand mentions (suspicious)

6. **Login Form Detection**
   - Identifies form fields: username, password, email
   - Detects login page elements

## Usage

### Basic Text Extraction
```python
from vision.ocr_analyzer import OCRAnalyzer

analyzer = OCRAnalyzer()
text = analyzer.extract_text("screenshot.png")
print(text)
```

### Phishing Analysis
```python
from vision.ocr_analyzer import analyze_screenshot_text

result = analyze_screenshot_text("suspicious_site.png")

print(f"Score: {result['score']}")
print(f"Indicators: {result['indicators']}")
print(f"Extracted Text: {result['text']}")
```

### With Confidence Scores
```python
analyzer = OCRAnalyzer()
results = analyzer.extract_text_with_confidence("screenshot.png")

for item in results:
    print(f"{item['text']} (confidence: {item['confidence']}%)")
```

### Visualize Detected Text
```python
analyzer = OCRAnalyzer()
analyzer.visualize_text_regions(
    "input.png",
    "output_with_boxes.png"
)
```

### Integrated with Screenshot Analyzer
```python
from vision.screenshot_analyzer import ScreenshotAnalyzer

# OCR is enabled by default
analyzer = ScreenshotAnalyzer(use_ocr=True)
score, indicators = analyzer.analyze("screenshot.png")

# Features now include OCR features
features = analyzer.get_features()
print(features['ocr_urgency_detected'])
print(features['ocr_text_length'])
```

## OCR Features for ML

The OCR analyzer provides 8 features for machine learning:

1. `ocr_urgency_detected` (binary) - Urgency keywords found
2. `ocr_sensitive_info_request` (binary) - Requests sensitive data
3. `ocr_spelling_errors` (binary) - Contains misspellings
4. `ocr_urls_found` (binary) - URLs detected in text
5. `ocr_url_count` (normalized) - Number of URLs
6. `ocr_brand_count` (normalized) - Number of brands mentioned
7. `ocr_login_form_detected` (binary) - Login form elements
8. `ocr_text_length` (normalized) - Amount of text extracted

## Testing

```bash
python test_ocr.py
```

Tests include:
- Text extraction accuracy
- Phishing indicator detection
- Confidence scoring
- URL detection
- Text region visualization

## Performance

- **Speed**: 200-500ms per screenshot (depends on text amount)
- **Accuracy**: 85-95% for clear text, 60-80% for stylized fonts
- **Memory**: ~100MB (Tesseract loaded)

## Best Practices

1. **Image Quality**: Higher resolution = better OCR accuracy
2. **Preprocessing**: Enabled by default for better results
3. **Language**: Currently English only (can be extended)
4. **Confidence Threshold**: Filter results with confidence > 30%

## Troubleshooting

### "Tesseract not found"
- **Windows**: Set path explicitly:
  ```python
  analyzer = OCRAnalyzer(tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
  ```
- **Linux/Mac**: Ensure tesseract is in PATH

### Low Accuracy
- Increase image resolution
- Use clearer screenshots
- Enable preprocessing (default)

### Slow Performance
- Reduce image size before OCR
- Process only specific regions
- Use batch processing for multiple images

## Examples

### Example 1: Phishing Login Page
```
Input: Screenshot of fake PayPal login
Output:
  Score: 60
  Indicators:
    - OCR detected urgency keywords: urgent, immediate
    - OCR detected sensitive info requests: password
    - OCR detected login form elements
  Text: "URGENT: Your PayPal account has been suspended..."
```

### Example 2: Legitimate Site
```
Input: Screenshot of real Amazon page
Output:
  Score: 5
  Indicators:
    - OCR detected login form elements
  Text: "Welcome to Amazon. Sign in to your account..."
```

## Integration with ML Pipeline

OCR features are automatically included when using the screenshot analyzer:

```python
from ml_trainer import MLTrainer

# CV features now include OCR
trainer = MLTrainer(use_ner=True, use_cv=True)
trainer.train_all('training_data.json')

# Total features: 24 (base) + 13 (NER) + 8 (CV) + 8 (OCR) = 53
```

## Future Enhancements

- Multi-language support
- Handwriting recognition
- Logo/image text extraction
- Layout analysis
- Table extraction
