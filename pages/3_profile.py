import streamlit as st
import pandas as pd

st.title("👤 Profile & History")

# LOGIN CHECK
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# CHECK HISTORY
if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("No history yet")
    st.stop()

# ---------------- SHOW HISTORY ----------------
st.subheader("📜 Your Analysis History")

for i, item in enumerate(reversed(st.session_state.history)):

    with st.expander(f"📊 {item['file_name']} | {item['time']}"):

        st.write(f"Rows: {item['rows']}")
        st.write(f"Columns: {item['cols']}")
        st.write(f"Column Names: {item['columns']}")

        # KPI
        if item.get("mean") is not None:
            st.write(f"📊 Mean: {round(item['mean'],2)}")

        if item.get("max") is not None:
            st.write(f"📈 Max: {item['max']}")

        # Insights
        if item.get("correlation") is not None:
            st.write(f"🔗 Correlation: {round(item['correlation'],2)}")

        if item.get("top_category") is not None:
            st.write(f"🏆 Top Category: {item['top_category']}")

        # VIEW DATA
        if "data" in item:
            if st.button(f"👀 View Dataset {i}"):

                df_view = pd.DataFrame(item["data"])
                st.dataframe(df_view.head())

        # DOWNLOAD
        if "data" in item:
            df_download = pd.DataFrame(item["data"])

            csv = df_download.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Dataset",
                data=csv,
                file_name=f"{item['file_name']}_history.csv",
                mime="text/csv",
                key=f"download_{i}"
            )
