import streamlit as st

def login():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")
      import streamlit as st

# INIT SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🔐 Login / Sign Up")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# LOGIN
with tab1:
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.switch_page("pages/2_Dashboard.py")

# SIGNUP
with tab2:
    new_user = st.text_input("Create Username")
    new_pwd = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        st.success("Account created! Please login.")
        
      
