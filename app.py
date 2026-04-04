import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from utils import clean_data, run_regression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Data Dashboard", layout="wide")

# ---------------- USER FUNCTIONS ----------------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

users = load_users()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "login"

# ---------------- LOGIN ----------------
if st.session_state["page"] == "login":

    st.title("🔐 Login / Signup")

    menu = st.radio("Select Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Signup":
        if st.button("Create Account"):
            if username in users:
                st.warning("User already exists")
            else:
                users[username] = password
                save_users(users)
                st.success("Account created successfully!")

    elif menu == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["page"] = "dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ---------------- DASHBOARD ----------------
st.title("📊 AI Data Analytics Dashboard")

st.sidebar.write(f"👋 Welcome, {st.session_state.get('username','User')}")
st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Go to",
    ["Upload & Clean", "ML & KPIs", "Visualization", "Advanced Insights"]
)

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"
    st.rerun()

# ---------------- UPLOAD ----------------
if section == "Upload & Clean":

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df_clean = clean_data(df)

        st.session_state["df"] = df
        st.session_state["df_clean"] = df_clean

        st.subheader("📄 Original Data")
        st.dataframe(df)

        st.subheader("🧹 Cleaned Data")
        st.dataframe(df_clean)

        # Data Quality Score
        missing = df.isnull().sum().sum()
        total = df.size
        score = 100 - (missing / total * 100)

        st.metric("📊 Data Quality Score", f"{round(score,2)}%")

        # Download button
        csv = df_clean.to_csv(index=False)

        st.download_button(
            label="📥 Download Cleaned Data",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

# ---------------- ML ----------------
if section == "ML & KPIs":

    df_clean = st.session_state.get("df_clean")

    if df_clean is not None:

        accuracy, numeric_df, predictions, y_test = run_regression(df_clean)

        st.subheader("📌 Key Metrics")

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df_clean.shape[0])
        col2.metric("Columns", df_clean.shape[1])
        col3.metric("Accuracy", f"{round(accuracy,2) if accuracy else 'N/A'}")

        st.subheader("📖 KPI Explanation")

        st.write(f"""
- Rows represent total observations  
- Columns represent variables  
- Accuracy shows model performance  
""")

        if predictions is not None:
            st.subheader("🤖 Model Predictions")

            pred_df = pd.DataFrame({
                "Actual": y_test.values[:10],
                "Predicted": predictions[:10]
            })

            st.dataframe(pred_df)

        # USER INPUT PREDICTION
        st.subheader("🎯 Try Your Own Prediction")

        input_data = {}

        for col in numeric_df.columns[:-1]:
            input_data[col] = st.number_input(f"Enter {col}")

        if st.button("Predict"):

            from sklearn.linear_model import LinearRegression

            X = numeric_df.iloc[:, :-1]
            y = numeric_df.iloc[:, -1]

            model = LinearRegression()
            model.fit(X, y)

            input_df = pd.DataFrame([input_data])
            result = model.predict(input_df)

            st.success(f"Predicted Value: {round(result[0],2)}")

    else:
        st.warning("Upload data first")

# ---------------- VISUALIZATION ----------------
if section == "Visualization":

    df_clean = st.session_state.get("df_clean")

    if df_clean is not None:

        numeric_df = df_clean.select_dtypes(include=['number'])

        st.subheader("📊 Interactive Visualization")

        chart_type = st.selectbox("Chart Type", ["Line", "Bar"])
        x_axis = st.selectbox("Select X-axis", numeric_df.columns)
        y_axis = st.selectbox("Select Y-axis", numeric_df.columns)

        fig, ax = plt.subplots()

        if chart_type == "Line":
            ax.plot(df_clean[x_axis], df_clean[y_axis])
        else:
            ax.bar(df_clean[x_axis], df_clean[y_axis])

        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{y_axis} vs {x_axis}")

        st.pyplot(fig)

        # 🔥 AI BUTTON
        if st.button("🤖 Explain this Chart"):

            st.subheader("🧠 AI Explanation")

            st.write(f"""
📊 **Chart Breakdown**

- X-axis (**{x_axis}**) represents the independent variable  
- Y-axis (**{y_axis}**) represents the dependent variable  

📌 **Why this chart is used:**  
The {chart_type} chart helps visualize how {y_axis} changes with {x_axis}.

📈 **What this shows:**  
- Relationship between {x_axis} and {y_axis}  
- Trends or patterns in the dataset  

💡 **Business Insight:**  
This helps in identifying key factors influencing {y_axis}, useful for decision-making and forecasting.
""")

    else:
        st.warning("Upload data first")

# ---------------- ADVANCED INSIGHTS ----------------
if section == "Advanced Insights":

    df_clean = st.session_state.get("df_clean")

    if df_clean is not None:

        st.subheader("🧠 Smart Insights")

        numeric_df = df_clean.select_dtypes(include=['number'])

        for col in numeric_df.columns:
            st.write(f"""
🔹 **{col}**
- Mean: {round(numeric_df[col].mean(),2)}
- Max: {numeric_df[col].max()}
- Min: {numeric_df[col].min()}
""")

    else:
        st.warning("Upload data first")

