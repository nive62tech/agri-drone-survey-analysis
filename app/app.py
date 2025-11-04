# 🌾 AGRI-DRONE SURVEY DASHBOARD (Phase 3)

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="AgriDrone Survey Dashboard", layout="wide")

st.title("🌾 AgriDrone Farmer Survey Dashboard")
st.markdown("Explore interactive visualizations for all 5 sections (A–E)")

# --- PATH CONFIGURATION ---
base_dir = os.path.dirname(os.path.dirname(__file__))  # go up one level from app/
results_dir = os.path.join(base_dir, "results")

# --- LOAD CSV HELPER ---
def load_csv(filename):
    file_path = os.path.join(results_dir, filename)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        st.warning(f"⚠️ {filename} not found in /results folder.")
        return None

# --- SIDEBAR ---
st.sidebar.header("🔍 Filters")
sections = ["A - General Info", "B - Constraints", "C - Drone Awareness", "D - Customisation Needs", "E - Support Training"]
selected_section = st.sidebar.selectbox("Select Section", sections)

# --- MAP SECTION TO FILE ---
section_map = {
    "A - General Info": "f1_value_counts.csv",
    "B - Constraints": "f2_value_counts.csv",
    "C - Drone Awareness": "f3_value_counts.csv",
    "D - Customisation Needs": "f4_value_counts.csv",
    "E - Support Training": "f5_value_counts.csv"
}

filename = section_map[selected_section]

# --- LOAD SELECTED SECTION ---
df = load_csv(filename)

# --- VISUALIZATION ---
if df is not None:
    st.subheader(f"📊 {selected_section} Responses")

    # If dataframe has two columns, assume Response/Count format
    if df.shape[1] == 2:
        df.columns = ["Response", "Count"]
        fig = px.bar(df.head(15), x="Response", y="Count",
                     color="Response", title=f"Top Responses – {selected_section}",
                     template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(df.head())

    st.caption("🔸 Data source: results/" + filename)
else:
    st.info("Please make sure all f1–f5 CSV files are generated inside /results folder.")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed as part of **Phase 3 – Streamlit Dashboard** for AgriDrone Survey Analysis Project.")
