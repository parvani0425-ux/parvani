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
.kpi-card { background: rgba(102,103,171,0.08); border: 1px solid rgba(102,103,171,0.2); border-radius: 14px; padding: 18px 16px; position: relative; overflow: hidden; text-align: left; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #7B337E, #6667AB); }
.kpi-label { font-size: 10px; color: rgba(245,213,224,0.38); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 7px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 26px; color: #F5D5E0; font-weight: 700; line-height: 1; margin-bottom: 3px; }
.kpi-sub { font-size: 11px; color: rgba(102,103,171,0.75); }
.section-head { font-family: 'Playfair Display', serif; font-size: 18px; color: #F5D5E0; font-weight: 700; margin: 28px 0 14px; padding-left: 12px; border-left: 3px solid #7B337E; }
.insight-row { background: rgba(123,51,126,0.1); border: 1px solid rgba(123,51,126,0.22); border-radius: 10px; padding: 11px 15px; font-size: 13px; color: rgba(245,213,224,0.72); margin-bottom: 8px; }
.moon-div { height: 1px; background: linear-gradient(90deg, transparent, rgba(102,103,171,0.2), transparent); margin: 24px 0; }
.file-card { background: rgba(102,103,171,0.07); border: 1px solid rgba(102,103,171,0.2); border-radius: 16px; padding: 22px; margin-bottom: 6px; position: relative; overflow: hidden; }
.file-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #7B337E, #6667AB); }
.file-name { font-family: 'Playfair Display', serif; font-size: 20px; color: #F5D5E0; font-weight: 700; margin-bottom: 4px; }
.file-meta { font-size: 11px; color: rgba(245,213,224,0.35); letter-spacing: 0.5px; }
.stButton > button { background: linear-gradient(135deg, #7B337E, #6667AB) !important; color: #F5D5E0 !important; border: none !important; border-radius: 10px !important; font-size: 12px !important; font-weight: 600 !important; box-shadow: 0 3px 14px rgba(123,51,126,0.25) !important; }
.stDownloadButton > button { background: rgba(102,103,171,0.1) !important; border: 1px solid rgba(102,103,171,0.28) !important; color: #6667AB !important; border-radius: 10px !important; font-size: 12px !important; }
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

# ── PLOT THEME ──
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(22,4,37,0)",
    plot_bgcolor="rgba(22,4,37,0)",
    font=dict(color="#F5D5E0", family="DM Sans", size=10),
    xaxis=dict(gridcolor="rgba(102,103,171,0.1)", linecolor="rgba(102,103,171,0.15)", tickfont=dict(size=9)),
    yaxis=dict(gridcolor="rgba(102,103,171,0.1)", linecolor="rgba(102,103,171,0.15)", tickfont=dict(size=9)),
    margin=dict(l=10, r=10, t=28, b=10),
)
COLORS = ["#7B337E", "#6667AB", "#F5D5E0", "#9B59B6", "#BDC3E7", "#420D4B"]

# ── LOAD HISTORY ──
history_file = "history.json"
if not os.path.exists(history_file):
    st.markdown("""<div style="text-align:center;padding:80px 20px;">
        <div style="font-size:48px;margin-bottom:16px;">📭</div>
        <div style="font-family:'Playfair Display',serif;font-size:20px;color:rgba(245,213,224,0.4);margin-bottom:8px;">No history yet</div>
        <div style="font-size:13px;color:rgba(245,213,224,0.25);">Upload a dataset from the Dashboard to get started.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

try:
    content = open(history_file).read().strip()
    history = json.loads(content) if content else []
except:
    st.error("⚠️ History file corrupted.")
    history = []

if not history:
    st.markdown("""<div style="text-align:center;padding:80px 20px;">
        <div style="font-size:48px;margin-bottom:16px;">📭</div>
        <div style="font-family:'Playfair Display',serif;font-size:20px;color:rgba(245,213,224,0.4);">No history found</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

if "expanded" not in st.session_state:
    st.session_state.expanded = {}

st.markdown(f'<div style="font-size:13px;color:rgba(245,213,224,0.35);margin-bottom:24px;">🗂 {len(history)} analysis session{"s" if len(history)!=1 else ""} on record</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
# ── HISTORY LOOP
# ════════════════════════════════════════════════
for i, entry in enumerate(reversed(history)):
    idx        = len(history) - 1 - i
    stats      = entry.get("stats", {})
    corr       = entry.get("correlation")
    r2         = entry.get("r2_score")
    top_cat    = entry.get("top_category")
    fname      = entry.get("file_name", "Unknown file")
    ftime      = entry.get("time", "")
    data_dict  = entry.get("data", {})
    rows_stored = len(next(iter(data_dict.values()), [])) if data_dict else 0

    mean_v   = round(stats.get("mean") or 0, 2)
    median_v = round(stats.get("median") or 0, 2)
    std_v    = round(stats.get("std") or 0, 2)
    corr_v   = round(corr, 4) if corr is not None else None
    r2_v     = round(r2, 4) if r2 is not None and r2 >= 0 else None

    # ── File header ──
    st.markdown(f"""
    <div class="file-card">
        <div class="file-name">📂 {fname}</div>
        <div class="file-meta">🕒 {ftime} &nbsp;·&nbsp; 🗃 {rows_stored} rows stored</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row 1: Stats ──
    st.markdown('<div class="section-head">📌 KPI Summary</div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(f'<div class="kpi-card"><div class="kpi-label">Rows Stored</div><div class="kpi-value">{rows_stored}</div><div class="kpi-sub">records saved</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="kpi-label">Mean</div><div class="kpi-value">{mean_v}</div><div class="kpi-sub">average value</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="kpi-label">Median</div><div class="kpi-value">{median_v}</div><div class="kpi-sub">50th percentile</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card"><div class="kpi-label">Std Dev</div><div class="kpi-value">{std_v}</div><div class="kpi-sub">variability</div></div>', unsafe_allow_html=True)
    k5.markdown(f'<div class="kpi-card"><div class="kpi-label">Top Category</div><div class="kpi-value" style="font-size:16px;">{top_cat if top_cat else "—"}</div><div class="kpi-sub">most frequent</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── KPI Row 2: Model ──
    m1, m2, m3 = st.columns(3)
    if corr_v is not None:
        strength  = "Strong" if abs(corr_v) > 0.7 else "Moderate" if abs(corr_v) > 0.4 else "Weak"
        direction = "Positive ↑" if corr_v > 0 else "Negative ↓"
        m1.markdown(f'<div class="kpi-card"><div class="kpi-label">Correlation</div><div class="kpi-value" style="font-size:22px;">{corr_v}</div><div class="kpi-sub">{strength} {direction}</div></div>', unsafe_allow_html=True)
    else:
        m1.markdown(f'<div class="kpi-card"><div class="kpi-label">Correlation</div><div class="kpi-value" style="font-size:22px;">N/A</div><div class="kpi-sub">not computed</div></div>', unsafe_allow_html=True)

    if r2_v is not None:
        fit = "Strong fit ✅" if r2_v > 0.7 else "Moderate fit ⚠️" if r2_v > 0.4 else "Weak fit ❌"
        variance_pct = round(r2_v * 100, 1)
        m2.markdown(f'<div class="kpi-card"><div class="kpi-label">R² Score</div><div class="kpi-value" style="font-size:22px;">{r2_v}</div><div class="kpi-sub">{fit}</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="kpi-card"><div class="kpi-label">Variance Explained</div><div class="kpi-value" style="font-size:22px;">{variance_pct}%</div><div class="kpi-sub">by regression model</div></div>', unsafe_allow_html=True)
    else:
        m2.markdown(f'<div class="kpi-card"><div class="kpi-label">R² Score</div><div class="kpi-value" style="font-size:22px;">N/A</div><div class="kpi-sub">not computed</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="kpi-card"><div class="kpi-label">Variance Explained</div><div class="kpi-value" style="font-size:22px;">—</div><div class="kpi-sub">no model data</div></div>', unsafe_allow_html=True)

    # ── Smart Insight rows ──
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="insight-row">📊 Mean = <b>{mean_v}</b> · Median = <b>{median_v}</b> · Std Dev = <b>{std_v}</b></div>', unsafe_allow_html=True)
    if corr_v is not None:
        st.markdown(f'<div class="insight-row">🔗 Correlation = <b>{corr_v}</b> — <b>{strength} {direction}</b> relationship between the two main numerical variables.</div>', unsafe_allow_html=True)
    if r2_v is not None:
        st.markdown(f'<div class="insight-row">📈 Model explains <b>{variance_pct}%</b> of variance — R² = <b>{r2_v}</b> ({fit})</div>', unsafe_allow_html=True)
    if top_cat:
        st.markdown(f'<div class="insight-row">🏆 Most frequent category: <b>{top_cat}</b> — dominates the dataset.</div>', unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── ACTION BUTTONS ──
    b1, b2, b3 = st.columns([1.2, 1, 4])
    with b1:
        is_open = st.session_state.expanded.get(f"prev_{idx}", False)
        label   = "🔼 Collapse" if is_open else "👁 Preview & Charts"
        if st.button(label, key=f"btn_{idx}"):
            st.session_state.expanded[f"prev_{idx}"] = not is_open
            st.rerun()
    with b2:
        if data_dict:
            df_dl = pd.DataFrame(data_dict)
            st.download_button("⬇️ Download CSV", df_dl.to_csv(index=False).encode(),
                               f"{fname}_history.csv", "text/csv", key=f"dl_{idx}")

    # ════════════════════════════════════════════════
    # ── EXPANDED PREVIEW SECTION
    # ════════════════════════════════════════════════
    if st.session_state.expanded.get(f"prev_{idx}") and data_dict:
        df = pd.DataFrame(data_dict)
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        # ── Data table ──
        st.markdown('<div class="section-head">📋 Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

        # ── Live KPIs ──
        if len(num_cols) > 0:
            col0   = num_cols[0]
            avg_v  = round(df[col0].mean(), 2)
            max_v  = df[col0].max()
            min_v  = df[col0].min()
            rng_v  = round(max_v - min_v, 2)
            med_v  = round(df[col0].median(), 2)
            q1, q3 = df[col0].quantile(0.25), df[col0].quantile(0.75)
            outs   = len(df[(df[col0] < q1 - 1.5*(q3-q1)) | (df[col0] > q3 + 1.5*(q3-q1))])

            st.markdown('<div class="section-head">📌 Live KPI Dashboard</div>', unsafe_allow_html=True)
            lk1, lk2, lk3, lk4 = st.columns(4)
            lk1.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Records</div><div class="kpi-value">{len(df)}</div><div class="kpi-sub">rows in preview</div></div>', unsafe_allow_html=True)
            lk2.markdown(f'<div class="kpi-card"><div class="kpi-label">Avg {col0}</div><div class="kpi-value">{avg_v}</div><div class="kpi-sub">mean value</div></div>', unsafe_allow_html=True)
            lk3.markdown(f'<div class="kpi-card"><div class="kpi-label">Max {col0}</div><div class="kpi-value">{max_v}</div><div class="kpi-sub">peak value</div></div>', unsafe_allow_html=True)
            lk4.markdown(f'<div class="kpi-card"><div class="kpi-label">Min {col0}</div><div class="kpi-value">{min_v}</div><div class="kpi-sub">floor value</div></div>', unsafe_allow_html=True)

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            lk5, lk6, lk7 = st.columns(3)
            lk5.markdown(f'<div class="kpi-card"><div class="kpi-label">Range</div><div class="kpi-value">{rng_v}</div><div class="kpi-sub">max − min spread</div></div>', unsafe_allow_html=True)
            lk6.markdown(f'<div class="kpi-card"><div class="kpi-label">Median {col0}</div><div class="kpi-value">{med_v}</div><div class="kpi-sub">50th percentile</div></div>', unsafe_allow_html=True)
            if len(cat_cols) > 0:
                top_b  = df[cat_cols[0]].value_counts().idxmax()
                top_cn = df[cat_cols[0]].value_counts().max()
                lk7.markdown(f'<div class="kpi-card"><div class="kpi-label">Top {cat_cols[0]}</div><div class="kpi-value" style="font-size:16px;">{top_b}</div><div class="kpi-sub">{top_cn} entries</div></div>', unsafe_allow_html=True)

            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="insight-row">📊 Average <b>{col0}</b> is <b>{avg_v}</b> — typical value across all records.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-row">📏 Range of <b>{rng_v}</b> — spread between lowest and highest values.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-row">🔍 <b>{outs}</b> outlier{"s" if outs!=1 else ""} detected in <b>{col0}</b> using IQR method.</div>', unsafe_allow_html=True)
            if len(num_cols) >= 2:
                cr = round(df[num_cols[0]].corr(df[num_cols[1]]), 3)
                s  = "strong" if abs(cr) > 0.7 else "moderate" if abs(cr) > 0.4 else "weak"
                d  = "positive ↑" if cr > 0 else "negative ↓"
                st.markdown(f'<div class="insight-row">🔗 Correlation between <b>{num_cols[0]}</b> and <b>{num_cols[1]}</b>: r = <b>{cr}</b> — {s} {d} relationship.</div>', unsafe_allow_html=True)
            if len(cat_cols) > 0:
                top_val = df[cat_cols[0]].value_counts().idxmax()
                top_pct = round(df[cat_cols[0]].value_counts().max() / len(df) * 100, 1)
                st.markdown(f'<div class="insight-row">🏆 <b>{top_val}</b> is the most frequent {cat_cols[0]} at <b>{top_pct}%</b> of stored rows.</div>', unsafe_allow_html=True)

        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

        # ── CHARTS ──
        if len(num_cols) >= 1:
            st.markdown('<div class="section-head">📊 Visual Analysis</div>', unsafe_allow_html=True)

            # Row 1
            st.markdown('<div style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(102,103,171,0.6);margin-bottom:12px;">── Row 1 · Relationship & Distribution</div>', unsafe_allow_html=True)
            ch1, ch2, ch3 = st.columns(3)

            with ch1:
                if len(num_cols) >= 2:
                    st.markdown(f'<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">① Scatter — {num_cols[0]} vs {num_cols[1]}</div>', unsafe_allow_html=True)
                    fig_s = px.scatter(df, x=num_cols[0], y=num_cols[1], color_discrete_sequence=[COLORS[0]], opacity=0.75)
                    fig_s.update_layout(**PLOT_LAYOUT, height=210)
                    fig_s.update_traces(marker=dict(size=6))
                    st.plotly_chart(fig_s, use_container_width=True, key=f"sc_{idx}")
                    cr2 = round(df[num_cols[0]].corr(df[num_cols[1]]), 3)
                    st.markdown(f"""<ul style='margin:4px 0 12px;padding-left:16px;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 <b>Why:</b> Both vars numerical → shows correlation</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 <b>X ({num_cols[0]}):</b> Independent · <b>Y ({num_cols[1]}):</b> Dependent</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 r = <b>{cr2}</b> — {'strong' if abs(cr2)>0.7 else 'moderate' if abs(cr2)>0.4 else 'weak'} {'positive ↑' if cr2>0 else 'negative ↓'}</li>
                    </ul>""", unsafe_allow_html=True)

            with ch2:
                st.markdown(f'<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">② Histogram — {num_cols[0]}</div>', unsafe_allow_html=True)
                fig_h = px.histogram(df, x=num_cols[0], nbins=15, color_discrete_sequence=[COLORS[1]])
                fig_h.update_layout(**PLOT_LAYOUT, height=210)
                st.plotly_chart(fig_h, use_container_width=True, key=f"hi_{idx}")
                skew_v = round(df[num_cols[0]].skew(), 2)
                sk_lbl = "right-skewed ↗" if skew_v > 0.5 else "left-skewed ↙" if skew_v < -0.5 else "normal ≈"
                st.markdown(f"""<ul style='margin:4px 0 12px;padding-left:16px;'>
                    <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 <b>Why:</b> Shows how {num_cols[0]} values spread</li>
                    <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 X = value bins · Y = count per bin</li>
                    <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Shape is <b>{sk_lbl}</b> (skew={skew_v})</li>
                </ul>""", unsafe_allow_html=True)

            with ch3:
                if len(cat_cols) > 0:
                    pie_data = df[cat_cols[0]].value_counts().nlargest(6)
                    st.markdown(f'<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">③ Donut — {cat_cols[0]} Share</div>', unsafe_allow_html=True)
                    fig_p = px.pie(values=pie_data.values, names=pie_data.index, color_discrete_sequence=COLORS, hole=0.45)
                    fig_p.update_layout(**PLOT_LAYOUT, height=210, legend=dict(font=dict(size=8)))
                    fig_p.update_traces(textfont_size=8)
                    st.plotly_chart(fig_p, use_container_width=True, key=f"pi_{idx}")
                    top_s   = pie_data.index[0]
                    top_pct = round(pie_data.values[0] / pie_data.values.sum() * 100, 1)
                    st.markdown(f"""<ul style='margin:4px 0 12px;padding-left:16px;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 <b>Why:</b> Proportional share of each category</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 Slice size = % of total records</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 <b>{top_s}</b> leads at <b>{top_pct}%</b></li>
                    </ul>""", unsafe_allow_html=True)
                elif len(num_cols) >= 2:
                    st.markdown(f'<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">③ Trend — {num_cols[1]}</div>', unsafe_allow_html=True)
                    fig_l = px.line(df, y=num_cols[1], color_discrete_sequence=[COLORS[3]])
                    fig_l.update_layout(**PLOT_LAYOUT, height=210)
                    fig_l.update_traces(line=dict(width=2))
                    st.plotly_chart(fig_l, use_container_width=True, key=f"ln_{idx}")
                    trend = "increasing ↑" if df[num_cols[1]].iloc[-1] > df[num_cols[1]].iloc[0] else "decreasing ↓"
                    st.markdown(f"""<ul style='margin:4px 0 12px;padding-left:16px;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 <b>Why:</b> Tracks {num_cols[1]} across records</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Overall trend: <b>{trend}</b></li>
                    </ul>""", unsafe_allow_html=True)

            # Row 2
            st.markdown('<div style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(102,103,171,0.6);margin:12px 0 12px;">── Row 2 · Category Breakdown & Correlations</div>', unsafe_allow_html=True)
            ch4, ch5, ch6 = st.columns(3)

            with ch4:
                if len(cat_cols) > 0:
                    top_cats = df[cat_cols[0]].value_counts().nlargest(7)
                    st.markdown(f'<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">④ Bar — Top {cat_cols[0]}</div>', unsafe_allow_html=True)
                    fig_b = px.bar(x=top_cats.index, y=top_cats.values, color_discrete_sequence=[COLORS[0]], text_auto=True)
                    fig_b.update_layout(**PLOT_LAYOUT, height=210)
                    fig_b.update_traces(marker_line_width=0)
                    st.plotly_chart(fig_b, use_container_width=True, key=f"br_{idx}")
                    dom = top_cats.index[0]; dom_pct = round(top_cats.values[0]/len(df)*100,1)
                    st.markdown(f"""<ul style='margin:4px 0 12px;padding-left:16px;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 <b>Why:</b> Categorical → ranks segments by count</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 X = category · Y = record count</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Top: <b>'{dom}'</b> at <b>{dom_pct}%</b></li>
                    </ul>""", unsafe_allow_html=True)

            with ch5:
                if len(cat_cols) > 0 and len(num_cols) > 0:
                    top7_idx = df[cat_cols[0]].value_counts().nlargest(7).index
                    df_box   = df[df[cat_cols[0]].isin(top7_idx)]
                    st.markdown(f'<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">⑤ Box — {num_cols[0]} by {cat_cols[0]}</div>', unsafe_allow_html=True)
                    fig_box = px.box(df_box, x=cat_cols[0], y=num_cols[0], color_discrete_sequence=[COLORS[1]])
                    fig_box.update_layout(**PLOT_LAYOUT, height=210)
                    st.plotly_chart(fig_box, use_container_width=True, key=f"bx_{idx}")
                    means = df_box.groupby(cat_cols[0])[num_cols[0]].mean().sort_values(ascending=False)
                    st.markdown(f"""<ul style='margin:4px 0 12px;padding-left:16px;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 <b>Why:</b> Compare {num_cols[0]} spread per group</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 Box height = variability · line = median</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Highest avg: <b>'{means.index[0]}'</b> ({round(means.iloc[0],2)})</li>
                    </ul>""", unsafe_allow_html=True)
                elif len(num_cols) >= 2:
                    st.markdown(f'<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">⑤ Trend — {num_cols[0]}</div>', unsafe_allow_html=True)
                    fig_l2 = px.line(df, y=num_cols[0], color_discrete_sequence=[COLORS[1]])
                    fig_l2.update_layout(**PLOT_LAYOUT, height=210)
                    fig_l2.update_traces(line=dict(width=2))
                    st.plotly_chart(fig_l2, use_container_width=True, key=f"ln2_{idx}")

            with ch6:
                if len(num_cols) >= 2:
                    corr_df = df[num_cols[:6]].corr()
                    st.markdown('<div style="font-size:13px;color:#F5D5E0;font-weight:600;margin-bottom:4px;">⑥ Correlation Heatmap</div>', unsafe_allow_html=True)
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
                    fig_heat.update_layout(**PLOT_LAYOUT, height=210)
                    st.plotly_chart(fig_heat, use_container_width=True, key=f"ht_{idx}")
                    st.markdown(f"""<ul style='margin:4px 0 12px;padding-left:16px;'>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📊 <b>Why:</b> All pairwise correlations in one view</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);margin-bottom:3px;'>📐 Each cell = correlation of that row × column</li>
                        <li style='font-size:11px;color:rgba(245,213,224,0.6);'>🔍 Bright = strong link · Dark = weak/negative</li>
                    </ul>""", unsafe_allow_html=True)

        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
