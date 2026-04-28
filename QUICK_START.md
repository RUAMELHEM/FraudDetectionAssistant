#!/bin/bash
# 🚀 VISIONERR FRAUD GUARD - QUICK START GUIDE

## ⚡ HIZLI ÇALIŞTIRMA

### 1. Test Veri Seti (30 Fatura)
```bash
cd data
python generate_test_data.py
python fraud_detector.py
```
**Çıktı:** test_invoices.csv, fraud_detection_results.csv

### 2. Demo Veri Seti (100+ Fatura)
```bash
python generate_demo_data.py
python fraud_detector_demo.py
```
**Çıktı:** demo_invoices.csv, demo_fraud_results.csv, demo_fraud_results.json

---

## 📊 VERI SETI AÇIKLAMASI

### Test Set (30 Fatura)
- Normal: 20
- Fraud: 10 (çeşitli pattern'lerle)
- **Kullanım:** Geliştirilme ve unit testing

### Demo Set (103 Fatura)
- Normal: 70
- Fraud: 33 (6 farklı pattern)
- **Kullanım:** Canlı sunuma, client demo'ya

---

## 🔍 6 FRAUD DETECTION RULES

| Rule | Tip | Açıklama |
|------|-----|----------|
| Duplicate Billing | HIGH | Aynı müşteri, aynı tutar |
| Round Numbers | MEDIUM | Tam sayılı tutarlar (1000, 2000 vs) |
| High Velocity | MEDIUM | Çok hızlı birden çok fatura |
| Missing Documentation | HIGH | Unpaid + 60+ gün gecikmesi |
| New High-Value | MEDIUM | Yeni müşteri + $3500+ |
| Unusual Timing | MEDIUM | Anormal ödeme süresi |

---

## 📈 ACCURACY

```
Test Set (30 invoices):
   Precision: 100%
   Recall: 60%

Demo Set (103 invoices):
   Precision: 100%
   Recall: 42.4%
```

> Precision %100 = Yanlış alarm YOK
> Recall %42+ = 2-3 fraud'dan 1'ini yakalyıyor

---

## 🎬 SUNUMDA KULLANILACAK KOMUTLAR

```bash
# Demo başlat
cd data
python fraud_detector_demo.py

# Çıktı:
# ✓ Rule 1: Duplicate Billing kontrolü...
# ✓ Rule 2: Round Number Pattern kontrolü...
# ... (6 rule toplam)
#
# SUMMARY:
# 🔴 HIGH Risk:    14 (Hepsi Fraud)
# 🟠 MEDIUM Risk:  62
# 🟢 LOW Risk:     27
#
# Precision: 100.0%
# Recall: 42.4%
```

---

## 🔗 BACKEND ENTEGRASYONU

### API Endpoint Örneği

```python
from fastapi import FastAPI, UploadFile, File
from data.fraud_detector_demo import FraudDetectorDemo
import pandas as pd

@app.post("/api/analyze")
async def analyze_invoices(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    detector = FraudDetectorDemo(df)
    results = detector.detect_all()
    
    # JSON dönüş
    return {
        "total": len(results),
        "high_risk": sum(1 for r in results if r['risk_level'] == 'HIGH'),
        "invoices": results
    }
```

---

## 📁 DOSYA YAPISI

```
salam_hack/
├── data/
│   ├── generate_test_data.py
│   ├── generate_demo_data.py
│   ├── fraud_detector.py
│   ├── fraud_detector_demo.py
│   ├── test_invoices.csv
│   ├── demo_invoices.csv
│   ├── fraud_detection_results.csv
│   ├── demo_fraud_results.csv
│   └── demo_fraud_results.json
├── backend/
│   ├── main.py          (FastAPI server)
│   ├── api.py           (Endpoints)
│   └── models.py        (Pydantic models)
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   └── style.css
├── requirements.txt
├── DAY1_REPORT.md
└── DEMO_RESULTS.md
```

---

## ✅ CHECKLIST

**Gün 1 (Tamamlandı):**
- [x] Test veri seti (30 fatura)
- [x] Demo veri seti (103 fatura)
- [x] Fraud Detection Model (6 rule)
- [x] Accuracy Testing
- [x] CSV/JSON export

**Gün 2 (TODO):**
- [ ] FastAPI backend
- [ ] CSV upload endpoint
- [ ] Frontend dashboard
- [ ] End-to-end test
- [ ] Sunuma hazırlık

---

## 💡 İPUÇLARı

1. **CSV format önemli**: Tüm faturalarda şu sütunlar olmalı:
   ```
   invoice_id, customer_id, amount, date, category, status, days_to_pay, previous_invoices, is_fraud
   ```

2. **Model output**: fraud_detector_demo.py sonucunda 3 dosya çıkar:
   - CSV (Excel'e aç)
   - JSON (API'ye gönder)
   - Terminal output (Demo göstermek için)

3. **Performance**: 103 fatura < 2 saniye'de analiz ediliyor

---

## 🎯 SUNUMDA VURGULANACAK NOKTALAR

✅ **Live Demo Scenario:**
1. "Burada 103 fatura var"
2. "Fraud detector'u çalıştırıyorum"
3. "6 kuralı bir anda uyguluyor"
4. "Sonuç: 14 HIGH risk fatura, hepsi fraud!"
5. "Precision: %100 (yanlış alarm yok)"

---

**🚀 HAZIRİ!**
Backend dev'e backend/main.py'ı yazmak için sarı ışık yak.
