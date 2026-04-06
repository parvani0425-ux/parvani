import streamlit as st
import random

# ---------- SHOW SIDEBAR ----------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: block;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION INIT ----------
if "captcha" not in st.session_state:
    st.session_state.captcha = random.randint(1000, 9999)

# ---------- STYLE ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f2027, #2c5364);
}

.login-box {
    max-width: 400px;
    margin: auto;
    margin-top: 80px;
    padding: 40px;
    border-radius: 15px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
}

.title {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    color: white;
}

.glow {
    width: 120px;
    height: 120px;
    margin: auto;
    border-radius: 50%;
    background: radial-gradient(circle, #00f2ff, #8e2de2);
    box-shadow: 0 0 60px #00f2ff, 0 0 120px #8e2de2;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown('<div class="login-box">', unsafe_allow_html=True)

st.markdown('<div class="glow"></div>', unsafe_allow_html=True)
st.markdown('<div class="title">🔐 Login / Sign Up</div>', unsafe_allow_html=True)

st.write("")

# ---------- FORM (ENTER KEY WORKS HERE) ----------
with st.form("login_form"):

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # ---------- CAPTCHA ----------
    st.write(f"🔢 Enter this code to verify: **{st.session_state.captcha}**")
    user_captcha = st.text_input("Verification Code")

    submitted = st.form_submit_button("Login")

# ---------- LOGIN LOGIC ----------
if submitted:

    if not username or not password:
        st.error("⚠️ Please enter all fields")

    elif user_captcha != str(st.session_state.captcha):
        st.error("❌ Wrong verification code (Not a bot check failed)")

    else:
        st.success("✅ Logged in successfully")

        # regenerate captcha after success
        st.session_state.captcha = random.randint(1000, 9999)

st.markdown('</div>', unsafe_allow_html=True)
