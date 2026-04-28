"""
Visionerr Fraud Guard - Machine Learning Model
Scikit-learn Random Forest Classifier for fraud detection
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

class MLFraudDetector:
    """Machine Learning based fraud detection using Random Forest"""
    
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = None
        self.scaler = None
        
    def load_data(self, csv_path):
        """Load invoice data from CSV"""
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded {len(df)} invoices from {csv_path}")
        print(f"✓ Fraud rate: {df['is_fraud'].sum()} frauds ({df['is_fraud'].mean()*100:.1f}%)")
        return df
    
    def prepare_features(self, df):
        """Prepare features for ML model"""
        df_copy = df.copy()
        
        # Feature engineering
        df_copy['amount_log'] = np.log1p(df_copy['amount'])
        df_copy['days_to_pay_normalized'] = (df_copy['days_to_pay'] - df_copy['days_to_pay'].mean()) / df_copy['days_to_pay'].std()
        df_copy['is_high_amount'] = (df_copy['amount'] > df_copy['amount'].quantile(0.75)).astype(int)
        df_copy['is_unusual_days'] = (df_copy['days_to_pay'] > 90).astype(int)
        df_copy['no_previous_invoices'] = (df_copy['previous_invoices'] == 0).astype(int)
        
        # Encode categorical variables
        categorical_features = ['category', 'status']
        for col in categorical_features:
            le = LabelEncoder()
            df_copy[col + '_encoded'] = le.fit_transform(df_copy[col])
            self.label_encoders[col] = le
        
        # Select features for model
        feature_cols = [
            'amount', 'days_to_pay', 'previous_invoices',
            'amount_log', 'days_to_pay_normalized', 
            'is_high_amount', 'is_unusual_days', 'no_previous_invoices',
            'category_encoded', 'status_encoded'
        ]
        
        self.feature_columns = feature_cols
        X = df_copy[feature_cols]
        y = df_copy['is_fraud']
        
        print(f"✓ Features prepared: {len(feature_cols)} features")
        return X, y, feature_cols
    
    def train(self, csv_path, test_size=0.2, random_state=42):
        """Train Random Forest model"""
        print("\n" + "="*70)
        print("TRAINING ML FRAUD DETECTOR (RANDOM FOREST)")
        print("="*70)
        
        # Load and prepare data
        df = self.load_data(csv_path)
        X, y, features = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"\n[SPLIT] Train: {len(X_train)} | Test: {len(X_test)}")
        print(f"[TRAIN FRAUD RATE] {y_train.mean()*100:.1f}%")
        print(f"[TEST FRAUD RATE] {y_test.mean()*100:.1f}%")
        
        # Train Random Forest
        print("\n[TRAINING] Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
            class_weight='balanced'  # Handle imbalanced data
        )
        
        self.model.fit(X_train, y_train)
        print("✓ Model trained successfully!")
        
        # Evaluate
        print("\n" + "="*70)
        print("MODEL PERFORMANCE")
        print("="*70)
        
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        print(f"\n[ACCURACY]  {accuracy*100:.1f}%")
        print(f"[PRECISION] {precision*100:.1f}%")
        print(f"[RECALL]    {recall*100:.1f}%")
        print(f"[F1-SCORE]  {f1*100:.1f}%")
        
        print("\n[CONFUSION MATRIX]")
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        print(f"  True Negatives:  {tn}")
        print(f"  False Positives: {fp}")
        print(f"  False Negatives: {fn}")
        print(f"  True Positives:  {tp}")
        
        print("\n[CLASSIFICATION REPORT]")
        print(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))
        
        # Feature importance
        print("\n[TOP 5 IMPORTANT FEATURES]")
        importances = pd.DataFrame({
            'feature': features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in importances.head(5).iterrows():
            print(f"  {row['feature']:.<30} {row['importance']*100:>6.2f}%")
        
        print("\n" + "="*70)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'model': self.model,
            'X_test': X_test,
            'y_test': y_test,
            'y_pred': y_pred
        }
    
    def predict(self, X):
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get probability predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        return self.model.predict_proba(X)
    
    def save_model(self, filepath):
        """Save model to pickle file"""
        if self.model is None:
            raise ValueError("No model to save")
        
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"✓ Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load model from pickle file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        print(f"✓ Model loaded from {filepath}")
        return self


def main():
    """Train and save the ML model"""
    # Get data path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'demo_invoices.csv')
    model_path = os.path.join(script_dir, 'fraud_detector_ml.pkl')
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found!")
        return
    
    # Train model
    detector = MLFraudDetector()
    results = detector.train(csv_path)
    
    # Save model
    detector.save_model(model_path)
    
    print(f"\n✓ ML Model training complete!")
    print(f"  Model file: {model_path}")
    print(f"\n[COMPARISON]")
    print(f"  Rule-based Recall:    42.4%")
    print(f"  ML Model Recall:      {results['recall']*100:.1f}%")
    print(f"  Improvement:          {(results['recall']*100 - 42.4):.1f}% points")


if __name__ == "__main__":
    main()
