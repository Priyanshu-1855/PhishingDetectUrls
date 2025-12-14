"""
Configuration file for phishing detection model.
Contains keyword dictionaries, trusted brands, scoring weights, and thresholds.
"""

# URL Analysis Configuration
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'secure', 'account', 'update', 'confirm', 'banking',
    'password', 'signin', 'ebay', 'paypal', 'amazon', 'apple', 'microsoft',
    'suspended', 'locked', 'unusual', 'click', 'urgent', 'immediately'
]

TRUSTED_BRANDS = [
    'google', 'facebook', 'amazon', 'paypal', 'microsoft', 'apple', 'netflix',
    'twitter', 'instagram', 'linkedin', 'ebay', 'walmart', 'target', 'chase',
    'bankofamerica', 'wellsfargo', 'citibank', 'americanexpress'
]

# Common TLDs used in phishing
SUSPICIOUS_TLDS = [
    '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click',
    '.link', '.download', '.stream', '.racing', '.bid', '.win'
]

# URL scoring weights
URL_WEIGHTS = {
    'has_ip': 25,
    'has_at_symbol': 20,
    'excessive_subdomains': 15,
    'long_url': 10,
    'suspicious_tld': 20,
    'brand_mismatch': 30,
    'suspicious_keyword': 15,
    'shortened_url': 10,
    'no_https': 5,
    'excessive_hyphens': 10,
    'port_number': 15
}

# Email Analysis Configuration
URGENCY_KEYWORDS = [
    'urgent', 'immediately', 'act now', 'limited time', 'expires', 'suspended',
    'locked', 'verify now', 'confirm now', 'click here', 'act fast', 'hurry',
    'last chance', 'final notice', 'action required', 'respond immediately',
    'within 24 hours', 'within 48 hours', 'account will be closed'
]

SENSITIVE_INFO_KEYWORDS = [
    'password', 'ssn', 'social security', 'credit card', 'cvv', 'pin',
    'account number', 'routing number', 'otp', 'verification code',
    'security code', 'bank account', 'debit card', 'full name',
    'date of birth', 'mother maiden name', 'tax id'
]

IMPERSONATION_INDICATORS = [
    'dear customer', 'dear user', 'dear member', 'valued customer',
    'account holder', 'dear sir/madam'
]

# Grammar/spelling error patterns (common in phishing)
GRAMMAR_INDICATORS = [
    'kindly', 'needful', 'revert back', 'do the needful', 'please kindly'
]

# AI-generated phishing indicators
AI_PHISHING_INDICATORS = [
    'i hope this message finds you well',
    'we regret to inform you',
    'we are writing to inform you',
    'please be advised',
    'for your convenience',
    'rest assured'
]

# Email scoring weights
EMAIL_WEIGHTS = {
    'urgency_language': 20,
    'sensitive_info_request': 30,
    'impersonation': 15,
    'grammar_errors': 10,
    'ai_generated': 10,
    'embedded_link': 15,
    'link_mismatch': 25,
    'no_personalization': 10,
    'suspicious_sender': 20
}

# Risk Classification Thresholds
RISK_THRESHOLDS = {
    'legitimate': (0, 30),
    'suspicious': (31, 70),
    'phishing': (71, 100)
}

# Confidence levels based on number of indicators
CONFIDENCE_LEVELS = {
    'low': (0, 2),      # 0-2 indicators found
    'medium': (3, 5),   # 3-5 indicators found
    'high': (6, 100)    # 6+ indicators found
}

# URL shortener domains
URL_SHORTENERS = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd',
    'buff.ly', 'adf.ly', 'bl.ink', 'lnkd.in', 'short.link'
]
