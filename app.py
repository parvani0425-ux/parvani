import streamlit as st

st.set_page_config(page_title="AI Data Platform", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at center, #0b0f1a, #020617);
    color: white;
}

/* CENTER CONTAINER */
.center-box {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh;
    text-align: center;
    position: relative;
}

/* GLOWING SPHERE */
.sphere {
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, #22d3ee, #6366f1);
    box-shadow: 0 0 120px rgba(99,102,241,0.6);
    position: absolute;
}

/* TEXT OVERLAY */
.overlay {
    position: relative;
    z-index: 2;
}

/* TITLE */
.title {
    font-size: 48px;
    font-weight: 700;
}

/* SUBTEXT */
.subtitle {
    font-size: 18px;
    color: #94a3b8;
    margin-bottom: 20px;
}

/* BUTTON */
.stButton>button {
    background: transparent;
    border: 1px solid #38bdf8;
    color: white;
    padding: 10px 25px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- CENTER UI ----------
st.markdown("""
<div class="center-box">

    <div class="sphere"></div>

    <div class="overlay">
        <div class="title">The Intelligent Data Sphere</div>
        <div class="subtitle">
            Clean • Analyze • Predict • Visualize your data intelligently 🚀
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

# ---------- BUTTON (REAL STREAMLIT BUTTON) ----------
col1, col2, col3 = st.columns([2,1,2])

with col2:
    if st.button("🔐 Login / Sign Up"):
        st.switch_page("pages/1_Login.py")
