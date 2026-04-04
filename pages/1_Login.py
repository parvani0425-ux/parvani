import streamlit as st
import json

def load_users():
    try:
        return json.load(open("users.json"))
    except:
        return {}

def save_users(users):
    json.dump(users, open("users.json","w"))

st.title("🔐 Login / Sign Up")

users = load_users()

tab1, tab2 = st.tabs(["Login","Signup"])

with tab1:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in users and users[u]==p:
            st.session_state["user"] = u
            st.success("Login successful")
        else:
            st.error("Wrong credentials")

with tab2:
    u = st.text_input("New Username")
    p = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        users[u]=p
        save_users(users)
        st.success("Account created")
