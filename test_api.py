"""
Test script to verify API is working and returning correct phishing scores
"""

import requests
import json

API_URL = "http://localhost:5000/api/v1/detect"
API_KEY = "demo-key-12345"

def test_url(url, description):
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print('='*70)
    
    try:
        response = requests.post(
            API_URL,
            headers={
                'Content-Type': 'application/json',
                'X-API-Key': API_KEY
            },
            json={'url': url}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Response:")
            print(f"   Classification: {result.get('classification')}")
            print(f"   Risk Score: {result.get('risk_score')}/100")
            print(f"   Confidence: {result.get('confidence')}")
            print(f"\n   Top Reasons:")
            for i, reason in enumerate(result.get('reasons', [])[:5], 1):
                print(f"   {i}. {reason}")
            
            # Check if it should trigger blocking warning
            if result.get('risk_score', 0) > 70:
                print(f"\n   🚫 SHOULD TRIGGER BLOCKING WARNING")
            else:
                print(f"\n   ✓ Should load normally (risk < 70)")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server!")
        print("   Make sure the server is running: python api/app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("PHISHING DETECTION API TEST")
    print("="*70)
    
    # Test suspicious URLs
    test_url(
        "http://secure-paypal-verify.tk",
        "Suspicious TLD (.tk) with phishing keywords"
    )
    
    test_url(
        "http://192.168.1.1/paypal/login",
        "IP address with phishing path"
    )
    
    test_url(
        "http://account-verify-login.com",
        "Multiple phishing keywords in domain"
    )
    
    test_url(
        "http://bit.ly/verify-account",
        "URL shortener with suspicious path"
    )
    
    # Test legitimate URLs
    test_url(
        "https://www.google.com",
        "Legitimate site (Google)"
    )
    
    test_url(
        "https://www.github.com",
        "Legitimate site (GitHub)"
    )
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print("\nIf suspicious URLs show risk_score > 70, the extension should block them.")
    print("Make sure to reload the extension in Chrome after any changes!")
