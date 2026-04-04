import streamlit as st

st.set_page_config(page_title="AI Data Platform", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

/* Remove padding */
.block-container {
    padding-top: 2rem;
}

/* Center container */
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
    flex-direction: column;
    position: relative;
}

/* Sphere */
.sphere {
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: radial-gradient(circle, #22d3ee, #6366f1);
    box-shadow: 0 0 120px rgba(99,102,241,0.7);
    position: absolute;
}

/* Text */
.title {
    font-size: 48px;
    font-weight: 700;
    color: white;
}

.subtitle {
    color: #94a3b8;
    font-size: 18px;
    margin-top: 10px;
    margin-bottom: 20px;
    text-align: center;
}

/* Background */
body {
    background: radial-gradient(circle at center, #0b0f1a, #020617);
}

</style>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown("""
<div class="center">
    <div class="sphere"></div>

    <div style="z-index:2; text-align:center;">
        <div class="title">The Intelligent Data Sphere</div>
        <div class="subtitle">
            Clean • Analyze • Predict • Visualize your data intelligently 🚀
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- BUTTON ----------
col1, col2, col3 = st.columns([2,1,2])

with col2:
    if st.button("🔐 Login / Sign Up"):
        st.switch_page("pages/1_Login.py")
        
