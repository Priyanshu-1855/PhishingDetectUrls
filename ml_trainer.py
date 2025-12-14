"""
ML Training Pipeline
Trains Random Forest and Neural Network models for phishing detection.
"""

import json
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from url_analyzer import URLAnalyzer
from email_analyzer import EmailAnalyzer

# Import NLP and CV modules
try:
    from nlp.ner_analyzer import NERAnalyzer
    NER_AVAILABLE = True
except ImportError:
    print("Warning: NER analyzer not available. Install spacy and run: python -m spacy download en_core_web_sm")
    NER_AVAILABLE = False

try:
    from vision.screenshot_analyzer import ScreenshotAnalyzer
    CV_AVAILABLE = True
except ImportError:
    print("Warning: Screenshot analyzer not available. Install opencv-python, Pillow, imagehash, scikit-image")
    CV_AVAILABLE = False


class MLTrainer:
    """ML model training pipeline."""
    
    def __init__(self, use_ner: bool = True, use_cv: bool = False):
        self.url_analyzer = URLAnalyzer()
        self.email_analyzer = EmailAnalyzer()
        
        # Initialize NER analyzer if available and requested
        self.use_ner = use_ner and NER_AVAILABLE
        if self.use_ner:
            self.ner_analyzer = NERAnalyzer()
            print("NER analyzer enabled")
        else:
            self.ner_analyzer = None
        
        # Initialize CV analyzer if available and requested
        self.use_cv = use_cv and CV_AVAILABLE
        if self.use_cv:
            self.cv_analyzer = ScreenshotAnalyzer()
            print("Screenshot analyzer enabled")
        else:
            self.cv_analyzer = None
        
        self.rf_model = None
        self.nn_model = None
        self.feature_names = []
    
    def extract_features(self, sample: dict) -> np.array:
        """
        Extract features from a sample for ML training.
        
        Args:
            sample: Dictionary with 'url', 'subject', 'body'
            
        Returns:
            Feature vector as numpy array
        """
        features = []
        
        # URL features
        if sample.get('url'):
            url_score, url_indicators = self.url_analyzer.analyze(sample['url'])
            url_features = self.url_analyzer.get_features()
            
            # Binary features from URL analysis
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
            
            # URL score as feature
            features.append(url_score / 100.0)  # Normalize to 0-1
            
            # URL length
            features.append(min(len(sample['url']) / 200.0, 1.0))  # Normalize
        else:
            features.extend([0] * 13)
        
        # Email features
        if sample.get('subject') or sample.get('body'):
            email_score, email_indicators = self.email_analyzer.analyze(
                sample.get('subject', ''),
                sample.get('body', '')
            )
            email_features = self.email_analyzer.get_features()
            
            # Binary features from email analysis
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
            
            # Email score as feature
            features.append(email_score / 100.0)  # Normalize to 0-1
            
            # Text length features
            subject_len = len(sample.get('subject', ''))
            body_len = len(sample.get('body', ''))
            features.append(min(subject_len / 100.0, 1.0))  # Normalize
            features.append(min(body_len / 1000.0, 1.0))  # Normalize
        else:
            features.extend([0] * 11)
        
        # NER features (if enabled)
        if self.use_ner and (sample.get('subject') or sample.get('body')):
            try:
                ner_score, ner_indicators, entities = self.ner_analyzer.analyze(
                    sample.get('subject', ''),
                    sample.get('body', ''),
                    sample.get('url', '')
                )
                ner_features = self.ner_analyzer.get_features()
                
                # NER binary features
                features.extend([
                    1 if ner_features.get('brand_entity_mismatch') else 0,
                    1 if ner_features.get('multiple_orgs') else 0,
                    1 if ner_features.get('has_money_entity') else 0,
                    1 if ner_features.get('multiple_money_mentions') else 0,
                    1 if ner_features.get('has_person_entity') else 0,
                    1 if ner_features.get('has_location_entity') else 0,
                    1 if ner_features.get('suspicious_location_context') else 0,
                    1 if ner_features.get('suspicious_entity_pattern') else 0,
                ])
                
                # NER count features (normalized)
                features.extend([
                    min(ner_features.get('person_entity_count', 0) / 5.0, 1.0),
                    min(ner_features.get('org_entity_count', 0) / 5.0, 1.0),
                    min(ner_features.get('money_entity_count', 0) / 3.0, 1.0),
                    min(ner_features.get('location_entity_count', 0) / 5.0, 1.0),
                ])
                
                # NER score as feature
                features.append(min(ner_score / 100.0, 1.0))
            except Exception as e:
                print(f"Error extracting NER features: {e}")
                features.extend([0] * 13)  # 8 binary + 4 count + 1 score
        elif self.use_ner:
            features.extend([0] * 13)
        
        # CV features (if enabled and screenshot available)
        if self.use_cv and sample.get('screenshot'):
            try:
                cv_score, cv_indicators = self.cv_analyzer.analyze(
                    sample['screenshot'],
                    sample.get('reference_screenshots')
                )
                cv_features = self.cv_analyzer.get_features()
                
                # CV features
                features.extend([
                    cv_features.get('edge_density', 0.0),
                    cv_features.get('max_reference_similarity', 0.0),
                    cv_features.get('template_match_score', 0.0),
                    1 if cv_features.get('excessive_warning_colors') else 0,
                    1 if cv_features.get('simple_layout') else 0,
                    1 if cv_features.get('high_similarity_to_known_site') else 0,
                    1 if cv_features.get('matches_phishing_template') else 0,
                ])
                
                # CV score as feature
                features.append(min(cv_score / 100.0, 1.0))
            except Exception as e:
                print(f"Error extracting CV features: {e}")
                features.extend([0] * 8)  # 3 continuous + 4 binary + 1 score
        elif self.use_cv:
            features.extend([0] * 8)
        
        return np.array(features)
    
    def prepare_dataset(self, data_file: str):
        """
        Load and prepare dataset for training.
        
        Args:
            data_file: Path to JSON dataset file
            
        Returns:
            X (features), y (labels)
        """
        with open(data_file, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        print(f"Loaded {len(dataset)} samples")
        
        X = []
        y = []
        
        for sample in dataset:
            features = self.extract_features(sample)
            X.append(features)
            y.append(sample['label'])
        
        return np.array(X), np.array(y)
    
    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train Random Forest classifier."""
        print("\n" + "="*60)
        print("Training Random Forest Classifier")
        print("="*60)
        
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.rf_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.rf_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nAccuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Cross-validation
        cv_scores = cross_val_score(self.rf_model, X_train, y_train, cv=5)
        print(f"\nCross-validation scores: {cv_scores}")
        print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Feature importance
        feature_importance = self.rf_model.feature_importances_
        print("\nTop 10 Most Important Features:")
        indices = np.argsort(feature_importance)[::-1][:10]
        for i, idx in enumerate(indices, 1):
            print(f"{i}. Feature {idx}: {feature_importance[idx]:.4f}")
        
        return self.rf_model
    
    def train_neural_network(self, X_train, y_train, X_test, y_test):
        """Train Neural Network (MLP) classifier."""
        print("\n" + "="*60)
        print("Training Neural Network (MLP) Classifier")
        print("="*60)
        
        self.nn_model = MLPClassifier(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            solver='adam',
            alpha=0.0001,
            batch_size=32,
            learning_rate='adaptive',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        
        self.nn_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.nn_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nAccuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return self.nn_model
    
    def save_models(self, models_dir: str = 'models'):
        """Save trained models to disk."""
        os.makedirs(models_dir, exist_ok=True)
        
        if self.rf_model:
            joblib.dump(self.rf_model, os.path.join(models_dir, 'random_forest.pkl'))
            print(f"\nRandom Forest model saved to {models_dir}/random_forest.pkl")
        
        if self.nn_model:
            joblib.dump(self.nn_model, os.path.join(models_dir, 'neural_network.pkl'))
            print(f"Neural Network model saved to {models_dir}/neural_network.pkl")
    
    def train_all(self, data_file: str, test_size: float = 0.2):
        """Train all models."""
        # Prepare data
        X, y = self.prepare_dataset(data_file)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Train models
        self.train_random_forest(X_train, y_train, X_test, y_test)
        self.train_neural_network(X_train, y_train, X_test, y_test)
        
        # Save models
        self.save_models()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train ML models for phishing detection")
    parser.add_argument('--data', type=str, default='training_data.json', help='Training data file')
    parser.add_argument('--test-size', type=float, default=0.2, help='Test set size (0.0-1.0)')
    
    args = parser.parse_args()
    
    trainer = MLTrainer()
    trainer.train_all(args.data, args.test_size)
