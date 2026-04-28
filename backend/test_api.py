"""
ADIM 6: TEST API
- Health check
- Single invoice detection
- Bulk detection
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint"""
    print("\n🧪 TEST: Health Check")
    try:
        # Note: This will fail if API isn't running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"   Response: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("   ⚠️  API not running - start with: python api.py")
        return None

def test_single_invoice():
    """Test single invoice detection"""
    print("\n🧪 TEST: Single Invoice Detection")
    
    invoice = {
        "invoice_id": "INV_TEST_001",
        "customer_id": "CUST_TEST_001",
        "amount": 5000.00,
        "date": "2024-01-15",
        "category": "Web Dev",
        "status": "Unpaid",
        "days_to_pay": 120,
        "previous_invoices": 0
    }
    
    print(f"   Input: {json.dumps(invoice, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/detect/single",
            json=invoice,
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Risk Level: {result.get('risk_level')}")
        print(f"   Risk Score: {result.get('risk_score')}/10")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {str(e)}")
        return None

def test_bulk_invoices():
    """Test bulk invoice detection"""
    print("\n🧪 TEST: Bulk Invoice Detection")
    
    bulk = {
        "invoices": [
            {
                "invoice_id": "INV_BULK_001",
                "customer_id": "CUST_BULK_001",
                "amount": 1500.00,
                "date": "2024-01-10",
                "category": "Web Dev",
                "status": "Paid",
                "days_to_pay": 10,
                "previous_invoices": 5
            },
            {
                "invoice_id": "INV_BULK_002",
                "customer_id": "CUST_BULK_002",
                "amount": 5000.00,
                "date": "2024-01-05",
                "category": "Consulting",
                "status": "Unpaid",
                "days_to_pay": 90,
                "previous_invoices": 0
            }
        ]
    }
    
    print(f"   Invoices: {len(bulk['invoices'])}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/detect/bulk",
            json=bulk,
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   HIGH Risk: {result['high_risk_count']}")
        print(f"   MEDIUM Risk: {result['medium_risk_count']}")
        print(f"   LOW Risk: {result['low_risk_count']}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("="*70)
    print("🧪 API TEST SUITE")
    print("="*70)
    print("\n⚠️  Make sure API is running first:")
    print("   cd c:\\Users\\rua\\OneDrive\\Desktop\\salam_hack\\backend")
    print("   python -m uvicorn api:app --reload")
    print("\nOr in backend directory:")
    print("   python api.py")
    print("\nThen run this test in another terminal:")
    print("="*70)
    
    # Try health check
    health = test_health()
    
    if health is None:
        print("\n❌ API IS NOT RUNNING")
        print("\nTo start API:")
        print("  cd backend")
        print("  python api.py")
        print("\nThen access:")
        print("  Browser: http://127.0.0.1:8000/docs (for interactive docs)")
        print("  API: http://127.0.0.1:8000")
    elif health:
        print("   ✅ PASS: API is running")
        test_single_invoice()
        test_bulk_invoices()
    
    print("\n" + "="*70)
