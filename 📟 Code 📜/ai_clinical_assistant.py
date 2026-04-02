import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from PIL import Image
import pytesseract

# Optional: audio recording
# from streamlit_audio_recorder import audio_recorder

# PDF OCR support
from pdf2image import convert_from_bytes

# ========== LOAD ENV ==========
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# ========== CONFIG ==========
st.set_page_config(page_title="🩺 AI Clinical Assistant 🤖", layout="wide")

if not api_key:
    st.error("🚨 GROQ_API_KEY not found. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"  # Latest supported model

# ========== HELPER FUNCTION ==========
def get_ai_response(prompt=None, messages=None):
    try:
        if messages:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
        else:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error ☠️ : {str(e)}"

# ========== SIDEBAR MODULES ==========
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
    "💡 Symptom Checker & Health Plan"
])

# =========================
# CHAT MODULE
# =========================
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

# =========================
# DIAGNOSIS MODULE
# =========================
elif page == "🧠 Diagnosis":
    st.header("🧠 Diagnosis Assistant 🤖")
    age = st.number_input("Age 🔢", 10, 100)
    gender = st.selectbox("Gender", ["Male ♂️", "Female ♀️", "Other ⚧️"])
    symptoms = st.text_area("Symptoms 🤒")
    if st.button("Analyze 🔎"):
        prompt = f"""
        Clinical assistant. Patient age: {age}, gender: {gender}, symptoms: {symptoms}.
        Provide possible diagnoses, risk level, suggested tests, and red flags.
        """
        with st.spinner("Analyzing..."):
            result = get_ai_response(prompt=prompt)
        st.write(result)

# =========================
# TREATMENT MODULE
# =========================
elif page == "💊 Treatment":
    st.header("💊 Treatment Planner 📜")
    diagnosis = st.text_area("🧠 Diagnosis 🩺")
    if st.button("Generate Plan 📜"):
        prompt = f"""
        Treatment planning assistant. Diagnosis: {diagnosis}.
        Provide treatment options, medications, lifestyle advice, and follow-up instructions.
        """
        with st.spinner("Generating treatment plan..."):
            result = get_ai_response(prompt=prompt)
        st.write(result)

# =========================
# DRUG CHECKER MODULE
# =========================
elif page == "💉 Drug Checker":
    st.header("💉 Drug Interaction Checker")
    drugs = st.text_area("Enter drugs 💊 (comma separated)")
    if st.button("Check ✅"):
        prompt = f"""
        Pharmacology assistant. Drugs: {drugs}.
        Provide interactions, warnings, and safer alternatives.
        """
        with st.spinner("Checking interactions..."):
            result = get_ai_response(prompt=prompt)
        st.write(result)

# =========================
# PRESCRIPTION OCR MODULE
# =========================
elif page == "📄 Prescription OCR & Analysis":
    st.header("📄 Prescription / Medical Report OCR")
    uploaded_file = st.file_uploader("Upload Prescription / Medical Report 📝", type=["png","jpg","jpeg","pdf"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            pages = convert_from_bytes(uploaded_file.read())
            text = "".join([pytesseract.image_to_string(page) for page in pages])
        else:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
        st.subheader("📝 Extracted Text:")
        st.write(text)
        prompt = f"Analyze this medical report and provide summary, key findings, and advice: {text}"
        with st.spinner("Analyzing..."):
            analysis = get_ai_response(prompt=prompt)
        st.subheader("💡 Analysis:")
        st.write(analysis)

# =========================
# X-RAY INTERPRETATION MODULE
# =========================
elif page == "🩻 X-Ray Interpretation":
    st.header("🩻 X-Ray / Scan Analysis")
    xray_file = st.file_uploader("Upload X-Ray / Scan 🩻", type=["png","jpg","jpeg"])
    if xray_file:
        st.image(xray_file, caption="Uploaded X-Ray / Scan", use_column_width=True)
        prompt = f"Radiology assistant: Analyze this X-Ray image (description: {xray_file.name}) and provide anomalies, possible diagnosis, and recommendations."
        with st.spinner("Analyzing X-Ray..."):
            result = get_ai_response(prompt=prompt)
        st.write(result)

# =========================
# VOICE CONSULTATION MODULE
# =========================
elif page == "🎤 Voice Consultation":
    st.header("🎤 Voice Consultation (Prototype)")
    st.info("Currently audio recording integration requires streamlit_audio_recorder or similar packages.")
    st.warning("Upload audio file manually (wav/mp3) for now.")
    voice_file = st.file_uploader("Upload voice note 🎙️", type=["wav","mp3"])
    if voice_file:
        # In production: send audio to Groq speech-to-text or Whisper
        st.success("Audio uploaded successfully! (Transcription feature pending)")
        st.info("You can later integrate Groq audio transcription model here.")

# =========================
# HEALTH RISK PREDICTION
# =========================
elif page == "⚠️ Health Risk Prediction":
    st.header("⚠️ Health Risk Prediction")
    age = st.number_input("Age 🔢", 10, 100, key="risk_age")
    gender = st.selectbox("Gender", ["Male ♂️", "Female ♀️", "Other ⚧️"], key="risk_gender")
    symptoms = st.text_area("Symptoms 🤒", key="risk_symptoms")
    medical_history = st.text_area("Medical History 📝", key="risk_history")
    if st.button("Predict Risk 🚨"):
        prompt = f"Predict potential health risks for patient with age {age}, gender {gender}, symptoms {symptoms}, history {medical_history}. Provide severity and recommended actions."
        with st.spinner("Predicting health risk..."):
            risk_result = get_ai_response(prompt=prompt)
        st.write(risk_result)

# =========================
# LAB REPORT ANALYZER
# =========================
elif page == "🧬 Lab Report Analyzer":
    st.header("🧬 Lab Report Analyzer")
    uploaded_lab = st.file_uploader("Upload Lab Report (PDF/Image) 🔬", type=["png","jpg","jpeg","pdf"])
    if uploaded_lab:
        if uploaded_lab.type == "application/pdf":
            pages = convert_from_bytes(uploaded_lab.read())
            lab_text = "".join([pytesseract.image_to_string(page) for page in pages])
        else:
            lab_text = pytesseract.image_to_string(Image.open(uploaded_lab))
        st.subheader("Extracted Lab Data:")
        st.write(lab_text)
        prompt = f"Analyze this lab report. Highlight abnormalities, key findings, and provide advice: {lab_text}"
        with st.spinner("Analyzing lab report..."):
            lab_analysis = get_ai_response(prompt=prompt)
        st.write(lab_analysis)

# =========================
# SYMPTOM CHECKER & HEALTH PLAN
# =========================
elif page == "💡 Symptom Checker & Health Plan":
    st.header("💡 Symptom Checker & Personalized Health Plan")
    age = st.number_input("Age 🔢", 10, 100, key="plan_age")
    gender = st.selectbox("Gender", ["Male ♂️", "Female ♀️", "Other ⚧️"], key="plan_gender")
    symptoms = st.text_area("Symptoms 🤒", key="plan_symptoms")
    lifestyle = st.text_area("Lifestyle / Habits 🏃‍♂️", key="plan_lifestyle")
    if st.button("Generate Health Plan 📜"):
        prompt = f"Patient info: Age {age}, Gender {gender}, Symptoms {symptoms}, Lifestyle {lifestyle}. Provide a personalized health plan including diet, exercise, preventive measures, and follow-up schedule."
        with st.spinner("Generating health plan..."):
            plan = get_ai_response(prompt=prompt)
        st.write(plan)

# ========== DISCLAIMER ==========
st.warning("⚠️ This tool 🤖 is for educational purposes only. NOT ❌ a real medical diagnosis. 🚨")
# =========================

# =========================
# FOOTER
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:orange;'>Designed & Developed by</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gold; font-weight:bold;'>💖 Hemant Katta 💝</p>", unsafe_allow_html=True)

# streamlit run ai_clinical_assistant.py