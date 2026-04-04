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

    # ---------------- CLEANING ----------------
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

    # ---------------- SMART SIMPLIFICATION ----------------
    st.subheader("🧠 Smart Data Simplification")

    if len(df) > 500:
        st.info("Large dataset detected → simplifying for better visuals")

        for col in df.select_dtypes(include="object").columns:
            top_vals = df[col].value_counts().nlargest(7).index
            df = df[df[col].isin(top_vals)]

        st.success("Showing top 5–7 categories only for clarity")

    # ---------------- KPI ----------------
    st.subheader("📌 KPI Dashboard")

    num_cols = df.select_dtypes(include=np.number).columns

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])

    if len(num_cols) > 0:
        c3.metric("Average", round(df[num_cols[0]].mean(), 2))
        c4.metric("Max", df[num_cols[0]].max())

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visual Analysis")

    if len(num_cols) >= 2:

        x = num_cols[0]
        y = num_cols[1]

        # SCATTER
        st.markdown(f"### 🔹 Scatter Plot ({x} vs {y})")
        st.write("Shows relationship between two numeric variables")
        fig1 = px.scatter(df, x=x, y=y, labels={x: x, y: y})
        st.plotly_chart(fig1, key="scatter")

        # LINE
        st.markdown(f"### 🔹 Trend Line ({y})")
        st.write("Shows trend pattern over dataset")
        fig2 = px.line(df, y=y, labels={"y": y})
        st.plotly_chart(fig2, key="line")

        # HIST
        st.markdown(f"### 🔹 Distribution ({x})")
        st.write("Shows frequency distribution")
        fig3 = px.histogram(df, x=x, labels={x: x})
        st.plotly_chart(fig3, key="hist")

        # BOX
        st.markdown(f"### 🔹 Outliers ({y})")
        st.write("Detects extreme values")
        fig4 = px.box(df, y=y, labels={"y": y})
        st.plotly_chart(fig4, key="box")

        # BAR (SMART CATEGORY LIMIT)
        cat_cols = df.select_dtypes(include="object").columns

        if len(cat_cols) > 0:
            cat = cat_cols[0]

            top = df[cat].value_counts().nlargest(7)

            st.markdown(f"### 🔹 Category Count ({cat})")
            st.write("Top categories for clean understanding")

            fig5 = px.bar(
                x=top.index,
                y=top.values,
                labels={"x": cat, "y": "Count"}
            )

            st.plotly_chart(fig5, key="bar")

        # ---------------- REGRESSION ----------------
        st.subheader("📈 Regression Analysis")

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

        # ---------------- PREDICTION ----------------
        st.subheader("🤖 Custom Prediction")

        user_val = st.number_input(f"Enter {x}")

        if st.button("Predict"):
            result = model.predict([[user_val]])
            st.success(f"Predicted {y}: {round(result[0],2)}")

        # ---------------- INSIGHTS ----------------
        st.subheader("🧠 Insights")

        if score > 0.7:
            st.write("Strong relationship → reliable predictions")
        elif score > 0.4:
            st.write("Moderate relationship")
        else:
            st.write("Weak relationship")

        # ---------------- FINAL DASHBOARD ----------------
        st.subheader("📊 Final Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig1, key="f1")
            st.plotly_chart(fig3, key="f3")

        with col2:
            st.plotly_chart(fig2, key="f2")
            st.plotly_chart(fig4, key="f4")

        # ---------------- CHAT ----------------
        st.subheader("💬 Ask Your Data")

        q = st.text_input("Ask something")

        if q:
            q = q.lower()
            if "average" in q:
                st.write(df.mean(numeric_only=True))
            elif "max" in q:
                st.write(df.max(numeric_only=True))
            elif "min" in q:
                st.write(df.min(numeric_only=True))
            else:
                st.write("Try: average, max, min")

    else:
        st.warning("Not enough numeric columns")
        
