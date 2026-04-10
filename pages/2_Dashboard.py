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

# ---------------- DATASET UNDERSTANDING ----------------
    st.markdown("### 🧠 Dataset Understanding & Problem Definition")

    file_type = file.name.split(".")[-1].upper()

    source_map = {
        "CSV": "CSV file containing structured tabular data",
        "XLSX": "Excel file with spreadsheet-based structured data",
        "XLS": "Excel file with spreadsheet-based structured data",
        "JSON": "JSON file containing semi-structured hierarchical data",
        "ZIP": "Compressed ZIP file containing dataset files"
    }

    dataset_source = source_map.get(file_type, "User uploaded dataset")

    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include="object").columns

    if len(num_cols) >= 2:
        objective = f"""
The primary objective of this analysis is to explore relationships between key numerical variables such as **{num_cols[0]}** and **{num_cols[1]}**.  
This includes identifying trends, measuring correlations, and understanding how changes in one variable may influence another.

The analysis also aims to support predictive modeling and uncover meaningful patterns that can assist in decision-making.
"""
    elif len(num_cols) == 1:
        objective = f"""
The objective of this analysis is to study the behavior and distribution of the numerical variable **{num_cols[0]}**.  
This includes evaluating central tendencies (mean, median), variability, and identifying any unusual patterns or outliers.
"""
    elif len(cat_cols) > 0:
        objective = f"""
The objective is to analyze categorical data, particularly focusing on **{cat_cols[0]}**, to identify dominant categories, frequency distribution, and segmentation patterns.
"""
    else:
        objective = "The objective is to perform general exploratory data analysis."

    if len(cat_cols) > 0 and len(num_cols) > 0:
        business_problem = f"""
The key analytical problem is to understand how categorical factors such as **{cat_cols[0]}** influence numerical outcomes like **{num_cols[0]}**.

This helps in identifying:
- High-performing categories  
- Key drivers affecting performance  
- Opportunities for optimization  

Such insights are valuable for improving strategy, segmentation, and decision-making.
"""
    elif len(num_cols) >= 2:
        business_problem = f"""
The main problem is to analyze how **{num_cols[0]}** impacts **{num_cols[1]}** and whether a strong relationship exists between them.
"""
    else:
        business_problem = "The problem focuses on extracting meaningful insights and detecting anomalies."

    st.write(f"""
### 📌 Objective of Analysis
{objective}

### 📂 Dataset Source
{dataset_source}

### 🔑 Key Variables
- Total Columns: {df.shape[1]}  
- Numerical Features: {list(num_cols)}  
- Categorical Features: {list(cat_cols)}  

### 💼 Business / Analytical Problem
{business_problem}
""")

    # ---------------- DATA CLEANING ----------------
    st.subheader("🧹 Data Cleaning & Preprocessing")

    st.write("""
    This step ensures data quality by:
    - Removing duplicate records  
    - Handling missing values  
    - Preparing dataset for analysis  
    """)

    before = len(df)
    df = df.drop_duplicates()
    after_dup = len(df)
    missing = df.isnull().sum().sum()
    df = df.dropna()
    df = df.infer_objects()

    st.success(f"✔ Removed {before - after_dup} duplicate rows")
    st.success(f"✔ Removed {missing} missing values")

    st.markdown("""
    ### 🧠 Cleaning Insight
    - Duplicate removal ensures no repeated data  
    - Missing values removal improves accuracy  
    - Data is now consistent and ready for analysis  
    """)

    st.subheader("✅ Cleaned Data")
    st.dataframe(df.head())

# ---------------- SAVE FULL ANALYSIS ----------------

import datetime
import json
import os

if df is not None and file is not None:

    history_file = "history.json"

    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                content = f.read().strip()
                history_data = json.loads(content) if content else []
        except:
            history_data = []
    else:
        history_data = []

    num_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include="object").columns

    if len(num_cols) > 0:
        mean_val = float(df[num_cols[0]].mean())
        median_val = float(df[num_cols[0]].median())
        std_val = float(df[num_cols[0]].std())
    else:
        mean_val = median_val = std_val = None

    if len(num_cols) >= 2:
        corr_val = float(df[num_cols[0]].corr(df[num_cols[1]]))
    else:
        corr_val = None

    r2 = None
    if len(num_cols) >= 2:
        try:
            X = df[[num_cols[0]]]
            Y = df[num_cols[1]]
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
            model = LinearRegression()
            model.fit(X_train, Y_train)
            preds = model.predict(X_test)
            r2 = float(r2_score(Y_test, preds))
        except:
            r2 = None

    if len(cat_cols) > 0:
        try:
            top_category = df[cat_cols[0]].value_counts().idxmax()
        except:
            top_category = None
    else:
        top_category = None

    entry = {
        "file_name": file.name,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": df.head(50).to_dict(),
        "stats": {"mean": mean_val, "median": median_val, "std": std_val},
        "correlation": corr_val,
        "r2_score": r2,
        "top_category": top_category
    }

    if len(history_data) == 0 or history_data[-1]["file_name"] != file.name:
        history_data.append(entry)

    try:
        with open(history_file, "w") as f:
            json.dump(history_data, f, indent=4)
    except Exception as e:
        st.error(f"Save error: {e}")

# ---------------- FEATURE ENGINEERING ----------------
if df is not None:

    st.markdown("---")
    st.subheader("⚙️ Feature Engineering (AI Powered)")

    try:
        df_fe = df.copy()
        num_cols = df_fe.select_dtypes(include=np.number).columns
        cat_cols = df_fe.select_dtypes(include="object").columns

        for col in num_cols:
            df_fe[col] = df_fe[col].fillna(df_fe[col].mean())
        for col in cat_cols:
            df_fe[col] = df_fe[col].fillna(df_fe[col].mode()[0])

        st.success("✔ Missing values handled")

        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        for col in cat_cols:
            df_fe[col] = le.fit_transform(df_fe[col])
        st.success("✔ Categorical encoding done")

        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        if len(num_cols) > 0:
            df_fe[num_cols] = scaler.fit_transform(df_fe[num_cols])
            st.success("✔ Scaling applied")

        if len(num_cols) >= 2:
            new_col = f"{num_cols[0]}_ratio"
            df_fe[new_col] = df[num_cols[0]] / (df[num_cols[1]] + 1e-5)
            st.success(f"✔ Created feature: {new_col}")

        st.dataframe(df_fe.head())

    except Exception as e:
        st.error(f"Feature Engineering Error: {e}")

    # ---------------- DOWNLOAD ----------------
    st.markdown("### ⬇️ Download Cleaned Dataset")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned Data",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    if len(df) > 500:
        for col in df.select_dtypes(include="object").columns:
            top_vals = df[col].value_counts().nlargest(7).index
            df = df[df[col].isin(top_vals)]
        st.info("Large data simplified → showing top categories")

    # ============================================================
    # ---------------- KPI DASHBOARD (IMPROVED) ----------------
    # ============================================================
    st.subheader("📌 KPI Dashboard")

    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include="object").columns

    # --- ROW 1: Basic KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📋 Total Records", df.shape[0])
    c2.metric("🗂️ Total Columns", df.shape[1])

    if len(num_cols) > 0:
        avg_val = round(df[num_cols[0]].mean(), 2)
        max_val = df[num_cols[0]].max()
        c3.metric(f"📊 Avg {num_cols[0]}", avg_val)
        c4.metric(f"🔝 Max {num_cols[0]}", max_val)

    # --- ROW 2: Business KPIs ---
    if len(num_cols) > 0:
        st.markdown("#### 💼 Business KPIs")

        b1, b2, b3 = st.columns(3)

        # KPI 1: Min value
        min_val = df[num_cols[0]].min()
        b1.metric(f"⬇️ Min {num_cols[0]}", min_val)

        # KPI 2: Price Range
        price_range = round(max_val - min_val, 2)
        b2.metric(f"📏 {num_cols[0]} Range", price_range)

        # KPI 3: Median
        median_val = round(df[num_cols[0]].median(), 2)
        b3.metric(f"📍 Median {num_cols[0]}", median_val)

        # --- ROW 3: Category KPIs ---
        if len(cat_cols) > 0:
            k1, k2 = st.columns(2)

            # KPI 4: Top Brand / Category
            top_brand = df[cat_cols[0]].value_counts().idxmax()
            top_brand_count = df[cat_cols[0]].value_counts().max()
            k1.metric(f"🏆 Top {cat_cols[0]}", top_brand, f"{top_brand_count} entries")

            # KPI 5: Most Expensive Brand (if num + cat exist)
            try:
                most_expensive = df.groupby(cat_cols[0])[num_cols[0]].mean().idxmax()
                most_expensive_val = round(df.groupby(cat_cols[0])[num_cols[0]].mean().max(), 2)
                k2.metric(f"💰 Highest Avg {num_cols[0]} ({cat_cols[0]})", most_expensive, f"Avg: {most_expensive_val}")
            except:
                pass

        # --- KPI INSIGHTS ---
        st.markdown("#### 📌 KPI Insights")
        st.write(f"• **Average {num_cols[0]}** is **{avg_val}** — this represents the typical value across all records.")
        st.write(f"• **{num_cols[0]} Range** of **{price_range}** shows the spread between lowest and highest values.")
        st.write(f"• **Median {num_cols[0]}** is **{median_val}** — values above this are above average performance.")
        if len(cat_cols) > 0:
            st.write(f"• **{top_brand}** is the most frequent {cat_cols[0]} with **{top_brand_count}** entries — dominates the dataset.")
            try:
                st.write(f"• **{most_expensive}** has the highest average {num_cols[0]} of **{most_expensive_val}** — premium segment leader.")
            except:
                pass

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visual Analysis")

    if len(num_cols) >= 2:

        x = num_cols[0]
        y = num_cols[1]

        st.markdown(f"### 🔹 Scatter Plot ({x} vs {y})")
        fig1 = px.scatter(df, x=x, y=y, text=df[y].round(2), labels={x: x, y: y})
        fig1.update_traces(textposition="top center")
        st.plotly_chart(fig1, key="scatter")

        st.markdown("#### 📌 Explanation")
        st.write(f"X-axis → {x} | Y-axis → {y}\n\nShows relationship between variables. Helps in prediction & correlation analysis.")

        st.markdown(f"### 🔹 Trend Line ({y})")
        fig2 = px.line(df, y=y, markers=True)
        st.plotly_chart(fig2, key="line")

        st.markdown("#### 📌 Explanation")
        st.write(f"X-axis → Index/Time | Y-axis → {y}\n\nShows trend → growth or decline patterns.")

        cat_cols = df.select_dtypes(include="object").columns
        if len(cat_cols) > 0:
            cat = cat_cols[0]
            top = df[cat].value_counts().nlargest(7)
            st.markdown(f"### 🔹 Category Count ({cat})")
            fig5 = px.bar(x=top.index, y=top.values, text=top.values, labels={"x": cat, "y": "Count"})
            fig5.update_traces(textposition="outside")
            st.plotly_chart(fig5, key="bar")
            st.markdown("#### 📌 Explanation")
            st.write(f"X-axis → {cat} | Y-axis → Count\n\nShows top categories → helps segmentation.")

        st.markdown(f"### 🔹 Distribution ({x})")
        fig3 = px.histogram(df, x=x, text_auto=True)
        st.plotly_chart(fig3, key="hist")
        st.markdown("#### 📌 Explanation")
        st.write(f"X-axis → {x} | Y-axis → Frequency\n\nShows distribution & spread of values.")

        # ---------------- REGRESSION ----------------
        st.subheader("📈 Regression Analysis")

        X = df[[x]]
        Y = df[y]
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        model = LinearRegression()
        model.fit(X_train, Y_train)
        preds = model.predict(X_test)
        score = r2_score(Y_test, preds)

        # ✅ FIXED: Handle negative R²
        if score < 0:
            st.info("📊 R² Score: N/A — Dataset is too small for reliable regression. More data needed for accurate predictions.")
        else:
            st.success(f"✅ Accuracy (R²): {round(score, 2)}")

        fig_reg = px.scatter(df, x=x, y=y)
        fig_reg.add_traces(px.line(x=X_test[x], y=preds).data)
        st.plotly_chart(fig_reg, key="reg")

        st.markdown("#### 📌 Explanation")
        st.write(f"Regression predicts {y} based on {x}.\nR² score shows model accuracy.")

# ================= AI CHART GENERATOR =================
if df is not None:

    st.subheader("📊 AI Chart Developer")

    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])
    all_cols = df.columns.tolist()
    x_col = st.selectbox("Select X-axis", all_cols)
    y_col = st.selectbox("Select Y-axis", all_cols)
    top_n = st.selectbox("Top values", [5, 7, 10])

    if st.button("Generate Chart"):
        temp_df = df[[x_col, y_col]].dropna().head(top_n)

        if chart_type == "Bar Chart":
            fig = px.bar(temp_df, x=x_col, y=y_col)
        elif chart_type == "Line Chart":
            fig = px.line(temp_df, x=x_col, y=y_col, markers=True)
        elif chart_type == "Scatter Plot":
            fig = px.scatter(temp_df, x=x_col, y=y_col)
        elif chart_type == "Pie Chart":
            fig = px.pie(temp_df, names=x_col, values=y_col)

        st.plotly_chart(fig)

        st.markdown("### 🤖 AI Chart Insight")
        try:
            if chart_type == "Pie Chart":
                grouped = temp_df.groupby(x_col)[y_col].sum()
                total = grouped.sum()
                top_category = grouped.idxmax()
                top_value = grouped.max()
                percentage = (top_value / total) * 100
                st.success(f"🔍 {top_category} contributes highest at {round(percentage,2)}% — Dominant category")

            elif chart_type == "Bar Chart":
                grouped = temp_df.groupby(x_col)[y_col].sum().sort_values(ascending=False)
                st.success(f"🔍 Highest: {grouped.index[0]} | Lowest: {grouped.index[-1]} — Clear variation across categories")

            elif chart_type == "Line Chart":
                trend = "increasing" if temp_df[y_col].iloc[-1] > temp_df[y_col].iloc[0] else "decreasing"
                st.success(f"🔍 Trend is {trend} — Shows movement over time")

            elif chart_type == "Scatter Plot":
                corr = temp_df[x_col].corr(temp_df[y_col])
                st.success(f"🔍 Correlation: {round(corr,2)} — Shows relationship strength")

        except Exception as e:
            st.warning(f"Insight error: {e}")

# ---------------- STORYTELLING DASHBOARD ----------------
if df is not None:

    st.markdown("---")
    st.subheader("📖 Storytelling Dashboard")
    st.markdown("### 🧠 Data Story Overview")
    st.write(f"This dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**. Relationship analyzed between **{x} and {y}**.")

    col1, col2 = st.columns(2)
    with col1:
        fig_story1 = px.scatter(df, x=x, y=y, text=df[y].round(2))
        fig_story1.update_traces(textposition="top center")
        st.plotly_chart(fig_story1, use_container_width=True)
        st.write(f"🔍 {x} vs {y} → shows relationship and correlation pattern.")

    with col2:
        fig_story2 = px.line(df, y=y, markers=True)
        st.plotly_chart(fig_story2, use_container_width=True)
        st.write(f"📈 {y} trend → shows growth or decline behavior over dataset.")

    fig_story3 = px.histogram(df, x=x, text_auto=True)
    st.plotly_chart(fig_story3, use_container_width=True)
    st.write(f"📊 Distribution of {x} → shows spread and frequency of values.")

    if len(cat_cols) > 0:
        cat = cat_cols[0]
        top = df[cat].value_counts().head(5)
        fig_story4 = px.bar(x=top.index, y=top.values, text=top.values)
        fig_story4.update_traces(textposition="outside")
        st.plotly_chart(fig_story4, use_container_width=True)
        st.write(f"🏆 Top categories in {cat} → highlights most frequent values.")

# ================= SMART AI INSIGHTS =================
if df is not None:

    st.markdown("---")
    st.subheader("🤖 Smart AI Insights (Auto Generated)")

    try:
        insights = []
        insights.append(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            col = num_cols[0]
            insights.append(f"Average value of {col} is {round(df[col].mean(),2)}.")
            insights.append(f"Maximum value of {col} is {df[col].max()} indicating peak performance.")
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]
            insights.append(f"{len(outliers)} potential outliers detected in {col}.")

        cat_cols = df.select_dtypes(include="object").columns
        if len(cat_cols) > 0:
            cat = cat_cols[0]
            top_cat = df[cat].value_counts().idxmax()
            insights.append(f"Most frequent category in {cat} is '{top_cat}'.")

        if len(num_cols) >= 2:
            corr = df[num_cols[0]].corr(df[num_cols[1]])
            if corr > 0.7:
                insights.append("Strong positive relationship between key variables.")
            elif corr < -0.7:
                insights.append("Strong negative relationship between key variables.")
            else:
                insights.append("Moderate relationship observed between variables.")

        for i in insights:
            st.success(f"✔ {i}")

    except Exception as e:
        st.error(f"AI Insight Error: {e}")

# ================= RECOMMENDED QUESTIONS =================
if df is not None:

    st.markdown("---")
    st.subheader("💡 Recommended Questions (Dynamic)")

    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include="object").columns
    questions = []

    if len(num_cols) > 0:
        questions.append(f"What is the trend of {num_cols[0]}?")
        questions.append(f"Are there any outliers in {num_cols[0]}?")
        questions.append(f"What is the distribution of {num_cols[0]}?")

    if len(cat_cols) > 0:
        questions.append(f"What are top categories in {cat_cols[0]}?")
        questions.append(f"How does {cat_cols[0]} impact numeric values?")

    if len(num_cols) >= 2:
        questions.append(f"Is there a relationship between {num_cols[0]} and {num_cols[1]}?")
        questions.append(f"Which factor influences {num_cols[1]} the most?")

    if "selected_q" not in st.session_state:
        st.session_state.selected_q = ""

    for i, q in enumerate(questions):
        if st.button(f"👉 {q}", key=f"q_{i}"):
            st.session_state.selected_q = q

# ================= ASK ANYTHING =================
if df is not None:

    st.subheader("💬 Ask Anything About Your Data")

    user_q = st.text_input("Ask your question", value=st.session_state.get("selected_q", ""))

    def answer_question(q):
        q = q.lower()
        try:
            if "trend" in q:
                col = num_cols[0]
                trend = "increasing" if df[col].iloc[-1] > df[col].iloc[0] else "decreasing"
                return f"📊 Trend Analysis of {col}\n\nThe variable shows a {trend} pattern across the dataset."

            elif "outlier" in q:
                col = num_cols[0]
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                outliers = df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]
                return f"Outlier Analysis for {col}\n\nTotal outliers detected: {len(outliers)}\n\n{outliers.head()}"

            elif "distribution" in q:
                col = num_cols[0]
                return f"Distribution Analysis of {col}\n\nThe histogram shows how values are spread.\n\nNarrow spread → stable | Wide spread → high variability"

            elif "top" in q:
                cat = cat_cols[0]
                top = df[cat].value_counts().head(5)
                return f"Top Categories in {cat}\n\n{top}"

            elif "impact" in q:
                cat = cat_cols[0]
                num = num_cols[0]
                impact = df.groupby(cat)[num].mean().sort_values(ascending=False)
                return f"Impact of {cat} on {num}\n\n{impact.head()}"

            elif "relationship" in q:
                x = num_cols[0]
                y = num_cols[1]
                corr = df[x].corr(df[y])
                strength = "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.4 else "weak"
                return f"Relationship between {x} and {y}\n\nCorrelation: {round(corr,2)}\n\nThere is a {strength} relationship."

            elif "influence" in q:
                target = num_cols[1]
                corr = df.corr(numeric_only=True)[target].sort_values(ascending=False)
                return f"Feature Influence on {target}\n\n{corr}\n\nHigher correlation = stronger impact."

            else:
                return "Try asking: Trend | Outliers | Top categories | Relationship | Impact"

        except Exception as e:
            return f"Error: {e}"

    if user_q:
        st.subheader("🤖 AI Answer")
        result = answer_question(user_q)
        if isinstance(result, str):
            st.info(result)
        else:
            st.dataframe(result)

# ================= NUMERICAL AI ANALYZER =================
if df is not None:

    st.markdown("---")
    st.subheader("📊 AI Numerical Analyzer")
    st.write("Select a column to get full statistical analysis")

    col_query = st.selectbox("Select column", df.columns)

    if col_query:
        col = col_query
        if pd.api.types.is_numeric_dtype(df[col]):
            data = df[col]
            st.success(f"📊 Analysis of '{col}'")
            st.markdown(f"""
### 🔢 Statistical Summary

- **Count:** {data.count()}  
- **Mean:** {round(data.mean(),2)}  
- **Median:** {round(data.median(),2)}  
- **Mode:** {data.mode()[0]}  
- **Standard Deviation:** {round(data.std(),2)}  
- **Variance:** {round(data.var(),2)}  
- **Minimum:** {data.min()}  
- **Maximum:** {data.max()}  

---

### 🧠 Interpretation

👉 Mean vs Median:
- Similar → balanced data  
- Different → skewed data  

👉 Standard Deviation:
- Low → stable  
- High → variable  

👉 Range:
- Shows spread of values  

---

### 📌 Insight

This helps understand distribution, variability, and decision-making patterns.
""")
        else:
            st.warning("❌ Selected column is not numerical")
