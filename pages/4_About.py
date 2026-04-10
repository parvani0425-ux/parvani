import streamlit as st

st.set_page_config(page_title="About — DataSphere", page_icon="🔮", layout="wide")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"] { background: #160425 !important; }
[data-testid="stHeader"] { background: rgba(22,4,37,0.95) !important; border-bottom: 1px solid rgba(102,103,171,0.15) !important; }
[data-testid="stSidebar"] { background: rgba(33,6,53,0.97) !important; border-right: 1px solid rgba(102,103,171,0.18) !important; }
[data-testid="stSidebar"] * { color: rgba(245,213,224,0.75) !important; }
[data-testid="stSidebar"] .stButton > button { background: rgba(102,103,171,0.12) !important; border: 1px solid rgba(102,103,171,0.25) !important; color: rgba(245,213,224,0.7) !important; border-radius: 8px !important; width: 100% !important; font-size: 13px !important; box-shadow: none !important; transform: none !important; }
.page-header { padding: 20px 0 16px; border-bottom: 1px solid rgba(102,103,171,0.15); margin-bottom: 28px; }
.page-label { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #6667AB; font-weight: 600; margin-bottom: 5px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 28px; color: #F5D5E0; font-weight: 700; }
.about-hero { background: linear-gradient(135deg, rgba(123,51,126,0.15), rgba(102,103,171,0.1)); border: 1px solid rgba(102,103,171,0.2); border-radius: 20px; padding: 40px; margin-bottom: 28px; position: relative; overflow: hidden; }
.about-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #7B337E, #6667AB, #7B337E); }
.about-hero-title { font-family: 'Playfair Display', serif; font-size: 36px; color: #F5D5E0; font-weight: 900; margin-bottom: 10px; }
.about-hero-sub { font-size: 15px; color: rgba(245,213,224,0.55); line-height: 1.75; max-width: 580px; }
.section-head { font-family: 'Playfair Display', serif; font-size: 20px; color: #F5D5E0; font-weight: 700; margin: 28px 0 16px; padding-left: 12px; border-left: 3px solid #7B337E; }
.feat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 24px; }
.feat-item { background: rgba(102,103,171,0.07); border: 1px solid rgba(102,103,171,0.18); border-radius: 12px; padding: 18px 16px; display: flex; gap: 14px; align-items: flex-start; }
.feat-item-icon { font-size: 22px; flex-shrink: 0; margin-top: 1px; }
.feat-item-text { flex: 1; }
.feat-item-name { font-size: 14px; font-weight: 600; color: #F5D5E0; margin-bottom: 4px; }
.feat-item-desc { font-size: 12px; color: rgba(245,213,224,0.45); line-height: 1.55; }
.tech-row { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 24px; }
.tech-chip { background: rgba(33,6,53,0.7); border: 1px solid rgba(102,103,171,0.25); border-radius: 8px; padding: 8px 16px; font-size: 12px; color: rgba(245,213,224,0.65); font-weight: 500; }
.tech-chip b { color: #6667AB; }
.moon-div { height: 1px; background: linear-gradient(90deg, transparent, rgba(102,103,171,0.2), transparent); margin: 24px 0; }
.stButton > button { background: linear-gradient(135deg, #7B337E, #6667AB) !important; color: #F5D5E0 !important; border: none !important; border-radius: 10px !important; font-size: 13px !important; font-weight: 600 !important; box-shadow: 0 3px 14px rgba(123,51,126,0.25) !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 0 20px; border-bottom: 1px solid rgba(102,103,171,0.18); margin-bottom: 20px;'>
        <div style='font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #6667AB; margin-bottom: 4px;'>Platform</div>
        <div style='font-family: Playfair Display, serif; font-size: 18px; color: #F5D5E0; font-weight: 700;'>🔮 DataSphere AI</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪  Logout"):
        st.session_state.logged_in = False
        st.switch_page("app.py")

st.markdown("""
<div class="page-header">
    <div class="page-label">Platform Info</div>
    <div class="page-title">About DataSphere AI</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-hero">
    <div class="about-hero-title">🔮 The Intelligent Data Sphere</div>
    <div class="about-hero-sub">An AI-powered data analysis platform that transforms raw datasets into powerful business intelligence — automatically, beautifully, and instantly. No coding required.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-head">Platform Features</div>', unsafe_allow_html=True)
st.markdown("""
<div class="feat-grid">
    <div class="feat-item">
        <div class="feat-item-icon">🧹</div>
        <div class="feat-item-text">
            <div class="feat-item-name">Auto Data Cleaning</div>
            <div class="feat-item-desc">Removes duplicates, handles missing values, corrects data types automatically.</div>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-item-icon">📊</div>
        <div class="feat-item-text">
            <div class="feat-item-name">KPI Dashboard</div>
            <div class="feat-item-desc">7 business metrics with automatic contextual interpretations.</div>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-item-icon">🤖</div>
        <div class="feat-item-text">
            <div class="feat-item-name">AI Q&A Engine</div>
            <div class="feat-item-desc">Ask anything about your data in plain English — get instant answers.</div>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-item-icon">📈</div>
        <div class="feat-item-text">
            <div class="feat-item-name">Regression Analysis</div>
            <div class="feat-item-desc">Linear regression with R² scoring and visual prediction overlays.</div>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-item-icon">⚙️</div>
        <div class="feat-item-text">
            <div class="feat-item-name">Feature Engineering</div>
            <div class="feat-item-desc">Encoding, scaling, and derived feature creation applied automatically.</div>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-item-icon">🎨</div>
        <div class="feat-item-text">
            <div class="feat-item-name">AI Chart Developer</div>
            <div class="feat-item-desc">Build custom charts interactively with AI-generated insights per chart.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-head">Technologies Used</div>', unsafe_allow_html=True)
st.markdown("""
<div class="tech-row">
    <div class="tech-chip"><b>Python</b> 3.10+</div>
    <div class="tech-chip"><b>Streamlit</b> Framework</div>
    <div class="tech-chip"><b>Pandas</b> Data Analysis</div>
    <div class="tech-chip"><b>NumPy</b> Numerics</div>
    <div class="tech-chip"><b>Plotly Express</b> Charts</div>
    <div class="tech-chip"><b>Scikit-learn</b> ML</div>
    <div class="tech-chip"><b>Streamlit Cloud</b> Deployment</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-head">Why We Built This</div>', unsafe_allow_html=True)
st.markdown("""
<div style='background: rgba(102,103,171,0.07); border: 1px solid rgba(102,103,171,0.18); border-radius: 14px; padding: 22px; font-size: 14px; color: rgba(245,213,224,0.65); line-height: 1.8;'>
    DataSphere AI was built to make data analysis <b style='color:#F5D5E0;'>accessible to everyone</b> — not just data scientists. 
    Whether you're a business analyst, student, or entrepreneur, you can upload any dataset and instantly understand what it's telling you.
    <br><br>
    No code. No setup. Just <b style='color:#F5D5E0;'>intelligence at your fingertips.</b>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;padding:32px 0 10px;color:rgba(245,213,224,0.18);font-size:12px;letter-spacing:2px;'>
    ✦ &nbsp; DataSphere AI &nbsp; · &nbsp; ai-data-tools.streamlit.app &nbsp; ✦
</div>
""", unsafe_allow_html=True)
