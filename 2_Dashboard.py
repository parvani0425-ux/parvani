import streamlit as st
import pandas as pd
import plotly.express as px
from utils import clean_data, run_regression

st.set_page_config(layout="wide")

st.title("📊 AI Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:

    with st.spinner("✨ Processing your data..."):
        df = pd.read_csv(uploaded_file)
        df_clean = clean_data(df)

    st.success("Data cleaned successfully")

    # ---------- DATA ----------
    st.subheader("📄 Data Preview")
    st.dataframe(df_clean)

    # ---------- KPI ----------
    st.subheader("📌 Key Metrics")

    col1, col2 = st.columns(2)
    col1.metric("Rows", df_clean.shape[0])
    col2.metric("Columns", df_clean.shape[1])

    # ---------- CHART ----------
    st.subheader("📊 Visualization")

    numeric_df = df_clean.select_dtypes(include='number')

    x_axis = st.selectbox("X-axis", numeric_df.columns)
    y_axis = st.selectbox("Y-axis", numeric_df.columns)
    chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])

    if chart_type == "Line":
        fig = px.line(df_clean, x=x_axis, y=y_axis)
    elif chart_type == "Bar":
        fig = px.bar(df_clean, x=x_axis, y=y_axis)
    else:
        fig = px.scatter(df_clean, x=x_axis, y=y_axis)

    st.plotly_chart(fig, use_container_width=True)

    # ---------- AI EXPLAIN ----------
    if st.button("🤖 Explain this chart"):
        st.write(f"""
📊 X-axis: {x_axis}  
📊 Y-axis: {y_axis}  

This chart shows how {y_axis} changes with {x_axis}.  
Useful for identifying trends and patterns.
""")

    # ---------- ML ----------
    st.subheader("🤖 Machine Learning")

    accuracy, _, predictions, y_test = run_regression(df_clean)

    if accuracy:
        st.metric("Model Accuracy", round(accuracy,2))

    # ---------- DOWNLOAD ----------
    st.download_button(
        "📥 Download Cleaned Data",
        df_clean.to_csv(index=False),
        "cleaned_data.csv"
    )

else:
    st.info("👆 Upload a CSV file to start")
    