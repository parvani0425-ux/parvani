import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from utils import clean_data, run_regression

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

# ---------------- SESSION SETUP ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "login"

# ---------------- LOGIN PAGE ----------------
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
                st.session_state["page"] = "dashboard"
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ---------------- DASHBOARD ----------------
st.title("📊 Data Analytics Dashboard")

# Sidebar
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Upload & Clean", "ML & KPIs", "Visualization"])

# Logout
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"
    st.experimental_rerun()

# ---------------- UPLOAD & CLEAN ----------------
if section == "Upload & Clean":

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df_clean = clean_data(df)

            # Save in session
            st.session_state["df"] = df
            st.session_state["df_clean"] = df_clean

            st.subheader("📄 Original Data")
            st.dataframe(df)

            st.subheader("🧹 Cleaned Data")
            st.dataframe(df_clean)

            st.success("✅ Data cleaned (duplicates & missing values removed)")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- ML & KPIs ----------------
if section == "ML & KPIs":

    df_clean = st.session_state.get("df_clean")

    if df_clean is not None:

        accuracy, numeric_df, predictions, y_test = run_regression(df_clean)

        st.subheader("📌 Key Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df_clean.shape[0])
        col2.metric("Columns", df_clean.shape[1])
        col3.metric("Accuracy", f"{round(accuracy,2)}" if accuracy else "N/A")

        if predictions is not None:
            st.subheader("🤖 Prediction Table")

            pred_df = pd.DataFrame({
                "Actual": y_test.values[:10],
                "Predicted": predictions[:10]
            })

            st.dataframe(pred_df)

    else:
        st.warning("⚠️ Please upload data first")

# ---------------- VISUALIZATION ----------------
if section == "Visualization":

    df_clean = st.session_state.get("df_clean")

    if df_clean is not None:

        st.subheader("📊 Data Visualization")

        numeric_df = df_clean.select_dtypes(include=['number'])

        for col in numeric_df.columns[:3]:

            fig, ax = plt.subplots()

            ax.plot(numeric_df[col])

            ax.set_title(f"{col} Trend")
            ax.set_xlabel("Index (Data Points)")
            ax.set_ylabel(col)

            st.pyplot(fig)

        # Insights button
        if st.button("Generate Insights"):

            accuracy, _, _, _ = run_regression(df_clean)

            st.subheader("🧠 Insights")

            st.write(f"""
            - Dataset contains {df_clean.shape[0]} rows  
            - Total features: {df_clean.shape[1]}  
            - Model accuracy: {round(accuracy,2) if accuracy else "N/A"}  
            - Data cleaned successfully  
            - Trends visualized using line charts  
            """)

    else:
        st.warning("⚠️ Please upload data first")
