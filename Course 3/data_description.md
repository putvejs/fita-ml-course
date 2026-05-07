# Data Description Report

**Server:** 87.110.123.151 | **Database:** `direct_payments` | **Generated:** 2026-05-07

---

## 1. Database Overview

The `direct_payments` database represents a **direct debit payment processing platform** — similar to GoCardless — that manages recurring bank-to-bank payment mandates on behalf of merchant organisations. The three tables form a clear hierarchy:

```
organisations  (431 rows)
    └── mandates  (9,381 rows)   — authorisations to pull funds
            └── payments  (33,461 rows) — individual payment executions
```

The data spans approximately **March 2018 – March 2020** (roughly 2 years of activity). Organisations sign up, create direct debit mandates with their customers, and then collect payments against those mandates — either manually via a dashboard, programmatically via an API, or through their own app.

---

## 2. Key Metrics

| Metric | Value |
|--------|-------|
| Total organisations | 431 |
| Total mandates | 9,381 |
| Total payments | 33,461 |
| **Total GBP collected** | **£3,998,939.69** |
| **Total EUR collected** | **€280,616.83** |
| Average GBP payment | £125.78 |
| Average EUR payment | €168.24 |
| Dominant payment scheme | BACS (96.1%) |
| SEPA Core scheme | 3.9% |
| Average days from creation to charge | **5.9 days** |

---

## 3. Notable Patterns & Insights

### Currency split — GBP dominant
95.0% of payments are in GBP (31,793 payments), confirming this is primarily a UK market operation. The 1,668 EUR payments (SEPA scheme) reflect a smaller European segment.

### Payment source channels
| Source | Payments | Total Amount | Avg Amount |
|--------|----------|-------------|------------|
| dashboard | 17,693 | £2,768,934 | £156.50 |
| app | 13,452 | £1,081,376 | £80.39 |
| api | 2,316 | £429,247 | £185.34 |

The **dashboard** is the dominant collection channel by volume and value. API-initiated payments have the highest average value (£185), suggesting automated high-value billing. App-sourced payments are smaller and more frequent — consistent with subscription or membership models.

### Sector breakdown
| Sector | Mandates | Payments | Total Volume |
|--------|----------|----------|-------------|
| digital_services_media_telecoms | 1,152 | 3,995 | £1,186,462 |
| professional_and_financial_services | 1,003 | 5,126 | £803,472 |
| sports_fitness | 3,959 | 12,170 | £734,094 |
| healthcare | — | — | £305,347 (top org) |
| tradesmen_and_non_professionals_services | — | — | £256,617 |

**Sports & fitness** has the most mandates (42% of total) — driven by gym memberships and sports clubs with many low-value regular payments. **Digital services** generates the highest total revenue despite fewer mandates, reflecting higher per-payment values (streaming, software subscriptions). **Professional & financial services** has the highest payments-per-mandate ratio, suggesting repeat billing on the same authorisations.

### Growth trajectory
Mandate creation shows strong early growth: from 114 new mandates in April 2018 to 990 in May 2018, peaking around mid-2018 and maintaining a steady plateau through 2019. This pattern is consistent with a platform that launched or expanded significantly in 2018.

### Charge timing
Payments are charged an average of **5.9 days** after creation (BACS requires a minimum 3 business days notice), which is the standard settlement window. The maximum of 368 days flags a small number of delayed/backdated entries worth investigating.

---

## 4. Potential Use Cases

- **Churn analysis**: Track organisations that stop creating new mandates or have declining payment frequency.
- **Sector benchmarking**: Compare payment frequency, average value, and mandate-to-payment conversion rates across `parent_vertical` groups.
- **Revenue forecasting**: Use the monthly mandate creation and payment trend data to project future collection volumes.
- **Fraud / anomaly detection**: Flag payments where `charge_date` is more than 14 days from `created_at`, or organisations with unusually high cancellation rates.
- **API vs dashboard segmentation**: Customers using the API are higher-value — useful for targeting premium feature upsells.
