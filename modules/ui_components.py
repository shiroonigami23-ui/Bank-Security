import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

def kpi_card(title, value, delta, color="green"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-lbl">{title}</div>
        <div class="kpi-val">{value}</div>
        <div style="color: {color}; font-size: 0.9rem;">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

def header_animation():
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json" # Shield Animation
    anim = load_lottieurl(lottie_url)
    st_lottie(anim, height=150, key="header")