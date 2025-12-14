"""
Quick OCR Demo - Test if Tesseract is working
"""

import os
import sys

# Check if pytesseract is installed
try:
    import pytesseract
    print("✓ pytesseract is installed")
except ImportError:
    print("✗ pytesseract not installed")
    sys.exit(1)

# Check if Tesseract executable exists
tesseract_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    '/usr/bin/tesseract',
    '/usr/local/bin/tesseract'
]

tesseract_found = None
for path in tesseract_paths:
    if os.path.exists(path):
        tesseract_found = path
        print(f"✓ Tesseract found at: {path}")
        pytesseract.pytesseract.tesseract_cmd = path
        break

if not tesseract_found:
    print("✗ Tesseract executable not found in common locations")
    print("\nSearching in PATH...")
    try:
        import subprocess
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Tesseract found in PATH")
            print(result.stdout.split('\n')[0])
        else:
            print("✗ Tesseract not in PATH")
    except:
        print("✗ Tesseract not accessible")
        print("\nPlease install Tesseract OCR:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Linux: sudo apt-get install tesseract-ocr")
        print("  Mac: brew install tesseract")
        sys.exit(1)

# Test OCR on a simple image
print("\n" + "="*70)
print("Testing OCR Functionality")
print("="*70)

try:
    import cv2
    import numpy as np
    
    # Create a simple test image with text
    img = np.ones((200, 600, 3), dtype=np.uint8) * 255
    
    # Add text
    cv2.putText(img, "URGENT: Account Suspended", (50, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    
    # Save test image
    test_path = "test_ocr_demo.png"
    cv2.imwrite(test_path, img)
    print(f"\n✓ Created test image: {test_path}")
    
    # Extract text
    from PIL import Image
    pil_img = Image.open(test_path)
    text = pytesseract.image_to_string(pil_img)
    
    print(f"\n✓ OCR Extracted Text:")
    print("-" * 70)
    print(text.strip())
    print("-" * 70)
    
    # Test with our OCR analyzer
    print("\n" + "="*70)
    print("Testing OCR Analyzer Module")
    print("="*70)
    
    from vision.ocr_analyzer import analyze_screenshot_text
    
    result = analyze_screenshot_text(test_path)
    
    print(f"\nPhishing Score: {result['score']}")
    print(f"\nIndicators:")
    if result['indicators']:
        for indicator in result['indicators']:
            print(f"  - {indicator}")
    else:
        print("  No suspicious indicators found")
    
    print(f"\nExtracted Text: '{result['text']}'")
    
    print(f"\nFeatures:")
    for feature, value in result['features'].items():
        if value > 0:
            print(f"  {feature}: {value}")
    
    # Clean up
    if os.path.exists(test_path):
        os.remove(test_path)
    
    print("\n" + "="*70)
    print("✓ OCR is working correctly!")
    print("="*70)
    
except Exception as e:
    print(f"\n✗ Error testing OCR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
