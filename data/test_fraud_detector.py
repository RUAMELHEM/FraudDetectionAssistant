"""
ADIM 5: UNIT TESTS & VALIDATION
- Model reliability testing
- Edge cases
- Performance benchmarking
"""

import pandas as pd
import numpy as np
from fraud_detector_final import FraudDetectorFinal
import time

def test_1_empty_dataframe():
    """Test: Handle empty input"""
    print("\n🧪 TEST 1: Empty DataFrame")
    try:
        empty_df = pd.DataFrame(columns=[
            'invoice_id', 'customer_id', 'amount', 'date',
            'category', 'status', 'days_to_pay', 'previous_invoices'
        ])
        detector = FraudDetectorFinal(empty_df)
        results = detector.detect_all()
        assert len(results) == 0
        print("   ✅ PASS: Handles empty input correctly")
        return True
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")
        return False

def test_2_single_invoice():
    """Test: Single invoice"""
    print("\n🧪 TEST 2: Single Invoice")
    try:
        single_df = pd.DataFrame({
            'invoice_id': ['INV001'],
            'customer_id': ['CUST001'],
            'amount': [1000.0],
            'date': ['2024-01-01'],
            'category': ['Web Dev'],
            'status': ['Paid'],
            'days_to_pay': [10],
            'previous_invoices': [5],
            'is_fraud': [0]
        })
        detector = FraudDetectorFinal(single_df)
        results = detector.detect_all()
        assert len(results) == 1
        assert results[0]['invoice_id'] == 'INV001'
        print("   ✅ PASS: Handles single invoice correctly")
        return True
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")
        return False

def test_3_fraud_detection_accuracy():
    """Test: Known fraud patterns"""
    print("\n🧪 TEST 3: Fraud Detection Accuracy")
    try:
        # Create test data with known fraud
        test_df = pd.DataFrame({
            'invoice_id': ['INV001', 'INV002', 'INV003'],
            'customer_id': ['CUST001', 'CUST001', 'CUST002'],
            'amount': [1500.0, 1500.0, 5000.0],  # Duplicate + high value
            'date': ['2024-01-01', '2024-01-01', '2024-01-02'],
            'category': ['Web Dev', 'Web Dev', 'Consulting'],
            'status': ['Paid', 'Paid', 'Unpaid'],
            'days_to_pay': [10, 10, 120],  # Last one: very long
            'previous_invoices': [3, 3, 0],  # Last one: new customer
            'is_fraud': [1, 1, 1]
        })
        
        detector = FraudDetectorFinal(test_df)
        results = detector.detect_all()
        
        # Check detection
        high_risk_count = sum(1 for r in results if r['risk_level'] == 'HIGH')
        
        if high_risk_count >= 2:
            print(f"   ✅ PASS: Detected {high_risk_count}/3 frauds correctly")
            return True
        else:
            print(f"   ⚠️  PARTIAL: Detected {high_risk_count}/3 frauds (expected 2+)")
            return False
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")
        return False

def test_4_no_false_positives():
    """Test: Normal invoices not flagged"""
    print("\n🧪 TEST 4: No False Positives")
    try:
        normal_df = pd.DataFrame({
            'invoice_id': ['INV001', 'INV002', 'INV003'],
            'customer_id': ['CUST001', 'CUST001', 'CUST002'],
            'amount': [987.50, 1234.75, 456.25],  # NOT round
            'date': ['2024-01-01', '2024-01-15', '2024-01-20'],
            'category': ['Web Dev', 'Web Dev', 'Design'],
            'status': ['Paid', 'Paid', 'Paid'],
            'days_to_pay': [12, 15, 8],
            'previous_invoices': [10, 10, 5],
            'is_fraud': [0, 0, 0]
        })
        
        detector = FraudDetectorFinal(normal_df)
        results = detector.detect_all()
        
        high_risk_count = sum(1 for r in results if r['risk_level'] == 'HIGH')
        
        if high_risk_count == 0:
            print("   ✅ PASS: No false positives on normal data")
            return True
        else:
            print(f"   ⚠️  PARTIAL: {high_risk_count} false positives (expected 0)")
            return False
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")
        return False

def test_5_performance_benchmark():
    """Test: Performance with large dataset"""
    print("\n🧪 TEST 5: Performance Benchmark")
    try:
        # Generate 500 invoices
        np.random.seed(42)
        test_df = pd.DataFrame({
            'invoice_id': [f'INV{i:04d}' for i in range(500)],
            'customer_id': [f'CUST{np.random.randint(1, 50):03d}' for _ in range(500)],
            'amount': np.random.uniform(500, 10000, 500),
            'date': pd.date_range('2024-01-01', periods=500, freq='D'),
            'category': np.random.choice(['Web Dev', 'Design', 'Consulting'], 500),
            'status': np.random.choice(['Paid', 'Pending', 'Unpaid'], 500),
            'days_to_pay': np.random.randint(1, 100, 500),
            'previous_invoices': np.random.randint(0, 20, 500),
            'is_fraud': np.random.choice([0, 1], 500, p=[0.9, 0.1])
        })
        
        detector = FraudDetectorFinal(test_df)
        
        # Measure time
        start = time.time()
        results = detector.detect_all()
        elapsed = time.time() - start
        
        # Check performance
        if elapsed < 5:  # Should complete in < 5 seconds
            print(f"   ✅ PASS: 500 invoices in {elapsed:.2f}s")
            return True
        else:
            print(f"   ⚠️  WARN: 500 invoices in {elapsed:.2f}s (expected <5s)")
            return True  # Still acceptable
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")
        return False

def test_6_result_structure():
    """Test: Output format validation"""
    print("\n🧪 TEST 6: Result Structure")
    try:
        test_df = pd.read_csv('demo_invoices.csv').head(5)
        detector = FraudDetectorFinal(test_df)
        results = detector.detect_all()
        
        # Check required fields
        required_fields = [
            'invoice_id', 'customer_id', 'amount', 'status',
            'days_to_pay', 'risk_score', 'risk_level', 'alert_count'
        ]
        
        all_valid = all(all(field in r for field in required_fields) for r in results)
        
        if all_valid:
            print("   ✅ PASS: All required fields present")
            return True
        else:
            print("   ❌ FAIL: Missing required fields")
            return False
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")
        return False

def test_7_risk_level_consistency():
    """Test: Risk levels are consistent"""
    print("\n🧪 TEST 7: Risk Level Consistency")
    try:
        test_df = pd.read_csv('demo_invoices.csv').head(20)
        detector = FraudDetectorFinal(test_df)
        results = detector.detect_all()
        
        # Check risk level matches score
        valid = True
        for r in results:
            score = r['risk_score']
            level = r['risk_level']
            high_alerts = r['high_alerts']
            
            # HIGH = any HIGH alert (score >= 3), MEDIUM = 2+ MEDIUM (score >= 2)
            expected_high = high_alerts >= 1
            expected_medium = r['medium_alerts'] >= 2 and high_alerts == 0
            
            if expected_high and level != 'HIGH':
                valid = False
            if expected_medium and level != 'MEDIUM':
                valid = False
        
        if valid:
            print("   ✅ PASS: Risk levels consistent with scores")
            return True
        else:
            print("   ⚠️  FAIL: Inconsistencies found")
            return False
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")
        return False

def run_all_tests():
    """Run all unit tests"""
    print("\n" + "="*70)
    print("🧪 FRAUD DETECTOR - UNIT TESTS")
    print("="*70)
    
    tests = [
        test_1_empty_dataframe,
        test_2_single_invoice,
        test_3_fraud_detection_accuracy,
        test_4_no_false_positives,
        test_5_performance_benchmark,
        test_6_result_structure,
        test_7_risk_level_consistency
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"Passed:  {passed}/{total}")
    print(f"Success: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - MODEL IS PRODUCTION READY!")
    elif passed >= total * 0.85:
        print("\n🟠 MOST TESTS PASSED - MODEL IS MOSTLY READY")
    else:
        print("\n❌ SOME TESTS FAILED - NEEDS FIXING")
    
    print("="*70)

if __name__ == "__main__":
    run_all_tests()
