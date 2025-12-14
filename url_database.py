"""
URL Database - Cache phishing URLs for fast lookup and learning
Uses SQLite for simplicity and portability
"""

import sqlite3
import hashlib
from datetime import datetime
import os

class URLDatabase:
    def __init__(self, db_path='data/url_cache.db'):
        """Initialize database connection"""
        # Create data directory if needed
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create database tables"""
        # URLs table - stores all checked URLs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                url_hash TEXT UNIQUE NOT NULL,
                classification TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                check_count INTEGER DEFAULT 1,
                reasons TEXT
            )
        ''')
        
        # Phishing patterns table - stores known phishing patterns
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phishing_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT UNIQUE NOT NULL,
                pattern_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                match_count INTEGER DEFAULT 0
            )
        ''')
        
        # Create indexes for fast lookup
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_url_hash ON urls(url_hash)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_classification ON urls(classification)')
        
        self.conn.commit()
    
    def get_url_hash(self, url):
        """Generate hash for URL"""
        return hashlib.sha256(url.encode()).hexdigest()
    
    def check_cache(self, url):
        """Check if URL exists in cache"""
        url_hash = self.get_url_hash(url)
        
        self.cursor.execute('''
            SELECT classification, risk_score, reasons, check_count
            FROM urls WHERE url_hash = ?
        ''', (url_hash,))
        
        result = self.cursor.fetchone()
        
        if result:
            # Update check count and last checked
            self.cursor.execute('''
                UPDATE urls 
                SET last_checked = CURRENT_TIMESTAMP,
                    check_count = check_count + 1
                WHERE url_hash = ?
            ''', (url_hash,))
            self.conn.commit()
            
            return {
                'cached': True,
                'classification': result[0],
                'risk_score': result[1],
                'reasons': result[2].split('|') if result[2] else [],
                'check_count': result[3] + 1
            }
        
        return {'cached': False}
    
    def add_url(self, url, classification, risk_score, reasons):
        """Add URL to cache"""
        url_hash = self.get_url_hash(url)
        reasons_str = '|'.join(reasons) if reasons else ''
        
        try:
            self.cursor.execute('''
                INSERT INTO urls (url, url_hash, classification, risk_score, reasons)
                VALUES (?, ?, ?, ?, ?)
            ''', (url, url_hash, classification, risk_score, reasons_str))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # URL already exists, update it
            self.cursor.execute('''
                UPDATE urls 
                SET classification = ?,
                    risk_score = ?,
                    reasons = ?,
                    last_checked = CURRENT_TIMESTAMP,
                    check_count = check_count + 1
                WHERE url_hash = ?
            ''', (classification, risk_score, reasons_str, url_hash))
            self.conn.commit()
            return True
    
    def get_phishing_urls(self, limit=100):
        """Get recent phishing URLs for training"""
        self.cursor.execute('''
            SELECT url, risk_score, reasons, first_seen
            FROM urls
            WHERE classification = 'Phishing'
            ORDER BY first_seen DESC
            LIMIT ?
        ''', (limit,))
        
        return [
            {
                'url': row[0],
                'risk_score': row[1],
                'reasons': row[2].split('|') if row[2] else [],
                'first_seen': row[3]
            }
            for row in self.cursor.fetchall()
        ]
    
    def add_phishing_pattern(self, pattern, pattern_type, confidence):
        """Add new phishing pattern learned from URLs"""
        try:
            self.cursor.execute('''
                INSERT INTO phishing_patterns (pattern, pattern_type, confidence)
                VALUES (?, ?, ?)
            ''', (pattern, pattern_type, confidence))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Pattern exists, update confidence
            self.cursor.execute('''
                UPDATE phishing_patterns
                SET confidence = ?,
                    match_count = match_count + 1
                WHERE pattern = ?
            ''', (confidence, pattern))
            self.conn.commit()
            return True
    
    def get_patterns(self, pattern_type=None):
        """Get learned phishing patterns"""
        if pattern_type:
            self.cursor.execute('''
                SELECT pattern, pattern_type, confidence, match_count
                FROM phishing_patterns
                WHERE pattern_type = ?
                ORDER BY confidence DESC
            ''', (pattern_type,))
        else:
            self.cursor.execute('''
                SELECT pattern, pattern_type, confidence, match_count
                FROM phishing_patterns
                ORDER BY confidence DESC
            ''')
        
        return [
            {
                'pattern': row[0],
                'type': row[1],
                'confidence': row[2],
                'matches': row[3]
            }
            for row in self.cursor.fetchall()
        ]
    
    def get_statistics(self):
        """Get database statistics"""
        stats = {}
        
        # Total URLs
        self.cursor.execute('SELECT COUNT(*) FROM urls')
        stats['total_urls'] = self.cursor.fetchone()[0]
        
        # Phishing URLs
        self.cursor.execute("SELECT COUNT(*) FROM urls WHERE classification = 'Phishing'")
        stats['phishing_urls'] = self.cursor.fetchone()[0]
        
        # Legitimate URLs
        self.cursor.execute("SELECT COUNT(*) FROM urls WHERE classification = 'Legitimate'")
        stats['legitimate_urls'] = self.cursor.fetchone()[0]
        
        # Total patterns
        self.cursor.execute('SELECT COUNT(*) FROM phishing_patterns')
        stats['total_patterns'] = self.cursor.fetchone()[0]
        
        return stats
    
    def close(self):
        """Close database connection"""
        self.conn.close()


# Example usage
if __name__ == '__main__':
    db = URLDatabase()
    
    print("Database initialized!")
    print("\nStatistics:", db.get_statistics())
    
    # Test adding a URL
    db.add_url(
        'http://paypal-verify.tk/login',
        'Phishing',
        85,
        ['Typosquatting', 'Suspicious TLD', 'Login keyword']
    )
    
    print("\nAfter adding URL:", db.get_statistics())
    
    # Test cache check
    cached = db.check_cache('http://paypal-verify.tk/login')
    print("\nCache check:", cached)
    
    db.close()
