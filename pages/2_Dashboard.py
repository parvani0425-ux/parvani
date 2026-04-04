import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import zipfile

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------- LOGIN ----------------
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

st.title("📊 AI Data Dashboard")

# ---------------- FILE ----------------
file = st.file_uploader("Upload File", type=["csv","xlsx","xls","zip","json"])

df = None

if file:
    ext = file.name.split(".")[-1].lower()

    if ext == "csv":
        df = pd.read_csv(file)
    elif ext in ["xlsx","xls"]:
        df = pd.read_excel(file)
    elif ext == "json":
        df = pd.read_json(file)
    elif ext == "zip":
        with zipfile.ZipFile(file) as z:
            for name in z.namelist():
                if name.endswith(".csv"):
                    df = pd.read_csv(z.open(name))
                    break

# ---------------- DATA ----------------
if df is not None:

    st.subheader("📂 Raw Data")
    st.dataframe(df.head())

    # CLEANING
    df = df.drop_duplicates()
    df = df.dropna()
    st.success("✔ Data cleaned successfully")

    # SIMPLIFY
    if len(df) > 500:
        for col in df.select_dtypes(include="object").columns:
            top = df[col].value_counts().nlargest(7).index
            df = df[df[col].isin(top)]
        st.info("Large data simplified → top categories used")

    # ---------------- KPI CARDS ----------------
    st.subheader("📌 KPI Cards")

    num_cols = df.select_dtypes(include=np.number).columns

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])

    if len(num_cols) > 0:
        c3.metric("Mean", round(df[num_cols[0]].mean(),2))
        c4.metric("Std Dev", round(df[num_cols[0]].std(),2))

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visual Analysis")

    if len(num_cols) >= 2:

        x = num_cols[0]
        y = num_cols[1]

        # SCATTER
        st.markdown(f"### 🔹 Scatter Plot ({x} vs {y})")
        st.write(f"X-axis → {x} (input/independent variable)")
        st.write(f"Y-axis → {y} (output/dependent variable)")

        fig1 = px.scatter(df, x=x, y=y, text=y)
        fig1.update_traces(textposition="top center")
        st.plotly_chart(fig1, key="scatter")

        st.info("Insight: Helps detect correlation between variables")

        # LINE
        st.markdown(f"### 🔹 Trend Line ({y})")
        st.write("X-axis → index/time")
        st.write(f"Y-axis → {y}")

        fig2 = px.line(df, y=y)
        st.plotly_chart(fig2, key="line")

        st.info("Insight: Shows increasing/decreasing trend")

        # HIST
        st.markdown(f"### 🔹 Distribution ({x})")
        st.write(f"X-axis → {x}")
        st.write("Y-axis → frequency")

        fig3 = px.histogram(df, x=x)
        st.plotly_chart(fig3, key="hist")

        st.info("Insight: Shows how values are spread")

        # BOX
        st.markdown(f"### 🔹 Outliers ({y})")
        fig4 = px.box(df, y=y)
        st.plotly_chart(fig4, key="box")

        st.info("Insight: Detects extreme values")

        # BAR
        cat_cols = df.select_dtypes(include="object").columns
        if len(cat_cols) > 0:
            cat = cat_cols[0]
            top = df[cat].value_counts().nlargest(7)

            st.markdown(f"### 🔹 Category Count ({cat})")

            fig5 = px.bar(
                x=top.index,
                y=top.values,
                text=top.values
            )
            fig5.update_traces(textposition='outside')

            st.plotly_chart(fig5, key="bar")

            st.info("Insight: Highlights most frequent categories")

        # ---------------- REGRESSION ----------------
        st.subheader("📈 Regression")

        X = df[[x]]
        Y = df[y]

        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2)

        model = LinearRegression()
        model.fit(X_train,Y_train)

        preds = model.predict(X_test)
        score = r2_score(Y_test,preds)

        st.success(f"Accuracy (R²): {round(score,2)}")

        fig_reg = px.scatter(df, x=x, y=y)
        fig_reg.add_traces(px.line(x=X_test[x], y=preds).data)
        st.plotly_chart(fig_reg, key="reg")

        # ---------------- DEEP INSIGHTS ----------------
        st.subheader("🧠 Deep Insights")

        corr = df[x].corr(df[y])

        if corr > 0.7:
            st.write("Strong positive relationship → prediction reliable")
        elif corr < -0.7:
            st.write("Strong negative relationship → inverse trend")
        else:
            st.write("Weak/moderate relationship → less reliable predictions")

        st.write("Distribution + outliers help understand data quality")

        # ---------------- ASK ----------------
        st.subheader("💬 Ask Your Data")

        option = st.selectbox(
            "Choose Analysis",
            ["Mean","Median","Mode","Max","Min","Std Dev","Variance"]
        )

        if st.button("Run Analysis"):

            if option == "Mean":
                result = df.mean(numeric_only=True)
                st.write(result)
                st.info("Mean = average → central tendency")

            elif option == "Median":
                result = df.median(numeric_only=True)
                st.write(result)
                st.info("Median = middle value → robust to outliers")

            elif option == "Mode":
                result = df.mode(numeric_only=True)
                st.write(result)
                st.info("Mode = most frequent value")

            elif option == "Max":
                result = df.max(numeric_only=True)
                st.write(result)
                st.info("Max = highest value")

            elif option == "Min":
                result = df.min(numeric_only=True)
                st.write(result)
                st.info("Min = lowest value")

            elif option == "Std Dev":
                result = df.std(numeric_only=True)
                st.write(result)
                st.info("Std Dev = variability/spread")

            elif option == "Variance":
                result = df.var(numeric_only=True)
                st.write(result)
                st.info("Variance = dispersion measure")

    else:
        st.warning("Not enough numeric columns")
        
