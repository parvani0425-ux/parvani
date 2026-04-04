import streamlit as st

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

st.title("ℹ️ About")

st.write("""
This AI Data Platform helps you:
- Clean data
- Generate KPIs
- Run ML models
- Visualize insights
- Track history
""")
