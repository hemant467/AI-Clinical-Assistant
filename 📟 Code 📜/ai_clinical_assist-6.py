import streamlit as st
import random
from groq import Groq
import os
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes

# =========================
# LOAD ENV & CONFIG
# =========================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("🚨 GROQ_API_KEY not found. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"
st.set_page_config(page_title="🩺 AI Clinical Assistant 🤖", layout="wide")

# =========================
# SESSION VARIABLES
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {}  # username: password
if "verification" not in st.session_state:
    st.session_state.verification = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None

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

def generate_math_challenge():
    a, b = random.randint(1, 20), random.randint(1, 20)
    st.session_state.verification = a + b
    return f"{a} + {b} = ?"

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
                st.session_state.current_user = username
                st.success("✅ Correct credentials!")
                st.info(f"Solve this to verify you are human: {generate_math_challenge()}")
            else:
                st.error("❌ Invalid username or password")

        if st.session_state.verification:
            user_input = st.text_input("Enter answer 🔢", key="login_math")
            if st.button("Verify ✅"):
                if user_input and int(user_input) == st.session_state.verification:
                    st.session_state.logged_in = True
                    st.session_state.verification = None
                    st.success(f"🎉 Welcome back, {st.session_state.current_user}!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Incorrect answer. Try again.")

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
                st.session_state.users[new_username] = new_password
                st.session_state.current_user = new_username
                st.success("✅ User created!")
                st.info(f"Solve this to verify you are human: {generate_math_challenge()}")

        if st.session_state.verification:
            user_input = st.text_input("Enter answer 🔢", key="signup_math")
            if st.button("Verify ✅"):
                if user_input and int(user_input) == st.session_state.verification:
                    st.session_state.logged_in = True
                    st.session_state.verification = None
                    st.success(f"🎉 Welcome, {st.session_state.current_user}!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Incorrect answer. Try again.")

    # =========================
    # FOOTER FOR LOGIN / SIGNUP
    # =========================
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:orange;'>Designed & Developed by</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gold; font-weight:bold;'>💖 Hemant Katta 💝</p>", unsafe_allow_html=True)

# =========================
# MAIN APP AFTER LOGIN
# =========================
else:
    # Logout
    if st.sidebar.button("Logout ⬅️"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.experimental_rerun()
    st.sidebar.info(f"Logged in as: {st.session_state.current_user}")

    # Sidebar modules
    page = st.sidebar.radio("✅ Choose Module", [
        "💬 Chat",
        "🧠 Diagnosis",
        "💊 Treatment",
        "💉 Drug Checker",
        "📄 Prescription OCR & Analysis",
        "🩻 X-Ray Interpretation",
        "🎤 Voice Consultation",
        "⚠️ Health Risk Prediction",
        "🧬 Lab Report Analyzer",
        "💡 Symptom Checker & Health Plan",
        "📝 Full Health Report Generator"
    ])

    # -------------------------
    # Chat Module
    # -------------------------
    if page == "💬 Chat":
        st.header("AI 🤖 Doctor Chat 💬")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        user_input = st.chat_input("Describe 📝 symptoms or case...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("AI 🤖 is typing..."):
                reply = get_ai_response(messages=st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    # -------------------------
    # Diagnosis Module
    # -------------------------
    elif page == "🧠 Diagnosis":
        st.header("🧠 Diagnosis Assistant 🤖")
        age = st.number_input("Age 🔢", 0, 120)
        gender = st.selectbox("Gender", ["Male ♂️", "Female ♀️", "Other ⚧️"])
        symptoms = st.text_area("Symptoms 🤒")
        if st.button("Analyze 🔎"):
            prompt = f"Patient age: {age}, gender: {gender}, symptoms: {symptoms}. Provide possible diagnoses, risk level, suggested tests, and red flags."
            with st.spinner("Analyzing..."):
                result = get_ai_response(prompt=prompt)
            st.write(result)

    # -------------------------
    # Treatment Module
    # -------------------------
    elif page == "💊 Treatment":
        st.header("💊 Treatment Planner 📜")
        diagnosis = st.text_area("🧠 Diagnosis 🩺")
        if st.button("Generate Plan 📜"):
            prompt = f"Treatment planning assistant. Diagnosis: {diagnosis}. Provide treatment options, medications, lifestyle advice, and follow-up instructions."
            with st.spinner("Generating treatment plan..."):
                result = get_ai_response(prompt=prompt)
            st.write(result)

    # -------------------------
    # Drug Checker Module
    # -------------------------
    elif page == "💉 Drug Checker":
        st.header("💉 Drug Interaction Checker")
        drugs = st.text_area("Enter drugs 💊 (comma separated)")
        if st.button("Check ✅"):
            prompt = f"Pharmacology assistant. Drugs: {drugs}. Provide interactions, warnings, and safer alternatives."
            with st.spinner("Checking interactions..."):
                result = get_ai_response(prompt=prompt)
            st.write(result)

    # -------------------------
    # Prescription OCR
    # -------------------------
    elif page == "📄 Prescription OCR & Analysis":
        st.header("📄 Prescription / Medical Report OCR")
        uploaded_file = st.file_uploader("Upload Prescription / Medical Report 📝", type=["png","jpg","jpeg","pdf"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                pages = convert_from_bytes(uploaded_file.read())
                text = "".join([pytesseract.image_to_string(p) for p in pages])
            else:
                text = extract_text_from_image(uploaded_file)
            st.subheader("📝 Extracted Text:")
            st.write(text)
            analysis = analyze_document(text, "medical report")
            st.subheader("💡 Analysis:")
            st.write(analysis)

    # -------------------------
    # X-Ray Interpretation
    # -------------------------
    elif page == "🩻 X-Ray Interpretation":
        st.header("🩻 X-Ray / Scan Analysis")
        xray_file = st.file_uploader("Upload X-Ray / Scan 🩻", type=["png","jpg","jpeg"])
        if xray_file:
            st.image(xray_file, caption="Uploaded X-Ray / Scan", use_column_width=True)
            prompt = f"Radiology assistant: Analyze this X-Ray image (description: {xray_file.name}) and provide anomalies, possible diagnosis, and recommendations."
            with st.spinner("Analyzing X-Ray..."):
                result = get_ai_response(prompt=prompt)
            st.write(result)

    # -------------------------
    # Voice Consultation (prototype)
    # -------------------------
    elif page == "🎤 Voice Consultation":
        st.header("🎤 Voice Consultation (Prototype)")
        st.info("Audio recording integration pending. Upload audio manually for now.")
        voice_file = st.file_uploader("Upload voice note 🎙️", type=["wav","mp3"])
        if voice_file:
            st.success("Audio uploaded! (Transcription feature pending)")

    # -------------------------
    # Health Risk Prediction
    # -------------------------
    elif page == "⚠️ Health Risk Prediction":
        st.header("⚠️ Health Risk Prediction")
        age = st.number_input("Age 🔢", 0, 120, key="risk_age")
        gender = st.selectbox("Gender", ["Male ♂️", "Female ♀️", "Other ⚧️"], key="risk_gender")
        symptoms = st.text_area("Symptoms 🤒", key="risk_symptoms")
        history = st.text_area("Medical History 📝", key="risk_history")
        if st.button("Predict Risk 🚨"):
            prompt = f"Predict potential health risks for patient with age {age}, gender {gender}, symptoms {symptoms}, history {history}. Provide severity and recommended actions."
            with st.spinner("Predicting health risk..."):
                result = get_ai_response(prompt=prompt)
            st.write(result)

    # -------------------------
    # Lab Report Analyzer
    # -------------------------
    elif page == "🧬 Lab Report Analyzer":
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

    # -------------------------
    # Symptom Checker & Health Plan
    # -------------------------
    elif page == "💡 Symptom Checker & Health Plan":
        st.header("💡 Symptom Checker & Personalized Health Plan")
        age = st.number_input("Age 🔢", 18, 120, key="plan_age")
        gender = st.selectbox("Gender", ["Male ♂️", "Female ♀️", "Other ⚧️"], key="plan_gender")
        symptoms = st.text_area("Symptoms 🤒", key="plan_symptoms")
        lifestyle = st.text_area("Lifestyle / Habits 🏃‍♂️", key="plan_lifestyle")
        if st.button("Generate Health Plan 📜"):
            prompt = f"Patient info: Age {age}, Gender {gender}, Symptoms {symptoms}, Lifestyle {lifestyle}. Provide a personalized health plan including diet, exercise, preventive measures, and follow-up schedule."
            with st.spinner("Generating health plan..."):
                plan = get_ai_response(prompt=prompt)
            st.write(plan)

    # -------------------------
    # Full Health Report Generator
    # -------------------------
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

    # =========================
    # FOOTER
    # =========================
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:orange;'>Designed & Developed by</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gold; font-weight:bold;'>💖 Hemant Katta 💝</p>", unsafe_allow_html=True)

    # -------------------------
    # Disclaimer
    # -------------------------
    st.warning("⚠️ This tool 🤖 is for educational purposes only. NOT ❌ a real medical diagnosis. 🚨")

    # streamlit run ai_clinical_assist-6.py