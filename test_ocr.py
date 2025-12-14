"""
Test script for OCR Analyzer
Demonstrates text extraction from screenshots using Tesseract OCR.
"""

import os
import cv2
import numpy as np
from vision.screenshot_utils import save_image

try:
    from vision.ocr_analyzer import OCRAnalyzer, analyze_screenshot_text
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("OCR not available. Install with: pip install pytesseract")
    print("Also install Tesseract OCR: https://github.com/tesseract-ocr/tesseract")


def create_test_image_with_text():
    """Create a test image with text for OCR testing."""
    test_dir = "test_screenshots"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a white background
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Add some text (simulating a phishing page)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Title
    cv2.putText(img, "URGENT: Account Suspended", (50, 50), 
                font, 0.8, (0, 0, 200), 2)
    
    # Body text
    cv2.putText(img, "Your PayPal account has been", (50, 120), 
                font, 0.6, (0, 0, 0), 1)
    cv2.putText(img, "suspended due to unusual activity.", (50, 160), 
                font, 0.6, (0, 0, 0), 1)
    
    # Call to action
    cv2.putText(img, "Verify your account immediately", (50, 220), 
                font, 0.7, (200, 0, 0), 2)
    
    # Form fields
    cv2.putText(img, "Username:", (50, 280), font, 0.5, (0, 0, 0), 1)
    cv2.rectangle(img, (150, 260), (500, 290), (100, 100, 100), 2)
    
    cv2.putText(img, "Password:", (50, 330), font, 0.5, (0, 0, 0), 1)
    cv2.rectangle(img, (150, 310), (500, 340), (100, 100, 100), 2)
    
    # Button
    cv2.rectangle(img, (200, 360), (400, 390), (0, 150, 0), -1)
    cv2.putText(img, "LOGIN", (270, 382), font, 0.6, (255, 255, 255), 2)
    
    path = os.path.join(test_dir, "phishing_with_text.png")
    save_image(img, path)
    
    return path


def test_text_extraction():
    """Test basic text extraction."""
    if not OCR_AVAILABLE:
        print("Skipping OCR tests - pytesseract not installed")
        return
    
    print("=" * 70)
    print("TEST 1: Text Extraction")
    print("=" * 70)
    
    img_path = create_test_image_with_text()
    
    try:
        analyzer = OCRAnalyzer()
        text = analyzer.extract_text(img_path)
        
        print(f"\nExtracted Text:")
        print("-" * 70)
        print(text)
        print("-" * 70)
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Tesseract OCR is installed:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Linux: sudo apt-get install tesseract-ocr")
        print("  Mac: brew install tesseract")
        print()


def test_phishing_detection():
    """Test phishing indicator detection in extracted text."""
    if not OCR_AVAILABLE:
        return
    
    print("=" * 70)
    print("TEST 2: Phishing Detection from OCR")
    print("=" * 70)
    
    img_path = create_test_image_with_text()
    
    try:
        result = analyze_screenshot_text(img_path)
        
        print(f"\nPhishing Score: {result['score']}")
        print(f"\nIndicators:")
        if result['indicators']:
            for indicator in result['indicators']:
                print(f"  - {indicator}")
        else:
            print("  No suspicious indicators found")
        
        print(f"\nFeatures:")
        for feature, value in result['features'].items():
            print(f"  {feature}: {value}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


def test_text_with_confidence():
    """Test text extraction with confidence scores."""
    if not OCR_AVAILABLE:
        return
    
    print("=" * 70)
    print("TEST 3: Text Extraction with Confidence")
    print("=" * 70)
    
    img_path = create_test_image_with_text()
    
    try:
        analyzer = OCRAnalyzer()
        results = analyzer.extract_text_with_confidence(img_path)
        
        print(f"\nDetected {len(results)} text regions:")
        print("-" * 70)
        
        # Show top 10 most confident detections
        sorted_results = sorted(results, key=lambda x: x['confidence'], reverse=True)
        for i, item in enumerate(sorted_results[:10], 1):
            if item['text'].strip():
                print(f"{i}. '{item['text']}' (confidence: {item['confidence']}%)")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


def test_url_detection():
    """Test URL detection in OCR text."""
    if not OCR_AVAILABLE:
        return
    
    print("=" * 70)
    print("TEST 4: URL Detection in OCR")
    print("=" * 70)
    
    # Create image with URL
    test_dir = "test_screenshots"
    img = np.ones((200, 600, 3), dtype=np.uint8) * 255
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "Visit: http://192.168.1.1/paypal", (50, 100), 
                font, 0.6, (0, 0, 0), 1)
    
    path = os.path.join(test_dir, "url_test.png")
    save_image(img, path)
    
    try:
        result = analyze_screenshot_text(path)
        
        print(f"\nPhishing Score: {result['score']}")
        print(f"\nIndicators:")
        for indicator in result['indicators']:
            print(f"  - {indicator}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


def test_visualize_regions():
    """Test visualization of detected text regions."""
    if not OCR_AVAILABLE:
        return
    
    print("=" * 70)
    print("TEST 5: Visualize Text Regions")
    print("=" * 70)
    
    img_path = create_test_image_with_text()
    output_path = "test_screenshots/ocr_visualization.png"
    
    try:
        analyzer = OCRAnalyzer()
        analyzer.visualize_text_regions(img_path, output_path)
        
        print(f"\nVisualization saved to: {output_path}")
        print("Green boxes show detected text regions with confidence scores")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("OCR ANALYZER TEST SUITE")
    print("=" * 70 + "\n")
    
    if not OCR_AVAILABLE:
        print("ERROR: pytesseract is not installed")
        print("\nInstall with:")
        print("  pip install pytesseract")
        print("\nAlso install Tesseract OCR:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Linux: sudo apt-get install tesseract-ocr")
        print("  Mac: brew install tesseract")
    else:
        try:
            test_text_extraction()
            test_phishing_detection()
            test_text_with_confidence()
            test_url_detection()
            test_visualize_regions()
            
            print("=" * 70)
            print("ALL TESTS COMPLETED")
            print("=" * 70)
            print("\nTest images created in: test_screenshots/")
            
        except Exception as e:
            print(f"\nError running tests: {e}")
            print("\nMake sure Tesseract OCR is installed and in your PATH")
