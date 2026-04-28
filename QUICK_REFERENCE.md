# 🚀 VISIONERR FRAUD GUARD - DEMO DAY QUICK REFERENCE

## ⏰ SUNUM SÜRESI: 7 dakika

```
0:00 - 0:10  Opening (10 sn)
0:10 - 0:40  Problem (30 sn)
0:40 - 1:20  Solution (40 sn)
1:20 - 2:00  Model Comparison (40 sn)
2:00 - 2:45  Detection Rules (45 sn)
2:45 - 4:45  LIVE DEMO (2 dakika) ⭐
4:45 - 5:25  Architecture (40 sn)
5:25 - 6:10  Benefits (45 sn)
6:10 - 6:40  Roadmap & Close (30 sn)
─────────────────────────
TOTAL: 6:40 dakika
```

---

## 🎬 DEMO KOMUTLARI (Kopyala-Yapıştır)

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Fraud Invoice Detection
```bash
curl -X POST http://127.0.0.1:8000/detect/single \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": "FRAUD_001",
    "customer_id": "SUSPECT_CORP",
    "amount": 5000,
    "date": "2024-04-28",
    "category": "Web Dev",
    "status": "Unpaid",
    "days_to_pay": 150,
    "previous_invoices": 0
  }'
```

### Normal Invoice Detection  
```bash
curl -X POST http://127.0.0.1:8000/detect/single \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": "NORMAL_001",
    "customer_id": "TRUSTED_CORP",
    "amount": 2000,
    "date": "2024-04-28",
    "category": "Consulting",
    "status": "Paid",
    "days_to_pay": 30,
    "previous_invoices": 5
  }'
```

---

## 📊 KEY METRICS

### Rule-Based Model
- **Precision:** 100%
- **Recall:** 42.4%
- **Rules:** 9
- **Status:** ✓ Deployed

### ML Model (Random Forest)
- **Accuracy:** 90.5%
- **Precision:** 77.8%
- **Recall:** 100%
- **F1-Score:** 87.5%
- **Status:** ✓ Active

### Improvement
- **Recall Boost:** +57.6% ✅

---

## 🔍 9 DETECTION RULES

1. **Duplicate Billing** - Same invoice twice
2. **Round Numbers** - $5000, $10000 patterns
3. **High Velocity** - Too many invoices fast
4. **Missing Docs** - Long payment terms (90+ days)
5. **New High-Value** - New customer + high amount
6. **Unusual Timing** - Weird hours/dates
7. **Frequency Anomaly** - More invoices than normal
8. **Amount Variance** - Inconsistent amounts
9. **Status Mismatch** - Payment status conflicts

**Scoring:** HIGH=3pts, MEDIUM=1pt  
**Risk Levels:** HIGH(≥5), MEDIUM(2-4), LOW(<2)

---

## 🎯 DEMO AÇIKLAMALAR

### Demo 1: Health Check
"API server hazır ve çalışıyor"

### Demo 2: Fraud Invoice
"Gördüğünüz gibi:
- 5000 dolar round number → uyarı
- 150 gün ödeme süresi → uyarı  
- Yeni müşteri + yüksek tutar → uyarı
- Risk Level: HIGH
- ML Model: 60% FRAUD olasılığı

Sistem bu faturayı engellemenizi öneriyor."

### Demo 3: Normal Invoice
"Karşılaştırın:
- 2000 dolar normal tutar
- 30 gün normal ödeme süresi
- Güvenilir müşteri (5 önceki fatura)
- Risk Level: LOW
- ML Model: 25% FRAUD (yani NORMAL)

Sistem bu faturayı approve ettiriyor."

---

## 📱 API ENDPOINTS

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Server status |
| `/stats` | GET | Model info |
| `/detect/single` | POST | Single invoice |
| `/detect/bulk` | POST | Multiple invoices |

---

## 🧠 AÇIKLAMALAR

**"Neden iki model?"**
Redundancy. Rule-based %100 precision verir (false alarm yok).
ML model hiçbir sahte kaçırmıyor. İkisi kombinesiyle optimal.

**"Accuracy neden 90%?"**
Test set'te 103 fatura. ML model bazılarını miss etti. 
Ama fraud detection'da Recall daha önemli (false negative worst).

**"Ölçeklenebilir mi?"**
Evet. <250ms per request. API stateless. Containerize edilebilir.

**"Kullanıcılar nasıl kullanacak?"**
REST API POST request. Biz HIGH/MEDIUM/LOW döneriz.
İleride web dashboard.

---

## ⚠️ İHTİYAT

Eğer demo fail olursa:
1. API bağlantısını kontrol et
2. WiFi test et
3. Terminal'i yenile
4. `python backend/run_server.py` çalıştır
5. 10 saniye bekle

Backup: `python demo_script.py` çalıştır (pre-coded test)

---

## 💬 JÜRY SORUSU HAZIRLIĞI

**Q: "Rakipleriniz kim?"**
A: "Stripe, PayPal, custom tools. Ama biz freelancer-first. 
Daha affordable, AI-native, open-source."

**Q: "Para modeli?"**
A: "Beta phase. V3'ten: Free (100/ay), Pro ($99/ay), Enterprise."

**Q: "Teknoloji unique mi?"**
A: "Evet. 9 rules + ML combination rare. Plus non-invasive design."

**Q: "Team?"**
A: "Solo for now (hackathon). Scalable architecture ready for team."

---

## 🎤 AÇILIŞ SÖYLEM

"Merhaba! 60 milyon freelancer var dünyada.
Bunların çoğu her gün sahte faturalarla karşılaşıyor.
Sonuç: Her yıl 20 milyar dolar kaybediliyor.

Visionerr Fraud Guard bu sorunu çözüyor.
AI-powered, non-invasive, real-time fraud detection.
Rule-based + ML model. %100 recall. Let me show you..."

---

## 🎬 KAPANIŞ SÖYLEM

"Bu Visionerr Fraud Guard v2.
Ama v3'de dashboard var, v4'de blockchain audit trail.

Temel: Freelancer'ları korumak. Finansal kayıpları minimumla.

Kod GitHub'da açık. Pull request'ler welcome.

Teşekkür ederim. Sorularınız?"

---

## ✅ GO TIME CHECKLIST

- [ ] API Server çalışıyor? `curl http://127.0.0.1:8000/health`
- [ ] Terminal font okunabilir mi?
- [ ] Laptop %100 batarya?
- [ ] WiFi strong?
- [ ] Slides hazır?
- [ ] GitHub link hazır?
- [ ] Takı rahat mı?
- [ ] Nefes al, başarısız olmayacaksın!

**LET'S GO! 🚀**
