"""
Dataset Generator for ML Training
Generates synthetic phishing and legitimate email/URL samples.
"""

import json
import random
from typing import List, Dict
import config


class DatasetGenerator:
    """Generates synthetic training data for ML models."""
    
    def __init__(self):
        self.phishing_samples = []
        self.legitimate_samples = []
    
    def generate_dataset(self, num_phishing: int = 500, num_legitimate: int = 500) -> List[Dict]:
        """
        Generate a balanced dataset of phishing and legitimate samples.
        
        Args:
            num_phishing: Number of phishing samples to generate
            num_legitimate: Number of legitimate samples to generate
            
        Returns:
            List of sample dictionaries with labels
        """
        dataset = []
        
        # Generate phishing samples
        for _ in range(num_phishing):
            sample = self._generate_phishing_sample()
            sample['label'] = 1  # 1 = phishing
            dataset.append(sample)
        
        # Generate legitimate samples
        for _ in range(num_legitimate):
            sample = self._generate_legitimate_sample()
            sample['label'] = 0  # 0 = legitimate
            dataset.append(sample)
        
        # Shuffle dataset
        random.shuffle(dataset)
        
        return dataset
    
    def _generate_phishing_sample(self) -> Dict:
        """Generate a synthetic phishing sample."""
        # Random phishing techniques
        techniques = [
            self._phishing_with_ip,
            self._phishing_with_subdomain,
            self._phishing_with_typosquatting,
            self._phishing_with_suspicious_tld,
            self._phishing_with_url_shortener,
        ]
        
        technique = random.choice(techniques)
        return technique()
    
    def _phishing_with_ip(self) -> Dict:
        """Phishing using IP address."""
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        brand = random.choice(config.TRUSTED_BRANDS)
        
        return {
            'url': f"http://{ip}/{brand}/login",
            'subject': random.choice([
                f"Urgent: {brand.capitalize()} Account Suspended",
                f"Security Alert - {brand.capitalize()}",
                f"Verify Your {brand.capitalize()} Account"
            ]),
            'body': self._generate_phishing_body(brand)
        }
    
    def _phishing_with_subdomain(self) -> Dict:
        """Phishing with excessive subdomains."""
        brand = random.choice(config.TRUSTED_BRANDS)
        subdomains = ['secure', 'login', 'verify', 'account', 'update']
        random.shuffle(subdomains)
        domain = '.'.join(subdomains[:3]) + f'.{brand}-verify.com'
        
        return {
            'url': f"https://{domain}",
            'subject': f"Action Required: {brand.capitalize()} Account",
            'body': self._generate_phishing_body(brand)
        }
    
    def _phishing_with_typosquatting(self) -> Dict:
        """Phishing with typosquatted domain."""
        brand = random.choice(config.TRUSTED_BRANDS)
        
        # Common typosquatting techniques
        typos = [
            brand.replace('a', '4'),
            brand.replace('o', '0'),
            brand.replace('e', '3'),
            brand + random.choice(['1', '2', '-secure', '-login']),
            brand.replace(brand[0], brand[0] * 2) if len(brand) > 2 else brand,
        ]
        
        typo_domain = random.choice(typos)
        
        return {
            'url': f"http://{typo_domain}.com/verify",
            'subject': f"{brand.capitalize()} - Immediate Action Required",
            'body': self._generate_phishing_body(brand)
        }
    
    def _phishing_with_suspicious_tld(self) -> Dict:
        """Phishing with suspicious TLD."""
        brand = random.choice(config.TRUSTED_BRANDS)
        tld = random.choice(config.SUSPICIOUS_TLDS)
        
        return {
            'url': f"http://{brand}-secure{tld}/login",
            'subject': f"Your {brand.capitalize()} account needs verification",
            'body': self._generate_phishing_body(brand)
        }
    
    def _phishing_with_url_shortener(self) -> Dict:
        """Phishing with URL shortener."""
        brand = random.choice(config.TRUSTED_BRANDS)
        shortener = random.choice(config.URL_SHORTENERS)
        
        return {
            'url': f"https://{shortener}/{random.choice(['abc123', 'xyz789', '1a2b3c'])}",
            'subject': f"{brand.capitalize()} Security Alert",
            'body': self._generate_phishing_body(brand)
        }
    
    def _generate_phishing_body(self, brand: str) -> str:
        """Generate phishing email body."""
        templates = [
            f"Dear customer, Your {brand} account has been suspended due to unusual activity. {random.choice(config.URGENCY_KEYWORDS).capitalize()} to verify your account. Provide your {random.choice(['password', 'account number', 'SSN', 'credit card'])}.",
            f"Dear valued customer, We detected suspicious login attempts on your {brand} account. Click here {random.choice(config.URGENCY_KEYWORDS)} to secure your account.",
            f"Dear user, Your {brand} account will be closed within {random.choice(['24', '48'])} hours unless you verify your identity. Enter your {random.choice(config.SENSITIVE_INFO_KEYWORDS)}.",
            f"I hope this message finds you well. We are writing to inform you that your {brand} account requires verification. Please be advised that failure to complete this process may result in service interruption.",
        ]
        
        return random.choice(templates)
    
    def _generate_legitimate_sample(self) -> Dict:
        """Generate a legitimate sample."""
        templates = [
            self._legitimate_receipt,
            self._legitimate_notification,
            self._legitimate_security_alert,
            self._legitimate_newsletter,
        ]
        
        template = random.choice(templates)
        return template()
    
    def _legitimate_receipt(self) -> Dict:
        """Legitimate purchase receipt."""
        brand = random.choice(['amazon', 'ebay', 'walmart', 'target'])
        name = random.choice(['John Smith', 'Sarah Johnson', 'Michael Chen', 'Emily Davis'])
        
        return {
            'url': f"https://www.{brand}.com/orders",
            'subject': f"Your {brand.capitalize()} order confirmation #{random.randint(100000, 999999)}",
            'body': f"Hi {name}, Thank you for your order. Your package will arrive on {random.choice(['Dec 15', 'Dec 16', 'Dec 17'])}. Track your order at https://www.{brand}.com/orders"
        }
    
    def _legitimate_notification(self) -> Dict:
        """Legitimate service notification."""
        services = [
            ('github', 'New issue in your repository'),
            ('linkedin', 'You have a new connection'),
            ('twitter', 'New follower notification'),
            ('netflix', 'New shows added to your list'),
        ]
        
        service, subject = random.choice(services)
        name = random.choice(['Alex', 'Jordan', 'Taylor', 'Morgan'])
        
        return {
            'url': f"https://www.{service}.com/notifications",
            'subject': subject,
            'body': f"Hi {name}, {subject}. View details at https://www.{service}.com/notifications"
        }
    
    def _legitimate_security_alert(self) -> Dict:
        """Legitimate security notification."""
        brand = random.choice(['google', 'microsoft', 'apple'])
        name = random.choice(['Chris Lee', 'Pat Wilson', 'Sam Brown'])
        
        return {
            'url': f"https://myaccount.{brand}.com/security",
            'subject': f"Security alert for your {brand.capitalize()} Account",
            'body': f"Hi {name}, We noticed a new sign-in to your account from a Windows device in New York. If this was you, you don't need to do anything. If not, review your account activity at https://myaccount.{brand}.com/security"
        }
    
    def _legitimate_newsletter(self) -> Dict:
        """Legitimate newsletter."""
        companies = ['TechCrunch', 'Medium', 'Substack', 'The Verge']
        company = random.choice(companies)
        
        return {
            'url': f"https://www.{company.lower().replace(' ', '')}.com",
            'subject': f"{company} Weekly Newsletter - {random.choice(['Tech News', 'Latest Articles', 'Top Stories'])}",
            'body': f"Here are this week's top stories from {company}. Read more at https://www.{company.lower().replace(' ', '')}.com"
        }
    
    def save_to_json(self, dataset: List[Dict], filename: str = 'training_data.json'):
        """Save dataset to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        print(f"Dataset saved to {filename}")
    
    def save_to_csv(self, dataset: List[Dict], filename: str = 'training_data.csv'):
        """Save dataset to CSV file."""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'subject', 'body', 'label'])
            writer.writeheader()
            writer.writerows(dataset)
        print(f"Dataset saved to {filename}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic training dataset")
    parser.add_argument('--phishing', type=int, default=500, help='Number of phishing samples')
    parser.add_argument('--legitimate', type=int, default=500, help='Number of legitimate samples')
    parser.add_argument('--format', choices=['json', 'csv', 'both'], default='both', help='Output format')
    parser.add_argument('--output', type=str, default='training_data', help='Output filename (without extension)')
    
    args = parser.parse_args()
    
    generator = DatasetGenerator()
    dataset = generator.generate_dataset(args.phishing, args.legitimate)
    
    print(f"Generated {len(dataset)} samples ({args.phishing} phishing, {args.legitimate} legitimate)")
    
    if args.format in ['json', 'both']:
        generator.save_to_json(dataset, f"{args.output}.json")
    
    if args.format in ['csv', 'both']:
        generator.save_to_csv(dataset, f"{args.output}.csv")
