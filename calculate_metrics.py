"""
Calculate Model Metrics - Simple Version
Works even if models can't be loaded
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

print("="*70)
print("MODEL PERFORMANCE METRICS")
print("="*70)

# Load test data
print("\n📂 Loading test dataset...")
test_data = pd.read_parquet('datasets/Testing.parquet')
print(f"✅ Loaded {len(test_data)} test samples")

# Prepare data
print("\n🔧 Preparing data...")

# Convert labels
if test_data['status'].dtype == 'object':
    label_mapping = {'legitimate': 0, 'phishing': 1}
    y_test = test_data['status'].map(label_mapping)
else:
    y_test = test_data['status']

# Prepare features
X_test = test_data.drop(columns=['status'])
if 'url' in X_test.columns:
    X_test = X_test.drop(columns=['url'])

# Convert to numeric
for col in X_test.columns:
    X_test[col] = pd.to_numeric(X_test[col], errors='coerce')
X_test = X_test.fillna(0)

print(f"✅ Features: {X_test.shape[1]}")
print(f"✅ Test samples: {X_test.shape[0]}")

# Load training data to retrain quickly
print("\n📂 Loading training dataset...")
train_data = pd.read_parquet('datasets/Training.parquet')

if train_data['status'].dtype == 'object':
    y_train = train_data['status'].map(label_mapping)
else:
    y_train = train_data['status']

X_train = train_data.drop(columns=['status'])
if 'url' in X_train.columns:
    X_train = X_train.drop(columns=['url'])

for col in X_train.columns:
    X_train[col] = pd.to_numeric(X_train[col], errors='coerce')
X_train = X_train.fillna(0)

print(f"✅ Training samples: {X_train.shape[0]}")

# Train models quickly
print("\n🔧 Training models for evaluation...")

print("   Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

print("   Training Neural Network...")
mlp_model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=300, random_state=42)
mlp_model.fit(X_train, y_train)

print("✅ Models trained")

# Evaluate models
models = {
    'Random Forest': rf_model,
    'Neural Network (MLP)': mlp_model
}

print("\n" + "="*70)
print("EVALUATION RESULTS")
print("="*70)

all_metrics = []

for model_name, model in models.items():
    print(f"\n{'='*70}")
    print(f"📊 {model_name.upper()}")
    print(f"{'='*70}")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary')
    f1 = f1_score(y_test, y_pred, average='binary')
    
    # Store for comparison
    all_metrics.append({
        'Model': model_name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1
    })
    
    # Display metrics
    print(f"\n📈 Performance Metrics:")
    print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"   F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n📊 Confusion Matrix:")
    print(f"                 Predicted")
    print(f"                 Legit  Phish")
    print(f"   Actual Legit  {cm[0][0]:5d}  {cm[0][1]:5d}")
    print(f"          Phish  {cm[1][0]:5d}  {cm[1][1]:5d}")
    
    # Detailed breakdown
    tn, fp, fn, tp = cm.ravel()
    print(f"\n📌 Detailed Breakdown:")
    print(f"   True Positives (TP):  {tp:5d} - Correctly identified phishing")
    print(f"   True Negatives (TN):  {tn:5d} - Correctly identified legitimate")
    print(f"   False Positives (FP): {fp:5d} - Legitimate marked as phishing")
    print(f"   False Negatives (FN): {fn:5d} - Phishing marked as legitimate")
    
    # Classification Report
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))

# Comparison table
print("\n" + "="*70)
print("MODEL COMPARISON")
print("="*70)

comparison_df = pd.DataFrame(all_metrics)
print("\n" + comparison_df.to_string(index=False, float_format=lambda x: f'{x:.4f}'))

# Best model
best_model = max(all_metrics, key=lambda x: x['F1-Score'])
print(f"\n🏆 Best Model: {best_model['Model']}")
print(f"   F1-Score: {best_model['F1-Score']:.4f} ({best_model['F1-Score']*100:.2f}%)")

print("\n" + "="*70)
print("✅ Metrics calculation complete!")
print("="*70)
