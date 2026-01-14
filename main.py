import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime, timedelta
import json
from collections import defaultdict
from modules.data_loader import load_model, load_data
from modules.ui_components import kpi_card, header_animation, timeline_chart, radar_chart
from modules.pdf_generator import create_download_link
from modules.risk_calculator import calculate_risk_score

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FinGuard Enterprise v4.0", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SUPREME CSS (Enhanced with Animations) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #0a0e17 0%, #141a24 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #161b22 0%, #1c2532 100%);
        border-right: 1px solid #2a3548;
        box-shadow: 5px 0 25px rgba(0,0,0,0.3);
    }
    
    /* Glowing Terminal Look */
    .metric-card {
        background: rgba(28, 33, 40, 0.9);
        border: 1px solid #3a4458;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 35px rgba(0,150,255,0.15);
        border-color: #4a9eff;
    }
    
    /* Custom Alert Feed Styles */
    .alert-box {
        background: linear-gradient(90deg, rgba(255, 75, 75, 0.15) 0%, rgba(255, 75, 75, 0.05) 100%);
        border-left: 4px solid #ff4b4b;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.2s ease;
    }
    
    .alert-box:hover {
        background: linear-gradient(90deg, rgba(255, 75, 75, 0.25) 0%, rgba(255, 75, 75, 0.1) 100%);
        transform: translateX(5px);
    }
    
    .safe-box {
        background: linear-gradient(90deg, rgba(46, 204, 113, 0.15) 0%, rgba(46, 204, 113, 0.05) 100%);
        border-left: 4px solid #2ecc71;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Custom Button Styles */
    .stButton > button {
        background: linear-gradient(45deg, #0066ff, #00ccff);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #0052cc, #00a3cc);
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(0, 102, 255, 0.4);
    }
    
    /* Terminal Text Animation */
    @keyframes terminal-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .terminal-cursor::after {
        content: '▋';
        animation: terminal-blink 1s infinite;
        color: #00ff88;
    }
    
    /* Custom Header */
    .main-header {
        background: linear-gradient(90deg, #1a237e, #311b92);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        border: 1px solid #4a4a8a;
        box-shadow: 0 5px 20px rgba(26, 35, 126, 0.3);
    }
    
    /* Progress Bar Custom */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ff88, #00ccff);
    }
    
    /* PDF Download Button Style */
    .pdf-download-btn {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        padding: 12px 24px;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        margin: 10px 0;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .pdf-download-btn:hover {
        background: linear-gradient(45deg, #c0392b, #a93226);
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(231, 76, 60, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE & AUTH ---
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'audit_log' not in st.session_state: 
    st.session_state.audit_log = []
if 'fraud_stats' not in st.session_state:
    st.session_state.fraud_stats = {
        'total_processed': 0,
        'fraud_detected': 0,
        'total_amount': 0,
        'fraud_amount': 0,
        'risk_score_history': []
    }
if 'recent_transactions' not in st.session_state:
    st.session_state.recent_transactions = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

CREDENTIALS = {
    "Khushee": "butterfly",
    "Kunal": "cheetah",
    "Aryan": "smooth",
    "Shiro": "oni",
    "Admin": "admin"
}

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # Enhanced Login UI
        st.markdown("""
        <div style='text-align: center; padding: 40px; border-radius: 15px; 
                    background: rgba(22, 27, 34, 0.8); border: 1px solid #2a3548;'>
            <h1 style='color: #00ccff; font-size: 2.5em; margin-bottom: 10px;'>🛡️</h1>
            <h1 style='color: #ffffff; margin-bottom: 5px;'>FinGuard v4.0</h1>
            <p style='color: #8899aa; margin-bottom: 30px;'>Enterprise Forensic Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("### 🔐 Secure Authentication")
            user = st.text_input("**Username**", placeholder="Enter credentials", key="username")
            pwd = st.text_input("**Password**", type="password", placeholder="••••••••", key="password")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("**Authenticate**", type="primary", use_container_width=True):
                    with st.spinner("Validating credentials..."):
                        time.sleep(0.5)
                        if user in CREDENTIALS and CREDENTIALS[user] == pwd:
                            st.session_state.logged_in = True
                            st.session_state.current_user = user
                            st.session_state.login_time = datetime.now()
                            st.success("✅ Authentication Successful!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("❌ Access Denied - Invalid Credentials")
                
                if st.button("🔄 Reset Session", type="secondary", use_container_width=True):
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #667788; font-size: 0.9em;'>
        <p>© 2024 FinGuard Enterprise | AML/KYC Compliance Platform</p>
        <p>For authorized personnel only. All activities are logged.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- LOAD ASSETS ---
@st.cache_data(ttl=300)
def load_cached_data():
    return load_model(), load_data()

model, data = load_cached_data()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    header_animation()
    
    # User Info
    st.markdown(f"""
    <div style='padding: 15px; background: rgba(40, 50, 70, 0.5); border-radius: 10px; margin-bottom: 20px;'>
        <p style='margin: 0; color: #8899aa; font-size: 0.9em;'>Logged in as:</p>
        <h4 style='margin: 5px 0; color: #00ccff;'>👤 {st.session_state.current_user}</h4>
        <p style='margin: 0; color: #667788; font-size: 0.8em;'>
        Since: {st.session_state.login_time.strftime('%H:%M:%S')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("🛡️ FinGuard")
    st.caption("Enterprise Forensic Intelligence v4.0")
    
    # Navigation
    menu_options = {
        "📡 Live Scanner": "Live Scanner",
        "🔍 Forensics Dashboard": "Forensics Dashboard",
        "🕸️ Network Explorer": "Network Explorer",
        "📊 Analytics Hub": "Analytics Hub",
        "📝 Audit Log": "Audit Log",
        "⚙️ System Config": "System Config"
    }
    
    menu = st.radio(
        "Navigation",
        list(menu_options.keys()),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # System Status
    status_col1, status_col2 = st.columns([1, 2])
    with status_col1:
        st.markdown("🔴" if len(st.session_state.alerts) > 5 else "🟢")
    with status_col2:
        st.caption(f"{len(st.session_state.alerts)} active alerts")
    
    # Quick Stats
    with st.expander("📈 Quick Stats", expanded=False):
        st.metric("Processed", f"{st.session_state.fraud_stats['total_processed']:,}")
        st.metric("Fraud Rate", f"{(st.session_state.fraud_stats['fraud_detected']/max(1, st.session_state.fraud_stats['total_processed'])*100):.2f}%")
        st.metric("Total Value", f"€{st.session_state.fraud_stats['total_amount']:,.0f}")
    
    # Logout
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# --- MODULE 1: LIVE SCANNER (Enhanced) ---
if menu_options[menu] == "Live Scanner":
    st.title("📡 Real-Time Transaction Monitor")
    
    # Header with Live Status
    st.markdown(f"""
    <div class='main-header'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h2 style='margin: 0; color: #ffffff;'>Live Transaction Scanner</h2>
                <p style='margin: 5px 0 0 0; color: #aaccff;'>Monitoring: <span class='terminal-cursor'>4,283 active sessions</span></p>
            </div>
            <div style='text-align: right;'>
                <p style='margin: 0; color: #00ff88; font-size: 1.2em;'>▲ 99.94% Accuracy</p>
                <p style='margin: 0; color: #8899aa; font-size: 0.9em;'>Last update: {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        kpi_card("System Accuracy", "99.94%", "+0.01%", "#2ecc71", icon="📈")
    with k2: 
        kpi_card("Live Traffic", "4.2M", "Active", "#3498db", icon="🔀")
    with k3: 
        kpi_card("Detected Threats", str(len([x for x in st.session_state.audit_log if "⚠" in x])), "Live", "#e74c3c", icon="🚨")
    with k4:
        kpi_card("Avg. Latency", "42ms", "Stable", "#9b59b6", icon="⚡")
    
    # Main Content
    col_ui, col_graph = st.columns([1, 2])
    
    with col_ui:
        st.subheader("🔒 Transaction Processing Gate")
        
        # Transaction Simulator
        with st.container():
            st.markdown("### Simulate Transaction")
            
            # Transaction Details
            col_a, col_b = st.columns(2)
            with col_a:
                tx_amount = st.slider("Amount (€)", 10, 10000, 500, 10)
                tx_type = st.selectbox("Type", ["Card Payment", "Bank Transfer", "Crypto", "Merchant"])
            with col_b:
                tx_country = st.selectbox("Country", ["US", "UK", "DE", "FR", "NL", "RU", "CN"])
                tx_velocity = st.select_slider("Velocity", ["Normal", "High", "Extreme"])
            
            # Process Button
            if st.button("🚀 Process Transaction", type="primary", use_container_width=True):
                with st.spinner("Analyzing transaction patterns..."):
                    time.sleep(0.8)
                    
                    # Generate transaction
                    tx = data.sample(1)
                    features = tx.drop(['Class'], axis=1)
                    tx_id = f"TX{np.random.randint(100000,999999)}"
                    
                    # Prediction
                    pred = model.predict(features)[0]
                    prob = model.predict_proba(features)[0][1] * 100
                    
                    # Calculate risk score
                    risk_score = calculate_risk_score(
                        amount=tx_amount,
                        probability=prob/100,
                        country=tx_country,
                        velocity=tx_velocity
                    )
                    
                    # Update stats
                    st.session_state.fraud_stats['total_processed'] += 1
                    st.session_state.fraud_stats['total_amount'] += tx_amount
                    
                    # Store recent transaction
                    st.session_state.recent_transactions.append({
                        'id': tx_id,
                        'amount': tx_amount,
                        'risk': risk_score,
                        'type': tx_type,
                        'time': datetime.now().strftime('%H:%M:%S')
                    })
                    
                    if pred == 1 or risk_score > 0.7:
                        st.session_state.fraud_stats['fraud_detected'] += 1
                        st.session_state.fraud_stats['fraud_amount'] += tx_amount
                        
                        alert_msg = f"🚨 HIGH RISK: ID {tx_id} | €{tx_amount:,.2f} | Score: {risk_score:.2%}"
                        st.session_state.audit_log.append(alert_msg)
                        st.session_state.alerts.append({
                            'id': tx_id,
                            'severity': 'HIGH',
                            'message': f'Potential fraud detected',
                            'time': datetime.now()
                        })
                        
                        # Alert Display
                        st.error(f"""
                        ### 🚨 FRAUD DETECTED
                        **Transaction ID:** {tx_id}  
                        **Amount:** €{tx_amount:,.2f}  
                        **Risk Score:** {risk_score:.2%}  
                        **Probability:** {prob:.2f}%  
                        **Action:** ❌ BLOCKED
                        """)
                        
                        # Generate PDF Report using your existing function
                        with st.expander("📋 Generate Forensic Report", expanded=True):
                            st.markdown(create_download_link(tx_id, f"{risk_score*100:.1f}", tx_amount, "HIGH RISK - BLOCKED"), 
                                      unsafe_allow_html=True)
                            
                    else:
                        success_msg = f"✅ APPROVED: ID {tx_id} | €{tx_amount:,.2f} | Score: {risk_score:.2%}"
                        st.session_state.audit_log.append(success_msg)
                        
                        st.success(f"""
                        ### ✅ TRANSACTION SECURE
                        **Transaction ID:** {tx_id}  
                        **Amount:** €{tx_amount:,.2f}  
                        **Risk Score:** {risk_score:.2%}  
                        **Probability:** {prob:.4f}%  
                        **Action:** ✓ APPROVED
                        """)
                        
                        # Generate safe transaction report
                        with st.expander("📋 Generate Transaction Report", expanded=False):
                            st.markdown(create_download_link(tx_id, f"{risk_score*100:.1f}", tx_amount, "SAFE - APPROVED"), 
                                      unsafe_allow_html=True)
        
        # Recent Transactions
        st.subheader("📋 Recent Activity")
        if st.session_state.recent_transactions:
            for tx in list(reversed(st.session_state.recent_transactions))[:5]:
                risk_color = "#ff4b4b" if tx['risk'] > 0.7 else "#2ecc71"
                st.markdown(f"""
                <div style='padding: 10px; margin: 5px 0; background: rgba(40, 44, 52, 0.5); border-radius: 8px; border-left: 4px solid {risk_color};'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span><strong>{tx['id']}</strong></span>
                        <span style='color: {risk_color};'>{tx['risk']:.1%}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.9em; color: #8899aa;'>
                        <span>€{tx['amount']:,.2f} • {tx['type']}</span>
                        <span>{tx['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No transactions processed yet. Click 'Process Transaction' to begin.")
    
    with col_graph:
        st.subheader("🧠 Deep Learning Vector Space")
        
        # 3D Visualization
        df_viz = data.sample(500)
        df_viz['Type'] = df_viz['Class'].map({0: 'Safe', 1: 'Fraud'})
        df_viz['Size'] = np.abs(df_viz['V11']) * 10
        
        fig = px.scatter_3d(
            df_viz, 
            x='V11', 
            y='V12', 
            z='V14', 
            color='Type',
            size='Size',
            color_discrete_map={'Safe': '#00ff88', 'Fraud': '#ff0000'},
            template="plotly_dark",
            hover_data=['V1', 'V2', 'V3'],
            opacity=0.8
        )
        
        fig.update_layout(
            scene=dict(
                xaxis_title="Feature V11",
                yaxis_title="Feature V12", 
                zaxis_title="Feature V14",
                bgcolor="rgba(0,0,0,0)"
            ),
            margin=dict(l=0, r=0, b=0, t=30)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Real-time metrics
        st.subheader("📊 Model Performance")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Precision", "99.2%", "0.3%")
        with col_m2:
            st.metric("Recall", "98.7%", "0.2%")
        with col_m3:
            st.metric("F1-Score", "98.9%", "0.25%")

# --- MODULE 2: FORENSICS DASHBOARD (Enhanced) ---
elif menu_options[menu] == "Forensics Dashboard":
    st.title("🔍 Forensic Intelligence Dashboard")
    
    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: kpi_card("Total Cases", "1,847", "+12 Today", "#4a6fff", icon="📁")
    with m2: kpi_card("Open Investigations", "24", "Active", "#ff6b4a", icon="🔎")
    with m3: kpi_card("Avg Resolution", "3.2h", "-0.5h", "#2ecc71", icon="⏱️")
    with m4: kpi_card("Evidence Items", "8,429", "+142", "#9b59b6", icon="📊")
    
    col_alert, col_map = st.columns([1, 2])
    
    with col_alert:
        st.subheader("🚨 Active Alerts Feed")
        
        # Generate sample alerts
        sample_alerts = [
            {"id": "FRAUD-001", "type": "Card Cloning", "score": 0.98, "amount": "€12,450", "location": "NL"},
            {"id": "FRAUD-002", "type": "Money Mule", "score": 0.87, "amount": "€8,900", "location": "RU"},
            {"id": "FRAUD-003", "type": "ATO Attack", "score": 0.92, "amount": "€23,100", "location": "US"},
            {"id": "FRAUD-004", "type": "Merchant Fraud", "score": 0.76, "amount": "€5,600", "location": "DE"}
        ]
        
        for alert in sample_alerts:
            severity_color = "#ff4b4b" if alert['score'] > 0.9 else "#ffa500"
            st.markdown(f"""
            <div class='alert-box'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div>
                        <strong>🔴 {alert['id']}</strong><br>
                        <small>{alert['type']}</small>
                    </div>
                    <span style='color: {severity_color}; font-weight: bold;'>{alert['score']:.2f}</span>
                </div>
                <div style='font-size: 0.85em; color: #aabbcc; margin-top: 5px;'>
                    💰 {alert['amount']} | 🌍 {alert['location']}
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 8px;'>
                    <button style='background: {severity_color}; color: white; border: none; padding: 4px 12px; border-radius: 4px; font-size: 0.8em;'>
                        Investigate
                    </button>
                    <span style='font-size: 0.8em; color: #667788;'>5m ago</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Generate PDF for all alerts
        if st.button("📥 Export All Alerts as PDF", use_container_width=True):
            # Create a summary PDF
            combined_id = f"ALERT-SUMMARY-{datetime.now().strftime('%Y%m%d')}"
            total_amount = sum([12450, 8900, 23100, 5600])
            avg_score = np.mean([0.98, 0.87, 0.92, 0.76])
            
            st.markdown(create_download_link(
                combined_id, 
                f"{avg_score*100:.1f}", 
                total_amount, 
                "ALERT SUMMARY"
            ), unsafe_allow_html=True)
    
    with col_map:
        st.subheader("🌍 Global Risk Heatmap")
        
        # Enhanced heatmap
        countries = ['US', 'UK', 'DE', 'FR', 'NL', 'RU', 'CN', 'BR', 'IN', 'AU']
        risk_data = pd.DataFrame({
            'country': countries * 3,
            'lat': [np.random.uniform(25, 50) for _ in range(len(countries)*3)],
            'lon': [np.random.uniform(-120, 150) for _ in range(len(countries)*3)],
            'risk': np.random.rand(len(countries)*3),
            'volume': np.random.randint(100, 10000, len(countries)*3)
        })
        
        fig_map = px.density_mapbox(
            risk_data, 
            lat='lat', 
            lon='lon', 
            z='risk',
            radius=20,
            zoom=1,
            mapbox_style="carto-darkmatter",
            color_continuous_scale=[[0, '#00ff88'], [0.5, '#ffa500'], [1, '#ff4b4b']],
            opacity=0.8
        )
        
        fig_map.update_layout(
            margin={"r":0,"t":30,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Risk Timeline
        st.subheader("📈 Risk Score Timeline")
        timeline_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'risk': np.random.rand(30) * 0.5 + 0.3
        })
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=timeline_data['date'],
            y=timeline_data['risk'],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#00ccff', width=3),
            marker=dict(size=6, color='#ffffff')
        ))
        
        fig_timeline.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=250,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})

# --- MODULE 3: NETWORK EXPLORER (Enhanced) ---
elif menu_options[menu] == "Network Explorer":
    st.title("🕸️ Fraud Network Intelligence")
    
    # Network Configuration
    col_config, col_stats = st.columns([1, 2])
    
    with col_config:
        st.subheader("Network Parameters")
        num_nodes = st.slider("Number of Nodes", 10, 50, 25)
        cluster_prob = st.slider("Cluster Probability", 0.0, 1.0, 0.15, 0.05)
        anomaly_nodes = st.slider("Anomaly Nodes (%)", 5, 30, 15)
        
        if st.button("🔄 Generate Network", type="primary"):
            st.rerun()
    
    with col_stats:
        st.subheader("Network Statistics")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        with stats_col1: st.metric("Total Nodes", num_nodes)
        with stats_col2: st.metric("Connections", f"{num_nodes * 3}")
        with stats_col3: st.metric("Density", "0.24")
    
    # Generate Network
    G = nx.powerlaw_cluster_graph(num_nodes, 3, cluster_prob)
    pos = nx.spring_layout(G, seed=42)
    
    # Add anomalies
    anomaly_count = int(num_nodes * anomaly_nodes / 100)
    anomaly_nodes_list = list(G.nodes())[:anomaly_count]
    
    # Create traces
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, 
        y=edge_y, 
        line=dict(width=0.8, color='rgba(100, 150, 200, 0.4)'), 
        mode='lines',
        hoverinfo='none'
    )
    
    # Node traces
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node in anomaly_nodes_list:
            node_colors.append('#ff4b4b')
            node_sizes.append(25)
        else:
            node_colors.append('#00ccff')
            node_sizes.append(15)
    
    node_trace = go.Scatter(
        x=node_x, 
        y=node_y, 
        mode='markers+text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        text=[f"N{i}" for i in range(num_nodes)],
        textposition="top center",
        hoverinfo='text',
        hovertext=[f"Node {i}<br>Connections: {len(list(G.neighbors(i)))}<br>Risk: {'High' if i in anomaly_nodes_list else 'Low'}" 
                   for i in range(num_nodes)]
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace], 
                   layout=go.Layout(
                       showlegend=False,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       xaxis=dict(showgrid=False, zeroline=False, visible=False),
                       yaxis=dict(showgrid=False, zeroline=False, visible=False),
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=0),
                       height=600
                   ))
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
    
    # Network Analysis
    st.subheader("🔍 Network Analysis")
    
    col_anal1, col_anal2, col_anal3 = st.columns(3)
    with col_anal1:
        st.markdown("**Centrality Analysis**")
        centrality = nx.degree_centrality(G)
        top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:3]
        for node, score in top_nodes:
            st.markdown(f"Node {node}: `{score:.3f}`")
    
    with col_anal2:
        st.markdown("**Community Detection**")
        communities = nx.community.greedy_modularity_communities(G)
        st.markdown(f"Detected: `{len(communities)}` communities")
    
    with col_anal3:
        st.markdown("**Anomaly Detection**")
        st.markdown(f"High-risk nodes: `{len(anomaly_nodes_list)}`")
        st.markdown(f"Risk score: `{(len(anomaly_nodes_list)/num_nodes):.1%}`")
    
    # Export Network Report
    st.subheader("📤 Export Network Analysis")
    if st.button("📄 Generate Network Report PDF", use_container_width=True):
        network_id = f"NETWORK-{datetime.now().strftime('%H%M%S')}"
        risk_score = len(anomaly_nodes_list) / num_nodes
        
        st.markdown(create_download_link(
            network_id,
            f"{risk_score*100:.1f}",
            num_nodes * 100,  # Simulated value
            "NETWORK ANALYSIS"
        ), unsafe_allow_html=True)

# --- MODULE 4: ANALYTICS HUB (New) ---
elif menu_options[menu] == "Analytics Hub":
    st.title("📊 Advanced Analytics Hub")
    
    # Data Overview
    st.subheader("📈 Transaction Analytics")
    
    # Generate sample time series data
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    analytics_data = pd.DataFrame({
        'Date': dates,
        'Total_Transactions': np.random.randint(1000, 5000, 30),
        'Fraud_Transactions': np.random.randint(10, 200, 30),
        'Avg_Amount': np.random.uniform(100, 1000, 30),
        'Risk_Score': np.random.rand(30) * 0.3 + 0.4
    })
    
    analytics_data['Fraud_Rate'] = (analytics_data['Fraud_Transactions'] / analytics_data['Total_Transactions']) * 100
    
    # Multiple charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=analytics_data['Date'],
            y=analytics_data['Total_Transactions'],
            name='Total',
            marker_color='#3498db'
        ))
        fig1.add_trace(go.Bar(
            x=analytics_data['Date'],
            y=analytics_data['Fraud_Transactions'],
            name='Fraud',
            marker_color='#e74c3c'
        ))
        fig1.update_layout(
            title="Transaction Volume",
            template="plotly_dark",
            barmode='group',
            height=300
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_chart2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=analytics_data['Date'],
            y=analytics_data['Fraud_Rate'],
            mode='lines+markers',
            name='Fraud Rate',
            line=dict(color='#ff4b4b', width=3),
            fill='tozeroy'
        ))
        fig2.add_hline(y=2.5, line_dash="dash", line_color="#00ff88", annotation_text="Threshold")
        fig2.update_layout(
            title="Fraud Rate (%)",
            template="plotly_dark",
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Feature Importance
    st.subheader("🎯 Model Feature Importance")
    
    # Simulate feature importance
    features = [f'V{i}' for i in range(1, 15)]
    importance = np.random.rand(14)
    importance = importance / importance.sum()
    
    feature_df = pd.DataFrame({
        'Feature': features,
        'Importance': importance
    }).sort_values('Importance', ascending=True)
    
    fig3 = go.Figure(go.Bar(
        x=feature_df['Importance'],
        y=feature_df['Feature'],
        orientation='h',
        marker_color='#00ccff'
    ))
    
    fig3.update_layout(
        template="plotly_dark",
        height=400,
        title="Feature Importance Scores",
        xaxis_title="Importance",
        yaxis_title="Feature"
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Export Analytics Report
    st.subheader("📤 Export Analytics Report")
    if st.button("📄 Generate Analytics Report PDF", use_container_width=True):
        report_id = f"ANALYTICS-{datetime.now().strftime('%Y%m%d')}"
        avg_fraud_rate = analytics_data['Fraud_Rate'].mean()
        
        st.markdown(create_download_link(
            report_id,
            f"{avg_fraud_rate:.1f}",
            analytics_data['Total_Transactions'].sum(),
            "ANALYTICS REPORT"
        ), unsafe_allow_html=True)

# --- MODULE 5: AUDIT LOG (Enhanced) ---
elif menu_options[menu] == "Audit Log":
    st.title("📝 System Audit & Activity Log")
    
    # Filters
    col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
    with col_filter1:
        log_type = st.selectbox("Log Type", ["All", "Fraud", "Approval", "System"])
    with col_filter2:
        date_range = st.selectbox("Time Range", ["Last 24h", "Last 7d", "Last 30d", "All"])
    with col_filter3:
        severity = st.multiselect("Severity", ["High", "Medium", "Low", "Info"], default=["High", "Medium"])
    with col_filter4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh Logs", use_container_width=True):
            st.rerun()
    
    # Log Display
    st.subheader("🔍 Activity Timeline")
    
    if st.session_state.audit_log:
        # Create timeline display
        for idx, log in enumerate(reversed(st.session_state.audit_log[-50:])):  # Last 50 entries
            timestamp = datetime.now() - timedelta(minutes=idx*5)
            
            # Determine log type
            if "⚠" in log or "🚨" in log:
                log_color = "#ff4b4b"
                log_icon = "🚨"
                log_type = "FRAUD"
            elif "✅" in log:
                log_color = "#2ecc71"
                log_icon = "✅"
                log_type = "APPROVAL"
            else:
                log_color = "#3498db"
                log_icon = "📝"
                log_type = "SYSTEM"
            
            # Timeline item
            col_time, col_content = st.columns([1, 4])
            
            with col_time:
                st.markdown(f"""
                <div style='text-align: right; color: #8899aa; font-size: 0.85em;'>
                    {timestamp.strftime('%H:%M:%S')}<br>
                    <small>{timestamp.strftime('%m/%d')}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col_content:
                st.markdown(f"""
                <div style='padding: 12px; margin: 5px 0; background: rgba(40, 44, 52, 0.7); 
                            border-radius: 8px; border-left: 4px solid {log_color};'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 1.2em; margin-right: 10px;'>{log_icon}</span>
                        <div style='flex-grow: 1;'>
                            <strong>{log}</strong><br>
                            <span style='font-size: 0.85em; color: {log_color};'>Type: {log_type}</span>
                        </div>
                        <span style='font-size: 0.8em; color: #667788;'>
                            ID: LOG{10000 - idx}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Summary
        st.markdown("---")
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        with col_sum1:
            fraud_count = len([x for x in st.session_state.audit_log if "⚠" in x or "🚨" in x])
            st.metric("Total Fraud Events", fraud_count)
        with col_sum2:
            st.metric("Total Log Entries", len(st.session_state.audit_log))
        with col_sum3:
            st.metric("Last Entry", st.session_state.audit_log[-1][:40] + "..." if st.session_state.audit_log else "None")
        
        # Export options
        st.subheader("📤 Export Options")
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        with col_exp1:
            # CSV Export
            if st.session_state.audit_log:
                log_df = pd.DataFrame({
                    'timestamp': [datetime.now() - timedelta(minutes=i*5) for i in range(len(st.session_state.audit_log))],
                    'message': st.session_state.audit_log,
                    'type': ['FRAUD' if "⚠" in x or "🚨" in x else 'APPROVAL' if "✅" in x else 'SYSTEM' for x in st.session_state.audit_log]
                })
                csv = log_df.to_csv(index=False)
                st.download_button(
                    label="📄 Export as CSV",
                    data=csv,
                    file_name="audit_logs.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col_exp2:
            # PDF Export
            if st.button("📊 Generate PDF Report", use_container_width=True):
                report_id = f"AUDIT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                fraud_rate = (fraud_count / len(st.session_state.audit_log)) * 100 if st.session_state.audit_log else 0
                
                st.markdown(create_download_link(
                    report_id,
                    f"{fraud_rate:.1f}",
                    len(st.session_state.audit_log),
                    "AUDIT LOG SUMMARY"
                ), unsafe_allow_html=True)
        
        with col_exp3:
            if st.button("🗑️ Clear Logs", use_container_width=True, type="secondary"):
                st.session_state.audit_log = []
                st.rerun()
    
    else:
        st.info("📭 No activity recorded yet. Process some transactions to see logs here.")

# --- MODULE 6: SYSTEM CONFIG (New) ---
elif menu_options[menu] == "System Config":
    st.title("⚙️ System Configuration")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔐 Security", "📈 Model", "🌐 Network", "📊 Monitoring"])
    
    with tab1:
        st.subheader("Security Settings")
        
        col_sec1, col_sec2 = st.columns(2)
        with col_sec1:
            st.checkbox("Enable 2FA", value=True)
            st.checkbox("IP Whitelisting", value=True)
            st.checkbox("Session Timeout (30m)", value=True)
        with col_sec2:
            st.checkbox("Encrypt Database", value=True)
            st.checkbox("Audit Trail", value=True)
            st.checkbox("Real-time Alerts", value=True)
        
        st.subheader("Risk Thresholds")
        fraud_threshold = st.slider("Fraud Probability Threshold", 0.5, 0.95, 0.85, 0.05)
        amount_threshold = st.number_input("High Amount Threshold (€)", 5000, 50000, 10000, 1000)
        
        if st.button("💾 Save Security Settings", type="primary"):
            st.success("Security settings updated successfully!")
            
            # Generate configuration report
            config_id = f"CONFIG-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            st.markdown(create_download_link(
                config_id,
                "100.0",  # Config is always 100% complete
                1,  # Dummy value
                "SYSTEM CONFIGURATION"
            ), unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Model Configuration")
        
        model_type = st.selectbox("Model Type", ["Random Forest", "Gradient Boosting", "Neural Network", "Ensemble"])
        
        col_mod1, col_mod2 = st.columns(2)
        with col_mod1:
            st.number_input("Max Depth", 5, 50, 20)
            st.number_input("Number of Trees", 50, 500, 100)
        with col_mod2:
            st.number_input("Learning Rate", 0.01, 0.5, 0.1, 0.01)
            st.number_input("Batch Size", 32, 512, 128)
        
        if st.button("🔄 Retrain Model", type="primary"):
            with st.spinner("Retraining model with new parameters..."):
                time.sleep(2)
                st.success("Model retrained successfully!")
    
    with tab3:
        st.subheader("Network Configuration")
        
        st.text_input("API Endpoint", "https://api.finguard.com/v4/")
        st.text_input("Database Host", "db.fraud-detection.internal")
        st.number_input("Connection Pool Size", 5, 100, 20)
        st.number_input("Timeout (seconds)", 5, 60, 30)
        
        if st.button("🔗 Test Connections", type="primary"):
            with st.spinner("Testing network connections..."):
                time.sleep(1.5)
                st.success("All connections tested successfully!")
    
    with tab4:
        st.subheader("Monitoring Settings")
        
        col_mon1, col_mon2 = st.columns(2)
        with col_mon1:
            st.checkbox("CPU Monitoring", value=True)
            st.checkbox("Memory Usage", value=True)
            st.checkbox("Disk I/O", value=True)
        with col_mon2:
            st.checkbox("Network Traffic", value=True)
            st.checkbox("Error Rate", value=True)
            st.checkbox("Latency Tracking", value=True)
        
        st.subheader("Alert Preferences")
        alert_email = st.text_input("Alert Email", "alerts@company.com")
        st.multiselect("Notification Channels", ["Email", "Slack", "SMS", "Webhook"], default=["Email", "Slack"])
        
        if st.button("📱 Save Monitoring Config", type="primary"):
            st.success("Monitoring configuration saved!")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #667788; font-size: 0.9em; padding: 20px;'>
    <p>🛡️ <strong>FinGuard Enterprise v4.0</strong> | AML/KYC Compliance Platform</p>
    <p>© 2024 Financial Intelligence Systems | All rights reserved | <a href='#' style='color: #00ccff;'>Privacy Policy</a> | <a href='#' style='color: #00ccff;'>Terms of Service</a></p>
    <p style='color: #445566; font-size: 0.8em; margin-top: 10px;'>
        Session ID: FIN-{session_id} | Version: 4.0.1 | Last Updated: {update_time}
    </p>
</div>
""".format(
    session_id=np.random.randint(100000, 999999),
    update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
), unsafe_allow_html=True)