"""
Database Statistics and Management
View and manage the URL cache database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from url_database import URLDatabase

def main():
    db = URLDatabase()
    
    print("="*70)
    print("URL DATABASE STATISTICS")
    print("="*70)
    
    stats = db.get_statistics()
    
    print(f"\n📊 Database Overview:")
    print(f"   Total URLs cached: {stats['total_urls']}")
    print(f"   Phishing URLs: {stats['phishing_urls']}")
    print(f"   Legitimate URLs: {stats['legitimate_urls']}")
    print(f"   Learned Patterns: {stats['total_patterns']}")
    
    # Show recent phishing URLs
    print(f"\n🚨 Recent Phishing URLs:")
    phishing_urls = db.get_phishing_urls(limit=10)
    
    if phishing_urls:
        for i, url_data in enumerate(phishing_urls, 1):
            print(f"\n   {i}. {url_data['url']}")
            print(f"      Risk Score: {url_data['risk_score']}/100")
            print(f"      Reasons: {', '.join(url_data['reasons'])}")
            print(f"      First Seen: {url_data['first_seen']}")
    else:
        print("   No phishing URLs in database yet")
    
    # Show learned patterns
    print(f"\n🎯 Learned Phishing Patterns:")
    patterns = db.get_patterns()
    
    if patterns:
        for i, pattern in enumerate(patterns[:10], 1):
            print(f"\n   {i}. Pattern: {pattern['pattern']}")
            print(f"      Type: {pattern['type']}")
            print(f"      Confidence: {pattern['confidence']:.2f}")
            print(f"      Matches: {pattern['matches']}")
    else:
        print("   No patterns learned yet")
    
    print("\n" + "="*70)
    print("✅ Database ready for fast URL lookups and learning!")
    print("="*70)
    
    db.close()

if __name__ == '__main__':
    main()
