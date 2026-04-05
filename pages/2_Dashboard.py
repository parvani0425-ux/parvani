import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import zipfile

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------- LOGIN CHECK ----------------
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

# ---------------- MAIN ----------------
st.title("📊 AI Data Dashboard")

file = st.file_uploader(
    "Upload File",
    type=["csv", "xlsx", "xls", "zip", "json"]
)

# ---------------- FILE HANDLING ----------------
df = None

if file:
    file_type = file.name.split(".")[-1].lower()

    if file_type == "csv":
        df = pd.read_csv(file)

    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(file)

    elif file_type == "json":
        df = pd.read_json(file)

    elif file_type == "zip":
        with zipfile.ZipFile(file) as z:
            for name in z.namelist():
                if name.endswith(".csv"):
                    df = pd.read_csv(z.open(name))
                    break

# ---------------- PROCESS ----------------
if df is not None:

    st.subheader("📂 Raw Data")
    st.dataframe(df.head())

    # CLEANING
    st.subheader("🧹 Data Cleaning")

    before = len(df)
    df = df.drop_duplicates()
    after_dup = len(df)

    missing = df.isnull().sum().sum()
    df = df.dropna()

    st.success(f"✔ Removed {before - after_dup} duplicates")
    st.success(f"✔ Removed {missing} missing values")

    st.subheader("✅ Cleaned Data")
    st.dataframe(df.head())

    # SIMPLIFY LARGE DATA
    if len(df) > 500:
        for col in df.select_dtypes(include="object").columns:
            top_vals = df[col].value_counts().nlargest(7).index
            df = df[df[col].isin(top_vals)]
        st.info("Large data simplified → showing top categories")

    # ---------------- KPI ----------------
    st.subheader("📌 KPI Dashboard")

    num_cols = df.select_dtypes(include=np.number).columns

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])

    if len(num_cols) > 0:
        c3.metric("Average", round(df[num_cols[0]].mean(), 2))
        c4.metric("Max", df[num_cols[0]].max())

        st.markdown("### 📊 KPI Insight")
        st.write(f"Mean shows average trend of {num_cols[0]}")
        st.write(f"Max shows peak value indicating extreme performance")

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visual Analysis")

    if len(num_cols) >= 2:

        x = num_cols[0]
        y = num_cols[1]

        # SCATTER
        st.markdown(f"### 🔹 Scatter Plot ({x} vs {y})")

        fig1 = px.scatter(
            df, x=x, y=y,
            text=df[y].round(2),
            labels={x: x, y: y}
        )
        fig1.update_traces(textposition="top center")
        st.plotly_chart(fig1, key="scatter")

        st.markdown("#### 📌 Explanation")
        st.write(f"""
        X-axis → {x}  
        Y-axis → {y}  

        Shows relationship between variables.  
        Helps in prediction & correlation analysis.
        """)

        # LINE
        st.markdown(f"### 🔹 Trend Line ({y})")

        fig2 = px.line(df, y=y, markers=True)
        st.plotly_chart(fig2, key="line")

        st.markdown("#### 📌 Explanation")
        st.write(f"""
        X-axis → Index/Time  
        Y-axis → {y}  

        Shows trend → growth or decline patterns.
        """)

        # BAR
        cat_cols = df.select_dtypes(include="object").columns

        if len(cat_cols) > 0:
            cat = cat_cols[0]
            top = df[cat].value_counts().nlargest(7)

            st.markdown(f"### 🔹 Category Count ({cat})")

            fig5 = px.bar(
                x=top.index,
                y=top.values,
                text=top.values,
                labels={"x": cat, "y": "Count"}
            )
            fig5.update_traces(textposition="outside")

            st.plotly_chart(fig5, key="bar")

            st.markdown("#### 📌 Explanation")
            st.write(f"""
            X-axis → {cat}  
            Y-axis → Count  

            Shows top categories → helps segmentation.
            """)

        # HISTOGRAM
        st.markdown(f"### 🔹 Distribution ({x})")

        fig3 = px.histogram(df, x=x, text_auto=True)
        st.plotly_chart(fig3, key="hist")

        st.markdown("#### 📌 Explanation")
        st.write(f"""
        X-axis → {x}  
        Y-axis → Frequency  

        Shows distribution & spread of values.
        """)

# ================= AI INSIGHTS (NEW) =================

if df is not None:

    st.markdown("---")
    st.subheader("🤖 Smart AI Insights")

    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include="object").columns

    # -------- SMART INSIGHTS --------
    st.markdown("### 📊 AI Insights")

    st.success(f"✔ Dataset has {df.shape[0]} rows & {df.shape[1]} columns")

    if len(cat_cols) > 0:
        st.success(f"✔ Most frequent {cat_cols[0]} → {df[cat_cols[0]].mode()[0]}")

    if len(num_cols) >= 2:
        corr_val = df[num_cols[0]].corr(df[num_cols[1]])
        st.success(f"✔ Correlation between {num_cols[0]} & {num_cols[1]} → {round(corr_val,2)}")

    # -------- RECOMMEND QUESTIONS --------
    st.markdown("### 💡 Recommended Questions")

    recommendations = []

    if len(num_cols) > 0:
        recommendations.append(f"What is the trend of {num_cols[0]}?")
        recommendations.append(f"What are outliers in {num_cols[0]}?")

    if len(cat_cols) > 0:
        recommendations.append(f"What are top categories in {cat_cols[0]}?")
        recommendations.append(f"How does {cat_cols[0]} affect values?")

    if "selected_q" not in st.session_state:
        st.session_state.selected_q = ""

    for i, q in enumerate(recommendations):
        if st.button(q, key=f"ai_q_{i}"):
            st.session_state.selected_q = q

    # -------- AI Q&A --------
    st.markdown("### 💬 Ask AI About Your Data")

    user_q = st.text_input("Ask anything", value=st.session_state.selected_q)

    def answer_ai(q):
        q = q.lower()

        try:
            if "trend" in q:
                return "Trend visible in line chart above."

            elif "outlier" in q:
                col = num_cols[0]
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                return df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]

            elif "top" in q:
                return df[cat_cols[0]].value_counts().head(5)

            elif "affect" in q:
                return df.groupby(cat_cols[0])[num_cols[0]].mean()

            else:
                return "Ask about trend, outliers, or categories."

        except Exception as e:
            return f"Error: {e}"

    if user_q:
        st.markdown("### 🤖 AI Answer")

        result = answer_ai(user_q)

        if isinstance(result, str):
            st.info(result)
        else:
            st.dataframe(result)
            
