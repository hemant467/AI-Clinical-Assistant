import streamlit as st
import random
from groq import Groq
import os
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# ========== LOAD ENV ==========
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("🚨 GROQ_API_KEY not found. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"

# ========== CONFIG ==========
st.set_page_config(page_title="🩺 AI Clinical Assistant 🤖", layout="wide")

# ========== SESSION STORAGE ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {}  # store username: password
if "otp" not in st.session_state:
    st.session_state.otp = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# =========================
# LOGIN / SIGNUP FLOW
# =========================
if not st.session_state.logged_in:
    st.title("🩺 Clinical AI 🤖 Assistant Login 🔐")

    choice = st.radio("Are you an existing user or a new user?", ["Existing User", "New User"])

    if choice == "Existing User":
        username = st.text_input("Username 📝", key="login_username")
        password = st.text_input("Password 🔒", type="password", key="login_password")
        if st.button("Login ➡️"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                # generate OTP
                otp = random.randint(1000, 9999)
                st.session_state.otp = otp
                st.session_state.current_user = username
                st.success(f"✅ OTP sent (simulation): {otp}")
                st.info("Enter the OTP below to complete login.")
            else:
                st.error("❌ Invalid username or password")
        
        # OTP verification
        if st.session_state.otp:
            user_otp = st.text_input("Enter OTP 🔢", key="login_otp")
            if st.button("Verify OTP ✅"):
                if user_otp and int(user_otp) == st.session_state.otp:
                    st.session_state.logged_in = True
                    st.session_state.otp = None
                    st.success(f"🎉 Welcome back, {st.session_state.current_user}!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid OTP. Try again.")

    elif choice == "New User":
        new_username = st.text_input("Create Username 📝", key="signup_username")
        new_password = st.text_input("Create Password 🔒", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password 🔒", type="password", key="signup_confirm")
        if st.button("Signup ➕"):
            if not new_username or not new_password:
                st.warning("⚠️ Enter both username and password")
            elif new_username in st.session_state.users:
                st.error("❌ Username already exists")
            elif new_password != confirm_password:
                st.error("❌ Passwords do not match")
            else:
                # Save user
                st.session_state.users[new_username] = new_password
                otp = random.randint(1000, 9999)
                st.session_state.otp = otp
                st.session_state.current_user = new_username
                st.success(f"✅ User created! OTP sent (simulation): {otp}")
                st.info("Enter the OTP below to complete signup.")

        # OTP verification
        if st.session_state.otp:
            user_otp = st.text_input("Enter OTP 🔢", key="signup_otp")
            if st.button("Verify OTP ✅"):
                if user_otp and int(user_otp) == st.session_state.otp:
                    st.session_state.logged_in = True
                    st.session_state.otp = None
                    st.success(f"🎉 Welcome, {st.session_state.current_user}!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid OTP. Try again.")

# =========================
# MAIN APP AFTER LOGIN
# =========================
else:
    # Logout button
    if st.sidebar.button("Logout ⬅️"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.experimental_rerun()

    st.sidebar.info(f"Logged in as: {st.session_state.current_user}")

    # =========================
    # HELPER FUNCTIONS
    # =========================
    def get_ai_response(prompt=None, messages=None):
        try:
            if messages:
                response = client.chat.completions.create(model=MODEL, messages=messages)
            else:
                response = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":prompt}])
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def extract_text_from_pdf(file):
        try:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            return text
        except Exception as e:
            return f"❌ Failed to read PDF: {str(e)}"

    def extract_text_from_image(file):
        try:
            image = Image.open(file)
            return pytesseract.image_to_string(image)
        except Exception as e:
            return f"❌ Failed to read image: {str(e)}"

    def analyze_document(text, description="document"):
        prompt = f"Analyze this {description} and provide summary, key findings, and advice:\n{text}"
        with st.spinner(f"Analyzing {description}..."):
            return get_ai_response(prompt)

    # =========================
    # SIDEBAR MODULE SELECTION
    # =========================
    page = st.sidebar.radio("✅ Choose Module", [
        "💬 Chat", "🧬 Lab Report Analyzer", "📄 Prescription OCR & Analysis", "📝 Full Health Report Generator"
    ])

    # =========================
    # MODULE IMPLEMENTATION
    # =========================
    if page == "🧬 Lab Report Analyzer":
        st.header("🧬 Lab Report Analyzer")
        uploaded_lab = st.file_uploader("Upload Lab Report (PDF/Image) 🔬", type=["png","jpg","jpeg","pdf"])
        if uploaded_lab:
            if uploaded_lab.type == "application/pdf":
                lab_text = extract_text_from_pdf(uploaded_lab)
            else:
                lab_text = extract_text_from_image(uploaded_lab)
            st.subheader("Extracted Lab Data:")
            st.text_area("OCR Output", lab_text, height=200)
            analysis = analyze_document(lab_text, "lab report")
            st.subheader("💡 Analysis:")
            st.write(analysis)

    elif page == "📝 Full Health Report Generator":
        st.header("📝 Full Health Report Generator")
        uploaded_files = st.file_uploader("Upload multiple files (PDF/Image) 🗂️", type=["png","jpg","jpeg","pdf"], accept_multiple_files=True)
        if uploaded_files:
            combined_text = ""
            for idx, file in enumerate(uploaded_files, start=1):
                st.subheader(f"{file.name}")
                if file.type == "application/pdf":
                    file_text = extract_text_from_pdf(file)
                else:
                    file_text = extract_text_from_image(file)
                combined_text += f"\n\n--- {file.name} ---\n{file_text}"
                st.text_area(f"OCR - {file.name}", file_text, height=150)
            if combined_text:
                full_report = analyze_document(combined_text, "multiple patient documents")
                st.subheader("📋 Full Health Report:")
                st.write(full_report)

# streamlit run ai_clinical_assist-4.py