import streamlit as st

st.set_page_config(page_title="Login — DataSphere", page_icon="🔮", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

* { font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #210635 0%, #420D4B 50%, #210635 100%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }

.login-wrap {
    max-width: 480px;
    margin: 60px auto 0;
    padding: 0 20px;
}
.login-logo {
    text-align: center;
    margin-bottom: 32px;
}
.login-logo-icon {
    font-size: 40px;
    display: block;
    margin-bottom: 10px;
}
.login-title {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    color: #F5D5E0;
    text-align: center;
    margin-bottom: 6px;
}
.login-sub {
    text-align: center;
    font-size: 14px;
    color: rgba(245,213,224,0.45);
    margin-bottom: 36px;
}
.card {
    background: rgba(102,103,171,0.08);
    border: 1px solid rgba(102,103,171,0.22);
    border-radius: 20px;
    padding: 36px 36px 28px;
    backdrop-filter: blur(12px);
}
.tab-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
    color: rgba(245,213,224,0.5);
    text-transform: uppercase;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(102,103,171,0.15);
}
/* Input styling */
.stTextInput > div > div > input {
    background: rgba(33,6,53,0.6) !important;
    border: 1px solid rgba(102,103,171,0.3) !important;
    border-radius: 10px !important;
    color: #F5D5E0 !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6667AB !important;
    box-shadow: 0 0 0 2px rgba(102,103,171,0.2) !important;
}
.stTextInput label { color: rgba(245,213,224,0.6) !important; font-size: 13px !important; font-weight: 500 !important; }
.stCheckbox label { color: rgba(245,213,224,0.55) !important; font-size: 13px !important; }
.stButton > button {
    background: linear-gradient(135deg, #7B337E, #6667AB) !important;
    color: #F5D5E0 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin-top: 8px !important;
    box-shadow: 0 4px 20px rgba(123,51,126,0.35) !important;
    transition: all 0.3s !important;
}
.stButton > button:hover { box-shadow: 0 6px 28px rgba(123,51,126,0.55) !important; transform: translateY(-1px) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: rgba(33,6,53,0.4) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(102,103,171,0.15) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: rgba(245,213,224,0.45) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 8px 24px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7B337E, #6667AB) !important;
    color: #F5D5E0 !important;
}
.back-link {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    color: rgba(245,213,224,0.3);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="login-wrap">
    <div class="login-logo">
        <span class="login-logo-icon">🔮</span>
    </div>
    <div class="login-title">Welcome Back</div>
    <div class="login-sub">Sign in to your DataSphere account</div>
</div>
""", unsafe_allow_html=True)

_, center, _ = st.columns([1, 2, 1])
with center:
    tab1, tab2 = st.tabs(["  🔑  Login  ", "  ✨  Sign Up  "])

    with tab1:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        user = st.text_input("Username", placeholder="Enter your username", key="login_user")
        pwd = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pwd")
        not_robot = st.checkbox("I am not a robot 🤖")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Sign In →", key="login_btn"):
            if not user or not pwd:
                st.error("⚠️ Please fill in all fields")
            elif not not_robot:
                st.error("❌ Please verify you are not a robot")
            else:
                st.session_state.logged_in = True
                st.success("✅ Login successful! Redirecting...")
                st.switch_page("pages/2_Dashboard.py")

    with tab2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        new_user = st.text_input("Choose Username", placeholder="Pick a username", key="su_user")
        new_pwd = st.text_input("Create Password", type="password", placeholder="Create a strong password", key="su_pwd")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Create Account →", key="signup_btn"):
            if not new_user or not new_pwd:
                st.error("⚠️ Please fill in all fields")
            else:
                st.success("✅ Account created! Please sign in.")

st.markdown('<div class="back-link">← <a href="/" style="color: rgba(245,213,224,0.4); text-decoration: none;">Back to Home</a></div>', unsafe_allow_html=True)
