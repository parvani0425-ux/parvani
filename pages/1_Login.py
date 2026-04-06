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
