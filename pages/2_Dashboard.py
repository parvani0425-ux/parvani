import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------- LOGIN CHECK ----------------
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 AI Platform")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard")
st.sidebar.page_link("pages/3_profile.py", label="Profile")
st.sidebar.page_link("pages/4_About.py", label="About")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

# ---------------- MAIN ----------------
st.title("📊 AI Data Dashboard")

file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if file:

    df = pd.read_csv(file)

    st.subheader("📂 Raw Data")
    st.dataframe(df.head())

    # ---------------- CLEANING ----------------
    st.subheader("🧹 Data Cleaning")

    before = df.shape[0]
    df = df.drop_duplicates()
    after_dup = df.shape[0]

    df = df.dropna()
    after_na = df.shape[0]

    st.success(f"✔ Removed {before - after_dup} duplicate rows")
    st.success(f"✔ Removed {after_dup - after_na} missing rows")

    st.subheader("✅ Cleaned Data")
    st.dataframe(df.head())

    # ---------------- KPI CARDS ----------------
    st.subheader("📌 KPI Dashboard")

    num_cols = df.select_dtypes(include=np.number).columns

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    if len(num_cols) > 0:
        col3.metric("Average", round(df[num_cols[0]].mean(), 2))
        col4.metric("Max", df[num_cols[0]].max())

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visual Analysis")

    if len(num_cols) >= 2:

        x = num_cols[0]
        y = num_cols[1]

        # SCATTER
        st.markdown("### 🔹 Scatter Plot")
        st.write(f"**Why this chart?** To understand relationship between {x} and {y}")
        fig1 = px.scatter(df, x=x, y=y, title=f"{x} vs {y}")
        st.plotly_chart(fig1)

        st.write("👉 Shows correlation pattern (positive/negative/no relation)")

        # LINE
        st.markdown("### 🔹 Trend Line")
        st.write("**Why?** To observe trends over index/time")
        fig2 = px.line(df, y=y, title=f"{y} Trend")
        st.plotly_chart(fig2)

        # HISTOGRAM
        st.markdown("### 🔹 Distribution")
        st.write(f"**Why?** To understand how {x} values are spread")
        fig3 = px.histogram(df, x=x, title=f"{x} Distribution")
        st.plotly_chart(fig3)

        # BOX
        st.markdown("### 🔹 Outliers")
        st.write(f"**Why?** To detect unusual values in {y}")
        fig4 = px.box(df, y=y, title=f"{y} Outliers")
        st.plotly_chart(fig4)

        # BAR (categorical if exists)
        cat_cols = df.select_dtypes(include='object').columns
        if len(cat_cols) > 0:
            st.markdown("### 🔹 Category Analysis")
            fig5 = px.bar(df, x=cat_cols[0], title="Category Count")
            st.plotly_chart(fig5)

        # ---------------- REGRESSION ----------------
        st.subheader("📈 Regression Model")

        X = df[[x]]
        Y = df[y]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        model = LinearRegression()
        model.fit(X_train, Y_train)

        preds = model.predict(X_test)
        score = r2_score(Y_test, preds)

        st.success(f"Model Accuracy (R²): {round(score, 2)}")

        fig_reg = px.scatter(df, x=x, y=y, title="Regression Fit")
        fig_reg.add_traces(px.line(x=X_test[x], y=preds).data)
        st.plotly_chart(fig_reg)

        st.write("👉 Regression helps predict future values based on past trends.")

        # ---------------- PREDICTION ----------------
        st.subheader("🤖 Custom Prediction")

        user_val = st.number_input(f"Enter value for {x}")

        if st.button("Predict"):
            result = model.predict([[user_val]])
            st.success(f"Predicted {y}: {round(result[0],2)}")

        # ---------------- ADVANCED PREDICTION ----------------
        st.subheader("⚙️ Advanced Prediction")

        custom_x = st.selectbox("Choose Feature", num_cols)

        val = st.number_input("Enter Value")

        if st.button("Run Custom Prediction"):
            model2 = LinearRegression()
            model2.fit(df[[custom_x]], df[y])
            res = model2.predict([[val]])
            st.success(f"Prediction: {round(res[0],2)}")

        # ---------------- INSIGHTS ----------------
        st.subheader("🧠 Insights")

        if score > 0.7:
            st.write("Strong relationship between variables → reliable predictions.")
        elif score > 0.4:
            st.write("Moderate relationship → decent predictions.")
        else:
            st.write("Weak relationship → predictions may not be reliable.")

        st.write("Check scatter + regression line for understanding patterns.")

        # ---------------- FINAL DASHBOARD ----------------
        st.subheader("📊 Final Summary Dashboard")

        c1, c2 = st.columns(2)

        with c1:
            st.plotly_chart(fig1)
            st.plotly_chart(fig3)

        with c2:
            st.plotly_chart(fig2)
            st.plotly_chart(fig4)

        # ---------------- ASK ANYTHING ----------------
        st.subheader("💬 Ask Questions About Data")

        question = st.text_input("Ask anything about your data")

        if question:
            if "average" in question.lower():
                st.write(df.mean(numeric_only=True))
            elif "max" in question.lower():
                st.write(df.max(numeric_only=True))
            elif "min" in question.lower():
                st.write(df.min(numeric_only=True))
            else:
                st.write("Try asking about average, max, min or trends")

    else:
        st.warning("Not enough numeric data for analysis.")
    
