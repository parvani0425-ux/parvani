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

