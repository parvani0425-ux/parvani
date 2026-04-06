import streamlit as st

# INIT SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🔐 Login / Sign Up")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# ---------------- LOGIN ----------------
with tab1:
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    # 🤖 Checkbox verification
    not_robot = st.checkbox("I am not a robot 🤖")

    if st.button("Login"):

        if not user or not pwd:
            st.error("⚠️ Fill all fields")

        elif not not_robot:
            st.error("❌ Please verify you are not a robot")

        else:
            st.session_state.logged_in = True
            st.success("✅ Login successful")
            st.switch_page("pages/2_Dashboard.py")


# ---------------- SIGN UP ----------------
with tab2:
    new_user = st.text_input("Create Username")
    new_pwd = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        st.success("Account created! Please login.")
      
