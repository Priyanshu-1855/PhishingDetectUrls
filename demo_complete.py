"""
Complete Demo: NLP + Computer Vision + OCR
Demonstrates all phishing detection features working together.
"""

import os
import cv2
import numpy as np
from vision.screenshot_utils import save_image

print("\n" + "="*80)
print("COMPLETE PHISHING DETECTION DEMO")
print("NLP (spaCy) + Computer Vision (OpenCV) + OCR (Tesseract)")
print("="*80)

# ============================================================================
# DEMO 1: NLP - Named Entity Recognition
# ============================================================================
print("\n" + "="*80)
print("DEMO 1: NLP - Named Entity Recognition")
print("="*80)

from nlp.ner_analyzer import analyze_text

phishing_email = {
    'subject': "URGENT: Your PayPal Account Has Been Suspended",
    'body': "Dear customer, Your PayPal account has been suspended due to unusual activity. Please send $500 to verify your identity within 24 hours or your account will be permanently closed. Contact our office in Nigeria immediately.",
    'url': "http://paypa1-secure.com/verify"
}

print(f"\nAnalyzing Email:")
print(f"Subject: {phishing_email['subject']}")
print(f"URL: {phishing_email['url']}")

result = analyze_text(
    phishing_email['subject'],
    phishing_email['body'],
    phishing_email['url']
)

print(f"\n🔍 NLP Analysis Results:")
print(f"   Phishing Score: {result['score']}")
print(f"\n   Detected Indicators:")
for indicator in result['indicators']:
    print(f"   ✗ {indicator}")

print(f"\n   Extracted Entities:")
for line in result['entity_summary'].split('\n'):
    if line:
        print(f"   • {line}")

# ============================================================================
# DEMO 2: Computer Vision - Screenshot Analysis
# ============================================================================
print("\n" + "="*80)
print("DEMO 2: Computer Vision - Screenshot Similarity Detection")
print("="*80)

# Create two test screenshots
print("\nCreating test screenshots...")

# Legitimate site simulation
img_legit = np.ones((600, 800, 3), dtype=np.uint8) * 255
cv2.rectangle(img_legit, (0, 0), (800, 80), (50, 100, 200), -1)  # Blue header
cv2.putText(img_legit, "Secure Bank", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
cv2.rectangle(img_legit, (200, 200), (600, 250), (100, 100, 100), 2)
cv2.rectangle(img_legit, (200, 280), (600, 330), (100, 100, 100), 2)
cv2.rectangle(img_legit, (300, 380), (500, 430), (50, 150, 50), -1)

legit_path = "demo_legit_site.png"
save_image(img_legit, legit_path)

# Phishing site simulation (similar but with red warning colors)
img_phish = np.ones((600, 800, 3), dtype=np.uint8) * 255
cv2.rectangle(img_phish, (0, 0), (800, 80), (50, 50, 200), -1)  # Red header
cv2.putText(img_phish, "Secure Bank", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
cv2.rectangle(img_phish, (200, 200), (600, 250), (100, 100, 100), 2)
cv2.rectangle(img_phish, (200, 280), (600, 330), (100, 100, 100), 2)
cv2.rectangle(img_phish, (300, 380), (500, 430), (50, 50, 200), -1)  # Red button

phish_path = "demo_phishing_site.png"
save_image(img_phish, phish_path)

from vision.screenshot_analyzer import ScreenshotAnalyzer

analyzer = ScreenshotAnalyzer(use_ocr=False)  # Disable OCR for this demo
similarity = analyzer.compare_screenshots(legit_path, phish_path)

print(f"\n🔍 Visual Similarity Analysis:")
print(f"   Comparing legitimate vs phishing screenshots...")
print(f"\n   Similarity Metrics:")
for metric, score in similarity.items():
    if metric != 'overall_similarity':
        print(f"   • {metric}: {score:.4f}")
print(f"\n   Overall Similarity: {similarity['overall_similarity']:.4f}")
print(f"   ⚠️  High similarity suggests potential clone/phishing site!")

# ============================================================================
# DEMO 3: OCR - Text Extraction from Screenshots
# ============================================================================
print("\n" + "="*80)
print("DEMO 3: OCR - Text Extraction from Screenshots")
print("="*80)

# Create a phishing page screenshot with text
print("\nCreating phishing page screenshot with text...")

img_ocr = np.ones((500, 700, 3), dtype=np.uint8) * 255
font = cv2.FONT_HERSHEY_SIMPLEX

# Add phishing text
cv2.putText(img_ocr, "URGENT: Account Suspended", (100, 80), font, 1.0, (0, 0, 200), 2)
cv2.putText(img_ocr, "Your PayPal account has been suspended", (80, 150), font, 0.7, (0, 0, 0), 1)
cv2.putText(img_ocr, "Please verify your password immediately", (80, 190), font, 0.7, (0, 0, 0), 1)
cv2.putText(img_ocr, "Username:", (100, 260), font, 0.6, (0, 0, 0), 1)
cv2.rectangle(img_ocr, (250, 240), (600, 275), (100, 100, 100), 2)
cv2.putText(img_ocr, "Password:", (100, 330), font, 0.6, (0, 0, 0), 1)
cv2.rectangle(img_ocr, (250, 310), (600, 345), (100, 100, 100), 2)
cv2.rectangle(img_ocr, (250, 400), (450, 445), (0, 150, 0), -1)
cv2.putText(img_ocr, "LOGIN", (310, 430), font, 0.8, (255, 255, 255), 2)

ocr_path = "demo_phishing_ocr.png"
save_image(img_ocr, ocr_path)

from vision.ocr_analyzer import analyze_screenshot_text

result = analyze_screenshot_text(ocr_path)

print(f"\n🔍 OCR Analysis Results:")
print(f"   Phishing Score: {result['score']}")
print(f"\n   Extracted Text:")
print("   " + "-"*70)
for line in result['text'].split('\n'):
    if line.strip():
        print(f"   {line}")
print("   " + "-"*70)

print(f"\n   Detected Indicators:")
for indicator in result['indicators']:
    print(f"   ✗ {indicator}")

print(f"\n   OCR Features:")
for feature, value in result['features'].items():
    if value > 0:
        print(f"   • {feature}: {value}")

# ============================================================================
# DEMO 4: Combined Analysis - All Features Together
# ============================================================================
print("\n" + "="*80)
print("DEMO 4: COMBINED ANALYSIS - All Features Working Together")
print("="*80)

print("\nAnalyzing phishing screenshot with OCR enabled...")

analyzer_full = ScreenshotAnalyzer(use_ocr=True)
score, indicators = analyzer_full.analyze(ocr_path)

print(f"\n🔍 Complete Analysis (Visual + OCR):")
print(f"   Total Phishing Score: {score}")
print(f"\n   All Detected Indicators:")
for i, indicator in enumerate(indicators, 1):
    print(f"   {i}. {indicator}")

features = analyzer_full.get_features()
print(f"\n   Total Features Extracted: {len(features)}")
print(f"\n   Key Features:")
for feature, value in sorted(features.items(), key=lambda x: x[1], reverse=True)[:10]:
    if value > 0:
        print(f"   • {feature}: {value}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print(f"""
✅ NLP Module (spaCy):
   • Extracted entities: Organizations, Money, Locations
   • Detected brand impersonation (PayPal mismatch)
   • Identified suspicious patterns (money + urgency + foreign location)
   
✅ Computer Vision Module (OpenCV):
   • Compared visual similarity between screenshots
   • Detected excessive warning colors (red)
   • Analyzed layout structure and complexity
   
✅ OCR Module (Tesseract):
   • Extracted text from screenshot images
   • Detected urgency keywords ("URGENT", "immediately")
   • Identified sensitive info requests ("password")
   • Recognized login form elements
   
✅ Combined System:
   • Total Features: 53 (24 base + 13 NER + 8 CV + 8 OCR)
   • Multi-layered phishing detection
   • Ready for ML model training
""")

# Cleanup
for path in [legit_path, phish_path, ocr_path]:
    if os.path.exists(path):
        os.remove(path)

print("="*80)
print("Demo completed! All test images have been cleaned up.")
print("="*80)
