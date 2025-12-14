"""
Email Analyzer Module
Uses NLP techniques to analyze email content for phishing indicators.
"""

import re
from typing import Dict, List, Tuple
from urllib.parse import urlparse
import config


class EmailAnalyzer:
    """Analyzes email content for phishing indicators using NLP."""
    
    def __init__(self):
        self.features = {}
        self.indicators = []
        self.score = 0
    
    def analyze(self, subject: str, body: str) -> Tuple[int, List[str]]:
        """
        Analyze email content for phishing indicators.
        
        Args:
            subject: Email subject line
            body: Email body text
            
        Returns:
            Tuple of (score, list of indicator descriptions)
        """
        self.features = {}
        self.indicators = []
        self.score = 0
        
        if not subject and not body:
            return 0, []
        
        subject = subject or ""
        body = body or ""
        
        # Combine for full text analysis
        full_text = f"{subject} {body}".lower()
        
        # Run all checks
        self._check_urgency_language(full_text)
        self._check_sensitive_info_request(full_text)
        self._check_impersonation(full_text)
        self._check_grammar_errors(full_text)
        self._check_ai_generated(full_text)
        self._check_embedded_links(body)
        self._check_personalization(full_text)
        self._check_subject_urgency(subject)
        
        return self.score, self.indicators
    
    def _check_urgency_language(self, text: str):
        """Detect urgency and fear-based language."""
        found_urgency = []
        for keyword in config.URGENCY_KEYWORDS:
            if keyword in text:
                found_urgency.append(keyword)
        
        if found_urgency:
            self.indicators.append(f"Email uses urgent language: '{found_urgency[0]}'")
            self.score += config.EMAIL_WEIGHTS['urgency_language']
            self.features['urgency_language'] = True
    
    def _check_sensitive_info_request(self, text: str):
        """Detect requests for sensitive information."""
        found_requests = []
        for keyword in config.SENSITIVE_INFO_KEYWORDS:
            if keyword in text:
                found_requests.append(keyword)
        
        if found_requests:
            # Check if it's actually requesting (not just mentioning)
            request_patterns = [
                r'enter\s+(?:your\s+)?', r'provide\s+(?:your\s+)?', r'confirm\s+(?:your\s+)?',
                r'verify\s+(?:your\s+)?', r'update\s+(?:your\s+)?', r'send\s+(?:your\s+)?',
                r'submit\s+(?:your\s+)?', r'input\s+(?:your\s+)?'
            ]
            
            for pattern in request_patterns:
                for keyword in found_requests:
                    if re.search(pattern + keyword, text):
                        self.indicators.append(f"Email requests sensitive information ({keyword})")
                        self.score += config.EMAIL_WEIGHTS['sensitive_info_request']
                        self.features['sensitive_info_request'] = True
                        return
    
    def _check_impersonation(self, text: str):
        """Detect impersonation attempts."""
        found_indicators = []
        for indicator in config.IMPERSONATION_INDICATORS:
            if indicator in text:
                found_indicators.append(indicator)
        
        if found_indicators:
            self.indicators.append(f"Email uses generic greeting suggesting impersonation: '{found_indicators[0]}'")
            self.score += config.EMAIL_WEIGHTS['impersonation']
            self.features['impersonation'] = True
    
    def _check_grammar_errors(self, text: str):
        """Detect grammar anomalies common in phishing."""
        found_errors = []
        for pattern in config.GRAMMAR_INDICATORS:
            if pattern in text:
                found_errors.append(pattern)
        
        if found_errors:
            self.indicators.append(f"Email contains unusual phrasing: '{found_errors[0]}'")
            self.score += config.EMAIL_WEIGHTS['grammar_errors']
            self.features['grammar_errors'] = True
    
    def _check_ai_generated(self, text: str):
        """Detect AI-generated phishing indicators."""
        found_ai_patterns = []
        for pattern in config.AI_PHISHING_INDICATORS:
            if pattern in text:
                found_ai_patterns.append(pattern)
        
        if len(found_ai_patterns) >= 2:
            self.indicators.append("Email shows signs of AI-generated phishing (over-formal, repetitive tone)")
            self.score += config.EMAIL_WEIGHTS['ai_generated']
            self.features['ai_generated'] = True
    
    def _check_embedded_links(self, body: str):
        """Check for embedded links and analyze them."""
        # Find URLs in email body
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, body)
        
        if urls:
            self.features['embedded_link'] = True
            
            # Check for link-text mismatch
            # Pattern: [text](url) or <a href="url">text</a>
            markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', body)
            html_links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>', body, re.IGNORECASE)
            
            mismatch_found = False
            
            # Check markdown links
            for text, url in markdown_links:
                if not self._check_link_text_match(text, url):
                    mismatch_found = True
                    break
            
            # Check HTML links
            for url, text in html_links:
                if not self._check_link_text_match(text, url):
                    mismatch_found = True
                    break
            
            if mismatch_found:
                self.indicators.append("Email contains links where display text doesn't match actual URL")
                self.score += config.EMAIL_WEIGHTS['link_mismatch']
                self.features['link_mismatch'] = True
            else:
                # Just having embedded links is slightly suspicious
                self.indicators.append("Email contains embedded links")
                self.score += config.EMAIL_WEIGHTS['embedded_link']
    
    def _check_link_text_match(self, text: str, url: str) -> bool:
        """Check if link text matches the actual URL domain."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            text_lower = text.lower()
            
            # Extract main domain
            parts = domain.split('.')
            if len(parts) >= 2:
                main_domain = parts[-2]
                # If text mentions a domain that doesn't match the URL, it's suspicious
                for brand in config.TRUSTED_BRANDS:
                    if brand in text_lower and brand not in domain:
                        return False
            
            return True
        except:
            return True
    
    def _check_personalization(self, text: str):
        """Check for lack of personalization (generic emails)."""
        # If email uses generic greetings and no personal name
        generic_patterns = [
            'dear customer', 'dear user', 'dear member', 'dear sir/madam',
            'valued customer', 'account holder'
        ]
        
        has_generic = any(pattern in text for pattern in generic_patterns)
        
        # Check if there's any capitalized name (simple heuristic)
        has_name = bool(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text))
        
        if has_generic and not has_name:
            self.indicators.append("Email lacks personalization, uses generic greeting")
            self.score += config.EMAIL_WEIGHTS['no_personalization']
            self.features['no_personalization'] = True
    
    def _check_subject_urgency(self, subject: str):
        """Analyze subject line for urgency triggers."""
        if not subject:
            return
        
        subject_lower = subject.lower()
        
        # Common urgent subject patterns
        urgent_subject_patterns = [
            'urgent', 'action required', 'immediate', 'suspended', 'locked',
            'verify', 'confirm', 'alert', 'warning', 'security', 'unusual activity'
        ]
        
        for pattern in urgent_subject_patterns:
            if pattern in subject_lower:
                # Don't double-count if already caught in urgency check
                if 'urgency_language' not in self.features:
                    self.indicators.append(f"Subject line uses urgent trigger: '{pattern}'")
                    self.score += 10
                break
    
    def get_features(self) -> Dict:
        """Return extracted features."""
        return self.features
