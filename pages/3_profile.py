import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Profile — DataSphere", page_icon="🔮", layout="wide")

# ── AUTH ──
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# ── STYLES ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"] { background: #160425 !important; }
[data-testid="stHeader"] { background: rgba(22,4,37,0.95) !important; border-bottom: 1px solid rgba(102,103,171,0.15) !important; }
[data-testid="stSidebar"] { background: rgba(33,6,53,0.97) !important; border-right: 1px solid rgba(102,103,171,0.18) !important; }
[data-testid="stSidebar"] * { color: rgba(245,213,224,0.75) !important; }
[data-testid="stSidebar"] .stButton > button { background: rgba(102,103,171,0.12) !important; border: 1px solid rgba(102,103,171,0.25) !important; color: rgba(245,213,224,0.7) !important; border-radius: 8px !important; width: 100% !important; font-size: 13px !important; box-shadow: none !important; }
.page-header { padding: 20px 0 16px; border-bottom: 1px solid rgba(102,103,171,0.15); margin-bottom: 28px; }
.page-label { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #6667AB; font-weight: 600; margin-bottom: 5px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 28px; color: #F5D5E0; font-weight: 700; }
.history-card { background: rgba(102,103,171,0.07); border: 1px solid rgba(102,103,171,0.18); border-radius: 16px; padding: 22px 22px 16px; margin-bottom: 6px; position: relative; overflow: hidden; }
.history-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #7B337E, #6667AB); }
.file-name { font-family: 'Playfair Display', serif; font-size: 18px; color: #F5D5E0; font-weight: 700; margin-bottom: 3px; }
.file-meta { font-size: 11px; color: rgba(245,213,224,0.35); margin-bottom: 16px; letter-spacing: 0.5px; }
.section-mini { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #6667AB; font-weight: 600; margin-bottom: 8px; margin-top: 14px; }
.stat-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 4px; }
.stat-chip { background: rgba(33,6,53,0.6); border: 1px solid rgba(102,103,171,0.2); border-radius: 8px; padding: 7px 13px; font-size: 12px; color: rgba(245,213,224,0.65); }
.stat-chip b { color: #F5D5E0; }
.badge-ok { display: inline-block; background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.28); color: #34d399; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 600; }
.badge-warn { display: inline-block; background: rgba(244,114,182,0.12); border: 1px solid rgba(244,114,182,0.28); color: #f472b6; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 600; }
.badge-na { display: inline-block; background: rgba(102,103,171,0.12); border: 1px solid rgba(102,103,171,0.25); color: rgba(245,213,224,0.4); border-radius: 6px; padding: 3px 10px; font-size: 11px; }
.moon-div { height: 1px; background: linear-gradient(90deg, transparent, rgba(102,103,171,0.2), transparent); margin: 20px 0; }
.insight-row { background: rgba(123,51,126,0.1); border: 1px solid rgba(123,51,126,0.22); border-radius: 10px; padding: 10px 14px; font-size: 12px; color: rgba(245,213,224,0.72); margin-bottom: 7px; }
.stButton > button { background: linear-gradient(135deg, #7B337E, #6667AB) !important; color: #F5D5E0 !important; border: none !important; border-radius: 10px !important; font-size: 12px !important; font-weight: 600 !important; box-shadow: 0 3px 14px rgba(123,51,126,0.25) !important; }
.stDownloadButton > button { background: rgba(102,103,171,0.1) !important; border: 1px solid rgba(102,103,171,0.28) !important; color: #6667AB !important; border-radius: 10px !important; font-size: 12px !important; }
.preview-header { font-family: 'Playfair Display', serif; font-size: 16px; color: #F5D5E0; font-weight: 700; margin: 18px 0 12px; padding-left: 12px; border-left: 3px solid #7B337E; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
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

# ── PAGE HEADER ──
st.markdown("""
<div class="page-header">
    <div class="page-label">User Account</div>
    <div class="page-title">Profile & Analysis History</div>
</div>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ──
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(22,4,37,0)",
    plot_bgcolor="rgba(22,4,37,0)",
    font=dict(color="#F5D5E0", family="DM Sans", size=10),
    xaxis=dict(gridcolor="rgba(102,103,171,0.1)", linecolor="rgba(102,103,171,0.15)", tickfont=dict(size=9)),
    yaxis=dict(gridcolor="rgba(102,103,171,0.1)", linecolor="rgba(102,103,171,0.15)", tickfont=dict(size=9)),
    margin=dict(l=10, r=10, t=24, b=10),
)
COLORS = ["#7B337E", "#6667AB", "#F5D5E0", "#9B59B6", "#BDC3E7", "#420D4B"]

# ── LOAD HISTORY ──
history_file = "history.json"
if not os.path.exists(history_file):
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
        <div style="font-size:48px;margin-bottom:16px;">📭</div>
        <div style="font-family:'Playfair Display',serif;font-size:20px;color:rgba(245,213,224,0.4);margin-bottom:8px;">No history yet</div>
        <div style="font-size:13px;color:rgba(245,213,224,0.25);">Upload a dataset from the Dashboard to get started.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    content = open(history_file).read().strip()
    history = json.loads(content) if content else []
except:
    st.error("⚠️ History file corrupted.")
    history = []

if not history:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
        <div style="font-size:48px;margin-bottom:16px;">📭</div>
        <div style="font-family:'Playfair Display',serif;font-size:20px;color:rgba(245,213,224,0.4);">No history found</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── SESSION STATE for expanded previews ──
if "expanded" not in st.session_state:
    st.session_state.expanded = {}

st.markdown(f'<div style="font-size:13px;color:rgba(245,213,224,0.35);margin-bottom:24px;">🗂 {len(history)} analysis session{"s" if len(history)!=1 else ""} on record</div>', unsafe_allow_html=True)

# ── HISTORY LOOP ──
for i, entry in enumerate(reversed(history)):
    idx = len(history) - 1 - i
    stats      = entry.get("stats", {})
    corr       = entry.get("correlation")
    r2         = entry.get("r2_score")
    top_cat    = entry.get("top_category")
    fname      = entry.get("file_name", "Unknown file")
    ftime      = entry.get("time", "")
    data_dict  = entry.get("data", {})
    rows_stored = len(next(iter(data_dict.values()), [])) if data_dict else 0

    # ── derived labels ──
    strength  = ("Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.4 else "Weak") if corr is not None else None
    direction = ("Positive ↑" if corr > 0 else "Negative ↓") if corr is not None else None

    if r2 is None or r2 < 0:
        r2_badge = '<span class="badge-na">R² N/A</span>'
    elif r2 > 0.7:
        r2_badge = f'<span class="badge-ok">R² {round(r2,4)} — Strong fit</span>'
    elif r2 > 0.4:
        r2_badge = f'<span class="badge-ok">R² {round(r2,4)} — Moderate fit</span>'
    else:
        r2_badge = f'<span class="badge-warn">R² {round(r2,4)} — Weak fit</span>'

    corr_chip = ""
    if corr is not None:
        corr_chip = f'<div class="stat-chip">Correlation <b>{round(corr,4)}</b> — {strength} {direction}</div>'
    else:
        corr_chip = '<div class="stat-chip">Correlation <b>N/A</b></div>'

    cat_chip = f'<div class="stat-chip">Top Category <b>{top_cat}</b></div>' if top_cat else ""

    # ── CARD ──
    st.markdown(f"""
    <div class="history-card">
        <div class="file-name">📂 {fname}</div>
        <div class="file-meta">🕒 {ftime} &nbsp;·&nbsp; 🗃 {rows_stored} rows stored</div>

        <div class="section-mini">📊 Statistics</div>
        <div class="stat-row">
            <div class="stat-chip">Mean &nbsp;<b>{round(stats.get('mean') or 0, 2)}</b></div>
            <div class="stat-chip">Median &nbsp;<b>{round(stats.get('median') or 0, 2)}</b></div>
            <div class="stat-chip">Std Dev &nbsp;<b>{round(stats.get('std') or 0, 2)}</b></div>
        </div>

        <div class="section-mini">🤖 Model Performance</div>
        <div class="stat-row">
            {corr_chip}
            <div class="stat-chip">{r2_badge}</div>
            {cat_chip}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ACTION BUTTONS ──
    b1, b2, b3 = st.columns([1, 1, 4])
    with b1:
        preview_key = f"preview_{idx}"
        label = "🔼 Collapse" if st.session_state.expanded.get(preview_key) else "👁 Preview"
        if st.button(label, key=f"btn_prev_{idx}"):
            st.session_state.expanded[preview_key] = not st.session_state.expanded.get(preview_key, False)
    with b2:
        if data_dict:
            df_dl = pd.DataFrame(data_dict)
            st.download_button(
                label="⬇️ Download",
                data=df_dl.to_csv(index=False).encode(),
                file_name=f"{fname}_history.csv",
                mime="text/csv",
                key=f"dl_{idx}"
            )

    # ── EXPANDED PREVIEW ──
    if st.session_state.expanded.get(f"preview_{idx}") and data_dict:
        df = pd.DataFrame(data_dict)
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
        st.markdown('<div class="preview-header">📋 Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        # ── AI Insights ──
        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
        st.markdown('<div class="preview-header">🤖 AI Insights</div>', unsafe_allow_html=True)

        if len(num_cols) > 0:
            col0 = num_cols[0]
            mean_v   = round(df[col0].mean(), 2)
            max_v    = df[col0].max()
            min_v    = df[col0].min()
            std_v    = round(df[col0].std(), 2)
            q1, q3   = df[col0].quantile(0.25), df[col0].quantile(0.75)
            outliers = len(df[(df[col0] < q1 - 1.5*(q3-q1)) | (df[col0] > q3 + 1.5*(q3-q1))])
            skew_v   = round(df[col0].skew(), 2)
            skew_lbl = "right-skewed ↗" if skew_v > 0.5 else "left-skewed ↙" if skew_v < -0.5 else "normally distributed ≈"

            st.markdown(f'<div class="insight-row">📊 <b>{col0}</b> ranges from <b>{min_v}</b> to <b>{max_v}</b> with a mean of <b>{mean_v}</b> and std dev of <b>{std_v}</b></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-row">📐 Distribution is <b>{skew_lbl}</b> (skew = {skew_v})</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-row">🔍 <b>{outliers}</b> outlier{"s" if outliers != 1 else ""} detected in <b>{col0}</b> using IQR method</div>', unsafe_allow_html=True)

        if len(cat_cols) > 0:
            top_val   = df[cat_cols[0]].value_counts().idxmax()
            top_count = df[cat_cols[0]].value_counts().max()
            pct       = round(top_count / len(df) * 100, 1)
            st.markdown(f'<div class="insight-row">🏆 Top <b>{cat_cols[0]}</b>: <b>{top_val}</b> — appears <b>{top_count}</b> times ({pct}% of stored rows)</div>', unsafe_allow_html=True)

        if len(num_cols) >= 2:
            cr = round(df[num_cols[0]].corr(df[num_cols[1]]), 3)
            s  = "strong" if abs(cr) > 0.7 else "moderate" if abs(cr) > 0.4 else "weak"
            d  = "positive ↑" if cr > 0 else "negative ↓"
            st.markdown(f'<div class="insight-row">🔗 Correlation between <b>{num_cols[0]}</b> and <b>{num_cols[1]}</b>: <b>r = {cr}</b> — {s} {d} relationship</div>', unsafe_allow_html=True)

        # ── CHARTS ──
        if len(num_cols) >= 1:
            st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
            st.markdown('<div class="preview-header">📈 Charts from This Dataset</div>', unsafe_allow_html=True)

            # Row 1
            ch1, ch2, ch3 = st.columns(3)

            with ch1:
                st.markdown(f'<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Distribution — {num_cols[0]}</div>', unsafe_allow_html=True)
                fig_h = px.histogram(df, x=num_cols[0], nbins=15, color_discrete_sequence=[COLORS[0]])
                fig_h.update_layout(**PLOT_LAYOUT, height=200)
                st.plotly_chart(fig_h, use_container_width=True, key=f"hist_{idx}")
                st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                    <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 Shows how <b>{num_cols[0]}</b> values spread across ranges</li>
                    <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 X = value bins · Y = count per bin</li>
                    <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Peak bin = most common value range</li>
                </ul>""", unsafe_allow_html=True)

            with ch2:
                if len(num_cols) >= 2:
                    st.markdown(f'<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Scatter — {num_cols[0]} vs {num_cols[1]}</div>', unsafe_allow_html=True)
                    fig_s = px.scatter(df, x=num_cols[0], y=num_cols[1], color_discrete_sequence=[COLORS[1]], opacity=0.7)
                    fig_s.update_layout(**PLOT_LAYOUT, height=200)
                    fig_s.update_traces(marker=dict(size=5))
                    st.plotly_chart(fig_s, use_container_width=True, key=f"scat_{idx}")
                    cr2 = round(df[num_cols[0]].corr(df[num_cols[1]]), 3)
                    st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 Reveals correlation between 2 numerical vars</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 X = {num_cols[0]} (cause) · Y = {num_cols[1]} (effect)</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 r = <b>{cr2}</b> — {'strong' if abs(cr2)>0.7 else 'moderate' if abs(cr2)>0.4 else 'weak'} relationship</li>
                    </ul>""", unsafe_allow_html=True)
                elif len(cat_cols) > 0:
                    top7 = df[cat_cols[0]].value_counts().nlargest(7)
                    st.markdown(f'<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Top {cat_cols[0]}</div>', unsafe_allow_html=True)
                    fig_b = px.bar(x=top7.index, y=top7.values, color_discrete_sequence=[COLORS[1]], text_auto=True)
                    fig_b.update_layout(**PLOT_LAYOUT, height=200)
                    fig_b.update_traces(marker_line_width=0)
                    st.plotly_chart(fig_b, use_container_width=True, key=f"bar_{idx}")
                    st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 Ranks top {cat_cols[0]} segments by frequency</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 X = category · Y = record count</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Tallest bar = dominant segment</li>
                    </ul>""", unsafe_allow_html=True)

            with ch3:
                if len(cat_cols) > 0:
                    pie_data = df[cat_cols[0]].value_counts().nlargest(6)
                    st.markdown(f'<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Share — {cat_cols[0]}</div>', unsafe_allow_html=True)
                    fig_p = px.pie(values=pie_data.values, names=pie_data.index,
                                   color_discrete_sequence=COLORS, hole=0.45)
                    fig_p.update_layout(**PLOT_LAYOUT, height=200, legend=dict(font=dict(size=8), orientation="v"))
                    fig_p.update_traces(textfont_size=8)
                    st.plotly_chart(fig_p, use_container_width=True, key=f"pie_{idx}")
                    top_s = pie_data.index[0]
                    top_pct = round(pie_data.values[0] / pie_data.values.sum() * 100, 1)
                    st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 Proportional share of each {cat_cols[0]} category</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 Slice size = % of total records</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 <b>{top_s}</b> leads at <b>{top_pct}%</b></li>
                    </ul>""", unsafe_allow_html=True)
                elif len(num_cols) >= 2:
                    st.markdown(f'<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Trend — {num_cols[1]}</div>', unsafe_allow_html=True)
                    fig_l = px.line(df, y=num_cols[1], color_discrete_sequence=[COLORS[3]])
                    fig_l.update_layout(**PLOT_LAYOUT, height=200)
                    fig_l.update_traces(line=dict(width=2))
                    st.plotly_chart(fig_l, use_container_width=True, key=f"line_{idx}")
                    trend = "increasing ↑" if df[num_cols[1]].iloc[-1] > df[num_cols[1]].iloc[0] else "decreasing ↓"
                    st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 Tracks {num_cols[1]} across all records</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 X = row index · Y = value magnitude</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Overall trend is <b>{trend}</b></li>
                    </ul>""", unsafe_allow_html=True)

            # Row 2 — Box + Heatmap (if enough columns)
            if len(num_cols) >= 2 or (len(num_cols) >= 1 and len(cat_cols) >= 1):
                ch4, ch5 = st.columns(2)

                with ch4:
                    if len(cat_cols) > 0:
                        top7_idx = df[cat_cols[0]].value_counts().nlargest(7).index
                        df_box = df[df[cat_cols[0]].isin(top7_idx)]
                        st.markdown(f'<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Box Plot — {num_cols[0]} by {cat_cols[0]}</div>', unsafe_allow_html=True)
                        fig_box = px.box(df_box, x=cat_cols[0], y=num_cols[0], color_discrete_sequence=[COLORS[0]])
                        fig_box.update_layout(**PLOT_LAYOUT, height=220)
                        st.plotly_chart(fig_box, use_container_width=True, key=f"box_{idx}")
                        st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 Compares {num_cols[0]} spread across {cat_cols[0]} groups</li>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 X = category · Y = {num_cols[0]} · box height = variability</li>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Dots beyond whiskers = outliers</li>
                        </ul>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Trend — {num_cols[0]}</div>', unsafe_allow_html=True)
                        fig_l2 = px.line(df, y=num_cols[0], color_discrete_sequence=[COLORS[0]])
                        fig_l2.update_layout(**PLOT_LAYOUT, height=220)
                        st.plotly_chart(fig_l2, use_container_width=True, key=f"line2_{idx}")
                        st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 Tracks {num_cols[0]} across all records</li>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);'>📐 X = row index · Y = value</li>
                        </ul>""", unsafe_allow_html=True)

                with ch5:
                    if len(num_cols) >= 2:
                        corr_df = df[num_cols[:6]].corr()
                        st.markdown('<div style="font-size:12px;color:rgba(245,213,224,0.6);margin-bottom:6px;">Correlation Heatmap</div>', unsafe_allow_html=True)
                        fig_heat = go.Figure(data=go.Heatmap(
                            z=corr_df.values,
                            x=corr_df.columns.tolist(),
                            y=corr_df.columns.tolist(),
                            colorscale=[[0,"#420D4B"],[0.5,"#6667AB"],[1,"#F5D5E0"]],
                            showscale=False,
                            text=np.round(corr_df.values, 2),
                            texttemplate="%{text}",
                            textfont=dict(size=8)
                        ))
                        fig_heat.update_layout(**PLOT_LAYOUT, height=220)
                        st.plotly_chart(fig_heat, use_container_width=True, key=f"heat_{idx}")
                        st.markdown(f"""<ul style='margin:4px 0 10px 0;padding-left:16px;list-style:disc;'>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 All pairwise correlations between numerical columns</li>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 Each cell = correlation of that row × column pair</li>
                            <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Bright = strong link · Dark = weak/negative</li>
                        </ul>""", unsafe_allow_html=True)

        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
