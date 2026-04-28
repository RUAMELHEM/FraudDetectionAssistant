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

# Add parent directory to path for model imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))

from fraud_detector_final import FraudDetectorFinal

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Visionerr Fraud Guard API",
    description="AI-powered fraud detection for freelancers",
    version="1.0.0"
)

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
        
        # Detect
        detector = FraudDetectorFinal(df)
        results = detector.detect_all()
        
        if not results:
            raise HTTPException(status_code=400, detail="Detection failed")
        
        result = results[0]
        
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
            details=alerts
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
        
        # Detect
        detector = FraudDetectorFinal(df)
        results = detector.detect_all()
        
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
        "model": {
            "version": "1.0.0",
            "name": "Fraud Detector Final",
            "rules": 9,
            "performance": {
                "precision": "100%",
                "recall": "42.4%",
                "f1_score": "59.4%"
            }
        },
        "deployment": {
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
    }

# ===== ERROR HANDLERS =====

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
    print("🚀 STARTING VISIONERR FRAUD GUARD API")
    print("="*70)
    print("📍 Server: http://127.0.0.1:8000")
    print("📚 Docs:   http://127.0.0.1:8000/docs")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
