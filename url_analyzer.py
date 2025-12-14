"""
URL Analyzer Module
Extracts features from URLs to detect phishing indicators.
"""

import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Tuple
import config


class URLAnalyzer:
    """Analyzes URLs for phishing indicators."""
    
    def __init__(self):
        self.features = {}
        self.indicators = []
        self.score = 0
    
    def analyze(self, url: str) -> Tuple[int, List[str]]:
        """
        Analyze a URL for phishing indicators.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Tuple of (score, list of indicator descriptions)
        """
        if not url:
            return 0, []
        
        self.features = {}
        self.indicators = []
        self.score = 0
        
        # Parse URL
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # Run all checks
            self._check_ip_address(domain)
            self._check_at_symbol(url)
            self._check_url_length(url)
            self._check_subdomains(domain)
            self._check_suspicious_tld(domain)
            self._check_https(parsed.scheme)
            self._check_suspicious_keywords(url.lower())
            self._check_brand_mismatch(domain)
            self._check_hyphens(domain)
            self._check_port(parsed.port)
            self._check_url_shortener(domain)
            
        except Exception as e:
            self.indicators.append(f"Malformed or invalid URL structure")
            self.score += 20
        
        return self.score, self.indicators
    
    def _check_ip_address(self, domain: str):
        """Check if URL uses IP address instead of domain name."""
        # IPv4 pattern
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        # IPv6 pattern (simplified)
        ipv6_pattern = r'\[?([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\]?'
        
        if re.search(ipv4_pattern, domain) or re.search(ipv6_pattern, domain):
            self.indicators.append("URL uses IP address instead of domain name")
            self.score += config.URL_WEIGHTS['has_ip']
            self.features['has_ip'] = True
    
    def _check_at_symbol(self, url: str):
        """Check for @ symbol in URL (can be used to obscure real domain)."""
        if '@' in url:
            self.indicators.append("URL contains '@' symbol, which can hide the real domain")
            self.score += config.URL_WEIGHTS['has_at_symbol']
            self.features['has_at_symbol'] = True
    
    def _check_url_length(self, url: str):
        """Check if URL is excessively long."""
        if len(url) > 75:
            self.indicators.append(f"URL is unusually long ({len(url)} characters)")
            self.score += config.URL_WEIGHTS['long_url']
            self.features['long_url'] = True
    
    def _check_subdomains(self, domain: str):
        """Check for excessive subdomains."""
        if domain:
            # Remove port if present
            domain = domain.split(':')[0]
            parts = domain.split('.')
            # More than 3 parts suggests excessive subdomains (e.g., login.secure.paypal.verify.com)
            if len(parts) > 3:
                self.indicators.append(f"URL has excessive subdomains ({len(parts) - 2} subdomains)")
                self.score += config.URL_WEIGHTS['excessive_subdomains']
                self.features['excessive_subdomains'] = True
    
    def _check_suspicious_tld(self, domain: str):
        """Check for suspicious top-level domains commonly used in phishing."""
        for tld in config.SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                self.indicators.append(f"URL uses suspicious top-level domain ({tld})")
                self.score += config.URL_WEIGHTS['suspicious_tld']
                self.features['suspicious_tld'] = True
                break
    
    def _check_https(self, scheme: str):
        """Check if URL uses HTTPS (note: HTTPS doesn't guarantee safety)."""
        if scheme != 'https':
            self.indicators.append("URL does not use HTTPS encryption")
            self.score += config.URL_WEIGHTS['no_https']
            self.features['no_https'] = True
    
    def _check_suspicious_keywords(self, url: str):
        """Check for suspicious keywords in URL."""
        found_keywords = []
        for keyword in config.SUSPICIOUS_KEYWORDS:
            if keyword in url:
                found_keywords.append(keyword)
        
        if found_keywords:
            self.indicators.append(f"URL contains suspicious keywords: {', '.join(found_keywords[:3])}")
            self.score += config.URL_WEIGHTS['suspicious_keyword']
            self.features['suspicious_keyword'] = True
    
    def _check_brand_mismatch(self, domain: str):
        """Check if URL impersonates a trusted brand."""
        domain_clean = domain.split(':')[0]  # Remove port
        
        for brand in config.TRUSTED_BRANDS:
            # Check if brand name appears in domain but isn't the actual domain
            if brand in domain_clean:
                # Extract the main domain (second-level domain)
                parts = domain_clean.split('.')
                if len(parts) >= 2:
                    main_domain = parts[-2]
                    # If brand appears but isn't the main domain, it's suspicious
                    if brand in domain_clean and brand != main_domain:
                        self.indicators.append(f"URL appears to impersonate '{brand}' but uses a different domain")
                        self.score += config.URL_WEIGHTS['brand_mismatch']
                        self.features['brand_mismatch'] = True
                        break
    
    def _check_hyphens(self, domain: str):
        """Check for excessive hyphens in domain (common in phishing)."""
        hyphen_count = domain.count('-')
        if hyphen_count >= 2:
            self.indicators.append(f"Domain contains multiple hyphens ({hyphen_count})")
            self.score += config.URL_WEIGHTS['excessive_hyphens']
            self.features['excessive_hyphens'] = True
    
    def _check_port(self, port):
        """Check for non-standard ports."""
        if port and port not in [80, 443]:
            self.indicators.append(f"URL uses non-standard port ({port})")
            self.score += config.URL_WEIGHTS['port_number']
            self.features['port_number'] = True
    
    def _check_url_shortener(self, domain: str):
        """Check if URL uses a URL shortening service."""
        for shortener in config.URL_SHORTENERS:
            if shortener in domain:
                self.indicators.append("URL uses a link shortening service, hiding the real destination")
                self.score += config.URL_WEIGHTS['shortened_url']
                self.features['shortened_url'] = True
                break
    
    def get_features(self) -> Dict:
        """Return extracted features."""
        return self.features
