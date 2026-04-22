import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import zipfile
import datetime
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler

st.set_page_config(page_title="Dashboard — DataSphere", page_icon="🔮", layout="wide")

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
[data-testid="stSidebar"] .stButton > button { background: rgba(102,103,171,0.12) !important; border: 1px solid rgba(102,103,171,0.25) !important; color: rgba(245,213,224,0.7) !important; border-radius: 8px !important; width: 100% !important; font-size: 13px !important; }
.page-header { padding: 20px 0 16px; border-bottom: 1px solid rgba(102,103,171,0.15); margin-bottom: 24px; }
.page-label { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #6667AB; font-weight: 600; margin-bottom: 5px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 28px; color: #F5D5E0; font-weight: 700; }
.section-head { font-family: 'Playfair Display', serif; font-size: 18px; color: #F5D5E0; font-weight: 700; margin: 28px 0 14px; padding-left: 12px; border-left: 3px solid #7B337E; }
.info-card { background: rgba(102,103,171,0.07); border: 1px solid rgba(102,103,171,0.18); border-radius: 14px; padding: 20px; margin-bottom: 14px; }
.kpi-card { background: rgba(102,103,171,0.08); border: 1px solid rgba(102,103,171,0.2); border-radius: 14px; padding: 18px 16px; position: relative; overflow: hidden; text-align: left; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #7B337E, #6667AB); }
.kpi-label { font-size: 10px; color: rgba(245,213,224,0.38); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 7px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 26px; color: #F5D5E0; font-weight: 700; line-height: 1; margin-bottom: 3px; }
.kpi-sub { font-size: 11px; color: rgba(102,103,171,0.75); }
.insight-row { background: rgba(123,51,126,0.1); border: 1px solid rgba(123,51,126,0.22); border-radius: 10px; padding: 11px 15px; font-size: 13px; color: rgba(245,213,224,0.72); margin-bottom: 8px; }
.moon-div { height: 1px; background: linear-gradient(90deg, transparent, rgba(102,103,171,0.2), transparent); margin: 24px 0; }
.chart-label { font-family: 'Playfair Display', serif; font-size: 16px; color: #F5D5E0; font-weight: 700; margin: 20px 0 8px; }
.chart-note { font-size: 12px; color: rgba(245,213,224,0.4); margin-bottom: 16px; line-height: 1.5; }
.stButton > button { background: linear-gradient(135deg, #7B337E, #6667AB) !important; color: #F5D5E0 !important; border: none !important; border-radius: 10px !important; font-size: 13px !important; font-weight: 600 !important; box-shadow: 0 3px 16px rgba(123,51,126,0.3) !important; transition: all 0.25s !important; padding: 10px 22px !important; }
.stButton > button:hover { box-shadow: 0 5px 22px rgba(123,51,126,0.5) !important; transform: translateY(-1px) !important; }
.stTextInput > div > div > input { background: rgba(33,6,53,0.7) !important; border: 1px solid rgba(102,103,171,0.28) !important; border-radius: 10px !important; color: #F5D5E0 !important; }
.stTextInput label, .stSelectbox label { color: rgba(245,213,224,0.55) !important; font-size: 12px !important; }
.stFileUploader > div { background: rgba(33,6,53,0.5) !important; border: 2px dashed rgba(102,103,171,0.3) !important; border-radius: 14px !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(33,6,53,0.5) !important; border-radius: 10px !important; padding: 3px !important; border: 1px solid rgba(102,103,171,0.15) !important; gap: 3px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 8px !important; color: rgba(245,213,224,0.4) !important; font-size: 12px !important; font-weight: 600 !important; border: none !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #7B337E, #6667AB) !important; color: #F5D5E0 !important; }
.stDownloadButton > button { background: rgba(102,103,171,0.12) !important; border: 1px solid rgba(102,103,171,0.3) !important; color: #6667AB !important; border-radius: 10px !important; }

/* ── STORYTELLING GRID ── */
.story-grid-outer {
    background: rgba(102,103,171,0.05);
    border: 1px solid rgba(102,103,171,0.15);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
}
.story-chart-title {
    font-family: 'Playfair Display', serif;
    font-size: 13px;
    color: #F5D5E0;
    font-weight: 700;
    margin-bottom: 2px;
}
.story-chart-note {
    font-size: 10px;
    color: rgba(245,213,224,0.35);
    margin-bottom: 10px;
}
.story-stat-chip {
    display: inline-block;
    background: rgba(123,51,126,0.18);
    border: 1px solid rgba(123,51,126,0.3);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 10px;
    color: rgba(245,213,224,0.65);
    margin-right: 6px;
    margin-top: 6px;
}
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
    <div class="page-label">Analytics Platform</div>
    <div class="page-title">AI Data Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ── FILE UPLOAD ──
file = st.file_uploader("Upload your dataset (CSV, Excel, JSON, ZIP)", type=["csv","xlsx","xls","zip","json"])

df = None
if file:
    ext = file.name.split(".")[-1].lower()
    if ext == "csv": df = pd.read_csv(file)
    elif ext in ["xlsx","xls"]: df = pd.read_excel(file)
    elif ext == "json": df = pd.read_json(file)
    elif ext == "zip":
        with zipfile.ZipFile(file) as z:
            for name in z.namelist():
                if name.endswith(".csv"):
                    df = pd.read_csv(z.open(name)); break

# ── PLOTLY THEME ──
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(22,4,37,0)",
    plot_bgcolor="rgba(22,4,37,0)",
    font=dict(color="#F5D5E0", family="DM Sans"),
    xaxis=dict(gridcolor="rgba(102,103,171,0.12)", linecolor="rgba(102,103,171,0.2)"),
    yaxis=dict(gridcolor="rgba(102,103,171,0.12)", linecolor="rgba(102,103,171,0.2)"),
    margin=dict(l=20, r=20, t=40, b=20),
)
COLORS = ["#7B337E","#6667AB","#F5D5E0","#420D4B","#9B59B6","#BDC3E7"]

if df is not None:

    # ── RAW DATA ──
    st.markdown('<div class="section-head">📂 Raw Dataset</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    # ── DATASET UNDERSTANDING ──
    st.markdown('<div class="section-head">🧠 Dataset Understanding</div>', unsafe_allow_html=True)
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="info-card">
            <div style='font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#6667AB;margin-bottom:12px;font-weight:600;'>Dataset Overview</div>
            <div style='color:rgba(245,213,224,0.8);font-size:13px;line-height:1.8;'>
                📌 <b style='color:#F5D5E0;'>Rows:</b> {df.shape[0]}<br>
                📌 <b style='color:#F5D5E0;'>Columns:</b> {df.shape[1]}<br>
                📌 <b style='color:#F5D5E0;'>Numerical:</b> {num_cols[:3]}<br>
                📌 <b style='color:#F5D5E0;'>Categorical:</b> {cat_cols[:3]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if len(num_cols) >= 2:
            obj_text = f"Explore relationships between <b style='color:#F5D5E0;'>{num_cols[0]}</b> and <b style='color:#F5D5E0;'>{num_cols[1]}</b>, identify trends, measure correlations, and support predictive modeling."
        elif len(cat_cols) > 0:
            obj_text = f"Analyze categorical variable <b style='color:#F5D5E0;'>{cat_cols[0]}</b> to identify dominant segments, frequency patterns, and business segmentation opportunities."
        else:
            obj_text = "Perform exploratory data analysis to understand structure, composition, and key characteristics."
        st.markdown(f"""
        <div class="info-card">
            <div style='font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#6667AB;margin-bottom:12px;font-weight:600;'>Objective</div>
            <div style='color:rgba(245,213,224,0.7);font-size:13px;line-height:1.75;'>{obj_text}</div>
        </div>
        """, unsafe_allow_html=True)

    if len(cat_cols) > 0 and len(num_cols) > 0:
        st.markdown(f"""
        <div class="info-card">
            <div style='font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#6667AB;margin-bottom:10px;font-weight:600;'>Business Problem</div>
            <div style='color:rgba(245,213,224,0.7);font-size:13px;line-height:1.75;'>
                Understand how <b style='color:#F5D5E0;'>{cat_cols[0]}</b> influences <b style='color:#F5D5E0;'>{num_cols[0]}</b> — identifying high-performing segments, key performance drivers, and optimization opportunities.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── DATA CLEANING ──
    st.markdown('<div class="section-head">🧹 Data Cleaning & Preprocessing</div>', unsafe_allow_html=True)
    before = len(df)
    df = df.drop_duplicates()
    after_dup = len(df)
    missing = df.isnull().sum().sum()
    df = df.dropna()
    df = df.infer_objects()

    cl1, cl2, cl3 = st.columns(3)
    cl1.success(f"✔ Removed **{before - after_dup}** duplicate rows")
    cl2.success(f"✔ Removed **{int(missing)}** missing values")
    cl3.success("✔ Data types corrected")

    st.markdown('<div class="section-head">✅ Cleaned Dataset</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    # ── SAVE HISTORY ──
    history_file = "history.json"
    num_cols_h = df.select_dtypes(include="number").columns
    cat_cols_h = df.select_dtypes(include="object").columns
    mean_val = float(df[num_cols_h[0]].mean()) if len(num_cols_h) > 0 else None
    median_val = float(df[num_cols_h[0]].median()) if len(num_cols_h) > 0 else None
    std_val = float(df[num_cols_h[0]].std()) if len(num_cols_h) > 0 else None
    corr_val = float(df[num_cols_h[0]].corr(df[num_cols_h[1]])) if len(num_cols_h) >= 2 else None
    r2_hist = None
    if len(num_cols_h) >= 2:
        try:
            Xh = df[[num_cols_h[0]]]; Yh = df[num_cols_h[1]]
            Xtr,Xte,Ytr,Yte = train_test_split(Xh,Yh,test_size=0.2)
            mh = LinearRegression(); mh.fit(Xtr,Ytr)
            r2_hist = float(r2_score(Yte, mh.predict(Xte)))
        except: pass
    top_cat_hist = df[cat_cols_h[0]].value_counts().idxmax() if len(cat_cols_h) > 0 else None
    entry = {"file_name": file.name, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             "data": df.head(50).to_dict(), "stats": {"mean": mean_val,"median": median_val,"std": std_val},
             "correlation": corr_val, "r2_score": r2_hist, "top_category": top_cat_hist}
    try:
        history_data = json.loads(open(history_file).read().strip()) if os.path.exists(history_file) else []
    except: history_data = []
    if not history_data or history_data[-1]["file_name"] != file.name:
        history_data.append(entry)
    try:
        with open(history_file,"w") as f: json.dump(history_data, f, indent=4)
    except: pass

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── FEATURE ENGINEERING ──
    st.markdown('<div class="section-head">⚙️ Feature Engineering</div>', unsafe_allow_html=True)
    try:
        df_fe = df.copy()
        num_cols_fe = df_fe.select_dtypes(include=np.number).columns
        cat_cols_fe = df_fe.select_dtypes(include="object").columns
        for c in num_cols_fe: df_fe[c] = df_fe[c].fillna(df_fe[c].mean())
        for c in cat_cols_fe: df_fe[c] = df_fe[c].fillna(df_fe[c].mode()[0])
        le = LabelEncoder()
        for c in cat_cols_fe: df_fe[c] = le.fit_transform(df_fe[c])
        scaler = StandardScaler()
        if len(num_cols_fe) > 0: df_fe[num_cols_fe] = scaler.fit_transform(df_fe[num_cols_fe])
        if len(num_cols_fe) >= 2:
            new_col = f"{num_cols_fe[0]}_ratio"
            df_fe[new_col] = df[num_cols_fe[0]] / (df[num_cols_fe[1]] + 1e-5)
        fe1, fe2, fe3, fe4 = st.columns(4)
        fe1.success("✔ Nulls imputed")
        fe2.success("✔ Encoding done")
        fe3.success("✔ Scaling applied")
        fe4.success(f"✔ `{new_col}` created" if len(num_cols_fe) >= 2 else "✔ Features ready")
        st.dataframe(df_fe.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Feature Engineering Error: {e}")

    st.download_button("⬇️ Download Cleaned CSV", df.to_csv(index=False).encode(), "cleaned_data.csv", "text/csv")

    if len(df) > 500:
        for c in df.select_dtypes(include="object").columns:
            df = df[df[c].isin(df[c].value_counts().nlargest(7).index)]
        st.info("Large dataset simplified — showing top 7 categories")

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── KPI DASHBOARD ──
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    st.markdown('<div class="section-head">📌 KPI Dashboard</div>', unsafe_allow_html=True)

    if len(num_cols) > 0:
        avg_val = round(df[num_cols[0]].mean(), 2)
        max_val = df[num_cols[0]].max()
        min_val = df[num_cols[0]].min()
        price_range = round(max_val - min_val, 2)
        median_val = round(df[num_cols[0]].median(), 2)

        k1,k2,k3,k4 = st.columns(4)
        k1.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Records</div><div class="kpi-value">{df.shape[0]}</div><div class="kpi-sub">rows in dataset</div></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="kpi-card"><div class="kpi-label">Avg {num_cols[0]}</div><div class="kpi-value">{avg_val}</div><div class="kpi-sub">mean value</div></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="kpi-card"><div class="kpi-label">Max {num_cols[0]}</div><div class="kpi-value">{max_val}</div><div class="kpi-sub">peak value</div></div>', unsafe_allow_html=True)
        k4.markdown(f'<div class="kpi-card"><div class="kpi-label">Min {num_cols[0]}</div><div class="kpi-value">{min_val}</div><div class="kpi-sub">floor value</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        k5,k6,k7 = st.columns(3)
        k5.markdown(f'<div class="kpi-card"><div class="kpi-label">Range</div><div class="kpi-value">{price_range}</div><div class="kpi-sub">max − min spread</div></div>', unsafe_allow_html=True)
        k6.markdown(f'<div class="kpi-card"><div class="kpi-label">Median {num_cols[0]}</div><div class="kpi-value">{median_val}</div><div class="kpi-sub">50th percentile</div></div>', unsafe_allow_html=True)

        if len(cat_cols) > 0:
            top_brand = df[cat_cols[0]].value_counts().idxmax()
            top_count = df[cat_cols[0]].value_counts().max()
            k7.markdown(f'<div class="kpi-card"><div class="kpi-label">Top {cat_cols[0]}</div><div class="kpi-value" style="font-size:18px;">{top_brand}</div><div class="kpi-sub">{top_count} entries</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="insight-row">📊 Average <b>{num_cols[0]}</b> is <b>{avg_val}</b> — represents the typical value across all records.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-row">📏 Range of <b>{price_range}</b> shows the spread between lowest and highest values in the dataset.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-row">📍 Median is <b>{median_val}</b> — half the dataset falls below this value.</div>', unsafe_allow_html=True)
        if len(cat_cols) > 0:
            st.markdown(f'<div class="insight-row">🏆 <b>{top_brand}</b> is the most frequent {cat_cols[0]} with <b>{top_count}</b> entries — dominates the dataset.</div>', unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # ── VISUAL ANALYSIS — ALL CHARTS IN ONE STORYTELLING GRID
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="section-head">📊 Visual Analysis — Data Storytelling</div>', unsafe_allow_html=True)

    # ── helper: compact bullet explanation ──
    def explain_chart(chart_type, x_col, y_col, df_ref, cat_col=None):
        bullets = {
            "scatter":    [f"📊 <b>Why:</b> Both {x_col} & {y_col} are numerical → scatter shows correlation", f"📐 <b>X ({x_col}):</b> Independent variable (the cause)", f"📐 <b>Y ({y_col}):</b> Dependent variable (the effect)"],
            "line":       [f"📊 <b>Why:</b> Tracks how {y_col} changes across ordered records", f"📐 <b>X:</b> Row index → record sequence (left = first, right = last)", f"📐 <b>Y ({y_col}):</b> Value being tracked — height = magnitude"],
            "histogram":  [f"📊 <b>Why:</b> Shows how {x_col} values are spread across the dataset", f"📐 <b>X ({x_col}):</b> Value ranges grouped into bins", f"📐 <b>Y (Count):</b> How many records fall in each bin — tall bar = common value"],
            "bar":        [f"📊 <b>Why:</b> {cat_col} is categorical → bar ranks segments by frequency", f"📐 <b>X ({cat_col}):</b> Each category as a separate bar", f"📐 <b>Y (Count):</b> Taller bar = more records in that segment"],
            "box":        [f"📊 <b>Why:</b> Compares {x_col} spread across {cat_col} groups at once", f"📐 <b>X ({cat_col}):</b> One box per category for side-by-side comparison", f"📐 <b>Y ({x_col}):</b> Box height = variability; line = median; dots = outliers"],
            "heatmap":    [f"📊 <b>Why:</b> Shows all pairwise correlations between numerical columns in one view", f"📐 <b>X & Y:</b> Same column names on both axes — each cell = correlation of that pair", f"📐 <b>Color:</b> Bright = strong relationship; dark = weak or negative"],
            "area":       [f"📊 <b>Why:</b> Highlights volume & magnitude of {x_col} over record sequence", f"📐 <b>X:</b> Row index → sequential order of records", f"📐 <b>Y ({x_col}):</b> Filled area below the line emphasizes size, not just direction"],
            "pie":        [f"📊 <b>Why:</b> Shows each {cat_col} category's share of the total", f"📐 <b>Slices:</b> One per category — bigger slice = larger proportion", f"📐 <b>Hole (donut):</b> Improves label readability vs. full pie"],
            "regression": [f"📊 <b>Why:</b> Models {x_col} as predictor → {y_col} as target", f"📐 <b>X ({x_col}):</b> Input fed to the model (independent variable)", f"📐 <b>Y ({y_col}):</b> What the model predicts — closer dots to line = better fit"],
            "residuals":  [f"📊 <b>Why:</b> Checks if the regression model has bias or errors", f"📐 <b>X (Residual):</b> Actual − Predicted; near zero = accurate prediction", f"📐 <b>Y (Count):</b> Bell curve centered at 0 = healthy model"],
        }

        def live_insight(ct, df_r, xc, yc, cc):
            try:
                if ct == "scatter":
                    cr = round(df_r[xc].corr(df_r[yc]), 3)
                    s = "strong" if abs(cr) > 0.7 else "moderate" if abs(cr) > 0.4 else "weak"
                    d = "positive ↑" if cr > 0 else "negative ↓"
                    return f"🔍 r = <b>{cr}</b> — <b>{s} {d}</b> relationship"
                elif ct == "histogram":
                    mean_v = round(df_r[xc].mean(), 2); skew_v = round(df_r[xc].skew(), 2)
                    sk = "right-skewed ↗" if skew_v > 0.5 else "left-skewed ↙" if skew_v < -0.5 else "normal ≈"
                    return f"🔍 Mean = <b>{mean_v}</b> · Shape is <b>{sk}</b>"
                elif ct == "bar" and cc:
                    vc = df_r[cc].value_counts(); top = vc.index[0]; pct = round(vc.iloc[0]/len(df_r)*100,1)
                    return f"🔍 Top segment: <b>'{top}'</b> at <b>{pct}%</b> of dataset"
                elif ct == "box" and cc:
                    means = df_r.groupby(cc)[xc].mean().sort_values(ascending=False)
                    return f"🔍 Highest avg: <b>'{means.index[0]}'</b> ({round(means.iloc[0],2)}) · Lowest: <b>'{means.index[-1]}'</b> ({round(means.iloc[-1],2)})"
            except: pass
            return ""

        rows = bullets.get(chart_type, [])
        insight = live_insight(chart_type, df_ref, x_col, y_col, cat_col)
        if insight: rows.append(insight)

        items = "".join(f"<li style='margin-bottom:5px;color:rgba(245,213,224,0.75);font-size:11.5px;'>{r}</li>" for r in rows)
        return f"<ul style='margin:6px 0 10px 0;padding-left:18px;list-style:disc;'>{items}</ul>"

    if len(num_cols) >= 2:
        x, y = num_cols[0], num_cols[1]

        # ══════════════════════════════
        # ROW 1 — Scatter · Line · Histogram(x)
        # ══════════════════════════════
        st.markdown("""
        <div style='font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(102,103,171,0.6);margin-bottom:12px;margin-top:4px;'>
        ── Row 1 · Relationship & Distribution
        </div>""", unsafe_allow_html=True)

        r1c1, r1c2, r1c3 = st.columns(3)

        with r1c1:
            st.markdown(f'<div class="story-chart-title">① Scatter — {x} vs {y}</div>', unsafe_allow_html=True)
            fig1 = px.scatter(df, x=x, y=y, color_discrete_sequence=[COLORS[0]])
            fig1.update_layout(**PLOT_LAYOUT, height=220)
            fig1.update_traces(marker=dict(size=5, opacity=0.75))
            st.plotly_chart(fig1, use_container_width=True, key="sc1")
            st.markdown(explain_chart("scatter", x, y, df), unsafe_allow_html=True)

        with r1c2:
            st.markdown(f'<div class="story-chart-title">② Trend Line — {y} over Records</div>', unsafe_allow_html=True)
            fig2 = px.line(df, y=y, markers=False, color_discrete_sequence=[COLORS[1]])
            fig2.update_layout(**PLOT_LAYOUT, height=220)
            fig2.update_traces(line=dict(width=2))
            st.plotly_chart(fig2, use_container_width=True, key="ln1")
            st.markdown(explain_chart("line", x, y, df), unsafe_allow_html=True)

        with r1c3:
            st.markdown(f'<div class="story-chart-title">③ Histogram — {x} Distribution</div>', unsafe_allow_html=True)
            fig3 = px.histogram(df, x=x, color_discrete_sequence=[COLORS[0]], nbins=20)
            fig3.update_layout(**PLOT_LAYOUT, height=220)
            st.plotly_chart(fig3, use_container_width=True, key="hi1")
            st.markdown(explain_chart("histogram", x, y, df), unsafe_allow_html=True)

        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

        # ══════════════════════════════
        # ROW 2 — Category Bar · Box Plot · Histogram(y)
        # ══════════════════════════════
        st.markdown("""
        <div style='font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(102,103,171,0.6);margin-bottom:12px;'>
        ── Row 2 · Category Breakdown & Spread
        </div>""", unsafe_allow_html=True)

        r2c1, r2c2, r2c3 = st.columns(3)

        with r2c1:
            if len(cat_cols) > 0:
                top_cats = df[cat_cols[0]].value_counts().nlargest(7)
                st.markdown(f'<div class="story-chart-title">④ Bar — Top {cat_cols[0]} Segments</div>', unsafe_allow_html=True)
                fig4 = px.bar(x=top_cats.index, y=top_cats.values, color_discrete_sequence=[COLORS[1]], text_auto=True)
                fig4.update_layout(**PLOT_LAYOUT, height=220)
                fig4.update_traces(marker_line_width=0)
                st.plotly_chart(fig4, use_container_width=True, key="br1")
                st.markdown(explain_chart("bar", x, y, df, cat_cols[0]), unsafe_allow_html=True)

        with r2c2:
            if len(cat_cols) > 0:
                st.markdown(f'<div class="story-chart-title">⑤ Box Plot — {x} by {cat_cols[0]}</div>', unsafe_allow_html=True)
                top7 = df[cat_cols[0]].value_counts().nlargest(7).index
                df_box = df[df[cat_cols[0]].isin(top7)]
                fig_box = px.box(df_box, x=cat_cols[0], y=x, color_discrete_sequence=[COLORS[0]])
                fig_box.update_layout(**PLOT_LAYOUT, height=220)
                st.plotly_chart(fig_box, use_container_width=True, key="bx1")
                st.markdown(explain_chart("box", x, y, df_box, cat_cols[0]), unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="story-chart-title">⑤ Box Plot — {x}</div>', unsafe_allow_html=True)
                fig_box = px.box(df, y=x, color_discrete_sequence=[COLORS[0]])
                fig_box.update_layout(**PLOT_LAYOUT, height=220)
                st.plotly_chart(fig_box, use_container_width=True, key="bx1")

        with r2c3:
            st.markdown(f'<div class="story-chart-title">⑥ Histogram — {y} Distribution</div>', unsafe_allow_html=True)
            fig_hist2 = px.histogram(df, x=y, color_discrete_sequence=[COLORS[4]], nbins=20)
            fig_hist2.update_layout(**PLOT_LAYOUT, height=220)
            st.plotly_chart(fig_hist2, use_container_width=True, key="hi2")
            st.markdown(explain_chart("histogram", y, x, df), unsafe_allow_html=True)

        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

        # ══════════════════════════════
        # ROW 3 — Heatmap · Area · Pie
        # ══════════════════════════════
        st.markdown("""
        <div style='font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(102,103,171,0.6);margin-bottom:12px;'>
        ── Row 3 · Correlations & Proportions
        </div>""", unsafe_allow_html=True)

        r3c1, r3c2, r3c3 = st.columns(3)

        with r3c1:
            st.markdown('<div class="story-chart-title">⑦ Correlation Heatmap — All Variables</div>', unsafe_allow_html=True)
            corr_df = df[num_cols[:6]].corr() if len(num_cols) >= 2 else df[num_cols].corr()
            fig_heat = go.Figure(data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns.tolist(),
                y=corr_df.columns.tolist(),
                colorscale=[[0,"#420D4B"],[0.5,"#6667AB"],[1,"#F5D5E0"]],
                showscale=False,
                text=np.round(corr_df.values, 2),
                texttemplate="%{text}",
                textfont=dict(size=9)
            ))
            fig_heat.update_layout(**PLOT_LAYOUT, height=220)
            st.plotly_chart(fig_heat, use_container_width=True, key="ht1")
            st.markdown(explain_chart("heatmap", x, y, df), unsafe_allow_html=True)

        with r3c2:
            st.markdown(f'<div class="story-chart-title">⑧ Area Chart — {x} Volume</div>', unsafe_allow_html=True)
            fig_area = px.area(df.head(100), y=x, color_discrete_sequence=[COLORS[1]])
            fig_area.update_layout(**PLOT_LAYOUT, height=220)
            fig_area.update_traces(line=dict(width=1.5), fillcolor="rgba(102,103,171,0.18)")
            st.plotly_chart(fig_area, use_container_width=True, key="ar1")
            st.markdown(explain_chart("area", x, y, df), unsafe_allow_html=True)

        with r3c3:
            if len(cat_cols) > 0:
                st.markdown(f'<div class="story-chart-title">⑨ Donut Pie — {cat_cols[0]} Share</div>', unsafe_allow_html=True)
                pie_data = df[cat_cols[0]].value_counts().nlargest(6)
                fig_pie = px.pie(values=pie_data.values, names=pie_data.index,
                                 color_discrete_sequence=COLORS, hole=0.45)
                fig_pie.update_layout(**PLOT_LAYOUT, height=220,
                                      legend=dict(font=dict(size=9), orientation="v"))
                fig_pie.update_traces(textfont_size=9)
                st.plotly_chart(fig_pie, use_container_width=True, key="pi1")
                st.markdown(explain_chart("pie", x, y, df, cat_cols[0]), unsafe_allow_html=True)

        # ══════════════════════════════
        # ROW 4 — Regression + Residuals
        # ══════════════════════════════
        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(102,103,171,0.6);margin-bottom:12px;'>
        ── Row 4 · Predictive Modelling
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="section-head">📈 Regression Analysis</div>', unsafe_allow_html=True)

        X_r = df[[x]]; Y_r = df[y]
        Xtr,Xte,Ytr,Yte = train_test_split(X_r, Y_r, test_size=0.2)
        mdl = LinearRegression(); mdl.fit(Xtr, Ytr)
        preds = mdl.predict(Xte)
        score = r2_score(Yte, preds)

        reg_c1, reg_c2 = st.columns([2, 1])

        with reg_c1:
            if score < 0:
                st.info("📊 R² Score: N/A — Dataset too small. Upload more data.")
            else:
                st.success(f"✅ R² Accuracy: **{round(score, 4)}** — Model explains **{round(score*100,1)}%** of variance")

            st.markdown(f'<div class="story-chart-title">⑩ Regression — {x} predicts {y}</div>', unsafe_allow_html=True)
            fig_reg = px.scatter(df, x=x, y=y, color_discrete_sequence=[COLORS[0]], opacity=0.5)
            fig_reg.add_trace(go.Scatter(x=Xte[x], y=preds, mode="lines", name="Regression Line",
                                          line=dict(color="#6667AB", width=2.5)))
            fig_reg.update_layout(**PLOT_LAYOUT, height=260, title=f"Regression: {x} → {y}")
            st.plotly_chart(fig_reg, use_container_width=True, key="reg1")

            st.markdown(explain_chart("regression", x, y, df), unsafe_allow_html=True)

        with reg_c2:
            st.markdown(f'<div class="story-chart-title">⑪ Residuals — Model Error Check</div>', unsafe_allow_html=True)
            residuals = Yte.values - preds
            fig_res = px.histogram(x=residuals, nbins=20, color_discrete_sequence=[COLORS[4]])
            fig_res.update_layout(**PLOT_LAYOUT, height=260, xaxis_title="Residual", yaxis_title="Count")
            st.plotly_chart(fig_res, use_container_width=True, key="res1")

            res_std = round(float(np.std(residuals)), 3)
            res_mean = round(float(np.mean(residuals)), 3)
            res_label = "symmetric ✅" if abs(res_mean) < res_std * 0.1 else "skewed ⚠️ bias detected"
            res_bullets = explain_chart("residuals", x, y, df)
            res_bullets += f"<ul style='margin:0 0 10px 0;padding-left:18px;list-style:disc;'><li style='margin-bottom:5px;color:rgba(245,213,224,0.75);font-size:11.5px;'>🔍 Mean error = <b>{res_mean}</b> · Std = <b>{res_std}</b> · Shape: <b>{res_label}</b></li></ul>"
            st.markdown(res_bullets, unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── AI CHART DEVELOPER ──
    st.markdown('<div class="section-head">🎨 AI Chart Developer</div>', unsafe_allow_html=True)
    ch1, ch2, ch3, ch4 = st.columns(4)
    chart_type = ch1.selectbox("Chart Type", ["Bar","Line","Scatter","Pie"])
    all_cols = df.columns.tolist()
    x_col = ch2.selectbox("X-axis", all_cols)
    y_col = ch3.selectbox("Y-axis", all_cols)
    top_n = ch4.selectbox("Top N", [5, 7, 10])

    if st.button("✨  Generate Chart"):
        temp_df = df[[x_col, y_col]].dropna().head(top_n)
        if chart_type == "Bar": fig_c = px.bar(temp_df, x=x_col, y=y_col, color_discrete_sequence=COLORS)
        elif chart_type == "Line": fig_c = px.line(temp_df, x=x_col, y=y_col, markers=True, color_discrete_sequence=COLORS)
        elif chart_type == "Scatter": fig_c = px.scatter(temp_df, x=x_col, y=y_col, color_discrete_sequence=COLORS)
        elif chart_type == "Pie": fig_c = px.pie(temp_df, names=x_col, values=y_col, color_discrete_sequence=COLORS)
        fig_c.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_c, use_container_width=True)

        try:
            if chart_type == "Pie":
                g = temp_df.groupby(x_col)[y_col].sum()
                pct = round((g.max()/g.sum())*100, 2)
                st.markdown(f'<div class="insight-row">🔍 <b>{g.idxmax()}</b> contributes the highest share at <b>{pct}%</b> — dominant category</div>', unsafe_allow_html=True)
            elif chart_type == "Bar":
                g = temp_df.groupby(x_col)[y_col].sum().sort_values(ascending=False)
                st.markdown(f'<div class="insight-row">🔍 Highest: <b>{g.index[0]}</b> · Lowest: <b>{g.index[-1]}</b> — clear variation across categories</div>', unsafe_allow_html=True)
            elif chart_type == "Line":
                trend = "📈 increasing" if temp_df[y_col].iloc[-1] > temp_df[y_col].iloc[0] else "📉 decreasing"
                st.markdown(f'<div class="insight-row">🔍 Trend is <b>{trend}</b> — shows directional movement over time</div>', unsafe_allow_html=True)
            elif chart_type == "Scatter":
                corr_c = temp_df[x_col].corr(temp_df[y_col])
                st.markdown(f'<div class="insight-row">🔍 Correlation: <b>{round(corr_c,3)}</b> — {"strong" if abs(corr_c)>0.7 else "moderate" if abs(corr_c)>0.4 else "weak"} relationship</div>', unsafe_allow_html=True)
        except: pass

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── SMART AI INSIGHTS ──
    st.markdown('<div class="section-head">🤖 Smart AI Insights</div>', unsafe_allow_html=True)
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    insights = [f"Dataset contains <b>{df.shape[0]}</b> rows and <b>{df.shape[1]}</b> columns."]
    if len(num_cols) > 0:
        col_i = num_cols[0]
        insights.append(f"Average <b>{col_i}</b> is <b>{round(df[col_i].mean(),2)}</b>.")
        insights.append(f"Maximum <b>{col_i}</b> is <b>{df[col_i].max()}</b> — indicates peak performance.")
        q1,q3 = df[col_i].quantile(0.25), df[col_i].quantile(0.75)
        outs = df[(df[col_i] < q1-1.5*(q3-q1)) | (df[col_i] > q3+1.5*(q3-q1))]
        insights.append(f"<b>{len(outs)}</b> potential outliers detected in <b>{col_i}</b>.")
    if len(cat_cols) > 0:
        insights.append(f"Most frequent <b>{cat_cols[0]}</b> is <b>'{df[cat_cols[0]].value_counts().idxmax()}'</b>.")
    if len(num_cols) >= 2:
        cr = df[num_cols[0]].corr(df[num_cols[1]])
        insights.append(f"{'Strong positive' if cr>0.7 else 'Strong negative' if cr<-0.7 else 'Moderate'} relationship (r={round(cr,3)}) between <b>{num_cols[0]}</b> and <b>{num_cols[1]}</b>.")
    for ins in insights:
        st.markdown(f'<div class="insight-row">✦ &nbsp; {ins}</div>', unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── RECOMMENDED QUESTIONS ──
    st.markdown('<div class="section-head">💡 Recommended Questions</div>', unsafe_allow_html=True)
    questions = []
    if len(num_cols) > 0:
        questions += [f"What is the trend of {num_cols[0]}?", f"Are there outliers in {num_cols[0]}?", f"What is the distribution of {num_cols[0]}?"]
    if len(cat_cols) > 0:
        questions += [f"What are top categories in {cat_cols[0]}?", f"How does {cat_cols[0]} impact values?"]
    if len(num_cols) >= 2:
        questions += [f"Is there a relationship between {num_cols[0]} and {num_cols[1]}?", f"Which factor influences {num_cols[1]} most?"]

    if "selected_q" not in st.session_state:
        st.session_state.selected_q = ""

    q_cols = st.columns(min(len(questions), 3))
    for idx, q in enumerate(questions):
        with q_cols[idx % 3]:
            if st.button(f"👉 {q}", key=f"q_{idx}"):
                st.session_state.selected_q = q

    # ── ASK ANYTHING ──
    st.markdown('<div class="section-head">💬 Ask Anything About Your Data</div>', unsafe_allow_html=True)
    user_q = st.text_input("Type your question here...", value=st.session_state.get("selected_q",""), placeholder="e.g. What is the trend of price?")

    def answer_question(q):
        q = q.lower()
        try:
            if "trend" in q:
                col_q = num_cols[0]
                trend = "increasing" if df[col_q].iloc[-1] > df[col_q].iloc[0] else "decreasing"
                return f"📊 <b>Trend of {col_q}:</b> The variable shows a <b>{trend}</b> pattern across the dataset."
            elif "outlier" in q:
                col_q = num_cols[0]
                q1o,q3o = df[col_q].quantile(0.25), df[col_q].quantile(0.75)
                outs_q = df[(df[col_q] < q1o-1.5*(q3o-q1o)) | (df[col_q] > q3o+1.5*(q3o-q1o))]
                return f"🔍 <b>Outliers in {col_q}:</b> <b>{len(outs_q)}</b> detected using IQR method."
            elif "distribution" in q:
                col_q = num_cols[0]
                return f"📊 <b>Distribution of {col_q}:</b> Mean={round(df[col_q].mean(),2)}, Std={round(df[col_q].std(),2)}. {'Narrow spread → stable data.' if df[col_q].std() < df[col_q].mean()*0.3 else 'Wide spread → high variability.'}"
            elif "top" in q:
                cat_q = cat_cols[0]
                top_q = df[cat_q].value_counts().head(5)
                return f"🏆 <b>Top {cat_q}:</b><br>" + "<br>".join([f"&nbsp;&nbsp;{k}: {v}" for k,v in top_q.items()])
            elif "impact" in q:
                cat_q = cat_cols[0]; num_q = num_cols[0]
                imp = df.groupby(cat_q)[num_q].mean().sort_values(ascending=False)
                return f"📈 <b>Impact of {cat_q} on {num_q}:</b><br>" + "<br>".join([f"&nbsp;&nbsp;{k}: {round(v,2)}" for k,v in imp.head(5).items()])
            elif "relationship" in q:
                cr_q = df[num_cols[0]].corr(df[num_cols[1]])
                strength = "strong" if abs(cr_q)>0.7 else "moderate" if abs(cr_q)>0.4 else "weak"
                return f"🔗 <b>Relationship:</b> Correlation = <b>{round(cr_q,3)}</b> — <b>{strength}</b> {'positive' if cr_q>0 else 'negative'} relationship."
            elif "influence" in q:
                tgt = num_cols[1]
                cr_all = df.corr(numeric_only=True)[tgt].sort_values(ascending=False)
                return f"⚡ <b>Feature Influence on {tgt}:</b><br>" + "<br>".join([f"&nbsp;&nbsp;{k}: {round(v,3)}" for k,v in cr_all.items()])
            else:
                return "💬 Try: <b>trend</b> · <b>outliers</b> · <b>distribution</b> · <b>top categories</b> · <b>relationship</b> · <b>impact</b>"
        except Exception as e:
            return f"Error: {e}"

    if user_q:
        result = answer_question(user_q)
        st.markdown(f'<div class="insight-row" style="background:rgba(102,103,171,0.1);border-color:rgba(102,103,171,0.3);">🤖 &nbsp; {result}</div>', unsafe_allow_html=True)

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ── NUMERICAL ANALYZER ──
    st.markdown('<div class="section-head">🔢 AI Numerical Analyzer</div>', unsafe_allow_html=True)
    col_q2 = st.selectbox("Select column for deep analysis", df.columns.tolist())
    if col_q2 and pd.api.types.is_numeric_dtype(df[col_q2]):
        d = df[col_q2]
        s1,s2,s3,s4 = st.columns(4)
        s1.markdown(f'<div class="kpi-card"><div class="kpi-label">Mean</div><div class="kpi-value">{round(d.mean(),2)}</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="kpi-card"><div class="kpi-label">Median</div><div class="kpi-value">{round(d.median(),2)}</div></div>', unsafe_allow_html=True)
        s3.markdown(f'<div class="kpi-card"><div class="kpi-label">Std Dev</div><div class="kpi-value">{round(d.std(),2)}</div></div>', unsafe_allow_html=True)
        s4.markdown(f'<div class="kpi-card"><div class="kpi-label">Variance</div><div class="kpi-value">{round(d.var(),2)}</div></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        s5,s6,s7,s8 = st.columns(4)
        s5.markdown(f'<div class="kpi-card"><div class="kpi-label">Min</div><div class="kpi-value">{d.min()}</div></div>', unsafe_allow_html=True)
        s6.markdown(f'<div class="kpi-card"><div class="kpi-label">Max</div><div class="kpi-value">{d.max()}</div></div>', unsafe_allow_html=True)
        s7.markdown(f'<div class="kpi-card"><div class="kpi-label">Mode</div><div class="kpi-value">{d.mode()[0]}</div></div>', unsafe_allow_html=True)
        s8.markdown(f'<div class="kpi-card"><div class="kpi-label">Count</div><div class="kpi-value">{d.count()}</div></div>', unsafe_allow_html=True)
        skew_note = "balanced (mean ≈ median)" if abs(d.mean()-d.median()) < d.std()*0.1 else "skewed (mean ≠ median)"
        st.markdown(f'<div class="insight-row" style="margin-top:12px;">📌 Distribution is <b>{skew_note}</b>. Std Dev of <b>{round(d.std(),2)}</b> indicates {"low variability — stable data." if d.std() < d.mean()*0.3 else "high variability."}</div>', unsafe_allow_html=True)
    elif col_q2:
        st.warning("⚠️ Selected column is not numerical")

    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════
    # ── 🧠 ML BRAIN — MULTI-MODEL TRAINING & PREDICTION ENGINE
    # ════════════════════════════════════════════════════════════════════
    if len(num_cols) >= 2:

        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(123,51,126,0.18), rgba(102,103,171,0.12));
            border: 1px solid rgba(102,103,171,0.3);
            border-radius: 20px;
            padding: 28px 28px 20px;
            margin: 8px 0 20px;
            position: relative;
            overflow: hidden;
        '>
            <div style='
                position: absolute; top: 0; left: 0; right: 0; height: 3px;
                background: linear-gradient(90deg, #7B337E, #6667AB, #F5D5E0, #6667AB, #7B337E);
            '></div>
            <div style='font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#6667AB;font-weight:600;margin-bottom:8px;'>Advanced Analytics</div>
            <div style='font-family:Playfair Display,serif;font-size:26px;color:#F5D5E0;font-weight:900;margin-bottom:8px;'>
                🧠 ML Brain
            </div>
            <div style='font-size:13px;color:rgba(245,213,224,0.5);line-height:1.6;max-width:600px;'>
                Train, compare, and evaluate multiple machine learning models on your dataset.
                Select your target variable, choose models, and get instant performance metrics.
            </div>
        </div>
        """, unsafe_allow_html=True)

        from sklearn.linear_model import LinearRegression, Ridge, Lasso
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.svm import SVR
        from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
        from sklearn.preprocessing import LabelEncoder as LE2
        import warnings
        warnings.filterwarnings("ignore")

        # ── Step 1: Configure ──
        st.markdown('<div class="section-head">⚙️ Step 1 — Configure Your Model</div>', unsafe_allow_html=True)

        cfg1, cfg2, cfg3 = st.columns(3)

        with cfg1:
            target_col = st.selectbox(
                "🎯 Target Variable (what to predict)",
                num_cols,
                help="The column your model will learn to predict"
            )

        with cfg2:
            feature_cols = [c for c in num_cols if c != target_col]
            selected_features = st.multiselect(
                "📊 Feature Variables (inputs)",
                feature_cols,
                default=feature_cols[:min(3, len(feature_cols))],
                help="Columns used as inputs to predict the target"
            )

        with cfg3:
            test_size = st.slider("🔀 Test Split %", 10, 40, 20, 5,
                                   help="% of data held out for testing") / 100

        # ── Model selector ──
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:rgba(245,213,224,0.45);margin-bottom:10px;letter-spacing:1px;">SELECT MODELS TO TRAIN</div>', unsafe_allow_html=True)

        MODEL_OPTIONS = {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(alpha=1.0),
            "Lasso Regression": Lasso(alpha=0.1),
            "Decision Tree": DecisionTreeRegressor(max_depth=5),
            "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=5),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=50),
            "K-Nearest Neighbors": KNeighborsRegressor(n_neighbors=3),
            "Support Vector Machine": SVR(kernel="rbf"),
        }

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc5, mc6, mc7, mc8 = st.columns(4)
        col_pairs = [(mc1,"Linear Regression"),(mc2,"Ridge Regression"),(mc3,"Lasso Regression"),
                     (mc4,"Decision Tree"),(mc5,"Random Forest"),(mc6,"Gradient Boosting"),
                     (mc7,"K-Nearest Neighbors"),(mc8,"Support Vector Machine")]

        selected_models = []
        for col, mname in col_pairs:
            with col:
                default_on = mname in ["Linear Regression","Random Forest","Decision Tree"]
                if st.checkbox(mname, value=default_on, key=f"ml_{mname}"):
                    selected_models.append(mname)

        st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

        # ── Train button ──
        train_btn = st.button("🚀  Train All Selected Models", key="train_ml")

        if train_btn and selected_features and selected_models:

            # ── Prepare data ──
            df_ml = df.copy()

            # Encode any remaining object cols just in case
            for c in df_ml.select_dtypes(include="object").columns:
                df_ml[c] = LE2().fit_transform(df_ml[c].astype(str))

            X_ml = df_ml[selected_features].fillna(0)
            Y_ml = df_ml[target_col].fillna(0)

            if len(X_ml) < 6:
                st.warning("⚠️ Dataset too small to train reliably. Need at least 6 rows.")
            else:
                Xtr_ml, Xte_ml, Ytr_ml, Yte_ml = train_test_split(
                    X_ml, Y_ml, test_size=test_size, random_state=42
                )

                results = []
                predictions_store = {}

                with st.spinner("Training models..."):
                    for mname in selected_models:
                        try:
                            mdl_i = MODEL_OPTIONS[mname]
                            mdl_i.fit(Xtr_ml, Ytr_ml)
                            preds_i = mdl_i.predict(Xte_ml)

                            r2_i   = round(float(r2_score(Yte_ml, preds_i)), 4)
                            mae_i  = round(float(mean_absolute_error(Yte_ml, preds_i)), 4)
                            rmse_i = round(float(np.sqrt(mean_squared_error(Yte_ml, preds_i))), 4)

                            results.append({
                                "Model": mname,
                                "R² Score": r2_i,
                                "MAE": mae_i,
                                "RMSE": rmse_i,
                                "Status": "✅ Good" if r2_i > 0.6 else "⚠️ Fair" if r2_i > 0.2 else "❌ Poor"
                            })
                            predictions_store[mname] = (preds_i, Yte_ml.values, r2_i)
                        except Exception as e:
                            results.append({
                                "Model": mname, "R² Score": None,
                                "MAE": None, "RMSE": None, "Status": f"Error: {e}"
                            })

                # ── Step 2: Results ──
                st.markdown('<div class="section-head">📊 Step 2 — Model Performance Comparison</div>', unsafe_allow_html=True)

                results_df = pd.DataFrame(results)
                valid = results_df[results_df["R² Score"].notna()].copy()

                # ── Leaderboard cards ──
                if not valid.empty:
                    best = valid.sort_values("R² Score", ascending=False).iloc[0]
                    worst = valid.sort_values("R² Score", ascending=True).iloc[0]

                    lb1, lb2, lb3 = st.columns(3)
                    lb1.markdown(f"""
                    <div class="kpi-card" style="border-color:rgba(123,51,126,0.5);">
                        <div class="kpi-label">🏆 Best Model</div>
                        <div class="kpi-value" style="font-size:16px;">{best['Model']}</div>
                        <div class="kpi-sub">R² = {best['R² Score']}</div>
                    </div>""", unsafe_allow_html=True)
                    lb2.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Best R² Score</div>
                        <div class="kpi-value">{best['R² Score']}</div>
                        <div class="kpi-sub">explains {round(best['R² Score']*100,1)}% variance</div>
                    </div>""", unsafe_allow_html=True)
                    lb3.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Best MAE</div>
                        <div class="kpi-value">{best['MAE']}</div>
                        <div class="kpi-sub">average prediction error</div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

                    # ── Results table ──
                    st.markdown('<div style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(102,103,171,0.6);margin-bottom:10px;">All Models — Performance Table</div>', unsafe_allow_html=True)
                    st.dataframe(
                        results_df.sort_values("R² Score", ascending=False),
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

                    # ── Step 3: Visual Comparison ──
                    st.markdown('<div class="section-head">📈 Step 3 — Visual Comparison</div>', unsafe_allow_html=True)

                    vc1, vc2 = st.columns(2)

                    with vc1:
                        # R² Bar chart
                        st.markdown('<div class="story-chart-title">R² Score — Higher is Better</div>', unsafe_allow_html=True)
                        fig_r2 = px.bar(
                            valid.sort_values("R² Score", ascending=True),
                            x="R² Score", y="Model", orientation="h",
                            color="R² Score",
                            color_continuous_scale=[[0,"#420D4B"],[0.5,"#6667AB"],[1,"#F5D5E0"]],
                            text="R² Score"
                        )
                        fig_r2.update_layout(**PLOT_LAYOUT, height=280, showlegend=False,
                                             coloraxis_showscale=False)
                        fig_r2.update_traces(textposition="outside", textfont_size=10)
                        st.plotly_chart(fig_r2, use_container_width=True, key="r2bar")

                    with vc2:
                        # MAE comparison
                        st.markdown('<div class="story-chart-title">MAE — Lower is Better</div>', unsafe_allow_html=True)
                        fig_mae = px.bar(
                            valid.sort_values("MAE", ascending=False),
                            x="MAE", y="Model", orientation="h",
                            color="MAE",
                            color_continuous_scale=[[0,"#F5D5E0"],[0.5,"#6667AB"],[1,"#420D4B"]],
                            text="MAE"
                        )
                        fig_mae.update_layout(**PLOT_LAYOUT, height=280, showlegend=False,
                                               coloraxis_showscale=False)
                        fig_mae.update_traces(textposition="outside", textfont_size=10)
                        st.plotly_chart(fig_mae, use_container_width=True, key="maebar")

                    # ── Actual vs Predicted for best model ──
                    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="section-head">🎯 Step 4 — Best Model: Actual vs Predicted</div>', unsafe_allow_html=True)

                    best_name = best["Model"]
                    if best_name in predictions_store:
                        preds_best, actual_best, r2_best = predictions_store[best_name]

                        avp1, avp2 = st.columns(2)

                        with avp1:
                            st.markdown(f'<div class="story-chart-title">Actual vs Predicted — {best_name}</div>', unsafe_allow_html=True)
                            avp_df = pd.DataFrame({"Actual": actual_best, "Predicted": preds_best})
                            fig_avp = px.scatter(avp_df, x="Actual", y="Predicted",
                                                  color_discrete_sequence=[COLORS[0]], opacity=0.7)
                            # Perfect prediction line
                            mn = min(actual_best.min(), preds_best.min())
                            mx = max(actual_best.max(), preds_best.max())
                            fig_avp.add_trace(go.Scatter(x=[mn,mx], y=[mn,mx], mode="lines",
                                                          name="Perfect Fit",
                                                          line=dict(color="#6667AB", width=2, dash="dash")))
                            fig_avp.update_layout(**PLOT_LAYOUT, height=260)
                            st.plotly_chart(fig_avp, use_container_width=True, key="avp1")
                            st.markdown(f'<div class="insight-row">📌 Points on the dashed line = perfect predictions. Closer to line = better model. R² = <b>{r2_best}</b></div>', unsafe_allow_html=True)

                        with avp2:
                            st.markdown(f'<div class="story-chart-title">Residuals — {best_name}</div>', unsafe_allow_html=True)
                            res_best = actual_best - preds_best
                            fig_res_best = px.histogram(x=res_best, nbins=20,
                                                         color_discrete_sequence=[COLORS[4]])
                            fig_res_best.update_layout(**PLOT_LAYOUT, height=260,
                                                        xaxis_title="Residual (Actual − Predicted)",
                                                        yaxis_title="Count")
                            fig_res_best.add_vline(x=0, line_dash="dash",
                                                    line_color="rgba(245,213,224,0.4)")
                            st.plotly_chart(fig_res_best, use_container_width=True, key="res_best")
                            res_m = round(float(np.mean(res_best)), 3)
                            res_s = round(float(np.std(res_best)), 3)
                            sym = "symmetric ✅ — unbiased model" if abs(res_m) < res_s*0.15 else "skewed ⚠️ — model has bias"
                            st.markdown(f'<div class="insight-row">📌 Mean error = <b>{res_m}</b> · Std = <b>{res_s}</b> · Shape: <b>{sym}</b></div>', unsafe_allow_html=True)

                    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

                    # ── Step 5: Feature Importance ──
                    st.markdown('<div class="section-head">⭐ Step 5 — Feature Importance</div>', unsafe_allow_html=True)

                    fi_shown = False
                    for mname_fi in ["Random Forest", "Gradient Boosting", "Decision Tree"]:
                        if mname_fi in selected_models and mname_fi in predictions_store:
                            try:
                                mdl_fi = MODEL_OPTIONS[mname_fi]
                                importances = mdl_fi.feature_importances_
                                fi_df = pd.DataFrame({
                                    "Feature": selected_features,
                                    "Importance": importances
                                }).sort_values("Importance", ascending=True)

                                st.markdown(f'<div class="story-chart-title">Feature Importance — {mname_fi}</div>', unsafe_allow_html=True)
                                fig_fi = px.bar(fi_df, x="Importance", y="Feature", orientation="h",
                                                 color="Importance",
                                                 color_continuous_scale=[[0,"#420D4B"],[0.5,"#6667AB"],[1,"#F5D5E0"]],
                                                 text=fi_df["Importance"].round(3))
                                fig_fi.update_layout(**PLOT_LAYOUT, height=max(200, len(selected_features)*45),
                                                      coloraxis_showscale=False)
                                fig_fi.update_traces(textposition="outside", textfont_size=10)
                                st.plotly_chart(fig_fi, use_container_width=True, key=f"fi_{mname_fi}")

                                top_feat = fi_df.sort_values("Importance", ascending=False).iloc[0]
                                st.markdown(f'<div class="insight-row">⭐ Most important feature: <b>{top_feat["Feature"]}</b> with importance score <b>{round(top_feat["Importance"],3)}</b> — this variable has the strongest influence on predicting <b>{target_col}</b>.</div>', unsafe_allow_html=True)
                                fi_shown = True
                                break
                            except:
                                pass

                    if not fi_shown:
                        # Fallback: correlation-based importance
                        if len(selected_features) > 0:
                            corr_imp = abs(df_ml[selected_features].corrwith(df_ml[target_col])).sort_values(ascending=True)
                            fi_df2 = pd.DataFrame({"Feature": corr_imp.index, "Correlation": corr_imp.values})
                            st.markdown('<div class="story-chart-title">Feature Importance (Correlation-Based)</div>', unsafe_allow_html=True)
                            fig_fi2 = px.bar(fi_df2, x="Correlation", y="Feature", orientation="h",
                                              color="Correlation",
                                              color_continuous_scale=[[0,"#420D4B"],[0.5,"#6667AB"],[1,"#F5D5E0"]],
                                              text=fi_df2["Correlation"].round(3))
                            fig_fi2.update_layout(**PLOT_LAYOUT, height=max(200, len(selected_features)*45),
                                                   coloraxis_showscale=False)
                            fig_fi2.update_traces(textposition="outside", textfont_size=10)
                            st.plotly_chart(fig_fi2, use_container_width=True, key="fi_corr")

                    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)

                    # ── Step 6: Predict on New Input ──
                    st.markdown('<div class="section-head">🔮 Step 6 — Predict New Values</div>', unsafe_allow_html=True)
                    st.markdown('<div style="font-size:12px;color:rgba(245,213,224,0.4);margin-bottom:16px;">Enter values below and get an instant prediction from the best model</div>', unsafe_allow_html=True)

                    pred_cols = st.columns(min(len(selected_features), 4))
                    input_vals = {}
                    for idx_f, feat in enumerate(selected_features):
                        with pred_cols[idx_f % 4]:
                            col_min = float(df_ml[feat].min())
                            col_max = float(df_ml[feat].max())
                            col_mean = float(df_ml[feat].mean())
                            input_vals[feat] = st.number_input(
                                f"{feat}",
                                min_value=col_min,
                                max_value=col_max,
                                value=col_mean,
                                key=f"pred_input_{feat}"
                            )

                    if st.button("🔮  Generate Prediction", key="predict_btn"):
                        try:
                            best_mdl = MODEL_OPTIONS[best_name]
                            input_array = np.array([[input_vals[f] for f in selected_features]])
                            prediction = best_mdl.predict(input_array)[0]

                            st.markdown(f"""
                            <div style='
                                background: linear-gradient(135deg, rgba(123,51,126,0.2), rgba(102,103,171,0.15));
                                border: 1px solid rgba(102,103,171,0.4);
                                border-radius: 16px;
                                padding: 28px;
                                text-align: center;
                                margin-top: 16px;
                                position: relative;
                                overflow: hidden;
                            '>
                                <div style='position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7B337E,#6667AB,#F5D5E0);'></div>
                                <div style='font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#6667AB;margin-bottom:8px;'>Predicted Value</div>
                                <div style='font-family:Playfair Display,serif;font-size:52px;color:#F5D5E0;font-weight:900;line-height:1;margin-bottom:10px;'>
                                    {round(prediction, 4)}
                                </div>
                                <div style='font-size:13px;color:rgba(245,213,224,0.5);'>
                                    Target: <b style='color:#F5D5E0;'>{target_col}</b> &nbsp;·&nbsp; Model: <b style='color:#6667AB;'>{best_name}</b>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Prediction error: {e}")

                    # ── ML Insights Summary ──
                    st.markdown('<div class="moon-div"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-head">🧠 ML Brain Summary</div>', unsafe_allow_html=True)

                    ml_insights = [
                        f"Trained <b>{len(selected_models)}</b> models on <b>{len(selected_features)}</b> features to predict <b>{target_col}</b>.",
                        f"Best performing model: <b>{best['Model']}</b> with R² = <b>{best['R² Score']}</b>.",
                        f"Best model explains <b>{round(best['R² Score']*100,1)}%</b> of variance in <b>{target_col}</b>." if best['R² Score'] > 0 else f"Models have low R² — consider uploading a larger dataset for reliable predictions.",
                        f"Training set: <b>{len(Xtr_ml)}</b> rows · Test set: <b>{len(Xte_ml)}</b> rows ({int(test_size*100)}% split).",
                        f"Lowest prediction error (MAE): <b>{best['MAE']}</b> from <b>{best['Model']}</b> — meaning predictions are off by this amount on average.",
                    ]
                    for ins in ml_insights:
                        st.markdown(f'<div class="insight-row">🧠 &nbsp; {ins}</div>', unsafe_allow_html=True)

        elif train_btn and not selected_features:
            st.warning("⚠️ Please select at least one feature variable to train.")
        elif train_btn and not selected_models:
            st.warning("⚠️ Please select at least one model to train.")
