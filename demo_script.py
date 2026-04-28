#!/usr/bin/env python3
"""
Visionerr Fraud Guard - Live Demo Script
Real-time fraud detection API testing
"""

import requests
import json
from datetime import datetime
import time

API_URL = "http://127.0.0.1:8000"

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_result(title, data):
    """Pretty print JSON result"""
    print(f"\n{title}:")
    print(json.dumps(data, indent=2))

def demo_1_health_check():
    """Test 1: Health Check"""
    print_header("DEMO 1: HEALTH CHECK")
    
    try:
        response = requests.get(f"{API_URL}/health")
        print_result("✓ API Health Status", response.json())
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def demo_2_model_stats():
    """Test 2: Model Statistics"""
    print_header("DEMO 2: MODEL STATISTICS")
    
    try:
        response = requests.get(f"{API_URL}/stats")
        stats = response.json()
        
        print("\n[RULE-BASED MODEL]")
        print(f"  Name: {stats['rule_based_model']['name']}")
        print(f"  Rules: {stats['rule_based_model']['rules']}")
        print(f"  Precision: {stats['rule_based_model']['performance']['precision']}")
        print(f"  Recall: {stats['rule_based_model']['performance']['recall']}")
        
        print("\n[ML MODEL]")
        print(f"  Name: {stats['ml_model']['name']}")
        print(f"  Active: {stats['ml_model']['active']}")
        print(f"  Accuracy: {stats['ml_model']['performance']['accuracy']}")
        print(f"  Precision: {stats['ml_model']['performance']['precision']}")
        print(f"  Recall: {stats['ml_model']['performance']['recall']}")
        print(f"  F1-Score: {stats['ml_model']['performance']['f1_score']}")
        
        print("\n[TOP FEATURES]")
        for feature in stats['ml_model']['top_features']:
            print(f"  • {feature}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def demo_3_fraud_detection():
    """Test 3: Fraud Invoice Detection"""
    print_header("DEMO 3: FRAUD INVOICE DETECTION (HIGH RISK)")
    
    invoice = {
        "invoice_id": "DEMO_FRAUD_001",
        "customer_id": "SUSPECT_CORP",
        "amount": 5000,
        "date": "2024-04-28",
        "category": "Web Dev",
        "status": "Unpaid",
        "days_to_pay": 150,
        "previous_invoices": 0
    }
    
    print("\n[INPUT]")
    print(json.dumps(invoice, indent=2))
    
    try:
        start = time.time()
        response = requests.post(f"{API_URL}/detect/single", json=invoice)
        elapsed = time.time() - start
        
        result = response.json()
        
        print(f"\n[RESPONSE TIME] {elapsed*1000:.1f}ms")
        print(f"\n[RISK ASSESSMENT]")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Risk Score: {result['risk_score']}")
        print(f"  Rule-Based Alerts: {result['alert_count']}")
        
        if result.get('ml_fraud_probability'):
            print(f"\n[ML MODEL VERDICT]")
            print(f"  Fraud Probability: {result['ml_fraud_probability']:.1%}")
            print(f"  Prediction: {result['ml_prediction']}")
        
        print(f"\n[DETECTED ALERTS]")
        for alert in result['details']:
            print(f"  [{alert['severity']}] {alert['rule']}")
            print(f"    → {alert['reason']}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def demo_4_normal_detection():
    """Test 4: Normal Invoice Detection"""
    print_header("DEMO 4: NORMAL INVOICE DETECTION (LOW RISK)")
    
    invoice = {
        "invoice_id": "DEMO_NORMAL_001",
        "customer_id": "TRUSTED_CORP",
        "amount": 2000,
        "date": "2024-04-28",
        "category": "Consulting",
        "status": "Paid",
        "days_to_pay": 30,
        "previous_invoices": 5
    }
    
    print("\n[INPUT]")
    print(json.dumps(invoice, indent=2))
    
    try:
        start = time.time()
        response = requests.post(f"{API_URL}/detect/single", json=invoice)
        elapsed = time.time() - start
        
        result = response.json()
        
        print(f"\n[RESPONSE TIME] {elapsed*1000:.1f}ms")
        print(f"\n[RISK ASSESSMENT]")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Risk Score: {result['risk_score']}")
        print(f"  Rule-Based Alerts: {result['alert_count']}")
        
        if result.get('ml_fraud_probability'):
            print(f"\n[ML MODEL VERDICT]")
            print(f"  Fraud Probability: {result['ml_fraud_probability']:.1%}")
            print(f"  Prediction: {result['ml_prediction']}")
        
        if result['details']:
            print(f"\n[DETECTED ALERTS]")
            for alert in result['details']:
                print(f"  [{alert['severity']}] {alert['rule']}")
                print(f"    → {alert['reason']}")
        else:
            print(f"\n✓ No alerts - Invoice appears legitimate")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def demo_5_bulk_detection():
    """Test 5: Bulk Detection"""
    print_header("DEMO 5: BULK DETECTION (10 INVOICES)")
    
    invoices = [
        {"invoice_id": "B001", "customer_id": "C001", "amount": 5000, "date": "2024-04-28", 
         "category": "Web Dev", "status": "Unpaid", "days_to_pay": 120, "previous_invoices": 0},
        {"invoice_id": "B002", "customer_id": "C002", "amount": 2000, "date": "2024-04-28",
         "category": "Consulting", "status": "Paid", "days_to_pay": 30, "previous_invoices": 5},
        {"invoice_id": "B003", "customer_id": "C003", "amount": 1500, "date": "2024-04-28",
         "category": "Design", "status": "Pending", "days_to_pay": 60, "previous_invoices": 2},
        {"invoice_id": "B004", "customer_id": "C004", "amount": 3000, "date": "2024-04-28",
         "category": "Marketing", "status": "Unpaid", "days_to_pay": 95, "previous_invoices": 0},
        {"invoice_id": "B005", "customer_id": "C005", "amount": 1800, "date": "2024-04-28",
         "category": "Content", "status": "Paid", "days_to_pay": 15, "previous_invoices": 10},
        {"invoice_id": "B006", "customer_id": "C006", "amount": 4500, "date": "2024-04-28",
         "category": "Web Dev", "status": "Unpaid", "days_to_pay": 110, "previous_invoices": 0},
        {"invoice_id": "B007", "customer_id": "C007", "amount": 2500, "date": "2024-04-28",
         "category": "Consulting", "status": "Paid", "days_to_pay": 45, "previous_invoices": 3},
        {"invoice_id": "B008", "customer_id": "C008", "amount": 1200, "date": "2024-04-28",
         "category": "Design", "status": "Pending", "days_to_pay": 30, "previous_invoices": 8},
        {"invoice_id": "B009", "customer_id": "C009", "amount": 3500, "date": "2024-04-28",
         "category": "Marketing", "status": "Unpaid", "days_to_pay": 150, "previous_invoices": 1},
        {"invoice_id": "B010", "customer_id": "C010", "amount": 2200, "date": "2024-04-28",
         "category": "Content", "status": "Paid", "days_to_pay": 20, "previous_invoices": 6},
    ]
    
    print(f"\n[PROCESSING] {len(invoices)} invoices...")
    
    try:
        start = time.time()
        response = requests.post(f"{API_URL}/detect/bulk", json={"invoices": invoices})
        elapsed = time.time() - start
        
        result = response.json()
        
        print(f"\n[RESPONSE TIME] {elapsed*1000:.1f}ms ({len(invoices)} invoices)")
        print(f"\n[SUMMARY STATISTICS]")
        print(f"  Total Invoices: {result['total_invoices']}")
        print(f"  High Risk: {result['high_risk_count']} invoices")
        print(f"  Medium Risk: {result['medium_risk_count']} invoices")
        print(f"  Low Risk: {result['low_risk_count']} invoices")
        print(f"  ML Model Active: {result['summary'].get('ml_model_active', 'N/A')}")
        
        print(f"\n[RESULTS BY RISK LEVEL]")
        
        high_risk = [r for r in result['results'] if r['risk_level'] == 'HIGH']
        if high_risk:
            print(f"\n  🔴 HIGH RISK ({len(high_risk)}):")
            for r in high_risk:
                print(f"     {r['invoice_id']}: ${r['amount']} - {r['alert_count']} alerts")
        
        medium_risk = [r for r in result['results'] if r['risk_level'] == 'MEDIUM']
        if medium_risk:
            print(f"\n  🟡 MEDIUM RISK ({len(medium_risk)}):")
            for r in medium_risk:
                print(f"     {r['invoice_id']}: ${r['amount']} - {r['alert_count']} alerts")
        
        low_risk = [r for r in result['results'] if r['risk_level'] == 'LOW']
        if low_risk:
            print(f"\n  🟢 LOW RISK ({len(low_risk)}):")
            for r in low_risk:
                print(f"     {r['invoice_id']}: ${r['amount']} - {r['alert_count']} alerts")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def demo_6_performance():
    """Test 6: Performance Benchmark"""
    print_header("DEMO 6: PERFORMANCE BENCHMARK")
    
    invoice = {
        "invoice_id": "PERF_TEST",
        "customer_id": "PERF_CUST",
        "amount": 2500,
        "date": "2024-04-28",
        "category": "Web Dev",
        "status": "Paid",
        "days_to_pay": 45,
        "previous_invoices": 3
    }
    
    print("\n[BENCHMARKING] 100 sequential requests...")
    
    try:
        times = []
        for i in range(100):
            start = time.time()
            requests.post(f"{API_URL}/detect/single", json=invoice)
            elapsed = time.time() - start
            times.append(elapsed * 1000)
            
            if (i + 1) % 25 == 0:
                print(f"  {i + 1} requests completed...")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n[RESULTS]")
        print(f"  Average Response Time: {avg_time:.1f}ms")
        print(f"  Min Response Time: {min_time:.1f}ms")
        print(f"  Max Response Time: {max_time:.1f}ms")
        print(f"  Throughput: {1000/avg_time:.0f} requests/second")
        print(f"  Status: {'✓ EXCELLENT' if avg_time < 500 else '✓ GOOD'}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all demos"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                                ║")
    print("║                   VISIONERR FRAUD GUARD - LIVE DEMO SCRIPT                    ║")
    print("║                                                                                ║")
    print("║                         AI-Powered Fraud Detection                            ║")
    print("║                                                                                ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")
    
    print(f"\n[INFO] Starting demo at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] API URL: {API_URL}")
    
    # Run all demos
    results = {
        "1. Health Check": demo_1_health_check(),
        "2. Model Stats": demo_2_model_stats(),
        "3. Fraud Detection": demo_3_fraud_detection(),
        "4. Normal Detection": demo_4_normal_detection(),
        "5. Bulk Detection": demo_5_bulk_detection(),
        "6. Performance": demo_6_performance(),
    }
    
    # Summary
    print_header("DEMO SUMMARY")
    print("\n")
    for test, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test:<30} {status}")
    
    total_passed = sum(1 for v in results.values() if v)
    total_tests = len(results)
    
    print(f"\n  Total: {total_passed}/{total_tests} demos passed")
    
    if total_passed == total_tests:
        print("\n  🎉 ALL DEMOS PASSED - READY FOR PRESENTATION! 🎉")
    else:
        print(f"\n  ⚠️  {total_tests - total_passed} demo(s) failed - Check API connection")
    
    print("\n" + "="*80)
    print("  Demo completed!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
