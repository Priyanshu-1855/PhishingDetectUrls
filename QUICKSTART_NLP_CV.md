# Quick Start: NLP and CV Features

## Installation

```bash
# Install dependencies
pip install spacy opencv-python Pillow imagehash scikit-image

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Test the Features

```bash
# Test NER analyzer
python test_ner.py

# Test CV analyzer
python test_cv.py
```

## Use in Your Code

### NER Analysis
```python
from nlp.ner_analyzer import analyze_text

result = analyze_text(
    subject="Urgent: PayPal Account",
    body="Verify your account immediately",
    url="http://paypa1-secure.com"
)
print(result['score'], result['indicators'])
```

### Screenshot Analysis
```python
from vision.screenshot_analyzer import analyze_screenshot

result = analyze_screenshot("suspicious_site.png")
print(result['score'], result['indicators'])
```

### Train ML Model
```python
from ml_trainer import MLTrainer

# With NER features
trainer = MLTrainer(use_ner=True, use_cv=False)
trainer.train_all('training_data.json')
```

## What You Get

- **13 new NER features**: Brand impersonation, entity analysis, money detection
- **8 new CV features**: Visual similarity, color analysis, layout detection
- **Enhanced accuracy**: Expected 3-7% improvement in phishing detection

See [`NLP_CV_FEATURES.md`](file:///c:/Users/priya/OneDrive/Desktop/PhishingModel/NLP_CV_FEATURES.md) for complete documentation.
