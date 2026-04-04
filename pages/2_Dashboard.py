import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import zipfile

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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

    # SIMPLIFY
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

        # KPI INSIGHT
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

        fig1 = px.scatter(df, x=x, y=y, text=y)
        fig1.update_traces(textposition="top center")
        st.plotly_chart(fig1, key="scatter")

        st.write(f"X-axis → {x} (input)")
        st.write(f"Y-axis → {y} (output)")
        st.info("Shows relationship between variables")

        # LINE
        st.markdown(f"### 🔹 Trend Line ({y})")
        fig2 = px.line(df, y=y)
        st.plotly_chart(fig2, key="line")

        st.write(f"X-axis → index/time | Y-axis → {y}")
        st.info("Shows trend over dataset")

        # HIST
        st.markdown(f"### 🔹 Distribution ({x})")
        fig3 = px.histogram(df, x=x)
        st.plotly_chart(fig3, key="hist")

        st.write(f"X-axis → {x} | Y-axis → frequency")
        st.info("Shows spread of values")

        # BOX
        st.markdown(f"### 🔹 Outliers ({y})")
        fig4 = px.box(df, y=y)
        st.plotly_chart(fig4, key="box")

        st.write(f"Y-axis → {y}")
        st.info("Detects extreme values")

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

            st.info("Shows top categories")

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

        # ---------------- INSIGHTS ----------------
        st.subheader("🧠 Insights")

        corr = df[x].corr(df[y])

        st.write(f"Correlation: {round(corr,2)}")

        if corr > 0.7:
            st.write("Strong relationship → reliable predictions")
        elif corr > 0.4:
            st.write("Moderate relationship")
        else:
            st.write("Weak relationship")

        # ---------------- ASK ----------------
        st.subheader("💬 Ask Your Data")

        option = st.selectbox(
            "Choose Analysis",
            ["Mean","Median","Mode","Max","Min","Std Dev","Variance"]
        )

        if st.button("Run Analysis"):

            if option == "Mean":
                st.write(df.mean(numeric_only=True))
                st.info("Average value")

            elif option == "Median":
                st.write(df.median(numeric_only=True))
                st.info("Middle value")

            elif option == "Mode":
                st.write(df.mode(numeric_only=True))
                st.info("Most frequent")

            elif option == "Max":
                st.write(df.max(numeric_only=True))

            elif option == "Min":
                st.write(df.min(numeric_only=True))

            elif option == "Std Dev":
                st.write(df.std(numeric_only=True))

            elif option == "Variance":
                st.write(df.var(numeric_only=True))

        # ---------------- STORYTELLING DASHBOARD ----------------
        st.subheader("📖 Storytelling Dashboard")

        st.write("### 🧠 What the Data Says:")

        st.write(f"- Dataset contains {df.shape[0]} rows and {df.shape[1]} columns")
        st.write(f"- Key variable: {x} influences {y}")

        if corr > 0.7:
            st.write(f"- Strong relationship: as {x} increases, {y} also increases significantly")
        elif corr < -0.7:
            st.write(f"- Inverse trend: as {x} increases, {y} decreases")
        else:
            st.write(f"- Weak relationship: other factors may affect {y}")

        st.write("- Distribution shows how values are spread across dataset")
        st.write("- Outliers indicate unusual patterns")

        st.success("Final Insight: Data can be used for prediction & decision-making")

    else:
        st.warning("Not enough numeric columns")
        
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

    # SIMPLIFY
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

        # KPI INSIGHT
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

        fig1 = px.scatter(df, x=x, y=y, text=y)
        fig1.update_traces(textposition="top center")
        st.plotly_chart(fig1, key="scatter")

        st.write(f"X-axis → {x} (input)")
        st.write(f"Y-axis → {y} (output)")
        st.info("Shows relationship between variables")

        # LINE
        st.markdown(f"### 🔹 Trend Line ({y})")
        fig2 = px.line(df, y=y)
        st.plotly_chart(fig2, key="line")

        st.write(f"X-axis → index/time | Y-axis → {y}")
        st.info("Shows trend over dataset")

        # HIST
        st.markdown(f"### 🔹 Distribution ({x})")
        fig3 = px.histogram(df, x=x)
        st.plotly_chart(fig3, key="hist")

        st.write(f"X-axis → {x} | Y-axis → frequency")
        st.info("Shows spread of values")

        # BOX
        st.markdown(f"### 🔹 Outliers ({y})")
        fig4 = px.box(df, y=y)
        st.plotly_chart(fig4, key="box")

        st.write(f"Y-axis → {y}")
        st.info("Detects extreme values")

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

            st.info("Shows top categories")

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

        # ---------------- INSIGHTS ----------------
        st.subheader("🧠 Insights")

        corr = df[x].corr(df[y])

        st.write(f"Correlation: {round(corr,2)}")

        if corr > 0.7:
            st.write("Strong relationship → reliable predictions")
        elif corr > 0.4:
            st.write("Moderate relationship")
        else:
            st.write("Weak relationship")

        # ---------------- ASK ----------------
        st.subheader("💬 Ask Your Data")

        option = st.selectbox(
            "Choose Analysis",
            ["Mean","Median","Mode","Max","Min","Std Dev","Variance"]
        )

        if st.button("Run Analysis"):

            if option == "Mean":
                st.write(df.mean(numeric_only=True))
                st.info("Average value")

            elif option == "Median":
                st.write(df.median(numeric_only=True))
                st.info("Middle value")

            elif option == "Mode":
                st.write(df.mode(numeric_only=True))
                st.info("Most frequent")

            elif option == "Max":
                st.write(df.max(numeric_only=True))

            elif option == "Min":
                st.write(df.min(numeric_only=True))

            elif option == "Std Dev":
                st.write(df.std(numeric_only=True))

            elif option == "Variance":
                st.write(df.var(numeric_only=True))

        # ---------------- STORYTELLING DASHBOARD ----------------
        st.subheader("📖 Storytelling Dashboard")

        st.write("### 🧠 What the Data Says:")

        st.write(f"- Dataset contains {df.shape[0]} rows and {df.shape[1]} columns")
        st.write(f"- Key variable: {x} influences {y}")

        if corr > 0.7:
            st.write(f"- Strong relationship: as {x} increases, {y} also increases significantly")
        elif corr < -0.7:
            st.write(f"- Inverse trend: as {x} increases, {y} decreases")
        else:
            st.write(f"- Weak relationship: other factors may affect {y}")

        st.write("- Distribution shows how values are spread across dataset")
        st.write("- Outliers indicate unusual patterns")

        st.success("Final Insight: Data can be used for prediction & decision-making")

    else:
        st.warning("Not enough numeric columns")
        
