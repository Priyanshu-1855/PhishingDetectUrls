"""
Demo Script for Judges - Phishing Detection System
Populate database with realistic test URLs for demonstration
"""

import requests
import time

API_URL = 'http://localhost:5000/api/v1/detect'
API_KEY = 'demo-key-12345'

# Test URLs for demonstration
demo_urls = [
    # HIGH RISK - Phishing URLs
    {
        'url': 'http://192.168.1.1/paypal/login',
        'category': 'PHISHING',
        'description': 'IP address + PayPal brand impersonation'
    },
    {
        'url': 'http://paypa1-verify.tk/secure/account',
        'category': 'PHISHING',
        'description': 'Typosquatting (1 instead of l) + suspicious TLD'
    },
    {
        'url': 'http://secure-chase-online-banking.com/login',
        'category': 'PHISHING',
        'description': 'Bank impersonation + credential harvesting'
    },
    {
        'url': 'http://microsoft-account-verify.ml/update',
        'category': 'PHISHING',
        'description': 'Microsoft impersonation + free TLD (.ml)'
    },
    {
        'url': 'http://amazon-security-alert.tk/verify-now',
        'category': 'PHISHING',
        'description': 'Amazon impersonation + urgency keywords'
    },
    {
        'url': 'http://192.168.0.100/google/signin',
        'category': 'PHISHING',
        'description': 'IP address + Google brand abuse'
    },
    {
        'url': 'http://apple-id-locked.cf/unlock',
        'category': 'PHISHING',
        'description': 'Apple impersonation + account threat'
    },
    {
        'url': 'http://secure-bankofamerica-login.com/verify',
        'category': 'PHISHING',
        'description': 'Bank of America impersonation'
    },
    
    # MEDIUM RISK - Suspicious URLs
    {
        'url': 'http://bit.ly/secure-login-2024',
        'category': 'SUSPICIOUS',
        'description': 'URL shortener + suspicious keywords'
    },
    {
        'url': 'http://account-update-required.com',
        'category': 'SUSPICIOUS',
        'description': 'Generic phishing keywords'
    },
    {
        'url': 'http://verify-your-account-now.net',
        'category': 'SUSPICIOUS',
        'description': 'Urgency + verification keywords'
    },
    {
        'url': 'http://secure-payment-portal.info',
        'category': 'SUSPICIOUS',
        'description': 'Payment + security keywords'
    },
    
    # LOW RISK - Legitimate URLs
    {
        'url': 'https://www.google.com',
        'category': 'LEGITIMATE',
        'description': 'Official Google domain'
    },
    {
        'url': 'https://www.github.com',
        'category': 'LEGITIMATE',
        'description': 'Official GitHub domain'
    },
    {
        'url': 'https://www.paypal.com',
        'category': 'LEGITIMATE',
        'description': 'Official PayPal domain'
    },
    {
        'url': 'https://www.microsoft.com',
        'category': 'LEGITIMATE',
        'description': 'Official Microsoft domain'
    },
    {
        'url': 'https://www.amazon.com',
        'category': 'LEGITIMATE',
        'description': 'Official Amazon domain'
    }
]

def test_url(url_data):
    """Test a single URL"""
    try:
        response = requests.post(
            API_URL,
            json={'url': url_data['url']},
            headers={'X-API-Key': API_KEY},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {url_data['category']}: {url_data['url']}")
            print(f"   Risk Score: {result.get('risk_score', 'N/A')}/100")
            print(f"   Classification: {result.get('classification', 'N/A')}")
            print(f"   Description: {url_data['description']}")
            print()
            return True
        else:
            print(f"❌ Error testing {url_data['url']}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test {url_data['url']}: {str(e)}")
        return False

def main():
    print("="*70)
    print("DEMO SCRIPT - POPULATING DATABASE FOR JUDGES")
    print("="*70)
    print()
    
    print("📋 Testing URLs to populate database...")
    print()
    
    success_count = 0
    total_count = len(demo_urls)
    
    for i, url_data in enumerate(demo_urls, 1):
        print(f"[{i}/{total_count}] Testing...")
        if test_url(url_data):
            success_count += 1
        time.sleep(0.5)  # Small delay between requests
    
    print("="*70)
    print(f"✅ Successfully tested {success_count}/{total_count} URLs")
    print()
    print("🎯 DEMO READY!")
    print()
    print("Next Steps:")
    print("1. Open database_viewer.html in browser")
    print("2. Refresh to see all cached URLs")
    print("3. Show judges the different risk levels")
    print("4. Demonstrate filtering by classification")
    print("5. Show how fast cached URLs respond (5ms)")
    print()
    print("="*70)

if __name__ == '__main__':
    main()
