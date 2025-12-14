"""
Test script for NER Analyzer
Demonstrates Named Entity Recognition capabilities for phishing detection.
"""

from nlp.ner_analyzer import NERAnalyzer, analyze_text


def test_brand_impersonation():
    """Test detection of brand impersonation."""
    print("=" * 70)
    print("TEST 1: Brand Impersonation Detection")
    print("=" * 70)
    
    subject = "Urgent: PayPal Account Suspended"
    body = "Dear customer, Your PayPal account has been suspended. Please verify your identity immediately."
    url = "http://paypa1-secure.com/verify"  # Fake PayPal domain
    
    analyzer = NERAnalyzer()
    score, indicators, entities = analyzer.analyze(subject, body, url)
    
    print(f"\nSubject: {subject}")
    print(f"URL: {url}")
    print(f"\nPhishing Score: {score}")
    print(f"\nIndicators:")
    for indicator in indicators:
        print(f"  - {indicator}")
    
    print(f"\nExtracted Entities:")
    print(analyzer.get_entity_summary())
    print()


def test_multiple_organizations():
    """Test detection of multiple organizations."""
    print("=" * 70)
    print("TEST 2: Multiple Organizations Detection")
    print("=" * 70)
    
    subject = "Transfer from Bank of America to Wells Fargo"
    body = "Dear customer, Please transfer funds from your Bank of America account to Wells Fargo and then to Chase Bank."
    url = "http://secure-banking.com"
    
    result = analyze_text(subject, body, url)
    
    print(f"\nSubject: {subject}")
    print(f"\nPhishing Score: {result['score']}")
    print(f"\nIndicators:")
    for indicator in result['indicators']:
        print(f"  - {indicator}")
    
    print(f"\nExtracted Entities:")
    print(result['entity_summary'])
    print()


def test_money_requests():
    """Test detection of suspicious money requests."""
    print("=" * 70)
    print("TEST 3: Suspicious Money Request Detection")
    print("=" * 70)
    
    subject = "Urgent: Send $5000 within 24 hours"
    body = "Dear user, You must send $5000 to verify your account within 24 hours or it will be closed."
    url = "http://example.com"
    
    result = analyze_text(subject, body, url)
    
    print(f"\nSubject: {subject}")
    print(f"\nPhishing Score: {result['score']}")
    print(f"\nIndicators:")
    for indicator in result['indicators']:
        print(f"  - {indicator}")
    
    print(f"\nExtracted Entities:")
    print(result['entity_summary'])
    print()


def test_legitimate_email():
    """Test with legitimate email."""
    print("=" * 70)
    print("TEST 4: Legitimate Email (Should have low score)")
    print("=" * 70)
    
    subject = "Your Amazon order #12345 has shipped"
    body = "Hi John Smith, Your order has been shipped and will arrive on December 15th. Track your package at https://www.amazon.com/orders"
    url = "https://www.amazon.com/orders"
    
    result = analyze_text(subject, body, url)
    
    print(f"\nSubject: {subject}")
    print(f"\nPhishing Score: {result['score']}")
    print(f"\nIndicators:")
    if result['indicators']:
        for indicator in result['indicators']:
            print(f"  - {indicator}")
    else:
        print("  No suspicious indicators found")
    
    print(f"\nExtracted Entities:")
    print(result['entity_summary'])
    print()


def test_geographic_context():
    """Test detection of suspicious geographic context."""
    print("=" * 70)
    print("TEST 5: Suspicious Geographic Context")
    print("=" * 70)
    
    subject = "Bank Transfer Required"
    body = "Dear customer, Your Bank of America account requires verification. Please send funds to our office in Nigeria immediately."
    url = "http://bankofamerica-verify.com"
    
    result = analyze_text(subject, body, url)
    
    print(f"\nSubject: {subject}")
    print(f"\nPhishing Score: {result['score']}")
    print(f"\nIndicators:")
    for indicator in result['indicators']:
        print(f"  - {indicator}")
    
    print(f"\nExtracted Entities:")
    print(result['entity_summary'])
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("NER ANALYZER TEST SUITE")
    print("=" * 70 + "\n")
    
    try:
        test_brand_impersonation()
        test_multiple_organizations()
        test_money_requests()
        test_legitimate_email()
        test_geographic_context()
        
        print("=" * 70)
        print("ALL TESTS COMPLETED")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError running tests: {e}")
        print("\nMake sure you have installed spaCy and downloaded the model:")
        print("  pip install spacy")
        print("  python -m spacy download en_core_web_sm")
