import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Profile — DataSphere", page_icon="🔮", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"] { background: #160425 !important; }
[data-testid="stHeader"] { background: rgba(22,4,37,0.95) !important; border-bottom: 1px solid rgba(102,103,171,0.15) !important; }
[data-testid="stSidebar"] { background: rgba(33,6,53,0.97) !important; border-right: 1px solid rgba(102,103,171,0.18) !important; }
[data-testid="stSidebar"] * { color: rgba(245,213,224,0.75) !important; }
[data-testid="stSidebar"] .stButton > button { background: rgba(102,103,171,0.12) !important; border: 1px solid rgba(102,103,171,0.25) !important; color: rgba(245,213,224,0.7) !important; border-radius: 8px !important; width: 100% !important; font-size: 13px !important; }
.page-header { padding: 20px 0 16px; border-bottom: 1px solid rgba(102,103,171,0.15); margin-bottom: 28px; }
.page-label { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #6667AB; font-weight: 600; margin-bottom: 5px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 28px; color: #F5D5E0; font-weight: 700; }
.history-card { background: rgba(102,103,171,0.07); border: 1px solid rgba(102,103,171,0.18); border-radius: 16px; padding: 24px; margin-bottom: 20px; position: relative; overflow: hidden; }
.history-card::before { content: ''; position: absolute; top: 0; left: 0; bottom: 0; width: 3px; background: linear-gradient(180deg, #7B337E, #6667AB); }
.file-name { font-family: 'Playfair Display', serif; font-size: 18px; color: #F5D5E0; font-weight: 700; margin-bottom: 4px; padding-left: 12px; }
.file-meta { font-size: 12px; color: rgba(245,213,224,0.35); padding-left: 12px; margin-bottom: 18px; letter-spacing: 0.5px; }
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; padding-left: 12px; }
.stat-chip { background: rgba(33,6,53,0.6); border: 1px solid rgba(102,103,171,0.2); border-radius: 8px; padding: 8px 14px; font-size: 12px; color: rgba(245,213,224,0.65); }
.stat-chip b { color: #F5D5E0; }
.badge-ok { display: inline-block; background: rgba(123,51,126,0.2); border: 1px solid rgba(123,51,126,0.35); color: #F5D5E0; border-radius: 6px; padding: 4px 12px; font-size: 12px; font-weight: 600; }
.badge-na { display: inline-block; background: rgba(102,103,171,0.15); border: 1px solid rgba(102,103,171,0.25); color: rgba(245,213,224,0.4); border-radius: 6px; padding: 4px 12px; font-size: 12px; }
.section-mini { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #6667AB; font-weight: 600; margin-bottom: 8px; padding-left: 12px; }
.moon-div { height: 1px; background: linear-gradient(90deg, transparent, rgba(102,103,171,0.2), transparent); margin: 16px 0; }
.stButton > button { background: linear-gradient(135deg, #7B337E, #6667AB) !important; color: #F5D5E0 !important; border: none !important; border-radius: 10px !important; font-size: 12px !important; font-weight: 600 !important; box-shadow: 0 3px 14px rgba(123,51,126,0.25) !important; }
.stDownloadButton > button { background: rgba(102,103,171,0.1) !important; border: 1px solid rgba(102,103,171,0.28) !important; color: #6667AB !important; border-radius: 10px !important; font-size: 12px !important; }
[data-testid="stSidebar"] .stButton > button { background: rgba(102,103,171,0.12) !important; border: 1px solid rgba(102,103,171,0.25) !important; color: rgba(245,213,224,0.7) !important; box-shadow: none !important; transform: none !important; }
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
    <div class="page-label">User Account</div>
    <div class="page-title">Profile & Analysis History</div>
</div>
""", unsafe_allow_html=True)

history_file = "history.json"
if not os.path.exists(history_file):
    st.markdown('<div style="text-align:center;padding:60px 20px;color:rgba(245,213,224,0.3);font-size:14px;">No analysis history yet.<br>Upload a dataset from the Dashboard to get started.</div>', unsafe_allow_html=True)
    st.stop()

try:
    content = open(history_file).read().strip()
    history = json.loads(content) if content else []
except:
    st.error("⚠️ History file corrupted.")
    history = []

if not history:
    st.markdown('<div style="text-align:center;padding:60px 20px;color:rgba(245,213,224,0.3);font-size:14px;">No analysis history found.</div>', unsafe_allow_html=True)
    st.stop()

st.markdown(f'<div style="font-size:13px;color:rgba(245,213,224,0.35);margin-bottom:20px;">{len(history)} analysis session{"s" if len(history)!=1 else ""} recorded</div>', unsafe_allow_html=True)

for i, entry in enumerate(reversed(history)):
    stats = entry.get("stats", {})
    corr = entry.get("correlation")
    r2 = entry.get("r2_score")
    top_cat = entry.get("top_category")

    strength = ("Strong" if abs(corr)>0.7 else "Moderate" if abs(corr)>0.4 else "Weak") if corr else None
    direction = ("Positive" if corr>0 else "Negative") if corr else None

    r2_badge = ""
    if r2 is None or r2 < 0:
        r2_badge = '<span class="badge-na">R² N/A</span>'
    else:
        r2_badge = f'<span class="badge-ok">R² {round(r2,4)}</span>'

    st.markdown(f"""
    <div class="history-card">
        <div class="file-name">📂 {entry['file_name']}</div>
        <div class="file-meta">🕒 {entry['time']} &nbsp;·&nbsp; 📊 {len(entry.get('data',{}))} rows stored</div>

        <div class="section-mini">Statistics</div>
        <div class="stat-row">
            <div class="stat-chip">Mean <b>{round(stats.get('mean',0) or 0, 2)}</b></div>
            <div class="stat-chip">Median <b>{round(stats.get('median',0) or 0, 2)}</b></div>
            <div class="stat-chip">Std Dev <b>{round(stats.get('std',0) or 0, 2)}</b></div>
        </div>

        <div class="section-mini" style="margin-top:10px;">Model Performance</div>
        <div class="stat-row">
            {'<div class="stat-chip">Correlation <b>' + str(round(corr,4)) + '</b> — ' + strength + ' ' + direction + '</div>' if corr is not None else '<div class="stat-chip">Correlation <b>N/A</b></div>'}
            <div class="stat-chip">{r2_badge}</div>
            {'<div class="stat-chip">Top Category <b>' + str(top_cat) + '</b></div>' if top_cat else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    btn1, btn2 = st.columns([1, 3])
    with btn1:
        if st.button(f"👀 View Data", key=f"view_{i}"):
            df_view = pd.DataFrame(entry["data"])
            st.dataframe(df_view, use_container_width=True)
    with btn2:
        df_dl = pd.DataFrame(entry["data"])
        st.download_button(
            label="⬇️ Download CSV",
            data=df_dl.to_csv(index=False).encode(),
            file_name=f"{entry['file_name']}_history.csv",
            mime="text/csv",
            key=f"dl_{i}"
        )
