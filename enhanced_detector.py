"""
Enhanced Phishing Detector with ML and Threat Intelligence
Production-ready version integrating all components.
"""

import json
from typing import Dict, Optional
from url_analyzer import URLAnalyzer
from email_analyzer import EmailAnalyzer
from risk_scorer import RiskScorer
from ml_predictor import MLPredictor
from threat_intel.aggregator import ThreatIntelAggregator


class EnhancedPhishingDetector:
    """
    Production phishing detector with ML and threat intelligence.
    """
    
    def __init__(self, use_ml: bool = True, use_threat_intel: bool = True):
        self.url_analyzer = URLAnalyzer()
        self.email_analyzer = EmailAnalyzer()
        self.risk_scorer = RiskScorer()
        
        # Optional components
        self.use_ml = use_ml
        self.use_threat_intel = use_threat_intel
        
        if use_ml:
            self.ml_predictor = MLPredictor()
        
        if use_threat_intel:
            self.threat_intel = ThreatIntelAggregator()
    
    def detect(
        self,
        url: Optional[str] = None,
        email_subject: Optional[str] = None,
        email_body: Optional[str] = None,
        include_details: bool = False
    ) -> Dict:
        """
        Comprehensive phishing detection with all available methods.
        
        Args:
            url: URL to analyze
            email_subject: Email subject line
            email_body: Email body text
            include_details: Include detailed analysis from all sources
            
        Returns:
            Detection result with classification and explanations
        """
        # Validate input
        if not url and not email_subject and not email_body:
            return {
                "classification": "Error",
                "risk_score": 0,
                "reasons": ["No input provided for analysis"],
                "confidence": "N/A"
            }
        
        # Rule-based analysis
        url_score = 0
        url_indicators = []
        if url:
            url_score, url_indicators = self.url_analyzer.analyze(url)
        
        email_score = 0
        email_indicators = []
        if email_subject or email_body:
            email_score, email_indicators = self.email_analyzer.analyze(
                email_subject or "",
                email_body or ""
            )
        
        # Base risk calculation
        result = self.risk_scorer.calculate_risk(
            url_score,
            url_indicators,
            email_score,
            email_indicators
        )
        
        # Add ML prediction if available
        if self.use_ml and hasattr(self, 'ml_predictor') and self.ml_predictor.models_loaded:
            ml_prob, ml_info = self.ml_predictor.predict(url, email_subject, email_body)
            if ml_prob is not None:
                result['ml_prediction'] = ml_info
                result['ml_risk_score'] = int(ml_prob * 100)
                
                # Adjust final score with ML input (weighted average)
                original_score = result['risk_score']
                ml_score = result['ml_risk_score']
                # 70% rule-based, 30% ML
                result['risk_score'] = int(original_score * 0.7 + ml_score * 0.3)
                
                # Re-classify based on new score
                if result['risk_score'] <= 30:
                    result['classification'] = "Legitimate"
                elif result['risk_score'] <= 70:
                    result['classification'] = "Suspicious"
                else:
                    result['classification'] = "Phishing"
        
        # Add threat intelligence if available and URL provided
        if self.use_threat_intel and url and hasattr(self, 'threat_intel'):
            try:
                threat_result = self.threat_intel.check_url(url)
                
                if include_details:
                    result['threat_intelligence'] = threat_result
                
                # Add threat intel boost to score
                threat_boost = self.threat_intel.get_threat_score_boost(url)
                if threat_boost > 0:
                    result['risk_score'] = min(100, result['risk_score'] + threat_boost)
                    
                    # Add threat intel reasons
                    aggregated = threat_result.get('aggregated', {})
                    if aggregated.get('threat_detected'):
                        result['reasons'].extend(aggregated.get('reasons', []))
                    
                    # Re-classify if needed
                    if result['risk_score'] > 70:
                        result['classification'] = "Phishing"
                    elif result['risk_score'] > 30:
                        result['classification'] = "Suspicious"
            except Exception as e:
                # Don't fail if threat intel is unavailable
                if include_details:
                    result['threat_intelligence_error'] = str(e)
        
        return result
    
    def detect_json(
        self,
        url: Optional[str] = None,
        email_subject: Optional[str] = None,
        email_body: Optional[str] = None,
        pretty: bool = False,
        include_details: bool = False
    ) -> str:
        """
        Detect phishing and return result as JSON string.
        """
        result = self.detect(url, email_subject, email_body, include_details)
        
        if pretty:
            return json.dumps(result, indent=2)
        return json.dumps(result)


# Example usage
if __name__ == "__main__":
    detector = EnhancedPhishingDetector(use_ml=True, use_threat_intel=True)
    
    print("=" * 60)
    print("Enhanced Phishing Detector - Production Version")
    print("=" * 60)
    print(f"ML Models: {'Loaded' if detector.ml_predictor.models_loaded else 'Not Available'}")
    print(f"Threat Intelligence: {'Enabled' if detector.use_threat_intel else 'Disabled'}")
    print("=" * 60)
    
    # Test with a phishing example
    result = detector.detect(
        url="http://paypal-secure.tk/verify",
        email_subject="Urgent: Account Suspended",
        email_body="Click here to verify your account immediately",
        include_details=True
    )
    
    print("\nTest Result:")
    print(json.dumps(result, indent=2))
