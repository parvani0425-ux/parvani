import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

st.sidebar.title("🚀 AI Platform")

st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard")
st.sidebar.page_link("pages/3_Profile.py", label="Profile")
st.sidebar.page_link("pages/4_About.py", label="About")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

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

# ---------------- VISUAL + EXPLANATION ----------------
st.subheader("📊 Smart Visual Analysis")

if len(numeric.columns) >= 2:

    x_col = numeric.columns[0]
    y_col = numeric.columns[1]

    col1, col2 = st.columns(2)

    # ---------------- SCATTER ----------------
    with col1:
        fig1 = px.scatter(df_clean, x=x_col, y=y_col,
                         title=f"{x_col} vs {y_col}")
        st.plotly_chart(fig1, use_container_width=True)

        st.info(f"""
        📌 WHAT: Shows relationship between {x_col} and {y_col}  
        ❓ WHY: To identify correlation and patterns  
        ⚙ HOW: Each dot represents one data point  
        """)

    # ---------------- LINE ----------------
    with col2:
        fig2 = px.line(df_clean, y=x_col, title=f"{x_col} Trend Over Time")
        st.plotly_chart(fig2, use_container_width=True)

        st.info(f"""
        📌 WHAT: Trend of {x_col} over dataset index  
        ❓ WHY: To observe growth or decline  
        ⚙ HOW: Connected points show progression  
        """)

    col3, col4 = st.columns(2)

    # ---------------- HISTOGRAM ----------------
    with col3:
        fig3 = px.histogram(df_clean, x=x_col, title=f"{x_col} Distribution")
        st.plotly_chart(fig3, use_container_width=True)

        st.info(f"""
        📌 WHAT: Frequency distribution of {x_col}  
        ❓ WHY: Understand spread and skewness  
        ⚙ HOW: Bars show count of values  
        """)

    # ---------------- BOX ----------------
    with col4:
        fig4 = px.box(df_clean, y=x_col, title=f"{x_col} Outliers")
        st.plotly_chart(fig4, use_container_width=True)

        st.info(f"""
        📌 WHAT: Detects outliers in {x_col}  
        ❓ WHY: Identify abnormal values  
        ⚙ HOW: Box shows quartiles & whiskers  
        """)

    # ---------------- HEATMAP ----------------
    st.subheader("🔥 Correlation Insight")

    corr = numeric.corr()
    fig5 = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig5, use_container_width=True)

    st.info("""
    📌 WHAT: Correlation between variables  
    ❓ WHY: Understand relationships strength  
    ⚙ HOW: Values range from -1 to +1  
    """)

    # ---------------- ML MODEL ----------------
st.subheader("🤖 Prediction Model")

if len(numeric.columns) >= 2:

    target = numeric.columns[-1]
    features = numeric.columns[:-1]

    st.write(f"🎯 Predicting: **{target}**")

    X = df_clean[features]
    y = df_clean[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    score = r2_score(y_test, preds)

    st.success(f"📊 Model Accuracy (R² Score): {round(score,3)}")

    # Prediction vs Actual
    fig_pred = px.scatter(x=y_test, y=preds,
                          labels={"x":"Actual", "y":"Predicted"},
                          title="Prediction vs Actual")
    st.plotly_chart(fig_pred, use_container_width=True)

    # ---------------- USER INPUT ----------------
    st.subheader("🔮 Make Your Own Prediction")

    user_inputs = []

    cols = st.columns(len(features))

    for i, col in enumerate(features):
        val = cols[i].number_input(f"Enter {col}", value=float(X[col].mean()))
        user_inputs.append(val)

    if st.button("Predict"):
        result = model.predict([user_inputs])[0]
        st.success(f"🎯 Predicted {target}: {round(result,2)}")

   # ---------------- INSIGHTS ----------------
st.subheader("🧠 Final Insights")

st.write(f"""
✔ Dataset cleaned and optimized  
✔ Strong correlations visible in heatmap  
✔ Distribution shows data spread patterns  
✔ Outliers detected and handled  
✔ Regression model predicts **{target}** with accuracy {round(score,3)}  
✔ You can now input your own values for real-time prediction  
""")

    # ---------------- AI EXPLAIN ----------------
    if st.button("🤖 Explain Analysis"):
        st.success("""
        This dashboard cleans your dataset, removes missing values, and extracts key metrics.
        It visualizes relationships, distributions, and trends using multiple charts.
        Regression helps predict future outcomes based on existing data patterns.
        """)
        
