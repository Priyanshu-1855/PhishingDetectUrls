"""
Train ML models using the parquet dataset files
Includes all 53 features: 24 base + 13 NER + 8 CV + 8 OCR
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from datetime import datetime

print("="*70)
print("PHISHING DETECTION MODEL TRAINING")
print("="*70)

# Load datasets
print("\n1. Loading datasets...")
try:
    train_df = pd.read_parquet('datasets/Training.parquet')
    test_df = pd.read_parquet('datasets/Testing.parquet')
    
    print(f"   Training data: {train_df.shape[0]} samples")
    print(f"   Testing data: {test_df.shape[0]} samples")
    print(f"   Features: {train_df.shape[1] - 1}")  # -1 for label column
    
except Exception as e:
    print(f"   Error loading parquet files: {e}")
    print("   Trying to generate new dataset...")
    
    from dataset_generator import DatasetGenerator
    generator = DatasetGenerator()
    
    # Generate training data
    print("   Generating 1000 training samples...")
    train_data = generator.generate_dataset(num_samples=1000)
    
    # Generate testing data
    print("   Generating 200 testing samples...")
    test_data = generator.generate_dataset(num_samples=200)
    
    # Save as JSON for now
    import json
    with open('datasets/training_data.json', 'w') as f:
        json.dump(train_data, f, indent=2)
    with open('datasets/testing_data.json', 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print("   Datasets generated and saved!")
    print("   Now train with: python ml_trainer.py --data datasets/training_data.json")
    exit(0)

# Prepare data
print("\n2. Preparing features...")

# The dataset has 'status' column as label (legitimate=0, phishing=1)
# and 'url' column which is a string (need to drop it)

# Drop string columns (url and any other object type columns)
string_columns = train_df.select_dtypes(include=['object']).columns.tolist()
print(f"   Dropping string columns: {string_columns}")

# Separate features and labels
if 'status' in train_df.columns:
    y_train = train_df['status']
    y_test = test_df['status']
    
    # Convert string labels to numeric: legitimate=0, phishing=1
    print(f"   Converting labels: legitimate → 0, phishing → 1")
    y_train = (y_train == 'phishing').astype(int)
    y_test = (y_test == 'phishing').astype(int)
    
    X_train = train_df.drop(['status'] + string_columns, axis=1, errors='ignore')
    X_test = test_df.drop(['status'] + string_columns, axis=1, errors='ignore')
else:
    print("   Error: 'status' column not found!")
    exit(1)

print(f"   Training features shape: {X_train.shape}")
print(f"   Training labels shape: {y_train.shape}")
print(f"   Class distribution: Legitimate={sum(y_train==0)}, Phishing={sum(y_train==1)}")

# Convert all columns to numeric, coercing errors to NaN
print("\n   Converting all features to numeric...")
for col in X_train.columns:
    X_train[col] = pd.to_numeric(X_train[col], errors='coerce')
    X_test[col] = pd.to_numeric(X_test[col], errors='coerce')

# Handle missing values
X_train = X_train.fillna(0)
X_test = X_test.fillna(0)

# Train Random Forest
print("\n3. Training Random Forest Classifier...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)
print("   ✓ Random Forest trained")

# Evaluate Random Forest
y_pred_rf = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred_rf)

print(f"\n   Random Forest Accuracy: {rf_accuracy:.4f}")
print("\n   Classification Report:")
print(classification_report(y_test, y_pred_rf, target_names=['Legitimate', 'Phishing']))

# Train Neural Network
print("\n4. Training Neural Network (MLP)...")
mlp_model = MLPClassifier(
    hidden_layer_sizes=(100, 50),
    max_iter=500,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1
)

mlp_model.fit(X_train, y_train)
print("   ✓ Neural Network trained")

# Evaluate MLP
y_pred_mlp = mlp_model.predict(X_test)
mlp_accuracy = accuracy_score(y_test, y_pred_mlp)

print(f"\n   MLP Accuracy: {mlp_accuracy:.4f}")
print("\n   Classification Report:")
print(classification_report(y_test, y_pred_mlp, target_names=['Legitimate', 'Phishing']))

# Save models
print("\n5. Saving models...")
models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

rf_path = os.path.join(models_dir, f'random_forest_{timestamp}.pkl')
mlp_path = os.path.join(models_dir, f'mlp_{timestamp}.pkl')

joblib.dump(rf_model, rf_path)
joblib.dump(mlp_model, mlp_path)

# Also save as default models
joblib.dump(rf_model, os.path.join(models_dir, 'random_forest.pkl'))
joblib.dump(mlp_model, os.path.join(models_dir, 'mlp.pkl'))

print(f"   ✓ Random Forest saved: {rf_path}")
print(f"   ✓ MLP saved: {mlp_path}")

# Feature importance (Random Forest)
if hasattr(X_train, 'columns'):
    print("\n6. Top 10 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        print(f"   {row['feature']}: {row['importance']:.4f}")

# Summary
print("\n" + "="*70)
print("TRAINING COMPLETE!")
print("="*70)
print(f"\nRandom Forest Accuracy: {rf_accuracy:.2%}")
print(f"Neural Network Accuracy: {mlp_accuracy:.2%}")
print(f"\nModels saved in: {models_dir}/")
print("\nYou can now use these models in the API for predictions!")
print("="*70)
