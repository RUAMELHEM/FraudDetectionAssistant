# 🚀 Visionerr Fraud Guard - Backend API

## Quick Start

### 1. Start API Server
```bash
cd backend
python api.py
```

### 2. Access Documentation
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **API Endpoint**: http://127.0.0.1:8000
- **Health Check**: http://127.0.0.1:8000/health

## API Endpoints

### 1. Health Check
```
GET /health
```
Check if API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "Fraud Detector API"
}
```

---

### 2. Detect Single Invoice
```
POST /detect/single
```

Analyze a single invoice for fraud indicators.

**Request:**
```json
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

**Response:**
```json
{
  "invoice_id": "INV001",
  "customer_id": "CUST001",
  "amount": 1500.50,
  "status": "Paid",
  "days_to_pay": 12,
  "risk_score": 3.0,
  "risk_level": "MEDIUM",
  "high_alerts": 0,
  "medium_alerts": 1,
  "alert_count": 1,
  "details": [
    {
      "rule": "Round Numbers",
      "severity": "MEDIUM",
      "reason": "Exact round: $1500.00"
    }
  ]
}
```

---

### 3. Bulk Invoice Detection
```
POST /detect/bulk
```

Analyze multiple invoices at once.

**Request:**
```json
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
    {
      "invoice_id": "INV002",
      "customer_id": "CUST002",
      "amount": 5000.00,
      "date": "2024-01-10",
      "category": "Consulting",
      "status": "Unpaid",
      "days_to_pay": 90,
      "previous_invoices": 0
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-01-15T10:35:20.123456",
  "total_invoices": 2,
  "high_risk_count": 1,
  "medium_risk_count": 1,
  "low_risk_count": 0,
  "results": [
    {
      "invoice_id": "INV001",
      "customer_id": "CUST001",
      "amount": 1500.50,
      "risk_level": "MEDIUM",
      "risk_score": 3.0,
      "details": [...]
    },
    {
      "invoice_id": "INV002",
      "customer_id": "CUST002",
      "amount": 5000.00,
      "risk_level": "HIGH",
      "risk_score": 7.0,
      "details": [...]
    }
  ],
  "summary": {
    "total": 2,
    "high_risk": 1,
    "medium_risk": 1,
    "low_risk": 0,
    "high_risk_percentage": "50.0%"
  }
}
```

---

### 4. Model Statistics
```
GET /stats
```

Get model performance metrics.

**Response:**
```json
{
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
    "timestamp": "2024-01-15T10:30:00.123456",
    "status": "active"
  }
}
```

---

## Risk Levels

| Level | Score | Meaning |
|-------|-------|---------|
| 🔴 HIGH | 6-10 | High fraud probability - Manual review needed |
| 🟠 MEDIUM | 3-5 | Medium risk - Monitor closely |
| 🟢 LOW | 0-2 | Normal - No action needed |

---

## Detection Rules (9 Rules)

### HIGH Severity Rules (3 points each)
1. **Duplicate Billing** - Same amount from same customer
2. **Missing Documentation** - Unpaid for 60+ days
3. **Combined Patterns** - New customer + High amount + Unpaid

### MEDIUM Severity Rules (1 point each)
4. **Round Numbers** - Suspiciously round amounts ($1000, $2000)
5. **High Velocity** - Too many invoices (4+) from one customer
6. **New High-Value** - New customer with high invoice ($3500+)
7. **Unusual Timing** - Anomalous payment delays (IQR-based)
8. **Frequency Anomaly** - Multiple invoices same day (4+)
9. **Amount Variance** - Unusual variance in customer amounts

---

## Usage Examples

### Python (requests)
```python
import requests

# Single invoice
response = requests.post(
    "http://127.0.0.1:8000/detect/single",
    json={
        "invoice_id": "INV001",
        "customer_id": "CUST001",
        "amount": 1500.50,
        "date": "2024-01-15",
        "category": "Web Dev",
        "status": "Paid",
        "days_to_pay": 12,
        "previous_invoices": 5
    }
)

result = response.json()
print(f"Risk Level: {result['risk_level']}")
print(f"Risk Score: {result['risk_score']}/10")
```

### JavaScript (fetch)
```javascript
// Bulk invoices
fetch('http://127.0.0.1:8000/detect/bulk', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    invoices: [
      {
        invoice_id: 'INV001',
        customer_id: 'CUST001',
        amount: 1500.50,
        date: '2024-01-15',
        category: 'Web Dev',
        status: 'Paid',
        days_to_pay: 12,
        previous_invoices: 5
      }
    ]
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### cURL
```bash
# Health check
curl http://127.0.0.1:8000/health

# Single detection
curl -X POST http://127.0.0.1:8000/detect/single \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": "INV001",
    "customer_id": "CUST001",
    "amount": 1500.50,
    "date": "2024-01-15",
    "category": "Web Dev",
    "status": "Paid",
    "days_to_pay": 12,
    "previous_invoices": 5
  }'
```

---

## Error Handling

All errors return structured JSON responses:

```json
{
  "status": "error",
  "code": 400,
  "message": "Validation error: Missing field: amount",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Common Error Codes
- **400**: Validation error (missing/invalid field)
- **500**: Server error (detection failed)

---

## Configuration

API runs on:
- **Host**: 0.0.0.0 (accessible from anywhere)
- **Port**: 8000
- **CORS**: Enabled for all origins

To change settings, edit `api.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Performance

- **Single Invoice**: ~50ms
- **Bulk (100 invoices)**: ~200ms
- **Bulk (1000 invoices)**: ~2s (max allowed)

---

## Next Steps

1. ✅ API Backend - DONE
2. ⬜ Frontend Dashboard - TODO
3. ⬜ Database Integration - TODO
4. ⬜ Authentication - TODO
5. ⬜ Deployment (Docker) - TODO

---

## Support

For issues or questions, check:
- `http://127.0.0.1:8000/docs` - Interactive API documentation
- `../data/fraud_results_final.json` - Sample output format
- `../README.md` - Project overview
