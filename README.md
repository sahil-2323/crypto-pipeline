# Serverless Crypto Data Pipeline (ETL)

A production-grade, serverless ETL (Extract, Transform, Load) pipeline that automates the ingestion of real-time cryptocurrency market data into a cloud PostgreSQL database. 

## 🏗️ Architecture Overview

The system leverages a decoupled, serverless cloud architecture designed for high efficiency, optimal resource utilization, and secure database connection scaling:

* **Data Source:** Live market metrics extracted via the **CoinGecko REST API**.
* **Compute Engine:** **AWS Lambda** executing a containerized Python environment.
* **Data Layer:** **Supabase (PostgreSQL)** cloud instance.
* **Networking proxy:** Structured routing via **Supabase Transaction Pooler** (Port 6543) to handle stateless cloud function connections.

## 🛠️ Tech Stack & Skills Showcased

* **Language:** Python (Pandas, SQLAlchemy, Psycopg2)
* **Cloud Infrastructure:** AWS Lambda, AWS EventBridge (CloudWatch Events)
* **Database:** PostgreSQL (Supabase)
* **DevOps/Data Engineering:** Custom Linux-x86_64 Lambda Layer compilation, connection pooling management, FinOps cost-optimization toggles.

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