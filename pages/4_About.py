import streamlit as st

# LOGIN CHECK
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# SIDEBAR
st.sidebar.title("🚀 AI Platform")

st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard")
st.sidebar.page_link("pages/3_profile.py", label="Profile")
st.sidebar.page_link("pages/4_About.py", label="About")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

# MAIN CONTENT
st.title("ℹ️ About")

st.write("""
### 🚀 AI Data Platform

This platform helps you:

✔ Clean messy datasets automatically  
✔ Generate KPIs instantly  
✔ Visualize data with smart charts  
✔ Run regression & predictions  
✔ Get insights & analysis  

---

### 🎯 Why we built this?

To make data analysis simple, fast, and beginner-friendly —  
so anyone can upload a file and understand it instantly.

---

### 🧠 Features

- Auto Data Cleaning
- AI Chart Suggestions
- KPI Dashboard
- Regression Models
- Insight Generation
""")
