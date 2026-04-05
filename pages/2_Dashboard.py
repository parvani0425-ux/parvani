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
    cat_cols = df.select_dtypes(include="object").columns

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])

    if len(num_cols) > 0:
        c3.metric("Average", round(df[num_cols[0]].mean(), 2))
        c4.metric("Max", df[num_cols[0]].max())
        st.markdown("### 📊 KPI Insight")
        st.write(f"Mean shows average trend of **{num_cols[0]}**")
        st.write(f"Max shows peak value indicating extreme performance")

    # ---------------- CHARTS & ANALYSIS ----------------
    if len(num_cols) >= 2:
        x, y = num_cols[0], num_cols[1]
        
        st.subheader("📊 Visual Analysis")
        
        # SCATTER
        st.markdown(f"### 🔹 Scatter Plot ({x} vs {y})")
        fig1 = px.scatter(df, x=x, y=y, text=df[y].round(2))
        fig1.update_traces(textposition="top center")
        st.plotly_chart(fig1, key="scatter")

        # LINE
        st.markdown(f"### 🔹 Trend Line ({y})")
        fig2 = px.line(df, y=y, markers=True)
        st.plotly_chart(fig2, key="line")

        # BAR
        if len(cat_cols) > 0:
            cat = cat_cols[0]
            top = df[cat].value_counts().nlargest(7)
            st.markdown(f"### 🔹 Category Count ({cat})")
            fig5 = px.bar(x=top.index, y=top.values, text=top.values, labels={"x": cat, "y": "Count"})
            st.plotly_chart(fig5, key="bar")

        # REGRESSION
        st.subheader("📈 Regression Analysis")
        X_reg, Y_reg = df[[x]], df[y]
        X_train, X_test, Y_train, Y_test = train_test_split(X_reg, Y_reg, test_size=0.2)
        model = LinearRegression().fit(X_train, Y_train)
        preds = model.predict(X_test)
        st.success(f"Accuracy (R²): {round(r2_score(Y_test, preds), 2)}")
        
        fig_reg = px.scatter(df, x=x, y=y)
        fig_reg.add_traces(px.line(x=X_test[x], y=preds).data)
        st.plotly_chart(fig_reg, key="reg")

        # FINAL INSIGHT (Correlation)
        st.markdown("### 🔍 Final Insight")
        corr = df[x].corr(df[y])
        if corr > 0.7:
            st.success(f"Strong positive relationship between {x} and {y}")
        elif corr < -0.7:
            st.warning("Strong negative relationship")
        else:
            st.info("Moderate/weak relationship")

    # ---------------- ASK SECTION ----------------
    st.subheader("💬 Ask Your Data")
    option = st.selectbox("Choose Analysis", ["Mean","Median","Max","Min","Std Dev"])
    if st.button("Run Analysis"):
        st.write(df.select_dtypes(include=np.number).agg(option.lower().replace(" ", "_")))

    # ================= AI SECTION =================
    st.markdown("---")
    st.subheader("🤖 AI Insights & Smart Recommendations")

    # Key Insights
    st.markdown("### 📊 Key Insights")
    st.info(f"✔ Dataset has {df.shape[0]} rows. Data is currently cleaned and ready.")
    if len(cat_cols) > 0:
        top_cat = df[cat_cols[0]].mode()[0]
        st.success(f"✔ Most frequent category in {cat_cols[0]} is **'{top_cat}'**")

    # Recommendations
    st.markdown("### 💡 Recommended Questions")
    recs = []
    if len(num_cols) > 0:
        recs.append(f"What is the trend of {num_cols[0]}?")
        recs.append(f"What are outliers in {num_cols[0]}?")
    if len(cat_cols) > 0:
        recs.append(f"What are top categories in {cat_cols[0]}?")

    if "selected_q" not in st.session_state:
        st.session_state.selected_q = ""

    for i, q in enumerate(recs):
        if st.button(q, key=f"rec_{i}"):
            st.session_state.selected_q = q

    # Ask Anything
    user_q = st.text_input("Ask your own question", value=st.session_state.selected_q)

    def answer_query(q):
        q = q.lower()
        if "trend" in q and len(num_cols) > 0:
            return f"The average value for {num_cols[0]} is {round(df[num_cols[0]].mean(), 2)}."
        elif "outlier" in q and len(num_cols) > 0:
            col = num_cols[0]
            q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            iqr = q3 - q1
            return df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]
        elif "top" in q and len(cat_cols) > 0:
            return df[cat_cols[0]].value_counts().head(5)
        return "Try asking about 'trends', 'outliers', or 'top categories'."

    if user_q:
        st.markdown("### 🤖 AI Answer")
        res = answer_query(user_q)
        if isinstance(res, str): st.info(res)
        else: st.dataframe(res)
            
