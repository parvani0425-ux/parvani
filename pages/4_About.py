import streamlit as st

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

st.sidebar.title("🚀 AI Platform")

st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard")
st.sidebar.page_link("pages/3_Profile.py", label="Profile")
st.sidebar.page_link("pages/4_About.py", label="About")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

st.title("ℹ️ About")

st.write("""
This AI Data Platform helps you:
- Clean data
- Generate KPIs
- Run ML models
- Visualize insights
- Track history
""")
