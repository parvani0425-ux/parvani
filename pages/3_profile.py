import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👤 Profile & History")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("No history yet")
    st.stop()

st.subheader("📜 Your Analysis History")

for i, item in enumerate(reversed(st.session_state.history)):

    with st.expander(f"📊 {item['file_name']} | {item['time']}"):

        df_view = pd.DataFrame(item["data"])

        st.write(f"Rows: {df_view.shape[0]}")
        st.write(f"Columns: {df_view.shape[1]}")

        # KPI
        if item.get("mean"):
            st.write(f"📊 Mean: {round(item['mean'],2)}")

        if item.get("max"):
            st.write(f"📈 Max: {item['max']}")

        # VIEW DATA
        if st.button(f"👀 View Dataset {i}"):
            st.dataframe(df_view.head())

        # ---------------- RECREATE CHARTS ----------------
        charts = item.get("charts", {})

        st.markdown("### 📊 Saved Charts")

        try:
            # Scatter
            if charts["scatter"]["x"] and charts["scatter"]["y"]:
                fig = px.scatter(df_view,
                                 x=charts["scatter"]["x"],
                                 y=charts["scatter"]["y"])
                st.plotly_chart(fig)

            # Line
            if charts["line"]["y"]:
                fig = px.line(df_view, y=charts["line"]["y"])
                st.plotly_chart(fig)

            # Histogram
            if charts["hist"]["x"]:
                fig = px.histogram(df_view, x=charts["hist"]["x"])
                st.plotly_chart(fig)

            # Bar
            if charts["bar"]["cat"]:
                top = df_view[charts["bar"]["cat"]].value_counts().head(5)
                fig = px.bar(x=top.index, y=top.values)
                st.plotly_chart(fig)

        except Exception as e:
            st.warning(f"Chart error: {e}")

        # DOWNLOAD
        csv = df_view.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Dataset",
            data=csv,
            file_name=f"{item['file_name']}_history.csv",
            mime="text/csv",
            key=f"download_{i}"
        )
