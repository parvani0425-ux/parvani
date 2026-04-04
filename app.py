import streamlit as st

# 🚀 PAGE CONFIG
st.set_page_config(
    page_title="AI Data Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ SIDEBAR (FORCE SHOW)
st.sidebar.title("🚀 AI Platform")
st.sidebar.write("Navigate using pages below 👇")

# 🎨 FULL PREMIUM UI STYLE
st.markdown("""
<style>

/* ===== BACKGROUND ANIMATION ===== */
.stApp {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1a1a2e);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ===== GLASSMORPHISM CARDS ===== */
.glass {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.3s;
}

.glass:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}

/* ===== TITLE ===== */
.title {
    font-size: 65px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #6a5cff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ===== SUBTITLE ===== */
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #c9d1d9;
    margin-bottom: 40px;
}

/* ===== BUTTON STYLE ===== */
.stButton>button {
    background: linear-gradient(90deg, #6a5cff, #00d4ff);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    padding: 10px 20px;
}

</style>
""", unsafe_allow_html=True)

# 🚀 HERO SECTION
st.markdown('<div class="title">🚀 AI Data Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn raw data into insights, visuals & predictions</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# 👉 CTA
st.info("👉 Use the sidebar to access Login, Dashboard & About pages")

st.write("")
st.write("")

# 📊 FEATURES SECTION
st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass">
    📊 <h4>Data Cleaning</h4>
    Remove missing values, duplicates, and messy data automatically.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass">
    🤖 <h4>AI Predictions</h4>
    Run regression models and get accuracy instantly.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass">
    📈 <h4>Interactive Charts</h4>
    Beautiful animated visualizations using Plotly.
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# 🌟 WHY SECTION
st.markdown("## 🌟 Why this platform?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass">
    ✔ Clean data instantly  
    ✔ Generate KPIs automatically  
    ✔ Beginner-friendly interface  
    ✔ No coding required  
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass">
    ✔ ML predictions built-in  
    ✔ Works with any CSV  
    ✔ Fast & interactive  
    ✔ Modern UI dashboard  
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# 🎯 FOOTER
st.markdown("---")
st.caption("✨ Built with Streamlit | AI Data Platform by You 🚀")
