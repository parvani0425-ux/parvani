import streamlit as st
import random

st.set_page_config(layout="centered")

# ---------- CAPTCHA ----------
if "captcha" not in st.session_state:
    st.session_state.captcha = random.randint(1000, 9999)

# ---------- STYLE ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f2027, #2c5364);
}

/* Center container */
.login-container {
    max-width: 420px;
    margin: auto;
    margin-top: 80px;
    padding: 35px;
    border-radius: 18px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    box-shadow: 0 0 25px rgba(0,255,255,0.15);
}

/* Title */
.title {
    text-align: center;
    font-size: 32px;
    font-weight: 600;
    color: white;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 14px;
    color: #aaa;
    margin-bottom: 25px;
}

/* Button */
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
    background: linear-gradient(90deg, #8e2de2, #4a00e0);
    color: white;
    border: none;
}

/* Inputs */
input {
    border-radius: 8px !important;
}

/* Glow circle */
.glow {
    width: 90px;
    height: 90px;
    margin: auto;
    border-radius: 50%;
    background: radial-gradient(circle, #00f2ff, #8e2de2);
    box-shadow: 0 0 50px #00f2ff, 0 0 100px #8e2de2;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown('<div class="login-container">', unsafe_allow_html=True)

st.markdown('<div class="glow"></div>', unsafe_allow_html=True)
st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Access your AI Dashboard</div>', unsafe_allow_html=True)

# ---------- FORM ----------
with st.form("login_form"):

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.markdown(f"🔢 Enter code: **{st.session_state.captcha}**")
    user_captcha = st.text_input("Verification")

    submitted = st.form_submit_button("Login")

# ---------- LOGIC ----------
if submitted:

    if not username or not password:
        st.error("⚠️ Fill all fields")

    elif user_captcha != str(st.session_state.captcha):
        st.error("❌ Wrong verification code")

    else:
        st.success("✅ Login successful")

        st.session_state.captcha = random.randint(1000, 9999)

st.markdown('</div>', unsafe_allow_html=True)
