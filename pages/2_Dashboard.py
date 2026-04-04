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

# ---------------- MAIN ----------------
st.title("📊 AI Data Dashboard")

file = st.file_uploader("Upload CSV File", type=["csv"])

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
        st.markdown("### 🔹 Scatter Plot")
        st.write(f"Why: Shows relationship between {x} and {y}")
        fig1 = px.scatter(df, x=x, y=y, title=f"{x} vs {y}")
        st.plotly_chart(fig1, key="scatter_main")

        # LINE
        st.markdown("### 🔹 Trend Line")
        st.write("Why: Shows trend over time/index")
        fig2 = px.line(df, y=y, title=f"{y} Trend")
        st.plotly_chart(fig2, key="line_main")

        # HISTOGRAM
        st.markdown("### 🔹 Distribution")
        st.write(f"Why: Shows distribution of {x}")
        fig3 = px.histogram(df, x=x, title=f"{x} Distribution")
        st.plotly_chart(fig3, key="hist_main")

        # BOX
        st.markdown("### 🔹 Outliers Detection")
        st.write(f"Why: Detects unusual values in {y}")
        fig4 = px.box(df, y=y, title=f"{y} Outliers")
        st.plotly_chart(fig4, key="box_main")

        # BAR
        cat_cols = df.select_dtypes(include="object").columns
        if len(cat_cols) > 0:
            st.markdown("### 🔹 Category Chart")
            st.write("Why: Shows category counts")
            fig5 = px.bar(df, x=cat_cols[0], title="Category Count")
            st.plotly_chart(fig5, key="bar_main")

        # ---------------- REGRESSION ----------------
        st.subheader("📈 Regression Analysis")

        X = df[[x]]
        Y = df[y]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        model = LinearRegression()
        model.fit(X_train, Y_train)

        preds = model.predict(X_test)
        score = r2_score(Y_test, preds)

        st.success(f"Model Accuracy (R² Score): {round(score, 2)}")

        fig_reg = px.scatter(df, x=x, y=y, title="Regression Fit")
        fig_reg.add_traces(px.line(x=X_test[x], y=preds).data)
        st.plotly_chart(fig_reg, key="reg_main")

        st.write("Why: Regression predicts future values based on trend")

        # ---------------- PREDICTION ----------------
        st.subheader("🤖 Custom Prediction")

        user_val = st.number_input(f"Enter value for {x}", key="basic_input")

        if st.button("Predict", key="basic_predict"):
            result = model.predict([[user_val]])
            st.success(f"Predicted {y}: {round(result[0],2)}")

        # ADVANCED
        st.subheader("⚙️ Advanced Prediction")

        custom_x = st.selectbox("Choose Feature", num_cols, key="feature_select")
        val = st.number_input("Enter Value", key="adv_input")

        if st.button("Run Custom Prediction", key="adv_predict"):
            model2 = LinearRegression()
            model2.fit(df[[custom_x]], df[y])
            res = model2.predict([[val]])
            st.success(f"Prediction: {round(res[0],2)}")

        # ---------------- INSIGHTS ----------------
        st.subheader("🧠 Insights")

        if score > 0.7:
            st.write("Strong relationship → high prediction reliability")
        elif score > 0.4:
            st.write("Moderate relationship → usable predictions")
        else:
            st.write("Weak relationship → low reliability")

        # ---------------- FINAL DASHBOARD ----------------
        st.subheader("📊 Final Dashboard")

        colA, colB = st.columns(2)

        with colA:
            st.plotly_chart(fig1, key="final_scatter")
            st.plotly_chart(fig3, key="final_hist")

        with colB:
            st.plotly_chart(fig2, key="final_line")
            st.plotly_chart(fig4, key="final_box")

        # ---------------- ASK ANYTHING ----------------
        st.subheader("💬 Ask Your Data")

        question = st.text_input("Ask something about your dataset")

        if question:
            if "average" in question.lower():
                st.write(df.mean(numeric_only=True))
            elif "max" in question.lower():
                st.write(df.max(numeric_only=True))
            elif "min" in question.lower():
                st.write(df.min(numeric_only=True))
            else:
                st.write("Try: average, max, min")

    else:
        st.warning("Not enough numeric columns")
        
