# 🗺 Roadmap — FinGuard Enterprise

> Back to the [README](../README.md).

## Where the project stands

Status: **v4.1.0**.

## Milestones

### v4.1 — Current (done)

- [x] XGBoost scoring, 4 analyst modules, PDF reports
- [x] Streamlit Cloud deployment and Android APK

### v4.2 — Security hardening

*Goal:* Production-grade access control.

- [ ] Move credentials to hashed secrets / OAuth instead of in-code demo users
- [ ] Role-based permissions per module
- [ ] Persist audit log to a database

### v5.0 — Smarter detection

- [ ] SHAP explanations per alert
- [ ] Graph-based features (GNN) from the network explorer
- [ ] Streaming ingestion (Kafka) and drift monitoring

## 🔭 Long-term Vision

A transparent fraud-ops cockpit where every alert is explained, traceable and exportable for investigators.

## How to help

Pick any unchecked item, open an issue to discuss the approach, then send a PR. Items in the earliest unfinished milestone are the highest priority.


---
*Last updated: 2026-11-13*
