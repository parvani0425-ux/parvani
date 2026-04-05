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

 # ---------------- REGRESSION ----------------
        st.subheader("📈 Regression Analysis")

        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import r2_score

        X = df[[x]]
        Y = df[y]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        model = LinearRegression()
        model.fit(X_train, Y_train)

        preds = model.predict(X_test)
        score = r2_score(Y_test, preds)

        st.success(f"Accuracy (R²): {round(score,2)}")

        fig_reg = px.scatter(df, x=x, y=y)
        fig_reg.add_traces(px.line(x=X_test[x], y=preds).data)
        st.plotly_chart(fig_reg, key="reg")

        st.markdown("#### 📌 Explanation")
        st.write(f"""
        Regression predicts {y} based on {x}.  
        R² score shows model accuracy.
        """)

# ================= AI CHART DEVELOPER =================
st.markdown("---")
st.subheader("📊 AI Chart Developer")

st.write("Create your own chart with AI explanation")

# Select chart type
chart_type = st.selectbox(
    "Select Chart Type",
    ["Bar Chart", "Scatter Plot", "Line Chart", "Pie Chart"]
)

# Select columns
all_cols = df.columns.tolist()

x_col = st.selectbox("Select X-axis", all_cols)
y_col = st.selectbox("Select Y-axis (numeric)", df.select_dtypes(include=np.number).columns)

# Top filter
top_n = st.selectbox("Select Top Values", [5, 7, 10, 20])

if st.button("Generate Chart"):

    try:
        temp_df = df.copy()

        # Apply top filter for categorical
        if temp_df[x_col].dtype == "object":
            top_vals = temp_df[x_col].value_counts().nlargest(top_n).index
            temp_df = temp_df[temp_df[x_col].isin(top_vals)]

        # Create chart
        if chart_type == "Bar Chart":
            fig = px.bar(temp_df, x=x_col, y=y_col, text=y_col)

        elif chart_type == "Scatter Plot":
            fig = px.scatter(temp_df, x=x_col, y=y_col)

        elif chart_type == "Line Chart":
            fig = px.line(temp_df, x=x_col, y=y_col, markers=True)

        elif chart_type == "Pie Chart":
            fig = px.pie(temp_df, names=x_col, values=y_col)

        st.plotly_chart(fig)

        # ---------------- AI EXPLANATION ----------------
        st.markdown("### 🤖 Chart Explanation")

        explanation = f"""
📊 **Chart Type:** {chart_type}

🔹 X-axis: {x_col}  
🔹 Y-axis: {y_col}  

### 🧠 What this chart shows:
This visualization helps understand how **{y_col} varies across {x_col}**.

### 📌 Why this chart:
- Bar → compares categories  
- Line → shows trend over time  
- Scatter → shows relationship  
- Pie → shows proportion  

### 🔍 Insight:
This helps identify:
- Top performing categories  
- Patterns and trends  
- Variations in data  

### 🎯 Conclusion:
Use this chart to support decision-making and data storytelling.
"""

        st.info(explanation)

    except Exception as e:
        st.error(f"Error generating chart: {e}")

  # ---------------- STORYTELLING DASHBOARD ----------------
        st.subheader("📖 Storytelling Dashboard")

        st.markdown("### 🧠 Data Story Overview")

        st.write(f"""
        This dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**.  
        Relationship analyzed between **{x} and {y}**.
        """)

        col1, col2 = st.columns(2)

        with col1:
            fig_story1 = px.scatter(df, x=x, y=y, text=df[y].round(2))
            fig_story1.update_traces(textposition="top center")
            st.plotly_chart(fig_story1, key="story_scatter")

            st.write(f"{x} vs {y} relationship → pattern shows correlation")

        with col2:
            fig_story2 = px.line(df, y=y, markers=True)
            st.plotly_chart(fig_story2, key="story_line")

            st.write(f"{y} trend shows growth/decline behavior")

        fig_story3 = px.histogram(df, x=x, text_auto=True)
        st.plotly_chart(fig_story3, key="story_hist")

        st.write(f"{x} distribution shows spread of values")

        if len(cat_cols) > 0:
            fig_story4 = px.bar(x=top.index, y=top.values, text=top.values)
            fig_story4.update_traces(textposition="outside")
            st.plotly_chart(fig_story4, key="story_bar")

            st.write(f"Top categories in {cat}")

# ================= SMART AI INSIGHTS =================
if df is not None:

    st.markdown("---")
    st.subheader("🤖 Smart AI Insights (Auto Generated)")

    try:
        insights = []

        # Dataset overview
        insights.append(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

        # Numeric insights
        num_cols = df.select_dtypes(include=np.number).columns

        if len(num_cols) > 0:
            col = num_cols[0]

            insights.append(f"Average value of {col} is {round(df[col].mean(),2)}.")
            insights.append(f"Maximum value of {col} is {df[col].max()} indicating peak performance.")

            # Outliers
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]

            insights.append(f"{len(outliers)} potential outliers detected in {col}.")

        # Category insights
        cat_cols = df.select_dtypes(include="object").columns

        if len(cat_cols) > 0:
            cat = cat_cols[0]
            top_cat = df[cat].value_counts().idxmax()
            insights.append(f"Most frequent category in {cat} is '{top_cat}'.")

        # Correlation insights
        if len(num_cols) >= 2:
            corr = df[num_cols[0]].corr(df[num_cols[1]])

            if corr > 0.7:
                insights.append("Strong positive relationship between key variables.")
            elif corr < -0.7:
                insights.append("Strong negative relationship between key variables.")
            else:
                insights.append("Moderate relationship observed between variables.")

        # SHOW INSIGHTS
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

    # Numeric-based questions
    if len(num_cols) > 0:
        questions.append(f"What is the trend of {num_cols[0]}?")
        questions.append(f"Are there any outliers in {num_cols[0]}?")
        questions.append(f"What is the distribution of {num_cols[0]}?")

    # Category-based questions
    if len(cat_cols) > 0:
        questions.append(f"What are top categories in {cat_cols[0]}?")
        questions.append(f"How does {cat_cols[0]} impact numeric values?")

    # Correlation-based
    if len(num_cols) >= 2:
        questions.append(f"Is there a relationship between {num_cols[0]} and {num_cols[1]}?")
        questions.append(f"Which factor influences {num_cols[1]} the most?")

    # Session state (IMPORTANT - prevents error)
    if "selected_q" not in st.session_state:
        st.session_state.selected_q = ""

    # Display buttons
    for i, q in enumerate(questions):
        if st.button(f"👉 {q}", key=f"q_{i}"):
            st.session_state.selected_q = q

# ================= ASK ANYTHING =================
if df is not None:

    st.subheader("💬 Ask Anything About Your Data")

    user_q = st.text_input(
        "Ask your question",
        value=st.session_state.get("selected_q", "")
    )

    def answer_question(q):
        q = q.lower()

        try:
            # ---------------- TREND ----------------
            if "trend" in q:
                col = num_cols[0]
                trend = "increasing" if df[col].iloc[-1] > df[col].iloc[0] else "decreasing"

                return f"""
📊 Trend Analysis of {col}

The variable shows a {trend} pattern across the dataset.

This indicates how values are changing over time or observations.

Conclusion:
This helps identify growth or decline patterns and supports forecasting.
"""

            # ---------------- OUTLIERS ----------------
            elif "outlier" in q:
                col = num_cols[0]

                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1

                outliers = df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]

                return f"""
Outlier Analysis for {col}

Total outliers detected: {len(outliers)}

Outliers are extreme values that differ significantly from others.

They may indicate:
- Data errors
- Rare events
- Exceptional cases

Recommendation:
Investigate before making decisions.

Sample:
{outliers.head()}
"""

            # ---------------- DISTRIBUTION ----------------
            elif "distribution" in q:
                col = num_cols[0]

                return f"""
Distribution Analysis of {col}

The histogram shows how values are spread.

Insights:
- Narrow spread → stable data
- Wide spread → high variability

Use this to understand consistency and risk.
"""

            # ---------------- TOP CATEGORIES ----------------
            elif "top" in q:
                cat = cat_cols[0]
                top = df[cat].value_counts().head(5)

                return f"""
Top Categories in {cat}

{top}

These categories appear most frequently.

Use case:
- Market trends
- Customer behavior
- Product popularity
"""

            # ---------------- IMPACT ----------------
            elif "impact" in q:
                cat = cat_cols[0]
                num = num_cols[0]

                impact = df.groupby(cat)[num].mean().sort_values(ascending=False)

                return f"""
Impact of {cat} on {num}

{impact.head()}

Higher values indicate stronger influence.

Helps identify high-performing categories.
"""

            # ---------------- RELATIONSHIP ----------------
            elif "relationship" in q:
                x = num_cols[0]
                y = num_cols[1]

                corr = df[x].corr(df[y])

                strength = (
                    "strong" if abs(corr) > 0.7 else
                    "moderate" if abs(corr) > 0.4 else
                    "weak"
                )

                return f"""
Relationship between {x} and {y}

Correlation: {round(corr,2)}

There is a {strength} relationship.

Positive → both increase together  
Negative → opposite movement  

Useful for prediction and modeling.
"""

            # ---------------- INFLUENCE ----------------
            elif "influence" in q:
                target = num_cols[1]

                corr = df.corr(numeric_only=True)[target].sort_values(ascending=False)

                return f"""
Feature Influence on {target}

{corr}

Higher correlation = stronger impact.

Useful for identifying key drivers in data.
"""

            # ---------------- DEFAULT ----------------
            else:
                return """
Try asking:

• Trend  
• Outliers  
• Top categories  
• Relationship  
• Impact  

Or click recommended questions above 👆
"""

        except Exception as e:
            return f"Error: {e}"

    # SHOW ANSWER
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

    # NEW DROPDOWN (FIXED)
    col_query = st.selectbox(
        "Select column",
        df.columns
    )

    if col_query:

        col = col_query

        if pd.api.types.is_numeric_dtype(df[col]):

            data = df[col]

            mean_val = data.mean()
            median_val = data.median()
            mode_val = data.mode()[0]
            std_val = data.std()
            var_val = data.var()
            min_val = data.min()
            max_val = data.max()
            count_val = data.count()

            st.success(f"📊 Analysis of '{col}'")

            st.markdown(f"""
### 🔢 Statistical Summary

- **Count:** {count_val}  
- **Mean:** {round(mean_val,2)}  
- **Median:** {round(median_val,2)}  
- **Mode:** {mode_val}  
- **Standard Deviation:** {round(std_val,2)}  
- **Variance:** {round(var_val,2)}  
- **Minimum:** {min_val}  
- **Maximum:** {max_val}  

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
            
