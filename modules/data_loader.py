import pandas as pd
import joblib
import streamlit as st
import numpy as np

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
        df1 = pd.read_csv("creditcard_part1.csv")
        df2 = pd.read_csv("creditcard_part2.csv")
        df = pd.concat([df1, df2], ignore_index=True)
        return df.sample(min(len(df), 3000), random_state=42)
    except FileNotFoundError:
        st.warning("⚠ Dataset CSVs not found. Using built-in synthetic demo data.")
        return _synthetic_dataset(3000)
    except Exception as e:
        st.error(f"❌ Data Load Error: {e}")
        st.stop()


def _synthetic_dataset(rows: int):
    rng = np.random.default_rng(42)
    data = {f"V{i}": rng.normal(0, 1, rows) for i in range(1, 29)}
    data["Amount"] = rng.uniform(0, 5000, rows)
    data["Class"] = rng.choice([0, 1], size=rows, p=[0.985, 0.015])
    return pd.DataFrame(data)
