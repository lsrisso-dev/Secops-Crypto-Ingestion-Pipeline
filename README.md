# Secops-Crypto-Ingestion-Pipeline

A resilient, high-performance asynchronous data ingestion pipeline designed to capture EVM blockchain events, validate transactional integrity, and feed a local structured database for dry-run quantitative trading.

## 🏗️ Architecture Overview

The system architecture focuses on low-latency data parsing, robust type-safety, and local-first data storage:
* **Ingestion Layer:** Connects to Web3 infrastructure via JSON-RPC nodes (Alchemy/Infura) to query execution logs and topics.
* **Validation Layer:** Implements strict data contracts and validation using **Pydantic V2** and runtime quality suite tests with **Great Expectations**.
* **Storage Layer:** Local, high-performance analytics database driven by **DuckDB**, persisting transaction states into time-partitioned **Parquet** files.
* **Security & CI/CD:** Static Application Security Testing (SAST) running automatically with **Bandit** integrated inside **GitHub Actions**.

## 🛠️ Tech Stack

* **Language:** Python 3.10 (via Miniconda `ibm_data` environment)
* **Data Processing & Validation:** Pydantic V2, Great Expectations, Pandas
* **Storage:** DuckDB, Apache Parquet
* **DevOps & Security:** GitHub Actions, Bandit SAST

## 🚀 Roadmap (Phase 1 Specifications)
- [ ] JSON-RPC Event ingestion worker setup.
- [ ] Strict schema models creation with Pydantic.
- [ ] Great Expectations data suite profile configuration.
- [ ] DuckDB storage engine and time-partitioning logic.
- [ ] Automated local Dry-Run SPOT execution module with SQLite logs.
