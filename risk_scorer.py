"""
Risk Scorer Module
Aggregates signals from URL and email analyzers to calculate final risk score.
"""

from typing import Dict, List
import config


class RiskScorer:
    """Calculates risk score and classification from analysis results."""
    
    def __init__(self):
        pass
    
    def calculate_risk(
        self,
        url_score: int,
        url_indicators: List[str],
        email_score: int,
        email_indicators: List[str]
    ) -> Dict:
        """
        Calculate final risk score and classification.
        
        Args:
            url_score: Score from URL analysis
            url_indicators: List of URL indicators found
            email_score: Score from email analysis
            email_indicators: List of email indicators found
            
        Returns:
            Dictionary with classification, risk_score, reasons, and confidence
        """
        # Combine scores (cap at 100)
        total_score = min(url_score + email_score, 100)
        
        # Combine all indicators
        all_indicators = url_indicators + email_indicators
        
        # Determine classification
        classification = self._classify(total_score)
        
        # Calculate confidence
        confidence = self._calculate_confidence(len(all_indicators))
        
        # Select top reasons (most important indicators)
        top_reasons = self._select_top_reasons(all_indicators, url_score, email_score)
        
        return {
            "classification": classification,
            "risk_score": total_score,
            "reasons": top_reasons,
            "confidence": confidence
        }
    
    def _classify(self, score: int) -> str:
        """Classify based on risk score."""
        if score <= config.RISK_THRESHOLDS['legitimate'][1]:
            return "Legitimate"
        elif score <= config.RISK_THRESHOLDS['suspicious'][1]:
            return "Suspicious"
        else:
            return "Phishing"
    
    def _calculate_confidence(self, indicator_count: int) -> str:
        """Calculate confidence level based on number of indicators."""
        for level, (min_count, max_count) in config.CONFIDENCE_LEVELS.items():
            if min_count <= indicator_count <= max_count:
                return level.capitalize()
        return "High"
    
    def _select_top_reasons(
        self,
        all_indicators: List[str],
        url_score: int,
        email_score: int
    ) -> List[str]:
        """
        Select the most important reasons to show.
        Prioritize based on severity and limit to top 3-5 reasons.
        """
        if not all_indicators:
            return ["No significant phishing indicators detected"]
        
        # Priority keywords for sorting (higher priority = more severe)
        priority_keywords = {
            'impersonate': 100,
            'brand': 100,
            'sensitive information': 90,
            'password': 90,
            'IP address': 85,
            '@': 80,
            'mismatch': 75,
            'urgent': 70,
            'suspicious top-level domain': 65,
            'shortening service': 60,
            'excessive subdomains': 55,
            'generic greeting': 50,
            'AI-generated': 45,
            'embedded links': 40,
        }
        
        # Score each indicator
        scored_indicators = []
        for indicator in all_indicators:
            score = 0
            for keyword, priority in priority_keywords.items():
                if keyword.lower() in indicator.lower():
                    score = max(score, priority)
            scored_indicators.append((score if score > 0 else 30, indicator))
        
        # Sort by score (descending) and take top 5
        scored_indicators.sort(reverse=True, key=lambda x: x[0])
        top_reasons = [indicator for _, indicator in scored_indicators[:5]]
        
        # If we have both URL and email indicators, ensure we include at least one of each
        url_keywords = ['URL', 'domain', 'link', 'address']
        email_keywords = ['Email', 'subject', 'greeting', 'language']
        
        has_url = any(any(kw in reason for kw in url_keywords) for reason in top_reasons)
        has_email = any(any(kw in reason for kw in email_keywords) for reason in top_reasons)
        
        # Balance the reasons if needed
        if url_score > 0 and email_score > 0:
            if not has_url and len(all_indicators) > len(top_reasons):
                # Find first URL indicator not in top_reasons
                for _, indicator in scored_indicators:
                    if any(kw in indicator for kw in url_keywords) and indicator not in top_reasons:
                        top_reasons.append(indicator)
                        break
            
            if not has_email and len(all_indicators) > len(top_reasons):
                # Find first email indicator not in top_reasons
                for _, indicator in scored_indicators:
                    if any(kw in indicator for kw in email_keywords) and indicator not in top_reasons:
                        top_reasons.append(indicator)
                        break
        
        return top_reasons[:5]  # Limit to 5 reasons max
