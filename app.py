import streamlit as st

# 🔥 PAGE CONFIG (FORCE SIDEBAR OPEN)
st.set_page_config(
    page_title="AI Data Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 👉 TEST SIDEBAR (REMOVE LATER IF YOU WANT)
st.sidebar.write("✅ Sidebar is working")

# 🌌 CUSTOM DARK + GRADIENT STYLE
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main {
    background: linear-gradient(135deg, #0e1117, #1a1f2e);
}

/* Title Styling */
.title {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #6a5cff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #9aa4b2;
    margin-bottom: 30px;
}

/* Feature Cards */
.card {
    background: #161b22;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# 🚀 HERO SECTION
st.markdown('<div class="title">🚀 AI Data Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn raw data into insights & predictions</div>', unsafe_allow_html=True)

st.write("")

# 📢 INFO BOX
st.info("👉 Open Dashboard, Login or About from the sidebar")

st.write("")

# ✨ FEATURES SECTION
st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">📊<br><b>Data Cleaning</b><br>Remove nulls, duplicates & errors</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">🤖<br><b>AI Predictions</b><br>Regression & accuracy insights</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">📈<br><b>Interactive Charts</b><br>Beautiful Plotly visualizations</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# 🌟 EXTRA SECTION (MAKE IT LOOK PREMIUM)
st.markdown("## 🌟 Why this tool?")

col1, col2 = st.columns(2)

with col1:
    st.write("""
    ✔ Clean messy datasets automatically  
    ✔ Generate KPIs instantly  
    ✔ Run ML models without coding  
    ✔ Understand data visually  
    """)

with col2:
    st.write("""
    ✔ Beginner friendly  
    ✔ Fast & interactive  
    ✔ Works with any CSV  
    ✔ Built with AI + Streamlit  
    """)

st.write("")
st.write("")

# 🎯 FOOTER
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | AI Data Platform")
