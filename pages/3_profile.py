import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.title("👤 Profile & Full Analysis History")

if not os.path.exists("history.json"):
    st.info("No history yet")
    st.stop()

with open("history.json", "r") as f:
    history = json.load(f)

for i, item in enumerate(reversed(history)):

    with st.expander(f"📊 {item['file_name']} | {item['time']}"):

        df_view = pd.DataFrame(item["data"])

        # ---------------- STATS ----------------
        st.markdown("### 📊 Statistics")

        stats = item.get("stats", {})

        st.write(f"Mean: {stats.get('mean')}")
        st.write(f"Median: {stats.get('median')}")
        st.write(f"Std Dev: {stats.get('std')}")

        # ---------------- RELATION ----------------
        st.markdown("### 🔗 Correlation")

        st.write(f"Correlation: {item.get('correlation')}")

        # ---------------- REGRESSION ----------------
        st.markdown("### 📈 Regression")

        st.write(f"R² Score: {item.get('r2_score')}")

        # ---------------- CATEGORY ----------------
        st.markdown("### 🏆 Top Category")

        st.write(item.get("top_category"))

        # ---------------- CHARTS ----------------
        st.markdown("### 📊 Charts")

        num_cols = df_view.select_dtypes(include='number').columns
        cat_cols = df_view.select_dtypes(include='object').columns

        if len(num_cols) >= 2:
            st.plotly_chart(px.scatter(df_view, x=num_cols[0], y=num_cols[1]))
            st.plotly_chart(px.line(df_view, y=num_cols[0]))

        if len(cat_cols) > 0:
            top = df_view[cat_cols[0]].value_counts().head(5)
            st.plotly_chart(px.bar(x=top.index, y=top.values))

        # ---------------- DATA ----------------
        if st.button(f"👀 View Data {i}"):
            st.dataframe(df_view.head())

        # ---------------- DOWNLOAD ----------------
        csv = df_view.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Dataset",
            data=csv,
            file_name="history_data.csv",
            mime="text/csv",
            key=f"dl_{i}"
        )
