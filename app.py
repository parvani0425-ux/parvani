import streamlit as st

st.set_page_config(layout="wide")

# ---------- HIDE SIDEBAR ON LANDING ----------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)


# ---------- STYLE ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f2027, #2c5364);
}

.main {
    background: transparent;
}

.hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 60px;
}

.title {
    font-size: 60px;
    font-weight: bold;
    color: white;
}

.subtitle {
    font-size: 18px;
    color: #bbb;
    margin-top: 10px;
}

.glow {
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, #00f2ff, #8e2de2);
    box-shadow: 0 0 100px #00f2ff, 0 0 200px #8e2de2;
    animation: pulse 3s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

.button {
    background: linear-gradient(90deg, #8e2de2, #4a00e0);
    padding: 10px 25px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ---------- HERO ----------
col1, col2 = st.columns([2,1])

with col1:
    st.markdown('<div class="title">The Intelligent Data Sphere</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Where Data Shapes Your Future 🚀</div>', unsafe_allow_html=True)

    if st.button("Login / Sign Up"):
        st.switch_page("pages/1_Login.py")

with col2:
    st.markdown('<div class="glow"></div>', unsafe_allow_html=True)


# ---------- FEATURES ----------
st.markdown("## ✨ Features")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("📊 Data Cleaning\n\nRemove missing values, duplicates instantly")

with c2:
    st.info("📈 AI Predictions\n\nRegression + insights automatically")

with c3:
    st.info("📉 Smart Charts\n\nAuto visualization suggestions")


# ---------- FOOTER ----------
st.markdown("---")
st.caption("✨ Built with Streamlit | AI Data Platform 🚀")
