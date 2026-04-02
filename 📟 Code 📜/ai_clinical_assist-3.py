import streamlit as st
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

# ========== SESSION LOGIN ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login(username, password):
    if username == "admin" and password == "password123":
        st.session_state.logged_in = True
        st.success("✅ Login successful!")
        st.experimental_rerun()
    else:
        st.error("❌ Invalid username or password")

if not st.session_state.logged_in:
    st.title("🩺 Clinical AI 🤖 Assistant Login 🔐")
    username = st.text_input("Username 📝")
    password = st.text_input("Password 🔒", type="password")
    if st.button("Login ➡️"):
        login(username, password)
else:
    # Logout button
    if st.sidebar.button("Logout ⬅️"):
        st.session_state.logged_in = False
        st.experimental_rerun()

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
                page_text = page.get_text()
                text += page_text + "\n"
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
    # EXAMPLES: LAB REPORT MODULE
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

    # =========================
    # EXAMPLES: FULL HEALTH REPORT GENERATOR
    # =========================
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

# streamlit run ai_clinical_assist-3.py