import streamlit as st

# ---------- SHOW SIDEBAR ----------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: block;
}
</style>
""", unsafe_allow_html=True)


# ---------- STYLE ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f2027, #2c5364);
}

/* Center box */
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

/* Title */
.title {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    color: white;
}

/* Glow effect */
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

username = st.text_input("Username")
password = st.text_input("Password", type="password")

st.write("")

if st.button("Login", use_container_width=True):
    if username and password:
        st.success("Logged in successfully ✅")
    else:
        st.error("Enter credentials")

st.markdown('</div>', unsafe_allow_html=True)
