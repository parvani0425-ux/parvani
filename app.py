import streamlit as st

st.set_page_config(page_title="AI Platform", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
}

/* Title */
.title {
    font-size: 70px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 22px;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown('<div class="title">AI Data Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Clean • Analyze • Predict • Visualize</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------- FEATURES ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="card">📊 Data Cleaning<br>Remove nulls & duplicates</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">📈 Smart Analytics<br>Auto KPIs & charts</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">🤖 AI Prediction<br>Regression & insights</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------- BUTTONS ----------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    if st.button("🔐 Login / Sign Up", use_container_width=True):
        st.switch_page("pages/1_Login.py")

st.caption("✨ Transform your data into decisions")
