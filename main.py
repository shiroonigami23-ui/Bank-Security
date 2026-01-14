import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_model, load_data
from modules.ui_components import kpi_card, header_animation
from modules.pdf_generator import create_download_link

# --- PAGE CONFIG ---
st.set_page_config(page_title="FinGuard Enterprise", page_icon="🛡", layout="wide")

# --- CUSTOM UI STYLING (Matching Images) ---
st.markdown("""
<style>
    /* Dark Theme Overrides */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* Alert Feed Styling */
    .alert-container {
        background: rgba(255, 50, 50, 0.05);
        border-left: 4px solid #ff4b4b;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    .alert-title { color: #ff4b4b; font-weight: bold; font-size: 0.8rem; }
    .alert-desc { font-size: 0.75rem; color: #cccccc; }
    
    /* Metrics Card Styling */
    .metric-box {
        background: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: white; }
    .metric-label { color: #8b949e; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'audit_log' not in st.session_state: st.session_state.audit_log = []

# --- LOGIN SCREEN (Preserved Exactly) ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("🛡 FinGuard Access")
        st.markdown("Enter secure credentials to access the banking mainframe.")
        CREDENTIALS = {"Khushee": "butterfly", "Kunal": "cheetah", "Aryan": "smooth", "Shiro": "oni", "Admin": "admin"}
        user = st.text_input("Username", placeholder="Enter ID")
        pwd = st.text_input("Password", type="password", placeholder="Enter Password")
        if st.button("Authenticate"):
            if user in CREDENTIALS and CREDENTIALS[user] == pwd:
                with st.spinner(f"Verifying Identity: {user.upper()}..."): time.sleep(1.0)
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("❌ Access Denied: Invalid Credentials")
    st.stop()

# --- LOAD ASSETS ---
model = load_model()
data = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡 FinGuard")
    st.caption("Enterprise Edition v3.0")
    menu = st.radio("Module", ["Live Scanner", "Forensics Dashboard", "Network Explorer", "Audit Log"])
    st.markdown("---")
    st.success("● Network Secure")

# --- MODULE 1: LIVE SCANNER (Enhanced) ---
if menu == "Live Scanner":
    c1, c2 = st.columns([1, 4])
    with c1: header_animation()
    with c2: 
        st.title("Real-Time Threat Monitor")
        st.caption("Listening on Port 443 | AES-256 Encryption Active")

    k1, k2, k3 = st.columns(3)
    with k1: kpi_card("System Accuracy", "99.94%", "+0.01%", "#2ecc71")
    with k2: kpi_card("Transactions Processed", "4.2M", "+12k today", "#3498db")
    with k3: kpi_card("Active Threats", "0", "System Clear", "#2ecc71")

    col_ui, col_graph = st.columns([1, 2])
    with col_ui:
        st.subheader("Transaction Gate")
        if st.button("Processing Incoming Packet", type="primary"):
            tx = data.sample(1)
            features = tx.drop(['Class'], axis=1)
            val, tx_id = tx.iloc[0]['Amount'], str(np.random.randint(100000,999999))
            prob = model.predict_proba(features)[0][1]
            if prob > 0.5:
                st.error("🚨 FRAUD DETECTED")
                st.markdown(create_download_link(tx_id, f"{prob*100:.2f}", val, "HIGH RISK"), unsafe_allow_html=True)
                st.session_state.audit_log.append(f"⚠ BLOCKED: ID {tx_id} | Amt €{val:.2f}")
            else:
                st.success("✅ Transaction Approved")
                st.session_state.audit_log.append(f"✅ APPROVED: ID {tx_id} | Amt €{val:.2f}")

    with col_graph:
        df_viz = data.sample(300)
        df_viz['Type'] = df_viz['Class'].map({0: 'Safe', 1: 'Fraud'})
        fig = px.scatter_3d(df_viz, x='V11', y='V12', z='V14', color='Type',
                            color_discrete_map={'Safe': '#00ff88', 'Fraud': '#ff0000'},
                            opacity=0.7, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# --- MODULE 2: FORENSICS DASHBOARD (Matches Image 1) ---
elif menu == "Forensics Dashboard":
    st.title("FORENSIC DASHBOARD OVERVIEW: REAL-TIME ALERTS AND RISK METRICS")
    
    col_alerts, col_map, col_metrics = st.columns([1.2, 3, 0.8])
    
    with col_alerts:
        st.subheader("Alerts Feed")
        alerts = [
            ("High Risk Transaction", "Source: Account 48... in Panama"),
            ("High Risk Transaction", "Suspicious transfer NY -> Russia"),
            ("High Risk Transaction", "Multiple failures in account 12"),
            ("High Risk Transaction", "High velocity account activity"),
            ("High Risk Transaction", "Rapid cross-border transfer")
        ]
        for title, desc in alerts:
            st.markdown(f"""
            <div class="alert-container">
                <div class="alert-title">🔴 {title}</div>
                <div class="alert-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_map:
        st.subheader("Risk Heatmap")
        # Generate dummy global risk points
        map_data = pd.DataFrame({
            'lat': [40.7128, 51.5074, 35.6895, -23.5505, 28.6139, -33.8688],
            'lon': [-74.0060, -0.1278, 139.6917, -46.6333, 77.2090, 151.2093],
            'risk': [100, 80, 90, 70, 85, 95]
        })
        fig_map = px.scatter_geo(map_data, lat='lat', lon='lon', size='risk',
                                 color_discrete_sequence=['#ff4b4b'], template="plotly_dark")
        fig_map.update_geos(showcountries=True, countrycolor="#30363d", showcoastlines=True, bgcolor="#0e1117")
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=400)
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.subheader("Transaction Risk Score Over Time")
        chart_data = pd.DataFrame(np.random.randn(50, 1), columns=['Risk Score'])
        st.line_chart(chart_data, height=150)

    with col_metrics:
        st.subheader("Key Metrics")
        st.markdown('<div class="metric-box"><div class="metric-label">Total Alerts (24h)</div><div class="metric-value">1,245</div></div><br>', unsafe_allow_html=True)
        st.markdown('<div class="metric-box"><div class="metric-label">False Positive Rate</div><div class="metric-value" style="color:#2ecc71">3.2% ↓</div></div><br>', unsafe_allow_html=True)
        st.markdown('<div class="metric-box"><div class="metric-label">Processing Latency</div><div class="metric-value">185 ms</div></div>', unsafe_allow_html=True)

# --- MODULE 3: NETWORK EXPLORER (Matches Image 2) ---
elif menu == "Network Explorer":
    st.title("NETWORK EXPLORER: VISUALIZING MULTI-HOP RELATIONSHIPS")
    st.caption("Influenced by: Neighbor nodes with high transaction velocity and circular payment patterns")
    
    # Create the Graph Visualization using Plotly
    edge_x = []
    edge_y = []
    node_x = [1, 2, 4, 3, 1.5, 4.5, 2.5, 3.5, 5, 0.5]
    node_y = [2, 4, 3, 1, 0.5, 1.5, 4.5, 2.5, 4, 3.5]
    
    # Create edges (Connections)
    connections = [(0,1), (1,2), (2,3), (3,0), (1,6), (2,8), (0,4), (3,5), (7,2), (9,1)]
    for edge in connections:
        edge_x.extend([node_x[edge[0]], node_x[edge[1]], None])
        edge_y.extend([node_y[edge[0]], node_y[edge[1]], None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#444'), hoverinfo='none', mode='lines')

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False, color=['#ff4b4b' if i % 3 == 0 else '#1f77b4' for i in range(len(node_x))],
            size=[40 if i % 3 == 0 else 25 for i in range(len(node_x))],
            line_width=2))

    fig_net = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False, hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    
    c_net, c_det = st.columns([3, 1])
    with c_net:
        st.plotly_chart(fig_net, use_container_width=True)
    with c_det:
        st.subheader("Cluster Details")
        st.info("Node ID: user_8829\nRisk Score: 0.94 (High)\nTransactions: 1,024")
        st.markdown("### Connected Entities")
        st.code("Acc_9921: High Risk\nAcc_1022: Low Risk\nAcc_0029: Suspicious")

# --- MODULE 4: AUDIT LOG (Preserved) ---
elif menu == "Audit Log":
    st.title("📝 System Audit Logs")
    if len(st.session_state.audit_log) > 0:
        for log in st.session_state.audit_log: st.code(log)
    else: st.info("No activity recorded in this session.")
