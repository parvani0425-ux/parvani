import streamlit as st
import json

st.title("🔐 Login / Signup")

# Load users
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

menu = st.radio("Choose Option", ["Login", "Signup"])

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if menu == "Signup":
    if st.button("Create Account"):
        if username in users:
            st.warning("User already exists")
        else:
            users[username] = password
            save_users(users)
            st.success("Account created!")

elif menu == "Login":
    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Welcome {username} 🎉")
        else:
            st.error("Invalid credentials")
            
