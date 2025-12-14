"""
Test script for Screenshot Analyzer
Demonstrates computer vision capabilities for phishing detection.
"""

import os
import cv2
import numpy as np
from vision.screenshot_analyzer import ScreenshotAnalyzer, analyze_screenshot
from vision.screenshot_utils import preprocess_image, save_image


def create_test_images():
    """Create sample test images for demonstration."""
    test_dir = "test_screenshots"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a simple test image (legitimate site simulation)
    img_legit = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Add some blue header
    cv2.rectangle(img_legit, (0, 0), (800, 100), (200, 100, 50), -1)
    
    # Add some text-like rectangles
    cv2.rectangle(img_legit, (50, 150), (750, 200), (50, 50, 50), 2)
    cv2.rectangle(img_legit, (50, 250), (750, 300), (50, 50, 50), 2)
    
    # Add a button-like element
    cv2.rectangle(img_legit, (300, 400), (500, 450), (50, 150, 50), -1)
    
    legit_path = os.path.join(test_dir, "legitimate.png")
    save_image(img_legit, legit_path)
    
    # Create a phishing site simulation (similar but with red warning colors)
    img_phish = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Add red header (warning color)
    cv2.rectangle(img_phish, (0, 0), (800, 100), (50, 50, 200), -1)
    
    # Add similar text-like rectangles
    cv2.rectangle(img_phish, (50, 150), (750, 200), (50, 50, 50), 2)
    cv2.rectangle(img_phish, (50, 250), (750, 300), (50, 50, 50), 2)
    
    # Add a red button
    cv2.rectangle(img_phish, (300, 400), (500, 450), (50, 50, 200), -1)
    
    phish_path = os.path.join(test_dir, "phishing.png")
    save_image(img_phish, phish_path)
    
    # Create a very simple page (suspicious)
    img_simple = np.ones((600, 800, 3), dtype=np.uint8) * 255
    cv2.rectangle(img_simple, (300, 250), (500, 350), (100, 100, 100), -1)
    
    simple_path = os.path.join(test_dir, "simple.png")
    save_image(img_simple, simple_path)
    
    return legit_path, phish_path, simple_path


def test_screenshot_comparison():
    """Test screenshot comparison functionality."""
    print("=" * 70)
    print("TEST 1: Screenshot Comparison")
    print("=" * 70)
    
    # Create test images
    legit_path, phish_path, simple_path = create_test_images()
    
    analyzer = ScreenshotAnalyzer()
    
    # Compare legitimate vs phishing
    print("\nComparing legitimate vs phishing screenshots:")
    results = analyzer.compare_screenshots(legit_path, phish_path)
    
    for metric, score in results.items():
        print(f"  {metric}: {score:.4f}")
    
    print()


def test_phishing_detection():
    """Test phishing detection on screenshots."""
    print("=" * 70)
    print("TEST 2: Phishing Detection")
    print("=" * 70)
    
    legit_path, phish_path, simple_path = create_test_images()
    
    # Test phishing screenshot
    print("\nAnalyzing phishing screenshot:")
    result = analyze_screenshot(phish_path)
    
    print(f"Phishing Score: {result['score']}")
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


def test_simple_layout_detection():
    """Test detection of overly simple layouts."""
    print("=" * 70)
    print("TEST 3: Simple Layout Detection")
    print("=" * 70)
    
    legit_path, phish_path, simple_path = create_test_images()
    
    # Test simple screenshot
    print("\nAnalyzing simple layout screenshot:")
    result = analyze_screenshot(simple_path)
    
    print(f"Phishing Score: {result['score']}")
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


def test_with_reference():
    """Test comparison with reference screenshots."""
    print("=" * 70)
    print("TEST 4: Reference Screenshot Comparison")
    print("=" * 70)
    
    legit_path, phish_path, simple_path = create_test_images()
    
    analyzer = ScreenshotAnalyzer()
    
    # Analyze phishing screenshot with legitimate as reference
    print("\nAnalyzing phishing screenshot with legitimate reference:")
    score, indicators = analyzer.analyze(phish_path, [legit_path])
    
    print(f"Phishing Score: {score}")
    print(f"\nIndicators:")
    if indicators:
        for indicator in indicators:
            print(f"  - {indicator}")
    else:
        print("  No suspicious indicators found")
    
    print()


def test_color_analysis():
    """Test color distribution analysis."""
    print("=" * 70)
    print("TEST 5: Color Distribution Analysis")
    print("=" * 70)
    
    legit_path, phish_path, simple_path = create_test_images()
    
    print("\nAnalyzing color distribution in phishing screenshot:")
    analyzer = ScreenshotAnalyzer()
    score, indicators = analyzer.analyze(phish_path)
    
    features = analyzer.get_features()
    
    print(f"Excessive warning colors: {features.get('excessive_warning_colors', 0)}")
    print(f"Edge density: {features.get('edge_density', 0):.4f}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SCREENSHOT ANALYZER TEST SUITE")
    print("=" * 70 + "\n")
    
    try:
        test_screenshot_comparison()
        test_phishing_detection()
        test_simple_layout_detection()
        test_with_reference()
        test_color_analysis()
        
        print("=" * 70)
        print("ALL TESTS COMPLETED")
        print("=" * 70)
        print("\nTest screenshots created in: test_screenshots/")
        
    except Exception as e:
        print(f"\nError running tests: {e}")
        print("\nMake sure you have installed the required packages:")
        print("  pip install opencv-python Pillow imagehash scikit-image")
