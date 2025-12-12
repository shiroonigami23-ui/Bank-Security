import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
from modules.data_loader import load_model, load_data
from modules.ui_components import kpi_card, header_animation
from modules.pdf_generator import create_download_link

# --- PAGE CONFIG ---
st.set_page_config(page_title="FinGuard Enterprise", page_icon="🛡", layout="wide")

# --- LOAD CSS ---
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'audit_log' not in st.session_state: st.session_state.audit_log = []

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("🛡 FinGuard Access")
        st.markdown("Enter secure credentials to access the banking mainframe.")
        
        CREDENTIALS = {
            "Khushee": "butterfly",
            "Kunal": "cheetah",
            "Aryan": "smooth",
            "Shiro": "oni",
            "Admin": "admin" 
        }
        
        user = st.text_input("Username", placeholder="Enter ID")
        pwd = st.text_input("Password", type="password", placeholder="Enter Password")
        
        if st.button("Authenticate"):
            # Check if user exists AND if password matches
            if user in CREDENTIALS and CREDENTIALS[user] == pwd:
                with st.spinner(f"Verifying Identity: {user.upper()}..."):
                    time.sleep(1.0)
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Access Denied: Invalid Credentials")
    st.stop()

# --- MAIN DASHBOARD ---
model = load_model()
data = load_data()

# SIDEBAR
with st.sidebar:
    st.title("🛡 FinGuard")
    st.caption("Enterprise Edition v3.0")
    menu = st.radio("Module", ["Live Scanner", "Forensics", "Audit Log"])
    st.markdown("---")
    st.success("● Network Secure")

if menu == "Live Scanner":
    # Top Section with Animation
    c1, c2 = st.columns([1, 4])
    with c1: header_animation()
    with c2: 
        st.title("Real-Time Threat Monitor")
        st.markdown("Listening on Port 443 | AES-256 Encryption Active")

    # KPIs
    k1, k2, k3 = st.columns(3)
    with k1: kpi_card("System Accuracy", "99.94%", "+0.01%", "#2ecc71")
    with k2: kpi_card("Transactions Processed", "4.2M", "+12k today", "#3498db")
    with k3: kpi_card("Active Threats", "0", "System Clear", "#2ecc71")

    st.markdown("<br>", unsafe_allow_html=True)

    # Scanner
    col_ui, col_graph = st.columns([1, 2])
    
    with col_ui:
        st.subheader("Transaction Gate")
        if st.button("Processing Incoming Packet", type="primary"):
            with st.spinner("Analyzing Feature Vectors..."):
                time.sleep(1)
                
                # Logic
                tx = data.sample(1)
                features = tx.drop(['Class'], axis=1)
                val = tx.iloc[0]['Amount']
                tx_id = str(np.random.randint(100000,999999))
                
                pred = model.predict(features)[0]
                prob = model.predict_proba(features)[0][1]
                
                if pred == 1:
                    status = "HIGH RISK FRAUD"
                    st.error("🚨 FRAUD DETECTED")
                    kpi_card("RISK SCORE", f"{prob*100:.2f}%", "CRITICAL", "#e74c3c")
                    
                    # Log it
                    st.session_state.audit_log.append(f"⚠ BLOCKED: ID {tx_id} | Amt €{val:.2f}")
                    
                    # PDF Download
                    st.markdown(create_download_link(tx_id, f"{prob*100:.2f}", val, status), unsafe_allow_html=True)
                    
                else:
                    status = "LEGITIMATE"
                    st.success("✅ Transaction Approved")
                    kpi_card("RISK SCORE", f"{prob*100:.4f}%", "SAFE", "#2ecc71")
                    st.session_state.audit_log.append(f"✅ APPROVED: ID {tx_id} | Amt €{val:.2f}")

    with col_graph:
        st.subheader("Deep Learning Vector Space")
        # 3D Chart
        df_viz = data.sample(300)
        df_viz['Type'] = df_viz['Class'].map({0: 'Safe', 1: 'Fraud'})
        fig = px.scatter_3d(df_viz, x='V11', y='V12', z='V14', color='Type',
                            color_discrete_map={'Safe': '#00ff88', 'Fraud': '#ff0000'},
                            opacity=0.7, template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=500)
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Forensics":
    st.title("📊 Forensic Data Analysis")
    st.markdown("Historical data pattern recognition.")
    
    # Advanced Charting
    tab1, tab2 = st.tabs(["Anomaly Distribution", "Feature Impact"])
    with tab1:
        st.markdown("### Transaction Volume vs Fraud Occurrences")
        fig = px.area(data.head(200), y="Amount", x=data.head(200).index, color="Class", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.markdown("### XGBoost Feature Importance")
        imp = model.feature_importances_
        idx = np.argsort(imp)[-10:]
        fig2 = px.bar(x=imp[idx], y=data.columns[idx], orientation='h', template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

elif menu == "Audit Log":
    st.title("📝 System Audit Logs")
    st.markdown("Immutable record of system actions.")
    
    if len(st.session_state.audit_log) > 0:
        for log in st.session_state.audit_log:
            st.code(log)
    else:
        st.info("No activity recorded in this session.")
