import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 AI Data Analytics Dashboard")

uploaded = st.file_uploader("Upload CSV file")

if uploaded:
    df = pd.read_csv(uploaded)

    # ---------------- RAW DATA ----------------
    st.subheader("📄 Raw Data")
    st.dataframe(df.head())

    # ---------------- CLEANING ----------------
    st.subheader("🧹 Data Cleaning")

    before = df.shape[0]
    nulls = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    df_clean = df.drop_duplicates().dropna()

    after = df_clean.shape[0]

    st.success(f"""
    ✔ Removed rows: {before - after}  
    ✔ Null values found: {nulls}  
    ✔ Duplicates removed: {duplicates}
    """)

    st.subheader("🧼 Cleaned Data")
    st.dataframe(df_clean.head())

    numeric = df_clean.select_dtypes(include='number')

    # ---------------- KPI CARDS ----------------
    st.subheader("📊 Key Metrics")

    if not numeric.empty:
        cols = st.columns(5)

        for i, col in enumerate(numeric.columns[:5]):
            cols[i].metric(
                label=f"{col}",
                value=round(numeric[col].mean(), 2),
                delta=f"Max: {round(numeric[col].max(),2)}"
            )

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visual Analytics (5 Charts)")

    if len(numeric.columns) >= 2:

        col1, col2 = st.columns(2)

        # 1️⃣ Scatter Plot
        with col1:
            fig1 = px.scatter(df_clean, x=numeric.columns[0], y=numeric.columns[1],
                              title="Scatter Plot (Relationship)")
            st.plotly_chart(fig1, use_container_width=True)

        # 2️⃣ Line Chart
        with col2:
            fig2 = px.line(df_clean, y=numeric.columns[0],
                           title="Trend Line")
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)

        # 3️⃣ Histogram
        with col3:
            fig3 = px.histogram(df_clean, x=numeric.columns[0],
                                title="Distribution")
            st.plotly_chart(fig3, use_container_width=True)

        # 4️⃣ Box Plot
        with col4:
            fig4 = px.box(df_clean, y=numeric.columns[0],
                          title="Outliers Detection")
            st.plotly_chart(fig4, use_container_width=True)

        # 5️⃣ Correlation Heatmap
        st.subheader("🔥 Correlation Heatmap")
        corr = numeric.corr()
        fig5 = px.imshow(corr, text_auto=True, title="Feature Correlation")
        st.plotly_chart(fig5, use_container_width=True)

    # ---------------- REGRESSION ----------------
    if len(numeric.columns) >= 2:
        st.subheader("🤖 Regression & Prediction")

        X = numeric.iloc[:, :-1]
        y = numeric.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = LinearRegression()
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        score = r2_score(y_test, preds)

        st.success(f"Model Accuracy (R²): {round(score, 3)}")

        # Prediction chart
        fig_pred = px.scatter(x=y_test, y=preds,
                              labels={'x': 'Actual', 'y': 'Predicted'},
                              title="Prediction vs Actual")
        st.plotly_chart(fig_pred, use_container_width=True)

    # ---------------- INSIGHTS ----------------
    st.subheader("🧠 Insights")

    if not numeric.empty:
        st.write(f"""
        - Dataset contains **{df_clean.shape[0]} cleaned rows**
        - Strong relationships visible in correlation heatmap
        - KPI values indicate overall trends in key variables
        - Regression model shows prediction capability with accuracy score
        """)

    # ---------------- AI EXPLAIN ----------------
    if st.button("🤖 Explain Analysis"):
        st.success("""
        This dashboard cleans your dataset, removes missing values, and extracts key metrics.
        It visualizes relationships, distributions, and trends using multiple charts.
        Regression helps predict future outcomes based on existing data patterns.
        """)
        
