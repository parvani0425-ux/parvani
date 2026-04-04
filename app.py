import streamlit as st

st.set_page_config(page_title="AI Data Platform", layout="wide")

# 🎨 BACKGROUND + STYLE
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #2c5364);
}
.main {
    background: transparent;
}
.glass {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
}
.title {
    font-size: 50px;
    font-weight: bold;
    color: #4facfe;
}
.subtitle {
    font-size: 18px;
    color: #ccc;
}
</style>
""", unsafe_allow_html=True)

# 🚀 HERO SECTION
st.markdown("<div class='title'>🚀 AI Data Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Turn raw data into insights & predictions</div>", unsafe_allow_html=True)

st.write("")

# 👉 CTA
st.info("👉 Go to **Login** from the sidebar to start")

# ✨ FEATURES
st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='glass'>📊 Data Cleaning<br><br>Remove missing values & duplicates</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass'>🤖 AI Predictions<br><br>Run regression models instantly</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='glass'>📈 Interactive Charts<br><br>Beautiful Plotly visuals</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.caption("✨ Built with Streamlit | AI Data Platform by You 🚀")
