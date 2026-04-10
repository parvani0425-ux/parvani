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

    # ── helper: smart explanation builder ──
    def explain_chart(chart_type, x_col, y_col, df_ref, cat_col=None):
        """Returns (why_chart, why_x, why_y, data_insight) as a styled HTML block."""

        chart_reasons = {
            "scatter": f"A <b>Scatter Plot</b> is chosen here because both <b>{x_col}</b> and <b>{y_col}</b> are numerical variables. It plots every single data point as a dot, making it perfect to visually detect whether the two variables move together (correlation), how tightly they cluster, and where outliers live. No other chart reveals the raw relationship between two continuous variables this clearly.",
            "line":    f"A <b>Line Chart</b> is used because <b>{y_col}</b> is a continuous numerical value that changes across sequential records. Connecting points with a line makes it easy to follow the direction of change — is the value rising, falling, or fluctuating? It's the go-to chart for spotting trends and momentum over time or ordered data.",
            "histogram": f"A <b>Histogram</b> is ideal here because we want to understand <b>how the values of {x_col} are distributed</b> across the dataset. Instead of showing individual points, it groups values into bins and counts how many fall in each. This reveals if the data is bell-shaped (normal), skewed left/right, or has multiple peaks — critical for understanding data quality and choosing the right model.",
            "bar":     f"A <b>Bar Chart</b> is the best choice for <b>{cat_col}</b> because it is a categorical variable. Each bar represents one category, and the height shows how frequently it appears. Bar charts make it effortless to rank and compare categories — the tallest bar immediately tells you which segment dominates the dataset.",
            "box":     f"A <b>Box Plot</b> is selected to show the <b>statistical spread of {x_col} broken down by {cat_col}</b>. It compresses five statistics into one shape — minimum, Q1, median, Q3, and maximum — and dots beyond the whiskers mark outliers. This is far more informative than just showing averages because it reveals how consistent or variable each group really is.",
            "heatmap": f"A <b>Correlation Heatmap</b> is the most efficient way to see <b>all pairwise relationships between numerical columns at once</b>. Each cell shows the correlation coefficient (−1 to +1) between two variables, color-coded for quick reading. Bright cells mean strong relationships — these pairs are the most important for feature selection and predictive modeling.",
            "area":    f"An <b>Area Chart</b> extends the line chart by filling the space below the line. It is used for <b>{x_col}</b> to emphasize the <b>magnitude and volume</b> of values over the record sequence — not just direction but the actual size of the signal. The filled area makes it easier to compare periods of high vs. low values at a glance.",
            "pie":     f"A <b>Donut / Pie Chart</b> is used for <b>{cat_col}</b> to show <b>proportional share</b> — how much of the total each category accounts for. When the question is 'what percentage does each group make up?', a pie chart answers it instantly. The hole in the center (donut style) improves readability for labels.",
            "regression": f"A <b>Regression Scatter with Fitted Line</b> is used to model the relationship between <b>{x_col}</b> (predictor) and <b>{y_col}</b> (target). The dots show real data; the line shows what the model predicts. The closer the dots hug the line, the stronger the predictive power. This is the foundation of understanding cause-and-effect in numerical data.",
            "residuals": f"A <b>Residual Histogram</b> checks the <b>health of the regression model</b>. Residuals are the errors — the gap between what the model predicted and what actually happened. If the bars form a symmetric bell curve centered near zero, the model is unbiased and reliable. If it's skewed or has fat tails, the model is missing something important.",
        }

        axis_reasons = {
            "scatter":   (f"<b>X-axis → {x_col}:</b> Placed on X because it is the <b>independent variable</b> — the one we suspect drives or influences the outcome. By convention, the cause goes on the horizontal axis.", f"<b>Y-axis → {y_col}:</b> Placed on Y because it is the <b>dependent variable</b> — the outcome we are trying to understand or predict. We read 'as X increases, does Y go up or down?'"),
            "line":      (f"<b>X-axis → Row Index:</b> The index represents the <b>sequence of records</b> — the natural order in which data was collected. This lets us read left-to-right as 'earlier to later'.", f"<b>Y-axis → {y_col}:</b> The value we are tracking over time. Height on the Y-axis directly encodes magnitude — taller = bigger value."),
            "histogram": (f"<b>X-axis → {x_col}:</b> The value range is divided into equal-width bins along the X-axis. Each bin represents a range of values (e.g., 100–200, 200–300). This shows <b>where values tend to cluster</b>.", f"<b>Y-axis → Count:</b> The height of each bar shows how many records fall into that bin. A tall bar means many records have that value — <b>the peak is the most common value range</b>."),
            "bar":       (f"<b>X-axis → {cat_col}:</b> Each category label sits on the X-axis. Categories are <b>discrete, non-ordered groups</b> — placing them horizontally makes comparison natural since we read left to right.", f"<b>Y-axis → Count / Frequency:</b> The height of each bar = how many records belong to that category. The <b>taller the bar, the more dominant that segment</b> is in your data."),
            "box":       (f"<b>X-axis → {cat_col}:</b> Each group/category sits on the X-axis so we can <b>compare distributions side by side</b>. The horizontal separation makes it easy to see which group is wider (more variable) or taller (higher median).", f"<b>Y-axis → {x_col}:</b> The numerical value being measured. The <b>vertical spread of each box shows how much {x_col} varies within that category</b>. A tall box = high variability; a flat box = consistent values."),
            "heatmap":   (f"<b>X-axis → Column Names:</b> Each column label on the X-axis represents one numerical feature.", f"<b>Y-axis → Column Names:</b> Same columns mirrored on Y. Each cell at the intersection shows the <b>correlation between that X and Y pair</b>. Diagonal cells are always 1.0 (a variable perfectly correlates with itself)."),
            "area":      (f"<b>X-axis → Row Index:</b> The sequential record order — reads as a time-like progression from first to last record in the dataset.", f"<b>Y-axis → {x_col}:</b> The numerical value whose <b>volume is being visualized</b>. The filled area below makes it easy to see when values are high (large area) vs. low (small area)."),
            "pie":       (f"<b>Slices → {cat_col} categories:</b> Each slice represents one category. The <b>angle and size of each slice</b> is proportional to its share of the total.", f"<b>Slice size → Record count:</b> A bigger slice = more records in that category. This lets you immediately see <b>which categories are major vs. minor players</b>."),
            "regression":(f"<b>X-axis → {x_col}:</b> The <b>predictor (independent) variable</b>. We feed this into the model — 'given this value of {x_col}, what will {y_col} be?'", f"<b>Y-axis → {y_col}:</b> The <b>target (dependent) variable</b> — what we are predicting. The regression line shows the model's best guess for Y at each value of X."),
            "residuals": (f"<b>X-axis → Residual Value:</b> The error for each prediction (actual − predicted). Values near <b>zero mean the model predicted correctly</b>. Large positive/negative values are big errors.", f"<b>Y-axis → Count:</b> How many predictions had that error size. A <b>tall central bar near zero</b> means most predictions were accurate."),
        }

        def data_insight_scatter(df_r, xc, yc):
            try:
                cr = df_r[xc].corr(df_r[yc])
                direction = "positive" if cr > 0 else "negative"
                strength = "strong" if abs(cr) > 0.7 else "moderate" if abs(cr) > 0.4 else "weak"
                return f"📌 <b>Data says:</b> Correlation between <b>{xc}</b> and <b>{yc}</b> is <b>r = {round(cr, 3)}</b> — a <b>{strength} {direction} relationship</b>. {'As one goes up, the other tends to go up too.' if cr > 0 else 'As one goes up, the other tends to come down.'} {'This is strong enough to build a predictive model.' if abs(cr) > 0.6 else 'The relationship exists but other factors also play a role.'}"
            except: return ""

        def data_insight_histogram(df_r, col):
            try:
                mean_v = round(df_r[col].mean(), 2)
                std_v  = round(df_r[col].std(), 2)
                skew_v = round(df_r[col].skew(), 2)
                skew_label = "right-skewed (long tail toward higher values — a few very large values pull the mean up)" if skew_v > 0.5 else "left-skewed (long tail toward lower values)" if skew_v < -0.5 else "approximately normal (bell-shaped, balanced around the mean)"
                return f"📌 <b>Data says:</b> <b>{col}</b> has a mean of <b>{mean_v}</b> and std dev of <b>{std_v}</b>. The distribution is <b>{skew_label}</b>. {'High std dev means values are spread widely — the dataset is diverse.' if std_v > mean_v * 0.3 else 'Low std dev means values cluster tightly around the mean — the dataset is consistent.'}"
            except: return ""

        def data_insight_bar(df_r, col):
            try:
                vc = df_r[col].value_counts()
                top, top_n = vc.index[0], vc.iloc[0]
                bot, bot_n = vc.index[-1], vc.iloc[-1]
                pct = round(top_n / len(df_r) * 100, 1)
                return f"📌 <b>Data says:</b> <b>'{top}'</b> is the most dominant category with <b>{top_n} records ({pct}% of dataset)</b>. <b>'{bot}'</b> is the least represented with only <b>{bot_n} records</b>. This imbalance {'is significant — models trained on this data may be biased toward the dominant class.' if pct > 50 else 'is moderate — the dataset has reasonable diversity across categories.'}"
            except: return ""

        def data_insight_box(df_r, num_c, cat_c):
            try:
                grp = df_r.groupby(cat_c)[num_c]
                means = grp.mean().sort_values(ascending=False)
                top_g = means.index[0]; top_mean = round(means.iloc[0], 2)
                bot_g = means.index[-1]; bot_mean = round(means.iloc[-1], 2)
                return f"📌 <b>Data says:</b> <b>'{top_g}'</b> has the highest average <b>{num_c}</b> at <b>{top_mean}</b>, while <b>'{bot_g}'</b> has the lowest at <b>{bot_mean}</b>. The gap of <b>{round(top_mean - bot_mean, 2)}</b> shows {'a significant performance difference between categories — worth investigating why.' if abs(top_mean - bot_mean) > df_r[num_c].std() else 'a moderate difference — categories are relatively similar in this metric.'}"
            except: return ""

        # pick which explanation set to use
        why = chart_reasons.get(chart_type, "")
        ax  = axis_reasons.get(chart_type, ("", ""))

        if chart_type == "scatter":   insight = data_insight_scatter(df_ref, x_col, y_col)
        elif chart_type in ["histogram", "area"]: insight = data_insight_histogram(df_ref, x_col)
        elif chart_type == "bar":     insight = data_insight_bar(df_ref, cat_col)
        elif chart_type == "box":     insight = data_insight_box(df_ref, x_col, cat_col)
        else: insight = ""

        html = f"""
        <div style='background:rgba(22,4,37,0.6);border:1px solid rgba(102,103,171,0.2);border-radius:12px;padding:14px 16px;margin-top:8px;margin-bottom:4px;'>
            <div style='font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#6667AB;font-weight:600;margin-bottom:10px;'>📖 Chart Explanation</div>
            <div style='font-size:12px;color:rgba(245,213,224,0.75);line-height:1.7;margin-bottom:10px;'>{why}</div>
            <div style='border-top:1px solid rgba(102,103,171,0.15);padding-top:10px;margin-bottom:8px;'>
                <div style='font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#7B337E;font-weight:600;margin-bottom:7px;'>⚙ Axis Choices</div>
                <div style='font-size:11px;color:rgba(245,213,224,0.65);line-height:1.7;margin-bottom:4px;'>{ax[0]}</div>
                <div style='font-size:11px;color:rgba(245,213,224,0.65);line-height:1.7;'>{ax[1]}</div>
            </div>
            {"<div style='border-top:1px solid rgba(102,103,171,0.15);padding-top:10px;'><div style='font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#9B59B6;font-weight:600;margin-bottom:6px;'>🔍 What Your Data Reveals</div><div style='font-size:12px;color:rgba(245,213,224,0.8);line-height:1.7;'>" + insight + "</div></div>" if insight else ""}
        </div>
        """
        return html

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

            reg_exp = explain_chart("regression", x, y, df)
            reg_exp_full = reg_exp.replace(
                "📖 Chart Explanation",
                f"📖 Regression Explanation — R² = {round(score,4)} ({'Strong fit' if score>0.7 else 'Moderate fit' if score>0.4 else 'Weak fit — more features needed'})"
            )
            st.markdown(reg_exp_full, unsafe_allow_html=True)

        with reg_c2:
            st.markdown(f'<div class="story-chart-title">⑪ Residuals — Model Error Check</div>', unsafe_allow_html=True)
            residuals = Yte.values - preds
            fig_res = px.histogram(x=residuals, nbins=20, color_discrete_sequence=[COLORS[4]])
            fig_res.update_layout(**PLOT_LAYOUT, height=260, xaxis_title="Residual", yaxis_title="Count")
            st.plotly_chart(fig_res, use_container_width=True, key="res1")

            res_std = round(float(np.std(residuals)), 3)
            res_mean = round(float(np.mean(residuals)), 3)
            res_skew = "symmetric ✅" if abs(res_mean) < res_std * 0.1 else "skewed ⚠️ — model has systematic bias"
            res_html = explain_chart("residuals", x, y, df)
            res_html_extra = res_html.replace(
                "</div></div>",
                f"<br><br>📌 <b>Your residuals:</b> Mean error = <b>{res_mean}</b> · Std = <b>{res_std}</b> · Shape is <b>{res_skew}</b></div></div>",
                1
            )
            st.markdown(res_html_extra, unsafe_allow_html=True)

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
