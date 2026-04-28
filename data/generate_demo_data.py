import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("🔨 Demo Veri Seti Oluşturuluyor (100 Fatura)...\n")

np.random.seed(42)  # Reproducible results

invoices = []
invoice_id = 1

# NORMAL INVOICES (70 tane - gerçekçi)
print("✓ Normal faturalar oluşturuluyor (70 tane)...")
for i in range(70):
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': f'CUST{np.random.randint(1, 30)}',
        'amount': np.random.uniform(500, 8000),
        'date': (datetime.now() - timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d'),
        'category': np.random.choice(['Web Dev', 'Design', 'Consulting', 'Content', 'Marketing', 'Analytics']),
        'status': np.random.choice(['Paid', 'Pending'], p=[0.7, 0.3]),
        'days_to_pay': np.random.randint(3, 45),
        'previous_invoices': np.random.randint(2, 20),
        'is_fraud': 0
    })
    invoice_id += 1

# FRAUD PATTERN 1: Duplicate Billing (5 tane)
print("✓ Duplicate Billing pattern'leri ekleniyor (5 tane)...")
for i in range(5):
    cust_id = f'CUST{100 + i}'
    amount = np.random.uniform(1500, 4000)
    date = (datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime('%Y-%m-%d')
    
    # İki fatura aynı tutarla
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': cust_id,
        'amount': amount,
        'date': date,
        'category': 'Web Dev',
        'status': 'Paid',
        'days_to_pay': np.random.randint(2, 10),
        'previous_invoices': 8,
        'is_fraud': 1
    })
    invoice_id += 1
    
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': cust_id,
        'amount': amount,
        'date': date,
        'category': 'Web Dev',
        'status': 'Paid',
        'days_to_pay': np.random.randint(2, 10),
        'previous_invoices': 8,
        'is_fraud': 1
    })
    invoice_id += 1

# FRAUD PATTERN 2: Round Numbers (8 tane)
print("✓ Round Number pattern'leri ekleniyor (8 tane)...")
round_amounts = [1000, 2000, 3000, 4000, 5000, 1500, 2500, 3500]
for amount in round_amounts:
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': f'CUST{110 + invoice_id % 10}',
        'amount': amount,
        'date': (datetime.now() - timedelta(days=np.random.randint(1, 90))).strftime('%Y-%m-%d'),
        'category': np.random.choice(['Design', 'Consulting']),
        'status': np.random.choice(['Paid', 'Pending']),
        'days_to_pay': np.random.randint(1, 30),
        'previous_invoices': np.random.randint(0, 5),
        'is_fraud': 1
    })
    invoice_id += 1

# FRAUD PATTERN 3: High Velocity (6 tane - aynı müşteriden)
print("✓ High Velocity pattern'leri ekleniyor (6 tane)...")
velocity_customer = 'CUST150'
for i in range(6):
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': velocity_customer,
        'amount': np.random.uniform(1000, 3000),
        'date': (datetime.now() - timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d'),
        'category': 'Content',
        'status': np.random.choice(['Paid', 'Pending']),
        'days_to_pay': 2,  # Çok hızlı
        'previous_invoices': 1,
        'is_fraud': 1
    })
    invoice_id += 1

# FRAUD PATTERN 4: Missing Documentation (4 tane)
print("✓ Missing Documentation pattern'leri ekleniyor (4 tane)...")
for i in range(4):
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': f'CUST{160 + i}',
        'amount': np.random.uniform(2000, 6000),
        'date': (datetime.now() - timedelta(days=np.random.randint(60, 150))).strftime('%Y-%m-%d'),
        'category': np.random.choice(['Consulting', 'Analytics']),
        'status': 'Unpaid',
        'days_to_pay': np.random.randint(80, 150),  # Çok uzun ödeme gecikmesi
        'previous_invoices': 0,
        'is_fraud': 1
    })
    invoice_id += 1

# FRAUD PATTERN 5: New High-Value Customer (3 tane)
print("✓ New High-Value Customer pattern'leri ekleniyor (3 tane)...")
for i in range(3):
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': f'CUST{170 + i}',
        'amount': np.random.uniform(6000, 12000),
        'date': (datetime.now() - timedelta(days=np.random.randint(1, 45))).strftime('%Y-%m-%d'),
        'category': np.random.choice(['Web Dev', 'Consulting']),
        'status': np.random.choice(['Paid', 'Pending']),
        'days_to_pay': 1,  # Çok hızlı ödeme (şüpheli)
        'previous_invoices': 0,  # Yeni müşteri
        'is_fraud': 1
    })
    invoice_id += 1

# FRAUD PATTERN 6: Unusual Timing (2 tane)
print("✓ Unusual Payment Timing pattern'leri ekleniyor (2 tane)...")
for i in range(2):
    invoices.append({
        'invoice_id': f'INV{invoice_id:03d}',
        'customer_id': f'CUST{173 + i}',
        'amount': np.random.uniform(1500, 3500),
        'date': (datetime.now() - timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d'),
        'category': 'Marketing',
        'status': 'Paid',
        'days_to_pay': 150,  # Çok uzun süre sonra ödeme
        'previous_invoices': 5,
        'is_fraud': 1
    })
    invoice_id += 1

# Veriyi DataFrame'e çevir
df = pd.DataFrame(invoices)

# Shuffle et
df = df.sample(frac=1).reset_index(drop=True)

# Kaydet
output_file = 'demo_invoices.csv'
df.to_csv(output_file, index=False)

# Özet istatistikler
print(f"\n{'='*60}")
print(f"✅ Demo Veri Seti Oluşturuldu: {output_file}")
print(f"{'='*60}")
print(f"\n📊 İSTATİSTİKLER:")
print(f"   Total Invoices:      {len(df)}")
print(f"   ✓ Normal:            {sum(df['is_fraud'] == 0)}")
print(f"   🚨 Fraud:            {sum(df['is_fraud'] == 1)}")
print(f"\n   Fraud Distribution:")
print(f"      • Duplicate Billing:        10 (2 per set)")
print(f"      • Round Numbers:            8")
print(f"      • High Velocity:            6")
print(f"      • Missing Documentation:    4")
print(f"      • New High-Value:           3")
print(f"      • Unusual Timing:           2")
print(f"      Total Fraud:                {sum(df['is_fraud'] == 1)}")

print(f"\n💰 AMOUNT İSTATİSTİKLERİ:")
print(f"   Min:     ${df['amount'].min():.2f}")
print(f"   Max:     ${df['amount'].max():.2f}")
print(f"   Mean:    ${df['amount'].mean():.2f}")
print(f"   Median:  ${df['amount'].median():.2f}")

print(f"\n🏢 CUSTOMER İSTATİSTİKLERİ:")
print(f"   Unique Customers: {df['customer_id'].nunique()}")
print(f"   Top Customer: {df['customer_id'].value_counts().index[0]} ({df['customer_id'].value_counts().values[0]} invoices)")

print(f"\n📂 STATUS DAĞILIMI:")
print(f"   {df['status'].value_counts().to_string()}")

print(f"\n✅ Hazır! Fraud detector ile analiz et:")
print(f"   python fraud_detector_demo.py")
