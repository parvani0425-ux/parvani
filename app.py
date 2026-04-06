import streamlit as st

st.set_page_config(page_title="AI Data Tool", layout="wide")

# -------- SESSION --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- LANDING PAGE --------
if not st.session_state.logged_in:

    st.title("The Intelligent Data Sphere")
    st.write("Where Data Shapes Your Future 🚀")

    if st.button("Login / Sign Up"):
        st.session_state.logged_in = True
        st.rerun()

# -------- AFTER LOGIN --------
else:

    # SIDEBAR
    with st.sidebar:
        st.title("📊 Navigation")

        page = st.radio(
            "Go to",
            ["Dashboard", "Profile", "About"]
        )

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # PAGE ROUTING
    if page == "Dashboard":
        st.switch_page("pages/2_Dashboard.py")

    elif page == "Profile":
        st.switch_page("pages/3_profile.py")

    elif page == "About":
        st.switch_page("pages/4_About.py")
