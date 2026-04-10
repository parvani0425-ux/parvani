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
    corr = entry.get('correlation')
    if corr is not None:
        strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.4 else "Weak"
        direction = "Positive" if corr > 0 else "Negative"
        st.write(f"Correlation: {round(corr, 4)}")
        st.write(f"📌 {strength} {direction} relationship between variables")
    else:
        st.write("Correlation: N/A")

    # ---------------- REGRESSION ----------------
    st.markdown("### 📉 Regression")
    r2 = entry.get('r2_score')

    if r2 is None:
        st.info("📊 R² Score: N/A — Not enough data for regression")
    elif r2 < 0:
        # ✅ FIXED: Clean message instead of confusing negative number
        st.info("📊 R² Score: N/A — Dataset is too small for reliable regression. More data improves accuracy.")
    else:
        st.success(f"✅ R² Score: {round(r2, 4)}")
        st.write(f"📌 Model explains {round(r2*100, 1)}% of the variation in the data")

    # ---------------- CATEGORY ----------------
    st.markdown("### 🏆 Top Category")
    top_cat = entry.get("top_category")
    if top_cat:
        st.write(f"🥇 {top_cat}")
    else:
        st.write("N/A")

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
