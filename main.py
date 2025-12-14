"""
Main CLI Interface for Phishing Detection Model
"""

import argparse
import json
import sys
from phishing_detector import PhishingDetector


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Phishing Detection Model - Analyze URLs and emails for phishing indicators",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a URL and email together
  python main.py --url "http://paypal-verify.tk" --subject "Account Suspended" --body "Click here to verify"
  
  # Analyze just a URL
  python main.py --url "http://suspicious-site.com/login"
  
  # Analyze just an email
  python main.py --subject "Urgent Action Required" --body "Your account will be closed"
  
  # Run test samples
  python main.py --test-samples test_samples.json
        """
    )
    
    parser.add_argument(
        '--url',
        type=str,
        help='URL to analyze'
    )
    
    parser.add_argument(
        '--subject',
        '--email-subject',
        type=str,
        dest='subject',
        help='Email subject line'
    )
    
    parser.add_argument(
        '--body',
        '--email-body',
        type=str,
        dest='body',
        help='Email body text'
    )
    
    parser.add_argument(
        '--test-samples',
        type=str,
        help='Path to JSON file with test samples'
    )
    
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output'
    )
    
    args = parser.parse_args()
    
    detector = PhishingDetector()
    
    # Handle test samples
    if args.test_samples:
        run_test_samples(detector, args.test_samples, args.pretty)
        return
    
    # Validate input
    if not args.url and not args.subject and not args.body:
        parser.print_help()
        sys.exit(1)
    
    # Run detection
    result = detector.detect(
        url=args.url,
        email_subject=args.subject,
        email_body=args.body
    )
    
    # Output result
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


def run_test_samples(detector: PhishingDetector, samples_file: str, pretty: bool):
    """Run detection on test samples from a JSON file."""
    try:
        with open(samples_file, 'r', encoding='utf-8') as f:
            samples = json.load(f)
        
        results = []
        for i, sample in enumerate(samples, 1):
            print(f"\n{'='*60}")
            print(f"Test Sample {i}: {sample.get('name', 'Unnamed')}")
            print(f"{'='*60}")
            
            result = detector.detect(
                url=sample.get('url'),
                email_subject=sample.get('subject'),
                email_body=sample.get('body')
            )
            
            print(json.dumps(result, indent=2))
            
            results.append({
                'sample': sample.get('name', f'Sample {i}'),
                'expected': sample.get('expected'),
                'result': result
            })
        
        # Summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        
        correct = 0
        for r in results:
            expected = r.get('expected', {}).get('classification')
            actual = r['result']['classification']
            match = expected == actual if expected else 'N/A'
            
            if match == True:
                correct += 1
            
            print(f"{r['sample']}: {actual} (Expected: {expected or 'N/A'}) {'✓' if match == True else '✗' if match == False else ''}")
        
        if any(r.get('expected') for r in results):
            accuracy = (correct / len([r for r in results if r.get('expected')])) * 100
            print(f"\nAccuracy: {accuracy:.1f}%")
    
    except FileNotFoundError:
        print(f"Error: Test samples file '{samples_file}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{samples_file}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
