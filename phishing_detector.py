"""
Phishing Detection Model
Main detection engine that orchestrates URL and email analysis.
"""

import json
from typing import Dict, Optional
from url_analyzer import URLAnalyzer
from email_analyzer import EmailAnalyzer
from risk_scorer import RiskScorer


class PhishingDetector:
    """Main phishing detection engine."""
    
    def __init__(self):
        self.url_analyzer = URLAnalyzer()
        self.email_analyzer = EmailAnalyzer()
        self.risk_scorer = RiskScorer()
    
    def detect(
        self,
        url: Optional[str] = None,
        email_subject: Optional[str] = None,
        email_body: Optional[str] = None
    ) -> Dict:
        """
        Detect phishing based on URL and email content.
        
        Args:
            url: URL to analyze (optional)
            email_subject: Email subject line (optional)
            email_body: Email body text (optional)
            
        Returns:
            Dictionary with classification, risk_score, reasons, and confidence
        """
        # Validate input
        if not url and not email_subject and not email_body:
            return {
                "classification": "Error",
                "risk_score": 0,
                "reasons": ["No input provided for analysis"],
                "confidence": "N/A"
            }
        
        # Analyze URL
        url_score = 0
        url_indicators = []
        if url:
            url_score, url_indicators = self.url_analyzer.analyze(url)
        
        # Analyze email
        email_score = 0
        email_indicators = []
        if email_subject or email_body:
            email_score, email_indicators = self.email_analyzer.analyze(
                email_subject or "",
                email_body or ""
            )
        
        # Calculate final risk
        result = self.risk_scorer.calculate_risk(
            url_score,
            url_indicators,
            email_score,
            email_indicators
        )
        
        return result
    
    def detect_json(
        self,
        url: Optional[str] = None,
        email_subject: Optional[str] = None,
        email_body: Optional[str] = None,
        pretty: bool = False
    ) -> str:
        """
        Detect phishing and return result as JSON string.
        
        Args:
            url: URL to analyze (optional)
            email_subject: Email subject line (optional)
            email_body: Email body text (optional)
            pretty: Whether to format JSON with indentation
            
        Returns:
            JSON string with detection results
        """
        result = self.detect(url, email_subject, email_body)
        
        if pretty:
            return json.dumps(result, indent=2)
        return json.dumps(result)


# Example usage
if __name__ == "__main__":
    detector = PhishingDetector()
    
    # Example 1: Phishing attempt
    print("=" * 60)
    print("Example 1: Suspected Phishing Email")
    print("=" * 60)
    result1 = detector.detect(
        url="http://paypal-secure-login.tk/verify",
        email_subject="Urgent: Account Suspended",
        email_body="Dear customer, Your PayPal account has been suspended due to unusual activity. Please verify your account immediately by clicking here: http://paypal-secure-login.tk/verify"
    )
    print(json.dumps(result1, indent=2))
    
    print("\n" + "=" * 60)
    print("Example 2: Legitimate Email")
    print("=" * 60)
    result2 = detector.detect(
        url="https://www.paypal.com/signin",
        email_subject="Your PayPal Receipt",
        email_body="Hi John, Thank you for your payment of $25.00 to Example Store. View your receipt at https://www.paypal.com/activity"
    )
    print(json.dumps(result2, indent=2))
    
    print("\n" + "=" * 60)
    print("Example 3: Suspicious Email")
    print("=" * 60)
    result3 = detector.detect(
        url="https://secure-account-verification.com",
        email_subject="Action Required",
        email_body="Dear valued customer, Please update your account information within 24 hours to avoid service interruption."
    )
    print(json.dumps(result3, indent=2))
