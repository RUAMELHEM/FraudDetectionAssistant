"""
ADIM 6: FASTAPI BACKEND
- Production-ready API
- JSON input/output
- Error handling
- API documentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import json
import logging
from datetime import datetime
import sys
import os
import pickle
import numpy as np

# Add parent directory to path for model imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))

from fraud_detector_final import FraudDetectorFinal
from fraud_detector_ml import MLFraudDetector

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Visionerr Fraud Guard API",
    description="AI-powered fraud detection for freelancers",
    version="2.0.0"
)

# Load models at startup
ml_detector = None
try:
    ml_detector = MLFraudDetector()
    model_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'fraud_detector_ml.pkl')
    if os.path.exists(model_path):
        ml_detector.load_model(model_path)
        logger.info("âœ“ ML Model loaded successfully")
    else:
        logger.warning("âš  ML Model file not found, using rule-based detection only")
        ml_detector = None
except Exception as e:
    logger.warning(f"âš  Failed to load ML model: {str(e)}")
    ml_detector = None

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODELS =====

class InvoiceInput(BaseModel):
    """Single invoice for detection"""
    invoice_id: str
    customer_id: str
    amount: float
    date: str
    category: str
    status: str
    days_to_pay: int
    previous_invoices: int

class BulkInvoiceInput(BaseModel):
    """Bulk invoices for detection"""
    invoices: List[InvoiceInput]

class FraudAlert(BaseModel):
    """Fraud alert details"""
    rule: str
    severity: str
    reason: str

class DetectionResult(BaseModel):
    """Single invoice detection result"""
    invoice_id: str
    customer_id: str
    amount: float
    status: str
    days_to_pay: int
    risk_score: float
    risk_level: str
    high_alerts: int
    medium_alerts: int
    alert_count: int
    details: List[FraudAlert]
    ml_fraud_probability: Optional[float] = None  # ML model probability
    ml_prediction: Optional[str] = None  # ML model fraud/normal

class BulkDetectionResponse(BaseModel):
    """Bulk detection response"""
    status: str
    timestamp: str
    total_invoices: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    results: List[DetectionResult]
    summary: dict

# ===== HELPER FUNCTIONS =====

def validate_invoice_data(invoice: dict) -> bool:
    """Validate invoice data"""
    required_fields = [
        'invoice_id', 'customer_id', 'amount', 'date',
        'category', 'status', 'days_to_pay', 'previous_invoices'
    ]
    
    for field in required_fields:
        if field not in invoice:
            raise ValueError(f"Missing field: {field}")
    
    # Type validation
    if not isinstance(invoice['amount'], (int, float)) or invoice['amount'] <= 0:
        raise ValueError("Amount must be positive number")
    
    if invoice['days_to_pay'] < 0:
        raise ValueError("days_to_pay cannot be negative")
    
    if invoice['previous_invoices'] < 0:
        raise ValueError("previous_invoices cannot be negative")
    
    return True

# ===== ENDPOINTS =====

@app.get("/", tags=["Info"])
def read_root():
    """API health check"""
    return {
        "service": "Visionerr Fraud Guard",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "single": "/detect/single",
            "bulk": "/detect/bulk",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Info"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Fraud Detector API"
    }

@app.post("/detect/single", response_model=DetectionResult, tags=["Detection"])
def detect_single_invoice(invoice: InvoiceInput):
    """
    Detect fraud for single invoice
    Uses both rule-based and ML models for detection
    
    Example:
    ```
    {
        "invoice_id": "INV001",
        "customer_id": "CUST001",
        "amount": 1500.50,
        "date": "2024-01-15",
        "category": "Web Dev",
        "status": "Paid",
        "days_to_pay": 12,
        "previous_invoices": 5
    }
    ```
    """
    try:
        # Validate
        validate_invoice_data(invoice.dict())
        
        # Convert to DataFrame
        df = pd.DataFrame([invoice.dict()])
        df['is_fraud'] = 0  # Unknown
        
        # Rule-based detection
        detector = FraudDetectorFinal(df)
        results = detector.detect_all()
        
        if not results:
            raise HTTPException(status_code=400, detail="Detection failed")
        
        result = results[0]
        
        # ML Model detection (if available)
        ml_fraud_prob = None
        ml_prediction = None
        
        if ml_detector is not None:
            try:
                # Prepare features for ML model (same as training)
                df_ml = df.copy()
                df_ml['amount_log'] = np.log1p(df_ml['amount'])
                df_ml['days_to_pay_normalized'] = (df_ml['days_to_pay'] - 47.8) / 41.2  # Using dataset mean/std
                df_ml['is_high_amount'] = (df_ml['amount'] > 4000).astype(int)  # ~75th percentile
                df_ml['is_unusual_days'] = (df_ml['days_to_pay'] > 90).astype(int)
                df_ml['no_previous_invoices'] = (df_ml['previous_invoices'] == 0).astype(int)
                
                # Encode categorical
                from sklearn.preprocessing import LabelEncoder
                le_cat = LabelEncoder()
                le_stat = LabelEncoder()
                
                # Use same encoding as training (Web Dev=0, etc.)
                categories = ['Consulting', 'Content', 'Design', 'Marketing', 'Web Dev']
                statuses = ['Paid', 'Pending', 'Unpaid']
                
                df_ml['category_encoded'] = categories.index(df_ml['category'].iloc[0]) if df_ml['category'].iloc[0] in categories else 0
                df_ml['status_encoded'] = statuses.index(df_ml['status'].iloc[0]) if df_ml['status'].iloc[0] in statuses else 0
                
                # Select features
                feature_cols = [
                    'amount', 'days_to_pay', 'previous_invoices',
                    'amount_log', 'days_to_pay_normalized', 
                    'is_high_amount', 'is_unusual_days', 'no_previous_invoices',
                    'category_encoded', 'status_encoded'
                ]
                
                X_ml = df_ml[feature_cols]
                
                # Predict
                ml_proba = ml_detector.predict_proba(X_ml)
                ml_fraud_prob = float(ml_proba[0][1])  # Probability of fraud
                ml_prediction = "FRAUD" if ml_fraud_prob > 0.5 else "NORMAL"
                
            except Exception as e:
                logger.warning(f"ML prediction error: {str(e)}")
                ml_fraud_prob = None
                ml_prediction = None
        
        # Format response
        alerts = [
            FraudAlert(
                rule=alert['rule'],
                severity=alert['severity'],
                reason=alert['reason']
            )
            for alert in result['details']
        ]
        
        return DetectionResult(
            invoice_id=result['invoice_id'],
            customer_id=result['customer_id'],
            amount=result['amount'],
            status=result['status'],
            days_to_pay=result['days_to_pay'],
            risk_score=result['risk_score'],
            risk_level=result['risk_level'],
            high_alerts=result['high_alerts'],
            medium_alerts=result['medium_alerts'],
            alert_count=result['alert_count'],
            details=alerts,
            ml_fraud_probability=ml_fraud_prob,
            ml_prediction=ml_prediction
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect/bulk", response_model=BulkDetectionResponse, tags=["Detection"])
def detect_bulk_invoices(bulk: BulkInvoiceInput):
    """
    Detect fraud for multiple invoices
    Uses both rule-based and ML models for detection
    
    Example:
    ```
    {
        "invoices": [
            {
                "invoice_id": "INV001",
                "customer_id": "CUST001",
                "amount": 1500.50,
                "date": "2024-01-15",
                "category": "Web Dev",
                "status": "Paid",
                "days_to_pay": 12,
                "previous_invoices": 5
            },
            ...
        ]
    }
    ```
    """
    try:
        if not bulk.invoices:
            raise HTTPException(status_code=400, detail="No invoices provided")
        
        if len(bulk.invoices) > 1000:
            raise HTTPException(status_code=400, detail="Maximum 1000 invoices per request")
        
        # Validate all
        for invoice in bulk.invoices:
            validate_invoice_data(invoice.dict())
        
        # Convert to DataFrame
        df = pd.DataFrame([inv.dict() for inv in bulk.invoices])
        df['is_fraud'] = 0  # Unknown
        
        # Rule-based detection
        detector = FraudDetectorFinal(df)
        results = detector.detect_all()
        
        # ML detection for all invoices (if available)
        ml_proba_list = [None] * len(results)
        ml_pred_list = ["NORMAL"] * len(results)
        
        if ml_detector is not None:
            try:
                from sklearn.preprocessing import LabelEncoder
                
                df_ml = df.copy()
                df_ml['amount_log'] = np.log1p(df_ml['amount'])
                df_ml['days_to_pay_normalized'] = (df_ml['days_to_pay'] - 47.8) / 41.2
                df_ml['is_high_amount'] = (df_ml['amount'] > 4000).astype(int)
                df_ml['is_unusual_days'] = (df_ml['days_to_pay'] > 90).astype(int)
                df_ml['no_previous_invoices'] = (df_ml['previous_invoices'] == 0).astype(int)
                
                categories = ['Consulting', 'Content', 'Design', 'Marketing', 'Web Dev']
                statuses = ['Paid', 'Pending', 'Unpaid']
                
                df_ml['category_encoded'] = df_ml['category'].apply(
                    lambda x: categories.index(x) if x in categories else 0
                )
                df_ml['status_encoded'] = df_ml['status'].apply(
                    lambda x: statuses.index(x) if x in statuses else 0
                )
                
                feature_cols = [
                    'amount', 'days_to_pay', 'previous_invoices',
                    'amount_log', 'days_to_pay_normalized', 
                    'is_high_amount', 'is_unusual_days', 'no_previous_invoices',
                    'category_encoded', 'status_encoded'
                ]
                
                X_ml = df_ml[feature_cols]
                ml_proba = ml_detector.predict_proba(X_ml)
                
                ml_proba_list = [float(p[1]) for p in ml_proba]  # Fraud probability
                ml_pred_list = ["FRAUD" if p > 0.5 else "NORMAL" for p in ml_proba_list]
                
            except Exception as e:
                logger.warning(f"ML prediction error: {str(e)}")
        
        # Format results
        detection_results = []
        for i, result in enumerate(results):
            alerts = [
                FraudAlert(
                    rule=alert['rule'],
                    severity=alert['severity'],
                    reason=alert['reason']
                )
                for alert in result['details']
            ]
            
            detection_results.append(DetectionResult(
                invoice_id=result['invoice_id'],
                customer_id=result['customer_id'],
                amount=result['amount'],
                status=result['status'],
                days_to_pay=result['days_to_pay'],
                risk_score=result['risk_score'],
                risk_level=result['risk_level'],
                high_alerts=result['high_alerts'],
                medium_alerts=result['medium_alerts'],
                alert_count=result['alert_count'],
                details=alerts,
                ml_fraud_probability=ml_proba_list[i],
                ml_prediction=ml_pred_list[i]
            ))
        
        # Calculate summary
        high_count = sum(1 for r in results if r['risk_level'] == 'HIGH')
        medium_count = sum(1 for r in results if r['risk_level'] == 'MEDIUM')
        low_count = sum(1 for r in results if r['risk_level'] == 'LOW')
        
        summary = {
            'total': len(results),
            'high_risk': high_count,
            'medium_risk': medium_count,
            'low_risk': low_count,
            'high_risk_percentage': f"{high_count/len(results)*100:.1f}%",
            'ml_model_active': ml_detector is not None
        }
        
        return BulkDetectionResponse(
            status="success",
            timestamp=datetime.now().isoformat(),
            total_invoices=len(results),
            high_risk_count=high_count,
            medium_risk_count=medium_count,
            low_risk_count=low_count,
            results=detection_results,
            summary=summary
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Bulk detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk detection failed: {str(e)}")
        
        # Format results
        detection_results = []
        for result in results:
            alerts = [
                FraudAlert(
                    rule=alert['rule'],
                    severity=alert['severity'],
                    reason=alert['reason']
                )
                for alert in result['details']
            ]
            
            detection_results.append(DetectionResult(
                invoice_id=result['invoice_id'],
                customer_id=result['customer_id'],
                amount=result['amount'],
                status=result['status'],
                days_to_pay=result['days_to_pay'],
                risk_score=result['risk_score'],
                risk_level=result['risk_level'],
                high_alerts=result['high_alerts'],
                medium_alerts=result['medium_alerts'],
                alert_count=result['alert_count'],
                details=alerts
            ))
        
        # Calculate summary
        high_count = sum(1 for r in results if r['risk_level'] == 'HIGH')
        medium_count = sum(1 for r in results if r['risk_level'] == 'MEDIUM')
        low_count = sum(1 for r in results if r['risk_level'] == 'LOW')
        
        summary = {
            'total': len(results),
            'high_risk': high_count,
            'medium_risk': medium_count,
            'low_risk': low_count,
            'high_risk_percentage': f"{high_count/len(results)*100:.1f}%"
        }
        
        return BulkDetectionResponse(
            status="success",
            timestamp=datetime.now().isoformat(),
            total_invoices=len(results),
            high_risk_count=high_count,
            medium_risk_count=medium_count,
            low_risk_count=low_count,
            results=detection_results,
            summary=summary
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Bulk detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk detection failed: {str(e)}")

@app.get("/stats", tags=["Info"])
def get_stats():
    """Get model statistics"""
    return {
        "api_version": "2.0.0",
        "rule_based_model": {
            "version": "1.0.0",
            "name": "Fraud Detector Final",
            "rules": 9,
            "performance": {
                "precision": "100%",
                "recall": "42.4%",
                "f1_score": "59.4%"
            }
        },
        "ml_model": {
            "active": ml_detector is not None,
            "name": "Random Forest Classifier",
            "performance": {
                "accuracy": "90.5%",
                "precision": "77.8%",
                "recall": "100.0%",
                "f1_score": "87.5%"
            },
            "top_features": [
                "previous_invoices (37.5%)",
                "days_to_pay_normalized (17.6%)",
                "days_to_pay (17.6%)",
                "amount (9.9%)"
            ]
        },
        "deployment": {
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "status": "error",
        "code": exc.status_code,
        "message": exc.detail,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("ðŸš€ STARTING VISIONERR FRAUD GUARD API")
    print("="*70)
    print("ðŸ“ Server: http://127.0.0.1:8000")
    print("ðŸ“š Docs:   http://127.0.0.1:8000/docs")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
