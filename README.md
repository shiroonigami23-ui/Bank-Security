# FinGuard Enterprise - Bank Security

![Version](https://img.shields.io/badge/version-4.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10+-yellow?style=for-the-badge&logo=python)
![Android](https://img.shields.io/badge/android-apk-success?style=for-the-badge&logo=android)
![Streamlit](https://img.shields.io/badge/streamlit-live-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

[![Live App](https://img.shields.io/badge/Live%20Demo-kaks--bank--security.streamlit.app-red?style=for-the-badge)](https://kaks-bank-security.streamlit.app)
[![Download APK](https://img.shields.io/badge/Download-APK-3ddc84?style=for-the-badge&logo=android)](https://github.com/shiroonigami23-ui/Bank-Security/releases/latest/download/finguard-mobile.apk)

AI-driven financial fraud detection system with:
- Streamlit analyst dashboard
- XGBoost model inference
- Forensic PDF report generation
- Android APK wrapper for mobile access to the live system

## Features
- Real-time fraud transaction simulation and scoring
- Interactive forensics dashboard and network explorer
- Audit log tracking
- Fraud report PDF download
- Android app (`finguard-mobile.apk`) linked to the live FinGuard deployment

## Project Structure
```text
Bank-Security/
├── main.py
├── modules/
│   ├── data_loader.py
│   ├── pdf_generator.py
│   ├── risk_calculator.py
│   └── ui_components.py
├── android/
│   └── app/...
├── fraud_model_xg.pkl
├── requirements.txt
└── .github/workflows/android-release.yml
```

## Setup (Python App)
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run:
```bash
python -m streamlit run main.py
```
or use:
```bash
FinGuard_Launcher.bat
```

## Dataset Handling
- Large CSV datasets are intentionally excluded from version control.
- If CSVs are absent, the app now uses synthetic fallback data for demo continuity.
- Model file `fraud_model_xg.pkl` remains part of the repo for inference.

## Android APK
- Source: `android/`
- Build output in release: `finguard-mobile.apk`
- The APK opens the existing live deployment:
  - https://kaks-bank-security.streamlit.app

## Release Automation
- Tag push `v*` triggers Android build workflow:
  - Builds APK
  - Publishes GitHub Release asset

## License
MIT
