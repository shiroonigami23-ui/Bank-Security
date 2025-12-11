import pandas as pd
import joblib
import streamlit as st

@st.cache_resource
def load_model():
    try:
        return joblib.load("fraud_model_xg.pkl")
    except FileNotFoundError:
        st.error("❌ CRTICAL ERROR: 'fraud_model_xg.pkl' missing.")
        st.stop()

@st.cache_data
def load_data():
    try:
        # Auto-merge logic
        df1 = pd.read_csv("creditcard_part1.csv")
        df2 = pd.read_csv("creditcard_part2.csv")
        df = pd.concat([df1, df2])
        return df.sample(3000) # Load subset for performance
    except Exception as e:
        st.error(f"❌ Data Load Error: {e}")
        st.stop()