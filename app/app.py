# --- 🌾 AGRIDRONE SURVEY DASHBOARD ---

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- ⚙️ PAGE SETTINGS ---
st.set_page_config(page_title="AgriDrone Survey Dashboard", layout="wide")

# --- 📂 DEFINE PATHS ---
base_path = os.path.dirname(os.path.dirname(__file__))  # go up one folder
results_path = os.path.join(base_path, "results")

# --- 🧾 LOAD DATA ---
summary_file = os.path.join(results_path, "summary_statistics.csv")

if os.path.exists(summary_file):
    df = pd.read_csv(summary_file)
else:
    st.error("❌ 'summary_statistics.csv' not found in results folder. Run EDA first.")
    st.stop()

# --- 🧭 SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")
sections = ['A', 'B', 'C', 'D', 'E']
selected_section = st.sidebar.selectbox("Select Section", sections)
st.sidebar.markdown("---")

st.title("🌾 AgriDrone Farmer Survey Dashboard")
st.write("Explore farmer survey responses interactively across Sections A–E.")

# --- 🗂️ SECTION TABS ---
tabA, tabB, tabC, tabD, tabE = st.tabs([
    "Section A", "Section B", "Section C", "Section D", "Section E"
])

# --- 🔹 FUNCTION TO DISPLAY CHARTS FOR EACH SECTION ---
def render_section(section_name):
    st.subheader(f"📘 Section {section_name} Overview")

    # Filter by section if applicable
    if "section" in df.columns:
        filtered_df = df[df["section"].astype(str).str.contains(section_name, case=False, na=False)]
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        st.warning(f"No data found for Section {section_name}")
        return

    # Example 1 — Distribution of responses
    fig1 = px.histogram(
        filtered_df,
        x="section",
        title=f"Response Distribution — Section {section_name}",
        color="section",
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Example 2 — Example question visualization (replace f1 with any question column)
    question_cols = [c for c in filtered_df.columns if c.startswith("f")]
    if question_cols:
        first_col = question_cols[0]
        fig2 = px.bar(
            filtered_df,
            x=first_col,
            color="section",
            title=f"Example Question ({first_col}) — Section {section_name}",
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("ℹ️ No question columns (like f1, f2, etc.) found in the dataset yet.")

# --- 🖼️ SHOW EACH SECTION TAB ---
with tabA: render_section("A")
with tabB: render_section("B")
with tabC: render_section("C")
with tabD: render_section("D")
with tabE: render_section("E")

# --- ✅ FOOTER ---
st.markdown("---")
st.caption("Developed as part of AgriDrone Survey Analysis • Phase 3 Dashboard")
