import streamlit as st

st.set_page_config(page_title="DataSphere AI", page_icon="🔮", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #210635 0%, #420D4B 50%, #210635 100%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
* { font-family: 'DM Sans', sans-serif; }
.stButton > button {
    background: linear-gradient(135deg, #7B337E, #6667AB) !important;
    color: #F5D5E0 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 36px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 24px rgba(123,51,126,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(123,51,126,0.6) !important;
}
.hero-wrap { padding: 70px 60px 20px; }
.badge {
    display: inline-block;
    background: rgba(102,103,171,0.18);
    border: 1px solid rgba(102,103,171,0.4);
    color: #6667AB;
    padding: 5px 18px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 22px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 66px;
    font-weight: 900;
    line-height: 1.08;
    color: #F5D5E0;
    margin-bottom: 6px;
}
.hero-accent { color: #6667AB; }
.hero-sub {
    font-size: 16px;
    color: rgba(245,213,224,0.5);
    font-weight: 300;
    margin-bottom: 38px;
    line-height: 1.8;
    max-width: 460px;
}
.orb-wrap { display: flex; align-items: center; justify-content: center; padding: 30px; }
.orb {
    width: 320px; height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #7B337E 0%, #420D4B 55%, #210635 100%);
    box-shadow: 0 0 80px rgba(123,51,126,0.5), 0 0 160px rgba(102,103,171,0.2), inset 0 0 50px rgba(245,213,224,0.07);
    animation: floatOrb 7s ease-in-out infinite;
    position: relative;
}
.orb::after {
    content: '';
    position: absolute;
    top: 12%; left: 18%;
    width: 35%; height: 22%;
    background: radial-gradient(circle, rgba(245,213,224,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
@keyframes floatOrb {
    0%,100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-16px) scale(1.02); }
}
.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(102,103,171,0.25), transparent); margin: 40px 60px; }
.section-wrap { padding: 0 60px 30px; }
.section-label { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #6667AB; font-weight: 600; margin-bottom: 10px; }
.section-title { font-family: 'Playfair Display', serif; font-size: 36px; color: #F5D5E0; font-weight: 700; margin-bottom: 36px; line-height: 1.2; }
.stat-grid { display: flex; gap: 0; margin: 20px 0 50px; background: rgba(102,103,171,0.06); border: 1px solid rgba(102,103,171,0.15); border-radius: 16px; overflow: hidden; }
.stat-item { flex: 1; text-align: center; padding: 28px 20px; border-right: 1px solid rgba(102,103,171,0.12); }
.stat-item:last-child { border-right: none; }
.stat-num { font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 900; background: linear-gradient(135deg, #F5D5E0 0%, #6667AB 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1; margin-bottom: 6px; }
.stat-label { font-size: 11px; color: rgba(245,213,224,0.35); text-transform: uppercase; letter-spacing: 2px; }
.feat-card { background: rgba(102,103,171,0.07); border: 1px solid rgba(102,103,171,0.18); border-radius: 18px; padding: 28px 24px; height: 100%; position: relative; overflow: hidden; }
.feat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #420D4B, #6667AB, #420D4B); }
.feat-icon { font-size: 30px; margin-bottom: 14px; display: block; }
.feat-name { font-family: 'Playfair Display', serif; font-size: 17px; color: #F5D5E0; font-weight: 700; margin-bottom: 8px; }
.feat-desc { font-size: 13px; color: rgba(245,213,224,0.45); line-height: 1.65; }
.footer { text-align: center; padding: 30px 0 20px; color: rgba(245,213,224,0.18); font-size: 12px; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

col_text, col_orb = st.columns([1.1, 0.9])
with col_text:
    st.markdown("""
    <div class="hero-wrap">
        <div class="badge">✦ &nbsp; AI · Analytics · Intelligence</div>
        <div class="hero-title">The Intelligent<br><span class="hero-accent">Data Sphere</span></div>
        <div class="hero-sub">Transform raw datasets into powerful business intelligence — automatically, beautifully, instantly.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='padding: 0 0 0 60px;'>", unsafe_allow_html=True)
    if st.button("🚀   Enter Platform"):
        st.switch_page("pages/1_Login.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col_orb:
    st.markdown('<div class="orb-wrap"><div class="orb"></div></div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-wrap">
    <div class="stat-grid">
        <div class="stat-item"><div class="stat-num">10+</div><div class="stat-label">Chart Types</div></div>
        <div class="stat-item"><div class="stat-num">7</div><div class="stat-label">KPI Metrics</div></div>
        <div class="stat-item"><div class="stat-num">AI</div><div class="stat-label">Powered Q&A</div></div>
        <div class="stat-item"><div class="stat-num">∞</div><div class="stat-label">Datasets</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-wrap">
    <div class="section-label">Platform Capabilities</div>
    <div class="section-title">Everything you need to understand your data</div>
</div>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
features = [
    ("🧹", "Auto Data Cleaning", "Remove duplicates, nulls and inconsistencies in one click."),
    ("📊", "KPI Dashboard", "7 business metrics with automatic interpretations."),
    ("🤖", "AI Q&A Engine", "Ask anything about your data in plain English."),
    ("📈", "Regression Model", "Linear regression with R² scoring and visual overlays."),
]
for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
    with col:
        st.markdown(f'<div class="feat-card"><span class="feat-icon">{icon}</span><div class="feat-name">{title}</div><div class="feat-desc">{desc}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="footer">✦ &nbsp; DataSphere AI &nbsp; · &nbsp; Powered by Streamlit &nbsp; ✦</div>', unsafe_allow_html=True)
