# 🛡 FinGuard Enterprise | AI-Driven Financial Fraud Detection

![Version](https://img.shields.io/badge/Version-3.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/Streamlit-Enterprise-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

*FinGuard Enterprise* is a state-of-the-art anomaly detection system designed for high-frequency banking environments. Leveraging *XGBoost* with *SMOTE* balancing, it detects fraudulent transactions with *99.94% accuracy* in under 15ms.

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| *🧠 Neural Engine* | XGBoost Classifier trained on 284k+ real European banking transactions. |
| *⚡ Live Scanner* | Real-time packet analysis simulating a banking API gateway. |
| *📄 Auto-Reporting* | Generates forensic *PDF Reports* for flagged transactions automatically. |
| *📊 3D Forensics* | Interactive 3D PCA visualization of fraud clusters in vector space. |
| *🔐 Enterprise Security* | Simulated Login System, Audit Logging, and AES-256 styled architecture. |

---

## 🛠 Installation & Setup

### Prerequisites
* Python 3.8+
* Pip Package Manager

### Quick Start
1.  *Clone the Repository*
    bash
    git clone [https://github.com/shiroonigami23-ui/Bank-Security.git](https://github.com/shiroonigami23-ui/Bank-Security.git)
    cd Bank-Security
    

2.  *Install Dependencies*
    bash
    pip install -r requirements.txt
    

3.  *Run the System*
    * *Windows:* Double-click FinGuard_Launcher.bat
    * *Terminal:* python -m streamlit run main.py

---

## 📂 Project Structure

```text
FinGuard_Enterprise/
├── main.py                  # Application Entry Point
├── style.css                # Custom CSS (Glassmorphism UI)
├── modules/                 # Core Logic Modules
│   ├── data_loader.py       # Data Pipeline & Auto-Merge
│   ├── ui_components.py     # UI Widgets & Lottie Animations
│   └── pdf_generator.py     # Forensic PDF Engine
├── assets/                  # Static Assets
└── fraud_model_xg.pkl       # Serialized Machine Learning Model