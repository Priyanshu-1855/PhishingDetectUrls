"""
ML Predictor Module
Loads trained ML models and provides ensemble predictions.
"""

import os
import numpy as np
import joblib
from typing import Dict, Optional, Tuple
from url_analyzer import URLAnalyzer
from email_analyzer import EmailAnalyzer


class MLPredictor:
    """ML-based phishing prediction with ensemble methods."""
    
    def __init__(self, models_dir: str = 'models'):
        self.models_dir = models_dir
        self.url_analyzer = URLAnalyzer()
        self.email_analyzer = EmailAnalyzer()
        self.rf_model = None
        self.nn_model = None
        self.models_loaded = False
        
        # Try to load models
        self._load_models()
    
    def _load_models(self):
        """Load trained models from disk."""
        rf_path = os.path.join(self.models_dir, 'random_forest.pkl')
        nn_path = os.path.join(self.models_dir, 'neural_network.pkl')
        
        try:
            if os.path.exists(rf_path):
                self.rf_model = joblib.load(rf_path)
                print(f"Loaded Random Forest model from {rf_path}")
            
            if os.path.exists(nn_path):
                self.nn_model = joblib.load(nn_path)
                print(f"Loaded Neural Network model from {nn_path}")
            
            if self.rf_model or self.nn_model:
                self.models_loaded = True
        except Exception as e:
            print(f"Warning: Could not load ML models: {e}")
            self.models_loaded = False
    
    def extract_features(self, url: Optional[str], email_subject: Optional[str], email_body: Optional[str]) -> np.array:
        """Extract features for ML prediction."""
        features = []
        
        # URL features
        if url:
            url_score, url_indicators = self.url_analyzer.analyze(url)
            url_features = self.url_analyzer.get_features()
            
            features.extend([
                1 if url_features.get('has_ip') else 0,
                1 if url_features.get('has_at_symbol') else 0,
                1 if url_features.get('long_url') else 0,
                1 if url_features.get('excessive_subdomains') else 0,
                1 if url_features.get('suspicious_tld') else 0,
                1 if url_features.get('no_https') else 0,
                1 if url_features.get('suspicious_keyword') else 0,
                1 if url_features.get('brand_mismatch') else 0,
                1 if url_features.get('excessive_hyphens') else 0,
                1 if url_features.get('port_number') else 0,
                1 if url_features.get('shortened_url') else 0,
            ])
            
            features.append(url_score / 100.0)
            features.append(min(len(url) / 200.0, 1.0))
        else:
            features.extend([0] * 13)
        
        # Email features
        if email_subject or email_body:
            email_score, email_indicators = self.email_analyzer.analyze(
                email_subject or '',
                email_body or ''
            )
            email_features = self.email_analyzer.get_features()
            
            features.extend([
                1 if email_features.get('urgency_language') else 0,
                1 if email_features.get('sensitive_info_request') else 0,
                1 if email_features.get('impersonation') else 0,
                1 if email_features.get('grammar_errors') else 0,
                1 if email_features.get('ai_generated') else 0,
                1 if email_features.get('embedded_link') else 0,
                1 if email_features.get('link_mismatch') else 0,
                1 if email_features.get('no_personalization') else 0,
            ])
            
            features.append(email_score / 100.0)
            
            subject_len = len(email_subject or '')
            body_len = len(email_body or '')
            features.append(min(subject_len / 100.0, 1.0))
            features.append(min(body_len / 1000.0, 1.0))
        else:
            features.extend([0] * 11)
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, url: Optional[str] = None, email_subject: Optional[str] = None, email_body: Optional[str] = None) -> Tuple[float, Dict]:
        """
        Predict phishing probability using ML models.
        
        Args:
            url: URL to analyze
            email_subject: Email subject
            email_body: Email body
            
        Returns:
            Tuple of (phishing_probability, model_info)
        """
        if not self.models_loaded:
            return None, {'error': 'ML models not loaded'}
        
        # Extract features
        features = self.extract_features(url, email_subject, email_body)
        
        predictions = {}
        probabilities = []
        
        # Random Forest prediction
        if self.rf_model:
            rf_prob = self.rf_model.predict_proba(features)[0][1]  # Probability of phishing
            predictions['random_forest'] = {
                'probability': float(rf_prob),
                'prediction': 'Phishing' if rf_prob > 0.5 else 'Legitimate'
            }
            probabilities.append(rf_prob)
        
        # Neural Network prediction
        if self.nn_model:
            nn_prob = self.nn_model.predict_proba(features)[0][1]
            predictions['neural_network'] = {
                'probability': float(nn_prob),
                'prediction': 'Phishing' if nn_prob > 0.5 else 'Legitimate'
            }
            probabilities.append(nn_prob)
        
        # Ensemble prediction (average)
        if probabilities:
            ensemble_prob = np.mean(probabilities)
            predictions['ensemble'] = {
                'probability': float(ensemble_prob),
                'prediction': 'Phishing' if ensemble_prob > 0.5 else 'Legitimate',
                'confidence': 'High' if abs(ensemble_prob - 0.5) > 0.3 else 'Medium' if abs(ensemble_prob - 0.5) > 0.15 else 'Low'
            }
            
            return ensemble_prob, predictions
        
        return None, predictions
    
    def get_ml_score(self, url: Optional[str] = None, email_subject: Optional[str] = None, email_body: Optional[str] = None) -> int:
        """
        Get ML-based risk score (0-100).
        
        Returns:
            Risk score from 0-100, or None if models not available
        """
        prob, info = self.predict(url, email_subject, email_body)
        
        if prob is not None:
            # Convert probability to 0-100 score
            return int(prob * 100)
        
        return None
