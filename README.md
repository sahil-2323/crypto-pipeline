# Serverless Multi-Stage Crypto Data Engineering Pipeline

A production-grade, event-driven data pipeline deployed on AWS Lambda that extracts live cryptocurrency financial data, performs robust feature engineering transformations, and dynamically logs analytical insights into an enterprise cloud database hosted on Supabase.

---

## 🏗️ Project Architecture

To protect production workflows and maintain raw historical records, this project is decoupled into two completely independent architectural stages. This layout allows for seamless raw auditing while giving downstream analytical scripts full isolated freedom.

```text
                  ┌──────────────────────┐
                  │  CoinGecko Public    │
                  │       REST API       │
                  └──────────┬───────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
   ┌────────────────────┐        ┌────────────────────┐
   │ AWS Lambda Stage 1 │        │ AWS Lambda Stage 2 │
   │  (Raw Ingestion)   │        │  (Analytical ETL)  │
   ├────────────────────┤        ├────────────────────┤
   │ • SQLAlchemy Core  │        │ • Pure Python 3.12 │
   │ • Psycopg2 Driver  │        │ • Native urllib    │
   │ • Custom Layer     │        │ • Zero-Dependency  │
   └──────────┬---------┘        └──────────┬---------┘
              │                             │
              ▼                             ▼
   ┌────────────────────┐        ┌────────────────────┐
   │ Supabase Table:    │        │ Supabase Table:    │
   │ raw_crypto_prices  │        │ transformed_       │
   │                    │        │ crypto_prices      │
   └────────────────────┘        └────────────────────┘
``` 
## 🛠️ Tech Stack & Cloud Infrastructure

* **Cloud Compute:** AWS Lambda (Serverless architecture running Python 3.12)
* **Automation:** Amazon EventBridge (Scheduled CRON rules set to `rate(1 hour)`)
* **Cloud Database:** Supabase (PostgreSQL engine with transaction connection pooling)
* **Core Languages:** Pure Python (Zero-dependency framework optimized for sub-second cloud execution)
* **Data Source:** CoinGecko Public Markets REST API

## 🚀 Key Engineering Challenges Solved

### 1. Cross-Platform Operating System Dependencies
**Problem:** The core database driver (`psycopg2`) requires OS-specific binaries. Developing on Windows caused compilation crashes when deployed to AWS Lambda's native Linux environment.
**Solution:** Cross-compiled a custom Linux-64 bit database layer framework natively and deployed it as an **AWS Lambda Layer**, decoupling driver dependencies from the core pipeline logic.

### 2. Cloud-to-Database Connection Starvation
**Problem:** Serverless functions scale horizontally instantly, which can easily overwhelm standard relational databases by opening too many direct connections. Additionally, AWS Lambda environments block direct IPv6 pathways natively.
**Solution:** Configured the database pipeline to route through the **Supabase IPv4 Transaction Pooler Proxy**, executing clean authentication handshakes and maximizing connection reuse.

### 3. FinOps & Cloud Resource Management
**Problem:** Continuous high-frequency cron scheduling risks exhausting cloud free-tier credits rapidly during non-assessment windows.
**Solution:** Deployed an orchestrator rule using **AWS EventBridge** with an administrative pause/resume state mechanism, allowing on-demand activation for presentation purposes while minimizing idle system cost.

## 📊 Engineered Features & Transformations

The analytical transformation pipeline processes the incoming API payload data arrays natively, creating custom business intelligence dimensions before landing the metrics in the database table:

* **Volatility Spread Percentage:** Tracks price instability and intraday trading risk by assessing high-to-low margins relative to baseline asset valuations:
  
  Volatility Spread % = ((High 24h - Low 24h) / Low 24h) * 100

* **Dynamic Currency Translation:** Converts global USD financial asset prices into localized Indian Rupee (INR) valuations using active macroeconomic scaling multipliers.
* **Temporal Auditing:** Injects automated, standardized UTC execution timestamps into every row vector for exact time-series trend tracking.
* **Fault-Tolerant Error Handling:** Implements programmatic inline fallback operators (`or 0`) to prevent pipeline crashes from unexpected null data fields sent by the public API.

## 📋 How to Run Locally / Replicate

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/crypto-pipeline.git](https://github.com/YOUR_GITHUB_USERNAME/crypto-pipeline.git)
   ```
2. Install dependencies:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary requests
   ```
3. Set your environment parameters:
   ```bash
   RAW_PASSWORD = "YOUR_DATABASE_PASSWORD"
   PROJECT_ID = "YOUR_SUPABASE_PROJECT_ID"

---

### 🚀 Step 2: Push It Up!

Once you save that file:
1. Open your terminal in that folder.
2. Run these final commands to complete the repository:
   ```bash
   git add README.md
   git commit -m "docs: add comprehensive production architecture documentation"
   git push

---

## 🗄️ Database Schema Layout

The target analytical table layout created inside the Supabase SQL Engine to store the calculated metrics:

```sql
CREATE TABLE IF NOT EXISTS transformed_crypto_prices (
    id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(50),
    current_price NUMERIC,
    market_cap BIGINT,
    high_24h NUMERIC,
    low_24h NUMERIC,
    price_change_percentage_24h NUMERIC,
    volatility_spread_pct NUMERIC,
    price_inr NUMERIC,
    extracted_at TIMESTAMP
);
