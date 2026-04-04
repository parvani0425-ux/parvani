import streamlit as st
import json
import datetime

st.set_page_config(page_title="Login", layout="wide")

# ---------------- USERS ----------------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# ---------------- HISTORY ----------------
def load_history():
    try:
        with open("login_history.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_history(username):
    history = load_history()
    history.append({
        "user": username,
        "time": str(datetime.datetime.now())
    })
    with open("login_history.json", "w") as f:
        json.dump(history, f, indent=4)

# ---------------- UI ----------------
st.title("🔐 Login / Sign Up")

users = load_users()

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# -------- LOGIN --------
with tab1:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success("✅ Login successful!")
            save_history(username)
        else:
            st.error("❌ Invalid credentials")

# -------- SIGNUP --------
with tab2:
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        if new_user in users:
            st.warning("⚠️ User already exists")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("🎉 Account created! Now login")

# -------- LOGIN HISTORY --------
st.markdown("---")
st.subheader("🕒 Recent Logins")

history = load_history()

if history:
    for item in history[-5:][::-1]:
        st.write(f"👤 {item['user']} | ⏰ {item['time']}")
else:
    st.info("No login history yet")
    