import streamlit as st
import json

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

st.sidebar.title("🚀 AI Platform")

st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard")
st.sidebar.page_link("pages/3_profile.py", label="Profile")
st.sidebar.page_link("pages/4_About.py", label="About")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

st.title("👤 Profile & History")

try:
    history = json.load(open("history.json"))
except:
    history = []

if history:
    st.subheader("📂 Previously Analyzed Files")

    for file in history[::-1]:
        st.write("📄", file)
else:
    st.info("No history yet")
