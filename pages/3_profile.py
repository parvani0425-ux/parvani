import streamlit as st
import json
import os
import pandas as pd

st.title("👤 Profile & Full Analysis History")

history_file = "history.json"

# ---------------- SAFE LOAD ----------------
if not os.path.exists(history_file):
    st.info("No history yet")
    st.stop()

try:
    with open(history_file, "r") as f:
        content = f.read().strip()

        if content == "":
            history = []
        else:
            history = json.loads(content)

except:
    st.error("⚠️ History file corrupted. Resetting...")
    history = []

# ---------------- NO DATA ----------------
if len(history) == 0:
    st.info("No analysis history found")
    st.stop()

# ---------------- SHOW HISTORY ----------------
for i, entry in enumerate(reversed(history)):

    st.markdown("---")
    st.subheader(f"📂 {entry['file_name']}")

    st.write(f"🕒 Time: {entry['time']}")
    st.write(f"📊 Rows: {entry['data'] and len(entry['data'])}")
    
    # ---------------- STATS ----------------
    st.markdown("### 📈 Statistics")

    stats = entry.get("stats", {})

    st.write(f"Mean: {stats.get('mean')}")
    st.write(f"Median: {stats.get('median')}")
    st.write(f"Std Dev: {stats.get('std')}")

    # ---------------- RELATION ----------------
    st.markdown("### 🔗 Relationship")

    st.write(f"Correlation: {entry.get('correlation')}")

    # ---------------- REGRESSION ----------------
    st.markdown("### 📉 Regression")

    st.write(f"R² Score: {entry.get('r2_score')}")

    # ---------------- CATEGORY ----------------
    st.markdown("### 🏆 Top Category")

    st.write(entry.get("top_category"))

    # ---------------- VIEW DATA ----------------
    if st.button(f"👀 View Data {i}"):

        df = pd.DataFrame(entry["data"])
        st.dataframe(df)

    # ---------------- DOWNLOAD ----------------
    df_download = pd.DataFrame(entry["data"])

    csv = df_download.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download Data",
        data=csv,
        file_name=f"{entry['file_name']}_history.csv",
        mime="text/csv"
    )
