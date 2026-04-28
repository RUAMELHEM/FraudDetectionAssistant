"""
ADIM 4: FINAL HYBRID MODEL
- V1'in başarılı patterns'ı koru
- V2'nin yeni rules'larını ekle
- Best recall + precision balance
"""

import pandas as pd
import numpy as np
import json
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger('FraudDetectorFinal')

class FraudDetectorFinal:
    """
    Final production-ready fraud detection
    """
    
    def __init__(self, invoices_df: pd.DataFrame):
        self.df = invoices_df
        self.alerts = []
        print(f"✓ Initialized with {len(invoices_df)} invoices")
    
    def detect_all(self) -> List[Dict]:
        """Run all detection rules"""
        self.alerts = []
        
        print("\n🔍 FINAL FRAUD DETECTION (HYBRID MODEL)...\n")
        
        # V1 proven rules (best recall)
        self.rule_duplicate_billing()
        self.rule_round_numbers()
        self.rule_velocity()
        self.rule_missing_docs()
        self.rule_new_customer_high_amount()
        self.rule_unusual_days_to_pay()
        
        # V2 new rules (additional patterns)
        self.rule_frequency_anomaly()
        self.rule_amount_variance()
        self.rule_status_mismatch()
        
        return self.score_results_final()
    
    # ===== PROVEN RULES (V1) =====
    
    def rule_duplicate_billing(self):
        print("✓ R1: Duplicate Billing")
        duplicates = self.df.groupby('customer_id')['amount'].apply(
            lambda x: x[x.duplicated(keep=False)]
        )
        
        for customer_id in duplicates.index.get_level_values(0).unique():
            customer_invoices = self.df[self.df['customer_id'] == customer_id]
            amount_duplicates = customer_invoices[customer_invoices['amount'].duplicated(keep=False)]
            
            for idx, row in amount_duplicates.iterrows():
                self.alerts.append({
                    'invoice_id': row['invoice_id'],
                    'rule': 'Duplicate Billing',
                    'severity': 'HIGH',
                    'score_impact': 3,
                    'reason': f"Same amount (${row['amount']:.2f}) from {customer_id}"
                })
    
    def rule_round_numbers(self):
        print("✓ R2: Round Numbers")
        for idx, row in self.df.iterrows():
            if row['amount'] % 100 == 0 and row['amount'] > 0:
                self.alerts.append({
                    'invoice_id': row['invoice_id'],
                    'rule': 'Round Numbers',
                    'severity': 'MEDIUM',
                    'score_impact': 1,
                    'reason': f"Exact round: ${row['amount']:.2f}"
                })
    
    def rule_velocity(self):
        print("✓ R3: High Velocity")
        customer_counts = self.df.groupby('customer_id').size()
        
        for customer_id, count in customer_counts.items():
            if count > 4:  # Threshold: 4+
                for idx, row in self.df[self.df['customer_id'] == customer_id].iterrows():
                    self.alerts.append({
                        'invoice_id': row['invoice_id'],
                        'rule': 'High Velocity',
                        'severity': 'MEDIUM',
                        'score_impact': 1,
                        'reason': f"Customer {count} invoices"
                    })
    
    def rule_missing_docs(self):
        print("✓ R4: Missing Documentation")
        for idx, row in self.df.iterrows():
            if row['status'] == 'Unpaid' and row['days_to_pay'] > 60:
                self.alerts.append({
                    'invoice_id': row['invoice_id'],
                    'rule': 'Missing Docs',
                    'severity': 'HIGH',
                    'score_impact': 3,
                    'reason': f"Unpaid {row['days_to_pay']} days"
                })
    
    def rule_new_customer_high_amount(self):
        print("✓ R5: New High-Value")
        for idx, row in self.df.iterrows():
            if row['previous_invoices'] < 2 and row['amount'] > 3500:
                self.alerts.append({
                    'invoice_id': row['invoice_id'],
                    'rule': 'New High-Value',
                    'severity': 'MEDIUM',
                    'score_impact': 1,
                    'reason': f"New customer + ${row['amount']:.2f}"
                })
    
    def rule_unusual_days_to_pay(self):
        print("✓ R6: Unusual Timing")
        q1 = self.df['days_to_pay'].quantile(0.25)
        q3 = self.df['days_to_pay'].quantile(0.75)
        iqr = q3 - q1
        
        upper_bound = q3 + 1.5 * iqr
        lower_bound = q1 - 1.5 * iqr
        
        for idx, row in self.df.iterrows():
            if row['days_to_pay'] > upper_bound or row['days_to_pay'] < lower_bound:
                self.alerts.append({
                    'invoice_id': row['invoice_id'],
                    'rule': 'Unusual Timing',
                    'severity': 'MEDIUM',
                    'score_impact': 1,
                    'reason': f"Timing {row['days_to_pay']} days"
                })
    
    # ===== NEW RULES (V2) =====
    
    def rule_frequency_anomaly(self):
        print("✓ R7: Frequency Anomaly")
        for customer_id in self.df['customer_id'].unique():
            customer_df = self.df[self.df['customer_id'] == customer_id]
            dates = customer_df['date'].value_counts()
            
            for date, count in dates.items():
                if count > 4:  # Multiple invoices same day
                    for idx, row in customer_df[customer_df['date'] == date].iterrows():
                        self.alerts.append({
                            'invoice_id': row['invoice_id'],
                            'rule': 'Frequency Anomaly',
                            'severity': 'MEDIUM',
                            'score_impact': 1,
                            'reason': f"{count} invoices same day"
                        })
    
    def rule_amount_variance(self):
        print("✓ R8: Amount Variance")
        for customer_id in self.df['customer_id'].unique():
            amounts = self.df[self.df['customer_id'] == customer_id]['amount'].values
            
            if len(amounts) > 3:
                mean = np.mean(amounts)
                std = np.std(amounts)
                
                if std > 0 and (std / mean) > 0.4:
                    for idx, row in self.df[self.df['customer_id'] == customer_id].iterrows():
                        z = abs((row['amount'] - mean) / std)
                        if z > 2:
                            self.alerts.append({
                                'invoice_id': row['invoice_id'],
                                'rule': 'Amount Variance',
                                'severity': 'MEDIUM',
                                'score_impact': 1,
                                'reason': f"Variance from avg"
                            })
    
    def rule_status_mismatch(self):
        print("✓ R9: Status Mismatch")
        for idx, row in self.df.iterrows():
            if row['status'] == 'Pending' and row['days_to_pay'] > 50:
                self.alerts.append({
                    'invoice_id': row['invoice_id'],
                    'rule': 'Status Mismatch',
                    'severity': 'MEDIUM',
                    'score_impact': 1,
                    'reason': f"Pending but {row['days_to_pay']} days old"
                })
    
    def score_results_final(self) -> List[Dict]:
        """Final scoring with smart thresholds"""
        results = []
        
        for idx, row in self.df.iterrows():
            invoice_alerts = [a for a in self.alerts if a['invoice_id'] == row['invoice_id']]
            
            # Calculate composite score
            high_alerts = sum(1 for a in invoice_alerts if a['severity'] == 'HIGH')
            medium_alerts = sum(1 for a in invoice_alerts if a['severity'] == 'MEDIUM')
            
            # Weighted: HIGH=3 points, MEDIUM=1 point
            risk_score = (high_alerts * 3) + (medium_alerts * 1)
            risk_score = min(risk_score, 10)  # Cap at 10
            
            # Smart thresholds for GOOD recall/precision balance
            if high_alerts >= 1:  # Any HIGH alert = HIGH risk
                risk_level = 'HIGH'
            elif medium_alerts >= 2:  # 2+ MEDIUM = MEDIUM risk
                risk_level = 'MEDIUM'
            elif medium_alerts >= 1:  # 1 MEDIUM = LOW-MEDIUM (still watch)
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            results.append({
                'invoice_id': row['invoice_id'],
                'customer_id': row['customer_id'],
                'amount': float(row['amount']),
                'status': row['status'],
                'days_to_pay': int(row['days_to_pay']),
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'high_alerts': high_alerts,
                'medium_alerts': medium_alerts,
                'alert_count': len(invoice_alerts),
                'actual_fraud': int(row.get('is_fraud', 0)),
                'details': invoice_alerts
            })
        
        return results

def print_final_results(results: List[Dict]):
    """Print detailed results"""
    print("\n" + "="*70)
    print("✅ FINAL MODEL RESULTS (HYBRID)")
    print("="*70)
    
    high_risk = sum(1 for r in results if r['risk_level'] == 'HIGH')
    medium_risk = sum(1 for r in results if r['risk_level'] == 'MEDIUM')
    low_risk = sum(1 for r in results if r['risk_level'] == 'LOW')
    
    actual_frauds = sum(1 for r in results if r['actual_fraud'] == 1)
    true_positives_high = sum(1 for r in results if r['risk_level'] == 'HIGH' and r['actual_fraud'] == 1)
    false_positives_high = sum(1 for r in results if r['risk_level'] == 'HIGH' and r['actual_fraud'] == 0)
    
    print(f"\n📊 RISK DISTRIBUTION:")
    print(f"   🔴 HIGH Risk:      {high_risk} ({high_risk/len(results)*100:.1f}%)")
    print(f"   🟠 MEDIUM Risk:    {medium_risk} ({medium_risk/len(results)*100:.1f}%)")
    print(f"   🟢 LOW Risk:       {low_risk} ({low_risk/len(results)*100:.1f}%)")
    
    print(f"\n🎯 ACCURACY METRICS:")
    print(f"   Actual Frauds:     {actual_frauds}")
    print(f"   True Positives:    {true_positives_high}/{actual_frauds}")
    print(f"   False Positives:   {false_positives_high}")
    
    if high_risk > 0:
        precision = true_positives_high / high_risk
        print(f"   Precision:         {precision:.1%} ✅")
    
    if actual_frauds > 0:
        recall = true_positives_high / actual_frauds
        print(f"   Recall:            {recall:.1%} ✅")
    
    # Top HIGH risk invoices
    print(f"\n⚠️  TOP HIGH RISK INVOICES:")
    high_risk_invoices = [r for r in results if r['risk_level'] == 'HIGH']
    sorted_high = sorted(high_risk_invoices, key=lambda x: x['risk_score'], reverse=True)
    
    for i, r in enumerate(sorted_high[:5], 1):
        fraud_status = "✓ FRAUD" if r['actual_fraud'] == 1 else "❌ NORMAL"
        print(f"\n   {i}. {r['invoice_id']} | ${r['amount']:.2f} | Score: {r['risk_score']}/10 | {fraud_status}")
        if r['details']:
            for alert in r['details'][:2]:
                print(f"      • {alert['rule']}: {alert['reason']}")

if __name__ == "__main__":
    print("="*70)
    print("ADIM 4: FINAL HYBRID MODEL (9 RULES - BALANCED)")
    print("="*70)
    
    # Load demo data
    df = pd.read_csv('demo_invoices.csv')
    
    # Run final detector
    detector = FraudDetectorFinal(df)
    results = detector.detect_all()
    
    # Print results
    print_final_results(results)
    
    # Calculate stats
    high_risk = sum(1 for r in results if r['risk_level'] == 'HIGH')
    medium_risk = sum(1 for r in results if r['risk_level'] == 'MEDIUM')
    low_risk = sum(1 for r in results if r['risk_level'] == 'LOW')
    
    actual_frauds = sum(1 for r in results if r['actual_fraud'] == 1)
    tp = sum(1 for r in results if r['risk_level'] == 'HIGH' and r['actual_fraud'] == 1)
    fp = sum(1 for r in results if r['risk_level'] == 'HIGH' and r['actual_fraud'] == 0)
    
    precision = tp / high_risk if high_risk > 0 else 0
    recall = tp / actual_frauds if actual_frauds > 0 else 0
    
    # Export
    csv_data = []
    for r in results:
        csv_data.append({
            'invoice_id': r['invoice_id'],
            'customer_id': r['customer_id'],
            'amount': r['amount'],
            'risk_score': r['risk_score'],
            'risk_level': r['risk_level'],
            'high_alerts': r['high_alerts'],
            'medium_alerts': r['medium_alerts'],
            'actual_fraud': r['actual_fraud']
        })
    
    pd.DataFrame(csv_data).to_csv('fraud_results_final.csv', index=False)
    
    # JSON for API
    json_data = []
    for r in results:
        json_data.append({
            'invoice_id': r['invoice_id'],
            'customer_id': r['customer_id'],
            'amount': r['amount'],
            'risk_score': r['risk_score'],
            'risk_level': r['risk_level'],
            'alerts': r['details']
        })
    
    with open('fraud_results_final.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"\n💾 EXPORTED:")
    print(f"   ✓ fraud_results_final.csv")
    print(f"   ✓ fraud_results_final.json")
    
    print(f"\n📈 SUMMARY:")
    print(f"   HIGH: {high_risk} | MEDIUM: {medium_risk} | LOW: {low_risk}")
    print(f"   Precision: {precision:.1%} | Recall: {recall:.1%}")
    
    print("\n" + "="*70)
    print("✅ ADIM 4 TAMAMLANDI - FINAL MODEL READY!")
    print("="*70)
