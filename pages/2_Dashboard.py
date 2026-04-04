import streamlit as st
import pandas as pd
import json
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 AI Data Analytics Dashboard")

# ---------------- FILE UPLOAD ----------------
uploaded = st.file_uploader("Upload your CSV file")

def save_history(file_name):
    try:
        history = json.load(open("history.json"))
    except:
        history = []
    history.append(file_name)
    json.dump(history, open("history.json", "w"))

if uploaded:
    df = pd.read_csv(uploaded)

    st.subheader("📄 Raw Data Preview")
    st.dataframe(df.head())

    # ---------------- DATA CLEANING ----------------
    st.subheader("🧹 Data Cleaning Report")

    before_rows = df.shape[0]
    nulls = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    df = df.drop_duplicates()
    df = df.dropna()

    after_rows = df.shape[0]

    st.success(f"""
    ✔ Removed {before_rows - after_rows} rows  
    ✔ Null values found: {nulls}  
    ✔ Duplicate rows removed: {duplicates}
    """)

    numeric_df = df.select_dtypes(include='number')

    # ---------------- KPI CARDS ----------------
    st.subheader("📊 Key Performance Indicators")

    if not numeric_df.empty:
        cols = st.columns(min(5, len(numeric_df.columns)))

        for i, col in enumerate(numeric_df.columns[:5]):
            value = round(numeric_df[col].mean(), 2)
            cols[i].metric(label=f"📈 {col}", value=value)

    # ---------------- REGRESSION ----------------
    if len(numeric_df.columns) >= 2:
        st.subheader("🤖 Regression Analysis")

        X = numeric_df.iloc[:, :-1]
        y = numeric_df.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = LinearRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        score = r2_score(y_test, predictions)

        st.success(f"Model Accuracy (R² Score): {round(score, 3)}")

    # ---------------- SMART VISUALIZATION ----------------
    st.subheader("📊 Smart Visualizations")

    cols = df.columns.tolist()

    x_axis = st.selectbox("Select X-axis", cols)
    y_axis = st.selectbox("Select Y-axis (optional)", [None] + cols)

    x_type = df[x_axis].dtype
    y_type = df[y_axis].dtype if y_axis else None

    fig = None
    chart_type = ""

    # AI-style recommendation
    if y_axis and str(x_type) != "object" and str(y_type) != "object":
        fig = px.scatter(df, x=x_axis, y=y_axis)
        chart_type = "Scatter Plot (Best for numeric relationships)"

    elif y_axis and (str(x_type) == "object" or str(y_type) == "object"):
        fig = px.bar(df, x=x_axis, y=y_axis)
        chart_type = "Bar Chart (Best for category comparison)"

    elif not y_axis and str(x_type) != "object":
        fig = px.histogram(df, x=x_axis)
        chart_type = "Histogram (Best for distribution)"

    elif "date" in x_axis.lower():
        fig = px.line(df, x=x_axis, y=y_axis)
        chart_type = "Line Chart (Best for time trends)"

    else:
        fig = px.line(df, x=x_axis)
        chart_type = "Line Chart"

    st.info(f"🤖 Recommended: {chart_type}")

    if fig:
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- INSIGHTS ----------------
    st.subheader("🧠 Insights")

    if y_axis:
        st.write(f"""
        - Relationship between **{x_axis}** and **{y_axis}**
        - Helps identify trends, patterns, and correlations
        - Useful for predictions and decision making
        """)
    else:
        st.write(f"""
        - Distribution of **{x_axis}**
        - Helps identify spread and outliers
        """)

    # ---------------- AI EXPLAIN ----------------
    if st.button("🤖 Explain this chart"):
        if y_axis:
            st.success(f"""
            This chart shows how {x_axis} affects {y_axis}.
            Patterns in this chart can help in forecasting and analysis.
            """)
        else:
            st.success(f"""
            This chart shows how values of {x_axis} are distributed.
            Useful for understanding variability and trends.
            """)

    # ---------------- MAP SUPPORT ----------------
    if "latitude" in df.columns and "longitude" in df.columns:
        st.subheader("🌍 Map Visualization")
        st.map(df[["latitude", "longitude"]])

    # ---------------- SAVE HISTORY ----------------
    save_history(uploaded.name)
