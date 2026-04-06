import streamlit as st
import random

# INIT SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "captcha" not in st.session_state:
    st.session_state.captcha = random.randint(1000, 9999)

st.title("🔐 Login / Sign Up")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# ---------------- LOGIN ----------------
with tab1:
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    # 🤖 CAPTCHA
    st.markdown(f"🤖 Verify you are not a robot")
    st.write(f"Enter this code: **{st.session_state.captcha}**")
    user_captcha = st.text_input("Enter code")

    if st.button("Login"):

        if not user or not pwd:
            st.error("⚠️ Fill all fields")

        elif user_captcha != str(st.session_state.captcha):
            st.error("❌ Wrong verification code")

        else:
            st.session_state.logged_in = True
            st.success("✅ Login successful")

            # Refresh captcha
            st.session_state.captcha = random.randint(1000, 9999)

            st.switch_page("pages/2_Dashboard.py")


# ---------------- SIGN UP ----------------
with tab2:
    new_user = st.text_input("Create Username")
    new_pwd = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        st.success("Account created! Please login.")
