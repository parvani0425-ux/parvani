import streamlit as st

st.set_page_config(page_title="AI Data Platform", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
body { background-color: #0e1117; }
.block-container { padding: 2rem 4rem; }

.hero {
    text-align: center;
    padding: 80px 20px;
}

.gradient-text {
    font-size: 60px;
    font-weight: 800;
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #9ca3af;
    font-size: 18px;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align: center;
}

.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: white;
    border: none;
}

.section { margin-top: 60px; }
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
<div class="gradient-text">🚀 AI Data Dashboard</div>
<p class="subtitle">Turn raw data into insights & predictions</p>
</div>
""", unsafe_allow_html=True)

# ---------- CTA ----------
st.info("👉 Open **Dashboard** from the sidebar")

# ---------- FEATURES ----------
st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

col1.markdown("<div class='card'>📊 Data Cleaning</div>", unsafe_allow_html=True)
col2.markdown("<div class='card'>🤖 AI Predictions</div>", unsafe_allow_html=True)
col3.markdown("<div class='card'>📈 Interactive Charts</div>", unsafe_allow_html=True)
